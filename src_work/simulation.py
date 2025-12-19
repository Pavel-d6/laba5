import random
from datetime import datetime
from typing import Optional, Dict, List
from library import Library
from book import Book, LibraryBook, EBook


class LibrarySimulation:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
            self._seed = seed
        else:
            self._seed = None
        
        self.library = Library("Тестоавя библиотека")
        self._step = 0
        self._log: List[str] = []
        self._event_counts: Dict[str, int] = {}
        
        self._initialize_library()
    
    def _initialize_library(self) -> None:
        initial_books = [
            LibraryBook(
                title="Война и мир",
                author="Лев Толстой",
                year=1869,
                genre="Роман",
                isbn="SIM-001",
                inventory_number="INV-001",
                shelf_location="A1"
            ),
            LibraryBook(
                title="Преступление и наказание",
                author="Фёдор Достоевский",
                year=1866,
                genre="Роман",
                isbn="SIM-002",
                inventory_number="INV-002",
                shelf_location="A2"
            ),
            EBook(
                title="1984",
                author="Джордж Оруэлл",
                year=1949,
                genre="Антиутопия",
                isbn="SIM-003",
                file_size_mb=2.5,
                format_type="EPUB"
            ),
            EBook(
                title="Мастер и Маргарита",
                author="Михаил Булгаков",
                year=1967,
                genre="Роман",
                isbn="SIM-004",
                file_size_mb=3.2,
                format_type="PDF"
            ),
        ]
        
        for book in initial_books:
            self.library.add_book(book)
        
        self._log_event(f"Инициализация: добавлено {len(initial_books)} начальных книг")
    
    def _log_event(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[Шаг {self._step:3d} | {timestamp}] {message}"
        self._log.append(log_entry)
        print(log_entry)
    
    def _count_event(self, event_type: str) -> None:
        self._event_counts[event_type] = self._event_counts.get(event_type, 0) + 1
    
    def _generate_random_book(self) -> Book:
        titles = [
            "Тайна старого замка", "Путешествие во времени", 
            "Загадочный остров", "Город мечты", "Последний рубеж",
            "Секретная лаборатория", "Потерянный мир", "Звёздный путь"
        ]
        authors = [
            "Иван Иванов", "Анна Петрова", "Сергей Сидоров",
            "Мария Кузнецова", "Алексей Смирнов", "Елена Васильева"
        ]
        genres = ["Роман", "Фантастика", "Детектив", "Приключения", "История"]
        years = list(range(1900, 2024))
        
        book_type = random.choice(["library", "ebook", "simple"])
        
        title = random.choice(titles) + f" #{random.randint(1, 1000)}"
        author = random.choice(authors)
        year = random.choice(years)
        genre = random.choice(genres)
        isbn = f"RND-{random.randint(1000, 9999)}"
        
        if book_type == "library":
            return LibraryBook(
                title=title, author=author, year=year, genre=genre, isbn=isbn,
                inventory_number=f"INV-{random.randint(100, 999)}",
                shelf_location=f"{random.choice('ABCD')}{random.randint(1, 10)}"
            )
        elif book_type == "ebook":
            return EBook(
                title=title, author=author, year=year, genre=genre, isbn=isbn,
                file_size_mb=round(random.uniform(1.0, 10.0), 1),
                format_type=random.choice(["PDF", "EPUB", "MOBI", "FB2"])
            )
        else:
            return Book(title, author, year, genre, isbn)
    
    def _event_add_book(self) -> None:
        new_book = self._generate_random_book()
        success = self.library.add_book(new_book)
        
        if success:
            self._log_event(f"Добавлена книга: '{new_book.title}' ({type(new_book).__name__})")
            self._count_event("add_book")
        else:
            self._log_event(f"Не удалось добавить книгу (возможно, дубликат ISBN)")
            self._count_event("add_book_failed")
    
    def _event_remove_random_book(self) -> None:
        book = self.library.get_random_book()
        if book:
            success = self.library.remove_book(book)
            if success:
                self._log_event(f"Удалена книга: '{book.title}'")
                self._count_event("remove_book")
            else:
                self._log_event(f"Не удалось удалить книгу: '{book.title}'")
                self._count_event("remove_book_failed")
        else:
            self._log_event("Нечего удалять (библиотека пуста)")
            self._count_event("remove_book_empty")
    
    def _event_search_random_author(self) -> None:
        all_books = list(self.library.get_all_books())
        if not all_books:
            self._log_event("Поиск невозможен: библиотека пуста")
            self._count_event("search_empty")
            return
        
        random_book = random.choice(all_books)
        author = random_book.author
        
        results = self.library.search_by_author(author)
        self._log_event(f"Поиск по автору '{author}': найдено {len(results)} книг")
        self._count_event("search_author")
    
    def _event_search_random_year(self) -> None:
        all_books = list(self.library.get_all_books())
        if not all_books:
            self._log_event("Поиск невозможен: библиотека пуста")
            self._count_event("search_empty")
            return
        
        random_book = random.choice(all_books)
        year = random_book.year
        
        results = self.library.search_by_year(year)
        self._log_event(f"Поиск по году {year}: найдено {len(results)} книг")
        self._count_event("search_year")
    
    def _event_search_nonexistent(self) -> None:
        fake_authors = ["Неизвестный Автор", "Вымышленный Писатель", "Тестовый Тест"]
        fake_author = random.choice(fake_authors)
        
        results = self.library.search_by_author(fake_author)
        self._log_event(f"Поиск несуществующего автора '{fake_author}': найдено {len(results)} книг")
        self._count_event("search_nonexistent")
    
    def _event_check_statistics(self) -> None:
        stats = self.library.get_stats()
        self._log_event(f"Статистика: {stats['total_books']} книг, "
                       f"{stats['unique_authors']} авторов, "
                       f"{stats['unique_years']} лет издания")
        self._count_event("check_stats")
    
    def run_step(self) -> None:
        self._step += 1
        
        events = [
            self._event_add_book,
            self._event_remove_random_book,
            self._event_search_random_author,
            self._event_search_random_year,
            self._event_search_nonexistent,
            self._event_check_statistics,
        ]
        
        chosen_event = random.choice(events)
        chosen_event()
    
    def run(self, steps: int = 20) -> None:
        print("\n" + "="*60)
        print(f"НАЧАЛО СИМУЛЯЦИИ БИБЛИОТЕКИ")
        print(f"Seed: {self._seed if self._seed is not None else 'случайный'}")
        print(f"Шагов: {steps}")
        print("="*60 + "\n")
        
        for _ in range(steps):
            self.run_step()
        
        self._print_summary()
    
    def _print_summary(self) -> None:
        print("\n" + "="*60)
        print("ИТОГИ СИМУЛЯЦИИ")
        print("="*60)
        
        stats = self.library.get_stats()
        print(f"\nСтатистика библиотеки:")
        print(f"  Название: {stats['library_name']}")
        print(f"  Всего книг: {stats['total_books']}")
        print(f"  Уникальных авторов: {stats['unique_authors']}")
        print(f"  Уникальных лет: {stats['unique_years']}")
        print(f"  Всего операций: {stats['total_operations']}")
        
        print(f"\nСтатистика событий (всего {self._step} шагов):")
        for event_type, count in sorted(self._event_counts.items()):
            percentage = (count / self._step) * 100
            print(f"  {event_type}: {count} ({percentage:.1f}%)")
        
        print(f"\nСостояние коллекций:")
        print(f"  BookCollection: {len(self.library.get_all_books())} книг")
        print(f"  IndexDict: {stats['unique_authors']} авторов индексировано")
        
        print("\n" + "="*60)
        print("СИМУЛЯЦИЯ ЗАВЕРШЕНА")
        print("="*60)


def run_simulation(steps: int = 20, seed: Optional[int] = None) -> None:
    simulation = LibrarySimulation(seed)
    simulation.run(steps)