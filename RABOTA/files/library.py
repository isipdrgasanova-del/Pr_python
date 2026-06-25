"""
Библиотека книг — бизнес-логика и работа с CSV.
"""

import csv
import os
from datetime import datetime

DATA_FILE = "books.csv"
FIELDNAMES = ["id", "title", "author", "year", "genre", "status", "added_at"]
VALID_STATUSES = {"прочитано", "не прочитано", "читаю"}


# ─────────────────────────── helpers ────────────────────────────

def _next_id(books: list[dict]) -> int:
    if not books:
        return 1
    return max(int(b["id"]) for b in books) + 1


def _validate_book(title: str, author: str, year: str | int, genre: str, status: str) -> None:
    if not str(title).strip():
        raise ValueError("Название книги не может быть пустым.")
    if not str(author).strip():
        raise ValueError("Автор не может быть пустым.")
    try:
        y = int(year)
    except (ValueError, TypeError):
        raise ValueError(f"Год должен быть числом, получено: {year!r}")
    current_year = datetime.now().year
    if not (0 < y <= current_year):
        raise ValueError(f"Год должен быть в диапазоне 1–{current_year}, получено: {y}")
    if status not in VALID_STATUSES:
        raise ValueError(f"Статус должен быть одним из {VALID_STATUSES}, получено: {status!r}")


# ─────────────────────────── I/O ────────────────────────────────

def load_books(filepath: str = DATA_FILE) -> list[dict]:
    """Загрузить список книг из CSV."""
    if not os.path.exists(filepath):
        return []
    books = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books


def save_books(books: list[dict], filepath: str = DATA_FILE) -> None:
    """Сохранить список книг в CSV."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(books)


# ─────────────────────────── CRUD ───────────────────────────────

def add_book(title: str, author: str, year: int | str,
             genre: str = "", status: str = "не прочитано",
             filepath: str = DATA_FILE) -> dict:
    """Добавить новую книгу. Возвращает созданную запись."""
    _validate_book(title, author, year, genre, status)
    books = load_books(filepath)
    book = {
        "id": str(_next_id(books)),
        "title": str(title).strip(),
        "author": str(author).strip(),
        "year": str(int(year)),
        "genre": str(genre).strip(),
        "status": status,
        "added_at": datetime.now().strftime("%Y-%m-%d"),
    }
    books.append(book)
    save_books(books, filepath)
    return book


def get_all_books(filepath: str = DATA_FILE) -> list[dict]:
    """Вернуть все книги."""
    return load_books(filepath)


def get_book_by_id(book_id: int | str, filepath: str = DATA_FILE) -> dict | None:
    """Найти книгу по ID."""
    books = load_books(filepath)
    for b in books:
        if str(b["id"]) == str(book_id):
            return b
    return None


def update_book(book_id: int | str, filepath: str = DATA_FILE, **fields) -> dict:
    """Обновить поля книги. Возвращает обновлённую запись."""
    books = load_books(filepath)
    for b in books:
        if str(b["id"]) == str(book_id):
            updated = {**b, **{k: str(v) for k, v in fields.items() if k in FIELDNAMES}}
            _validate_book(
                updated["title"], updated["author"], updated["year"],
                updated["genre"], updated["status"]
            )
            b.update(updated)
            save_books(books, filepath)
            return b
    raise KeyError(f"Книга с id={book_id} не найдена.")


def delete_book(book_id: int | str, filepath: str = DATA_FILE) -> dict:
    """Удалить книгу по ID. Возвращает удалённую запись."""
    books = load_books(filepath)
    for i, b in enumerate(books):
        if str(b["id"]) == str(book_id):
            removed = books.pop(i)
            save_books(books, filepath)
            return removed
    raise KeyError(f"Книга с id={book_id} не найдена.")


# ─────────────────────────── поиск / фильтрация ─────────────────

def search_books(query: str, filepath: str = DATA_FILE) -> list[dict]:
    """Поиск по названию или автору (регистронезависимый)."""
    q = query.strip().lower()
    if not q:
        return []
    return [
        b for b in load_books(filepath)
        if q in b["title"].lower() or q in b["author"].lower()
    ]


def filter_by_status(status: str, filepath: str = DATA_FILE) -> list[dict]:
    """Фильтр по статусу чтения."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Неизвестный статус: {status!r}")
    return [b for b in load_books(filepath) if b["status"] == status]


def filter_by_genre(genre: str, filepath: str = DATA_FILE) -> list[dict]:
    """Фильтр по жанру (регистронезависимый)."""
    g = genre.strip().lower()
    return [b for b in load_books(filepath) if b["genre"].lower() == g]


def filter_by_year(year: int | str, filepath: str = DATA_FILE) -> list[dict]:
    """Фильтр по году издания."""
    return [b for b in load_books(filepath) if b["year"] == str(year)]


def get_statistics(filepath: str = DATA_FILE) -> dict:
    """Вернуть статистику по библиотеке."""
    books = load_books(filepath)
    stats = {
        "total": len(books),
        "прочитано": 0,
        "не прочитано": 0,
        "читаю": 0,
        "genres": {},
    }
    for b in books:
        s = b.get("status", "не прочитано")
        if s in stats:
            stats[s] += 1
        g = b.get("genre", "").strip()
        if g:
            stats["genres"][g] = stats["genres"].get(g, 0) + 1
    return stats
