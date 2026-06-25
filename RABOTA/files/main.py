"""
Консольный интерфейс библиотеки книг.
Запуск: python main.py
"""

from library import (
    add_book, get_all_books, get_book_by_id,
    update_book, delete_book,
    search_books, filter_by_status, filter_by_genre, filter_by_year,
    get_statistics, VALID_STATUSES,
)

VERSION = "1.0.0"
DATA_FILE = "books.csv"


def _print_book(b):
    print(
        f"  [{b['id']}] \"{b['title']}\" - {b['author']}, {b['year']} г."
        f"  | {b['genre'] or 'жанр не указан'} | {b['status']}"
    )


def _print_books(books):
    if not books:
        print("  Книги не найдены.")
    else:
        for b in books:
            _print_book(b)


def menu_add():
    print("\n-- Добавить книгу --")
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    year = input("Год издания: ").strip()
    genre = input("Жанр (необязательно): ").strip()
    print(f"Статус: {', '.join(VALID_STATUSES)}")
    status = input("Статус [не прочитано]: ").strip() or "не прочитано"
    try:
        book = add_book(title, author, year, genre, status, DATA_FILE)
        print(f"Добавлена книга #{book['id']}: \"{book['title']}\"")
    except ValueError as e:
        print(f"Ошибка: {e}")


def menu_list():
    print("\n-- Все книги --")
    _print_books(get_all_books(DATA_FILE))


def menu_search():
    print("\n-- Поиск --")
    q = input("Введите запрос (название или автор): ").strip()
    _print_books(search_books(q, DATA_FILE))


def menu_filter():
    print("\n-- Фильтрация --")
    print("1. По статусу  2. По жанру  3. По году")
    choice = input("Выбор: ").strip()
    if choice == "1":
        print(f"Статусы: {', '.join(VALID_STATUSES)}")
        status = input("Статус: ").strip()
        try:
            _print_books(filter_by_status(status, DATA_FILE))
        except ValueError as e:
            print(f"Ошибка: {e}")
    elif choice == "2":
        genre = input("Жанр: ").strip()
        _print_books(filter_by_genre(genre, DATA_FILE))
    elif choice == "3":
        year = input("Год: ").strip()
        _print_books(filter_by_year(year, DATA_FILE))
    else:
        print("Неизвестный вариант.")


def menu_update():
    print("\n-- Редактировать книгу --")
    book_id = input("ID книги: ").strip()
    book = get_book_by_id(book_id, DATA_FILE)
    if not book:
        print(f"Книга #{book_id} не найдена.")
        return
    _print_book(book)
    print("Оставьте поле пустым, чтобы не менять значение.")
    fields = {}
    for field, label in [("title", "Название"), ("author", "Автор"),
                          ("year", "Год"), ("genre", "Жанр"), ("status", "Статус")]:
        val = input(f"{label} [{book[field]}]: ").strip()
        if val:
            fields[field] = val
    if not fields:
        print("Изменений нет.")
        return
    try:
        updated = update_book(book_id, DATA_FILE, **fields)
        print(f"Книга #{book_id} обновлена.")
        _print_book(updated)
    except (KeyError, ValueError) as e:
        print(f"Ошибка: {e}")


def menu_delete():
    print("\n-- Удалить книгу --")
    book_id = input("ID книги: ").strip()
    book = get_book_by_id(book_id, DATA_FILE)
    if not book:
        print(f"Книга #{book_id} не найдена.")
        return
    _print_book(book)
    confirm = input("Удалить? (да/нет): ").strip().lower()
    if confirm == "да":
        try:
            delete_book(book_id, DATA_FILE)
            print(f"Книга #{book_id} удалена.")
        except KeyError as e:
            print(f"Ошибка: {e}")
    else:
        print("Отменено.")


def menu_stats():
    print("\n-- Статистика --")
    st = get_statistics(DATA_FILE)
    print(f"  Всего книг   : {st['total']}")
    print(f"  Прочитано    : {st['прочитано']}")
    print(f"  Читаю        : {st['читаю']}")
    print(f"  Не прочитано : {st['не прочитано']}")
    if st["genres"]:
        print("  Жанры:")
        for g, cnt in sorted(st["genres"].items(), key=lambda x: -x[1]):
            print(f"    {g}: {cnt}")


MENU = {
    "1": ("Добавить книгу", menu_add),
    "2": ("Все книги", menu_list),
    "3": ("Поиск", menu_search),
    "4": ("Фильтрация", menu_filter),
    "5": ("Редактировать", menu_update),
    "6": ("Удалить книгу", menu_delete),
    "7": ("Статистика", menu_stats),
    "0": ("Выход", None),
}


def main():
    print(f"Библиотека книг v{VERSION}")
    while True:
        print("\n" + "-" * 30)
        for key, (label, _) in MENU.items():
            print(f"  {key}. {label}")
        choice = input("Выбор: ").strip()
        if choice == "0":
            print("До свидания!")
            break
        if choice in MENU:
            MENU[choice][1]()
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()