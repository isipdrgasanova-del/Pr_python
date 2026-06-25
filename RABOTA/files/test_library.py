"""
Модульные тесты для library.py (pytest).
Запуск: pytest tests/ -v --cov=library
"""

import os
import csv
import pytest
from library import (
    add_book, get_all_books, get_book_by_id,
    update_book, delete_book,
    search_books, filter_by_status, filter_by_genre, filter_by_year,
    get_statistics, load_books, save_books, VALID_STATUSES,
)


@pytest.fixture
def tmp_db(tmp_path):
    """Временный CSV-файл для каждого теста."""
    return str(tmp_path / "books.csv")


# ─────────────────────────── load / save ────────────────────────

class TestLoadSave:
    def test_load_empty_when_file_missing(self, tmp_db):
        assert load_books(tmp_db) == []

    def test_save_and_reload(self, tmp_db):
        books = [{"id": "1", "title": "Тест", "author": "А", "year": "2000",
                  "genre": "фантастика", "status": "не прочитано", "added_at": "2024-01-01"}]
        save_books(books, tmp_db)
        loaded = load_books(tmp_db)
        assert len(loaded) == 1
        assert loaded[0]["title"] == "Тест"

    def test_save_multiple_books(self, tmp_db):
        books = [
            {"id": "1", "title": "A", "author": "B", "year": "1990",
             "genre": "", "status": "прочитано", "added_at": "2024-01-01"},
            {"id": "2", "title": "C", "author": "D", "year": "2000",
             "genre": "", "status": "не прочитано", "added_at": "2024-01-02"},
        ]
        save_books(books, tmp_db)
        assert len(load_books(tmp_db)) == 2


# ─────────────────────────── add_book ───────────────────────────

class TestAddBook:
    def test_add_basic(self, tmp_db):
        book = add_book("Мастер и Маргарита", "Булгаков", 1967, "роман", "прочитано", tmp_db)
        assert book["id"] == "1"
        assert book["title"] == "Мастер и Маргарита"
        assert book["author"] == "Булгаков"
        assert book["year"] == "1967"
        assert book["status"] == "прочитано"

    def test_add_increments_id(self, tmp_db):
        b1 = add_book("Книга 1", "Автор 1", 2000, filepath=tmp_db)
        b2 = add_book("Книга 2", "Автор 2", 2001, filepath=tmp_db)
        assert int(b2["id"]) == int(b1["id"]) + 1

    def test_add_default_status(self, tmp_db):
        book = add_book("Тест", "Автор", 2020, filepath=tmp_db)
        assert book["status"] == "не прочитано"

    def test_add_empty_title_raises(self, tmp_db):
        with pytest.raises(ValueError, match="Название"):
            add_book("", "Автор", 2020, filepath=tmp_db)

    def test_add_empty_author_raises(self, tmp_db):
        with pytest.raises(ValueError, match="Автор"):
            add_book("Книга", "", 2020, filepath=tmp_db)

    def test_add_invalid_year_string_raises(self, tmp_db):
        with pytest.raises(ValueError, match="Год"):
            add_book("Книга", "Автор", "abc", filepath=tmp_db)

    def test_add_future_year_raises(self, tmp_db):
        with pytest.raises(ValueError):
            add_book("Книга", "Автор", 9999, filepath=tmp_db)

    def test_add_zero_year_raises(self, tmp_db):
        with pytest.raises(ValueError):
            add_book("Книга", "Автор", 0, filepath=tmp_db)

    def test_add_invalid_status_raises(self, tmp_db):
        with pytest.raises(ValueError, match="Статус"):
            add_book("Книга", "Автор", 2020, status="unknown", filepath=tmp_db)

    def test_add_persisted_to_file(self, tmp_db):
        add_book("Книга", "Автор", 2020, filepath=tmp_db)
        loaded = load_books(tmp_db)
        assert len(loaded) == 1

    def test_add_strips_whitespace(self, tmp_db):
        book = add_book("  Книга  ", "  Автор  ", 2020, filepath=tmp_db)
        assert book["title"] == "Книга"
        assert book["author"] == "Автор"


# ─────────────────────────── get / read ─────────────────────────

class TestGetBooks:
    def test_get_all_empty(self, tmp_db):
        assert get_all_books(tmp_db) == []

    def test_get_all_returns_all(self, tmp_db):
        add_book("A", "X", 2000, filepath=tmp_db)
        add_book("B", "Y", 2001, filepath=tmp_db)
        assert len(get_all_books(tmp_db)) == 2

    def test_get_by_id_found(self, tmp_db):
        book = add_book("А", "Б", 2010, filepath=tmp_db)
        found = get_book_by_id(book["id"], tmp_db)
        assert found is not None
        assert found["title"] == "А"

    def test_get_by_id_not_found(self, tmp_db):
        assert get_book_by_id(999, tmp_db) is None

    def test_get_by_id_string_or_int(self, tmp_db):
        book = add_book("Т", "А", 2000, filepath=tmp_db)
        assert get_book_by_id(int(book["id"]), tmp_db) is not None
        assert get_book_by_id(book["id"], tmp_db) is not None


# ─────────────────────────── update_book ────────────────────────

class TestUpdateBook:
    def test_update_title(self, tmp_db):
        book = add_book("Старое", "Автор", 2000, filepath=tmp_db)
        updated = update_book(book["id"], tmp_db, title="Новое")
        assert updated["title"] == "Новое"

    def test_update_status(self, tmp_db):
        book = add_book("Книга", "Автор", 2000, filepath=tmp_db)
        updated = update_book(book["id"], tmp_db, status="прочитано")
        assert updated["status"] == "прочитано"

    def test_update_persists(self, tmp_db):
        book = add_book("Книга", "Автор", 2000, filepath=tmp_db)
        update_book(book["id"], tmp_db, title="Изменено")
        reloaded = get_book_by_id(book["id"], tmp_db)
        assert reloaded["title"] == "Изменено"

    def test_update_nonexistent_raises(self, tmp_db):
        with pytest.raises(KeyError):
            update_book(999, tmp_db, title="X")

    def test_update_invalid_status_raises(self, tmp_db):
        book = add_book("Книга", "Автор", 2000, filepath=tmp_db)
        with pytest.raises(ValueError):
            update_book(book["id"], tmp_db, status="unknown_status")

    def test_update_invalid_year_raises(self, tmp_db):
        book = add_book("Книга", "Автор", 2000, filepath=tmp_db)
        with pytest.raises(ValueError):
            update_book(book["id"], tmp_db, year="abc")


# ─────────────────────────── delete_book ────────────────────────

class TestDeleteBook:
    def test_delete_existing(self, tmp_db):
        book = add_book("Книга", "Автор", 2000, filepath=tmp_db)
        removed = delete_book(book["id"], tmp_db)
        assert removed["id"] == book["id"]
        assert get_book_by_id(book["id"], tmp_db) is None

    def test_delete_nonexistent_raises(self, tmp_db):
        with pytest.raises(KeyError):
            delete_book(999, tmp_db)

    def test_delete_reduces_count(self, tmp_db):
        b1 = add_book("A", "X", 2000, filepath=tmp_db)
        add_book("B", "Y", 2001, filepath=tmp_db)
        delete_book(b1["id"], tmp_db)
        assert len(get_all_books(tmp_db)) == 1


# ─────────────────────────── search ─────────────────────────────

class TestSearchBooks:
    def test_search_by_title(self, tmp_db):
        add_book("Война и мир", "Толстой", 1869, filepath=tmp_db)
        add_book("Преступление и наказание", "Достоевский", 1866, filepath=tmp_db)
        results = search_books("Война", tmp_db)
        assert len(results) == 1
        assert results[0]["title"] == "Война и мир"

    def test_search_by_author(self, tmp_db):
        add_book("Книга", "Пушкин", 1830, filepath=tmp_db)
        add_book("Другая", "Лермонтов", 1840, filepath=tmp_db)
        results = search_books("Пушк", tmp_db)
        assert len(results) == 1

    def test_search_case_insensitive(self, tmp_db):
        add_book("Мастер и Маргарита", "Булгаков", 1967, filepath=tmp_db)
        assert len(search_books("мастер", tmp_db)) == 1
        assert len(search_books("МАСТЕР", tmp_db)) == 1

    def test_search_empty_query_returns_empty(self, tmp_db):
        add_book("Книга", "Автор", 2000, filepath=tmp_db)
        assert search_books("", tmp_db) == []

    def test_search_no_match(self, tmp_db):
        add_book("Книга", "Автор", 2000, filepath=tmp_db)
        assert search_books("xyz123", tmp_db) == []


# ─────────────────────────── filters ────────────────────────────

class TestFilters:
    def test_filter_by_status(self, tmp_db):
        add_book("A", "X", 2000, status="прочитано", filepath=tmp_db)
        add_book("B", "Y", 2001, status="не прочитано", filepath=tmp_db)
        result = filter_by_status("прочитано", tmp_db)
        assert len(result) == 1
        assert result[0]["title"] == "A"

    def test_filter_by_invalid_status_raises(self, tmp_db):
        with pytest.raises(ValueError):
            filter_by_status("unknown", tmp_db)

    def test_filter_by_genre(self, tmp_db):
        add_book("A", "X", 2000, genre="фантастика", filepath=tmp_db)
        add_book("B", "Y", 2001, genre="роман", filepath=tmp_db)
        result = filter_by_genre("фантастика", tmp_db)
        assert len(result) == 1

    def test_filter_by_genre_case_insensitive(self, tmp_db):
        add_book("A", "X", 2000, genre="Фантастика", filepath=tmp_db)
        result = filter_by_genre("фантастика", tmp_db)
        assert len(result) == 1

    def test_filter_by_year(self, tmp_db):
        add_book("A", "X", 2000, filepath=tmp_db)
        add_book("B", "Y", 2001, filepath=tmp_db)
        result = filter_by_year(2000, tmp_db)
        assert len(result) == 1

    def test_filter_by_year_no_match(self, tmp_db):
        add_book("A", "X", 2000, filepath=tmp_db)
        assert filter_by_year(1900, tmp_db) == []


# ─────────────────────────── statistics ─────────────────────────

class TestStatistics:
    def test_stats_empty(self, tmp_db):
        st = get_statistics(tmp_db)
        assert st["total"] == 0
        assert st["прочитано"] == 0

    def test_stats_counts(self, tmp_db):
        add_book("A", "X", 2000, status="прочитано", filepath=tmp_db)
        add_book("B", "Y", 2001, status="прочитано", filepath=tmp_db)
        add_book("C", "Z", 2002, status="не прочитано", filepath=tmp_db)
        st = get_statistics(tmp_db)
        assert st["total"] == 3
        assert st["прочитано"] == 2
        assert st["не прочитано"] == 1

    def test_stats_genres(self, tmp_db):
        add_book("A", "X", 2000, genre="фантастика", filepath=tmp_db)
        add_book("B", "Y", 2001, genre="фантастика", filepath=tmp_db)
        add_book("C", "Z", 2002, genre="роман", filepath=tmp_db)
        st = get_statistics(tmp_db)
        assert st["genres"]["фантастика"] == 2
        assert st["genres"]["роман"] == 1

    def test_stats_reading_status(self, tmp_db):
        add_book("A", "X", 2000, status="читаю", filepath=tmp_db)
        st = get_statistics(tmp_db)
        assert st["читаю"] == 1


# ─────────────────────────── edge cases ─────────────────────────

class TestEdgeCases:
    def test_add_book_with_string_year(self, tmp_db):
        book = add_book("Книга", "Автор", "2020", filepath=tmp_db)
        assert book["year"] == "2020"

    def test_id_is_unique_after_delete(self, tmp_db):
        b1 = add_book("A", "X", 2000, filepath=tmp_db)
        b2 = add_book("B", "Y", 2001, filepath=tmp_db)
        delete_book(b1["id"], tmp_db)
        b3 = add_book("C", "Z", 2002, filepath=tmp_db)
        ids = [b["id"] for b in get_all_books(tmp_db)]
        assert len(ids) == len(set(ids))  # все ID уникальны

    def test_whitespace_only_title_raises(self, tmp_db):
        with pytest.raises(ValueError):
            add_book("   ", "Автор", 2020, filepath=tmp_db)

    def test_all_valid_statuses(self, tmp_db):
        for i, status in enumerate(VALID_STATUSES):
            book = add_book(f"Книга {i}", "Автор", 2000 + i, status=status, filepath=tmp_db)
            assert book["status"] == status

    def test_search_returns_multiple_matches(self, tmp_db):
        add_book("Python Cookbook", "Beazley", 2013, filepath=tmp_db)
        add_book("Python Tricks", "Bader", 2017, filepath=tmp_db)
        add_book("Clean Code", "Martin", 2008, filepath=tmp_db)
        results = search_books("python", tmp_db)
        assert len(results) == 2

    # ── баг-регрессии (этап 5) ──────────────────────────────────

    def test_regression_update_does_not_duplicate(self, tmp_db):
        """Баг #1: update_book не должен создавать дубликаты."""
        add_book("Книга", "Автор", 2000, filepath=tmp_db)
        b = add_book("Другая", "Автор2", 2001, filepath=tmp_db)
        update_book(b["id"], tmp_db, title="Обновлено")
        assert len(get_all_books(tmp_db)) == 2

    def test_regression_negative_year_raises(self, tmp_db):
        """Баг #2: отрицательный год должен вызывать ошибку."""
        with pytest.raises(ValueError):
            add_book("Книга", "Автор", -100, filepath=tmp_db)

    def test_regression_filter_by_status_reading(self, tmp_db):
        """Баг #3: статус 'читаю' должен поддерживаться в фильтре."""
        add_book("A", "X", 2000, status="читаю", filepath=tmp_db)
        result = filter_by_status("читаю", tmp_db)
        assert len(result) == 1

    def test_regression_delete_correct_book(self, tmp_db):
        """Баг #4: удаление должно затрагивать только нужную книгу."""
        b1 = add_book("A", "X", 2000, filepath=tmp_db)
        b2 = add_book("B", "Y", 2001, filepath=tmp_db)
        delete_book(b1["id"], tmp_db)
        remaining = get_all_books(tmp_db)
        assert len(remaining) == 1
        assert remaining[0]["id"] == b2["id"]
