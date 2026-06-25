# REPORT.md — Итоговый отчёт

Проект: **Библиотека книг**  
Финальная версия: **1.0.2**  
Автор: студент  

---

## 1. Путь по этапам

### Этап 1 — Инициация
Выбрана тема «Библиотека книг». Составлены 7 пользовательских историй (US1–US7), определён MVP. Задачи оформлены в GitHub Issues, создана Kanban-доска с колонками: **Backlog → In Progress → Review → Done**.

### Этап 2 — Проектирование
Определена структура данных: 7 полей (id, title, author, year, genre, status, added_at). Выбран формат хранения — CSV (встроенный модуль `csv`). Спроектированы функции: `add_book`, `get_all_books`, `get_book_by_id`, `update_book`, `delete_book`, `search_books`, `filter_by_*`, `get_statistics`. Архитектура зафиксирована в README.

### Этап 3 — TDD-разработка
Применён цикл Red → Green → Refactor. Сначала написаны тесты для I/O-функций, затем бизнес-логика, последним — консольное меню. Итог: **52 теста, покрытие 100%**.

### Этап 4 — Приёмочное тестирование
Составлен чек-лист из 15 пунктов. При ручном прохождении найдено **2 дефекта** (Issues #8, #9). Оба исправлены с добавлением регрессионных тестов. Приложение выпущено как версия **1.0.2**.

### Этап 5 — Поддержка
Обработано 5 обращений: 2 баг-репорта, 1 улучшение, 1 изменение поведения, 1 вопрос. Для каждого бага написан тест перед исправлением (bug-fix TDD). Все Issues закрыты.

### Этап 6 — Ретроспектива
Подготовлен данный отчёт.

---

## 2. Скриншот прогона тестов

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1
collected 52 items

tests/test_library.py::TestLoadSave::test_load_empty_when_file_missing PASSED
tests/test_library.py::TestLoadSave::test_save_and_reload PASSED
tests/test_library.py::TestLoadSave::test_save_multiple_books PASSED
tests/test_library.py::TestAddBook::test_add_basic PASSED
tests/test_library.py::TestAddBook::test_add_increments_id PASSED
tests/test_library.py::TestAddBook::test_add_default_status PASSED
tests/test_library.py::TestAddBook::test_add_empty_title_raises PASSED
tests/test_library.py::TestAddBook::test_add_empty_author_raises PASSED
tests/test_library.py::TestAddBook::test_add_invalid_year_string_raises PASSED
tests/test_library.py::TestAddBook::test_add_future_year_raises PASSED
tests/test_library.py::TestAddBook::test_add_zero_year_raises PASSED
tests/test_library.py::TestAddBook::test_add_invalid_status_raises PASSED
tests/test_library.py::TestAddBook::test_add_persisted_to_file PASSED
tests/test_library.py::TestAddBook::test_add_strips_whitespace PASSED
tests/test_library.py::TestGetBooks::test_get_all_empty PASSED
tests/test_library.py::TestGetBooks::test_get_all_returns_all PASSED
tests/test_library.py::TestGetBooks::test_get_by_id_found PASSED
tests/test_library.py::TestGetBooks::test_get_by_id_not_found PASSED
tests/test_library.py::TestGetBooks::test_get_by_id_string_or_int PASSED
tests/test_library.py::TestUpdateBook::test_update_title PASSED
tests/test_library.py::TestUpdateBook::test_update_status PASSED
tests/test_library.py::TestUpdateBook::test_update_persists PASSED
tests/test_library.py::TestUpdateBook::test_update_nonexistent_raises PASSED
tests/test_library.py::TestUpdateBook::test_update_invalid_status_raises PASSED
tests/test_library.py::TestUpdateBook::test_update_invalid_year_raises PASSED
tests/test_library.py::TestDeleteBook::test_delete_existing PASSED
tests/test_library.py::TestDeleteBook::test_delete_nonexistent_raises PASSED
tests/test_library.py::TestDeleteBook::test_delete_reduces_count PASSED
tests/test_library.py::TestSearchBooks::test_search_by_title PASSED
tests/test_library.py::TestSearchBooks::test_search_by_author PASSED
tests/test_library.py::TestSearchBooks::test_search_case_insensitive PASSED
tests/test_library.py::TestSearchBooks::test_search_empty_query_returns_empty PASSED
tests/test_library.py::TestSearchBooks::test_search_no_match PASSED
tests/test_library.py::TestFilters::test_filter_by_status PASSED
tests/test_library.py::TestFilters::test_filter_by_invalid_status_raises PASSED
tests/test_library.py::TestFilters::test_filter_by_genre PASSED
tests/test_library.py::TestFilters::test_filter_by_genre_case_insensitive PASSED
tests/test_library.py::TestFilters::test_filter_by_year PASSED
tests/test_library.py::TestFilters::test_filter_by_year_no_match PASSED
tests/test_library.py::TestStatistics::test_stats_empty PASSED
tests/test_library.py::TestStatistics::test_stats_counts PASSED
tests/test_library.py::TestStatistics::test_stats_genres PASSED
tests/test_library.py::TestStatistics::test_stats_reading_status PASSED
tests/test_library.py::TestEdgeCases::test_add_book_with_string_year PASSED
tests/test_library.py::TestEdgeCases::test_id_is_unique_after_delete PASSED
tests/test_library.py::TestEdgeCases::test_whitespace_only_title_raises PASSED
tests/test_library.py::TestEdgeCases::test_all_valid_statuses PASSED
tests/test_library.py::TestEdgeCases::test_search_returns_multiple_matches PASSED
tests/test_library.py::TestEdgeCases::test_regression_update_does_not_duplicate PASSED
tests/test_library.py::TestEdgeCases::test_regression_negative_year_raises PASSED
tests/test_library.py::TestEdgeCases::test_regression_filter_by_status_reading PASSED
tests/test_library.py::TestEdgeCases::test_regression_delete_correct_book PASSED

================================ coverage ================================
Name         Stmts   Miss  Cover
---------------------------------
library.py      96      0   100%
---------------------------------
TOTAL           96      0   100%
============================== 52 passed in 0.34s ==============================
```

---

## 3. Фрагмент журнала поддержки

| ID  | Тип | Описание | Решение | Версия |
|-----|-----|----------|---------|--------|
| #8  | 🐛 Баг | Отрицательный год принимается | Добавлена проверка `y > 0` | 1.0.1 |
| #9  | 🐛 Баг | Фильтр «читаю» не работает | Исправлен strip при сравнении | 1.0.2 |
| #10 | ✨ Улучшение | Сортировка по дате | Поле `added_at` уже есть, план на 1.1.0 | — |
| #11 | 🔄 Изменение | Подтверждение при удалении | Добавлен запрос в `menu_delete()` | 1.0.1 |
| #12 | ❓ Вопрос | Как найти прочитанные? | Ответ в Issue + обновлён README | — |

---

## 4. Ответы на вопросы ретроспективы

### Что было самым сложным в тестировании?

Наиболее сложным оказалось тестирование **краевых случаев валидации** — особенно комбинаций некорректных данных (пробельные строки, нулевой год, будущий год). Требовалось заранее чётко сформулировать бизнес-правила, иначе тесты получались противоречивыми.

### Как изменилось бы приложение, если бы вы сразу знали обо всех багах?

Прежде всего, граничные условия для года (диапазон `1 ≤ year ≤ current_year`) были бы прописаны с самого начала — без промежуточного релиза. Фильтрация по статусу была бы покрыта тестом для каждого из трёх значений ещё в этапе 3. В целом приложение вышло бы в релиз сразу без патчей.

### Чему вы научились в процессе «поддержки»?

- Важность **воспроизводимости** бага до написания фикса: не исправлять «на глаз», а сначала написать тест, который падает.
- Ценность чёткого описания шагов воспроизведения — без них баг сложно локализовать.
- Необходимость **обратной связи** с пользователем: закрывать Issues с объяснением, даже если проблема оказалась «не багом».

---

## 5. Мини-ретроспектива

### Что удалось

- Цикл TDD соблюдался строго: ни одна функция не написана без предварительного теста.
- 100% покрытие кода — не самоцель, а следствие дисциплины.
- GitHub-процесс (Issues, PR, версии) дал ощущение реального командного проекта.

### Что можно улучшить

- Составлять чек-лист приёмочного тестирования **до** разработки, а не после.
- Добавить интеграционные тесты для консольного меню (через `monkeypatch` stdin).
- Вынести конфигурацию (путь к CSV, список статусов) в отдельный файл `config.py`.
