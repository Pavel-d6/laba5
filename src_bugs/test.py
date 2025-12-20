import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from simulation import run_simulation
from library import Library
from book import Book, LibraryBook, EBook


print("\n" + "="*70)
print("ОШИБКА 1: Off-by-one")
print("="*70)
print("Ожидается: 5 шагов, Будет: 6 шагов")
input("Нажми Enter для запуска...")

run_simulation(steps=5, seed=42)


print("\n" + "="*70)
print("ОШИБКА 2: Неверное логическое условие")
print("="*70)
input("Нажми Enter для запуска...")

library = Library("Тестовая библиотека")
print("\n1. Создаём книгу с ПУСТЫМ ISBN")
book = Book("Тестовая книга", "Тестовый Автор", 2024, "Роман", "")

print("2. Пытаемся добавить")
result = library.add_book(book)

print(f"\n>>> Результат: {result}")
print(f">>> Книг в библиотеке: {len(library)}")



print("\n" + "="*70)
print("ОШИБКА 3: Изменение коллекции во время итерации")
print("="*70)
input("Нажми Enter для запуска...")

library2 = Library("Тестовая библиотека 2")

print("\n1. Добавляем 3 книги жанра 'Роман'...")
library2.add_book(Book("Роман 1", "Автор 1", 2020, "Роман", "R1"))
library2.add_book(Book("Роман 2", "Автор 2", 2021, "Роман", "R2"))
library2.add_book(Book("Роман 3", "Автор 3", 2022, "Роман", "R3"))
library2.add_book(Book("Детектив", "Автор 4", 2023, "Детектив", "D1"))

print(f"Книг в библиотеке: {len(library2)}")

print("\n2. Пытаемся удалить все романы через метод remove_books_by_genre...")
print(">>> ОЖИДАЕТСЯ RuntimeError или неправильное удаление!")

try:
    removed = library2.remove_books_by_genre("Роман")
    print(f"\nУдалено: {removed}")
    print(f"Осталось книг: {len(library2)}")
    if removed == 2 and len(library2) == 2:
        print(">>> ОШИБКА ВОСПРОИЗВЕДЕНА! Удалено только 2 из 3 книг")
        print(">>> Причина: изменение списка во время итерации пропускает элементы")
except RuntimeError as e:
    print(f"\n>>> RuntimeError: {e}")
    print(">>> ОШИБКА ВОСПРОИЗВЕДЕНА!")


print("\n" + "="*70)
print("ОШИБКА 4: Изменяемое значение по умолчанию")
print("="*70)
input("Нажми Enter для запуска")

print("\n1. Создаём две книги БЕЗ параметра tags")
book1 = LibraryBook("Книга 1", "Автор 1", 2020, "Роман", "B1", "INV-1", "A1")
book2 = LibraryBook("Книга 2", "Автор 2", 2021, "Роман", "B2", "INV-2", "A2")

if id(book1.tags) == id(book2.tags):
    print("\n3. Добавляем тег в book1...")
    book1.tags.append("классика")
    
    print(f"book1.tags: {book1.tags}")
    print(f"book2.tags: {book2.tags}")
    
    if "классика" in book2.tags:
        print(">>> ОШИБКА ВОСПРОИЗВЕДЕНА! Тег появился в book2!")


print("\n" + "="*70)
print("ОШИБКА 5: Сравнение через is вместо ==")
print("="*70)
input("Нажми Enter для запуска...")

library3 = Library("Тестовая библиотека 3")

print("\n1. Тест с БОЛЬШИМ числом")
print("Добавляем 300 книг одного автора")

for i in range(300):
    library3.add_book(Book(f"Книга {i}", "Популярный Автор", 2024, "Роман", f"POP-{i}"))

results = library3.search_by_author("Популярный Автор")

print(f"\nКоличество книг: {len(results)}")
print(f"len(results) == 300: {len(results) == 300}")
print(f"len(results) is 300: {len(results) is 300}")

print(f"\nid(len(results)): {id(len(results))}")
print(f"id(300): {id(300)}")

if len(results) == 300 and not (len(results) is 300):
    print(">>> ОШИБКА ВОСПРОИЗВЕДЕНА! == True, но is False")
    print(">>> Для больших чисел is не работает")

print("\n2. Тест с МАЛЕНЬКИМ числом")
library4 = Library("Тестовая библиотека 4")
library4.add_book(Book("Единственная", "Одинокий Автор", 2024, "Роман", "SOLO"))

results2 = library4.search_by_author("Одинокий Автор")

print(f"\nКоличество книг: {len(results2)}")
print(f"len(results) == 1: {len(results2) == 1}")
print(f"len(results) is 1: {len(results2) is 1}")

if len(results2) is 1:
    print(">>> Для числа 1 оператор is работает")
    print(">>> Это показывает случайность is для чисел")
    print(">>> В коде с большими числами это приведёт к багам")

