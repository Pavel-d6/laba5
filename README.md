# Лабораторная работа №4: Симуляция библиотеки

## Описание

Система управления библиотекой с пользовательскими коллекциями и симуляцией событий.

## Вариант

**Вариант 1: "Библиотека"**

## Структура проекта

```
laba4/
├── src/
│   ├── book.py              # Классы книг (Book, LibraryBook, EBook)
│   ├── Сollection.py        # Пользовательские коллекции
│   ├── library.py           # Класс Library
│   └── simulation.py        # Симуляция событий
├── main.py                  # Точка входа
└── README.md               # Этот файл
```

## Требования

- Python 3.10+
- Стандартная библиотека Python (дополнительных пакетов не требуется)

## Установка и запуск

```bash
# Клонировать или скачать проект
cd laba4

# Запустить симуляцию
python main.py
```

## Реализованные компоненты

### 1. Классы предметной области

#### `Book` (базовый класс)
Содержит общие поля для всех типов книг:
- title, author, year, genre, isbn
- Магический метод `__add__()` для объединения книг

#### `LibraryBook` (библиотечная книга)
Расширяет `Book`:
- inventory_number, shelf_location
- Методы: `borrow()`, `return_book()`

#### `EBook` (электронная книга)
Расширяет `Book`:
- file_size_mb, format_type
- Метод: `download()`

### 2. Пользовательские коллекции

#### `BookCollection` (списочная коллекция через композицию)
Поддерживает:
- `__iter__` - итерация по книгам
- `__len__` - количество книг
- `__getitem__` - доступ по индексу и срезам
- `__contains__` - проверка наличия книги
- `add_book()`, `remove_book()` - добавление/удаление

#### `IndexDict` (словарная коллекция)
Тройная индексация книг:
- По ISBN (уникальный ключ)
- По автору (список книг)
- По году (список книг)

Поддерживает:
- `__iter__` - итерация по уникальным книгам
- `__len__` - количество книг
- `__getitem__` - универсальный поиск (ISBN/автор/год)
- `__contains__` - проверка наличия
- `add_book()`, `remove_book()` - синхронизированное добавление/удаление

### 3. Класс Library

Связывает коллекции и предоставляет API:
- Методы добавления/удаления книг
- Методы поиска: по автору, году, ISBN, жанру, названию
- Автоматическая синхронизация между `BookCollection` и `IndexDict`
- Статистика библиотеки

### 4. Симуляция

#### Функция `run_simulation(steps, seed)`
Параметры:
- `steps` - количество шагов симуляции (по умолчанию 20)
- `seed` - seed для генератора случайных чисел (для воспроизводимости)

#### Типы событий (6 штук):
1. Добавление новой книги
2. Удаление случайной книги
3. Поиск по автору
4. Поиск по году издания
5. Поиск несуществующего автора (проверка обработки)
6. Проверка статистики библиотеки

Все события логируются в консоль в формате:
```
[Шаг  5 | 14:32:15] Добавлена книга: 'Тайна старого замка #421' (LibraryBook)
```

## Примеры использования

### Базовое использование

```python
from library import Library
from book import Book, LibraryBook, EBook

# Создание библиотеки
library = Library("Моя библиотека")

# Добавление книг
book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "ISBN-001")
library.add_book(book1)

book2 = LibraryBook(
    "1984", "Джордж Оруэлл", 1949, "Антиутопия", "ISBN-002",
    inventory_number="INV-001", shelf_location="A1"
)
library.add_book(book2)

# Поиск
books_by_author = library.search_by_author("Лев Толстой")
books_by_year = library.search_by_year(1949)
book_by_isbn = library.search_by_isbn("ISBN-001")

# Статистика
print(library.get_stats())
```

### Работа с коллекциями

```python
from Сollection import BookCollection, IndexDict

# BookCollection
collection = BookCollection()
collection.add_book(book1)
collection.add_book(book2)

# Доступ по индексу
first_book = collection[0]

# Срезы
slice_books = collection[0:2]

# Итерация
for book in collection:
    print(book.title)

# IndexDict
index = IndexDict()
index.add_book(book1)
index.add_book(book2)

# Поиск по разным ключам
by_isbn = index["ISBN-001"]           # Книга
by_author = index["Лев Толстой"]      # Список книг
by_year = index[1949]                  # Список книг
```

### Запуск симуляции

```python
from simulation import run_simulation

# Симуляция с воспроизводимостью
run_simulation(steps=20, seed=42)

# Симуляция со случайными событиями
run_simulation(steps=30, seed=None)
```

## Ключевые особенности

### Композиция
`BookCollection` использует композицию вместо наследования:
```python
class BookCollection:
    def __init__(self):
        self._books: List[Book] = []  # Список внутри объекта
```

`IndexDict` поддерживает три типа индексов для быстрого поиска O(1):
```python
self._isbn_index = {}     # ISBN → книга
self._author_index = {}   # автор → [книги]
self._year_index = {}     # год → [книги]
```



seed гарантирует идентичную последовательность событий:
```python
random.seed(42)  
```

