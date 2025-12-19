from datetime import datetime


class Book: 
    """
    Базовый класс для любой книги.
    """
    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn
        self.is_available = True
        self.date_added = datetime.now().date()
    
    def __repr__(self) -> str:
        return f"'{self.title}' - {self.author} ({self.year})"
    
    def __str__(self) -> str:
        return f"Книга: {self.title}, Автор: {self.author}"
    
    def __add__(self, other) -> str:
        if isinstance(other, Book):
            return f"Подборка: '{self.title}' и '{other.title}'"
        return "Можно объединять только книги"
    
    def get_full_info(self) -> str:
        """информация о книге"""

        return (f"Название: {self.title}\n"
                f"Автор: {self.author}\n"
                f"Год: {self.year}\n"
                f"Жанр: {self.genre}\n"
                f"ISBN: {self.isbn}\n"
                f"Доступна: {'Да' if self.is_available else 'Нет'}")


class LibraryBook(Book):
    """
    Физическая книга, которая хранится в библиотеке.
    """
    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str,
                 inventory_number: str, shelf_location: str):
        super().__init__(title, author, year, genre, isbn)
        self.inventory_number = inventory_number
        self.shelf_location = shelf_location
        self.is_borrowed = False
        self.current_borrower = None
    
    def __repr__(self) -> str:
        """Строковое представление книги"""
        return f"[Библиотечная] {super().__repr__()} (№{self.inventory_number})"
    
    def borrow(self, borrower_name: str) -> str:
        """Выдать книгу читателю"""

        if self.is_borrowed:
            return f"Книга '{self.title}' уже выдана {self.current_borrower}"
        
        self.is_borrowed = True
        self.is_available = False
        self.current_borrower = borrower_name
        
        return f"Книга '{self.title}' выдана {borrower_name}"
    
    def return_book(self) -> str:
        """Вернуть книгу в библиотеку"""
        if not self.is_borrowed:
            return f"Книга '{self.title}' не была выдана"
        
        borrower = self.current_borrower
        self.is_borrowed = False
        self.is_available = True
        self.current_borrower = None
        
        return f"Книга '{self.title}' возвращена от {borrower}"


class EBook(Book):
    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str,
                 file_size_mb: float, format_type: str):
        super().__init__(title, author, year, genre, isbn)
        self.file_size_mb = file_size_mb
        self.format_type = format_type
        self.download_count = 0
    
    def __repr__(self) -> str:
        """Строковое представление книги"""
        return f"[Электронная] {super().__repr__()} ({self.format_type}, {self.file_size_mb}MB)"
    
    def download(self, user_id: str) -> str:
        """Скачать книгу"""
        self.download_count += 1
        
        estimated_time = self.file_size_mb / 10
        return (f"Книга '{self.title}' скачивается пользователем {user_id}. "
                f"Формат: {self.format_type}, Размер: {self.file_size_mb}MB, "
                f"Примерное время: {estimated_time:.1f} сек. "
                f"Всего скачиваний: {self.download_count}")