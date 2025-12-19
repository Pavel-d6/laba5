from typing import List, Optional, Union
from book import Book, LibraryBook, EBook
from Сollection import BookCollection, IndexDict


class Library:
    def __init__(self, name: str = "Главная библиотека"):
        self.name = name
        self._books = BookCollection()
        self._index = IndexDict()
        self._total_operations = 0
    
    def add_book(self, book: Book) -> bool:
        self._total_operations += 1
        
        if book.isbn in self._index:
            print(f"Книга с ISBN {book.isbn} уже существует")
            return False
        
        self._books.add_book(book)
        self._index.add_book(book)
        
        print(f"Книга '{book.title}' добавлена в библиотеку '{self.name}'")
        return True
    
    def remove_book(self, identifier: Union[Book, str]) -> bool:
        self._total_operations += 1
        
        if isinstance(identifier, Book):
            book = identifier
        elif isinstance(identifier, str):
            book = self._index.get(identifier)
            if book is None:
                print(f"Книга с ISBN '{identifier}' не найдена")
                return False
        else:
            print(f"Неверный идентификатор: {type(identifier)}")
            return False
        
        removed_from_collection = self._books.remove_book(book)
        removed_from_index = self._index.remove_book(book)
        
        if removed_from_collection and removed_from_index:
            print(f"Книга '{book.title}' удалена из библиотеки")
            return True
        elif removed_from_collection != removed_from_index:
            print(f"Ошибка синхронизации при удалении книги '{book.title}'")
            return False
        else:
            print(f"Книга '{book.title}' не найдена в библиотеке")
            return False
    
    def search_by_author(self, author: str) -> List[Book]:
        self._total_operations += 1
        return self._index.get(author, [])
    
    def search_by_year(self, year: int) -> List[Book]:
        self._total_operations += 1
        return self._index.get(year, [])
    
    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        self._total_operations += 1
        return self._index.get(isbn)
    
    def search_by_genre(self, genre: str) -> List[Book]:
        self._total_operations += 1
        return self._books.find_by_genre(genre)
    
    def search_by_title(self, keyword: str) -> List[Book]:
        self._total_operations += 1
        keyword_lower = keyword.lower()
        results = []
        
        for book in self._books:
            if keyword_lower in book.title.lower():
                results.append(book)
        
        return results
    
    def get_all_books(self) -> BookCollection:
        return self._books
    
    def get_random_book(self) -> Optional[Book]:
        return self._books.get_random_book()
    
    def get_stats(self) -> dict:
        return {
            'library_name': self.name,
            'total_books': len(self._books),
            'unique_authors': len(self._index._author_index),
            'unique_years': len(self._index._year_index),
            'total_operations': self._total_operations,
        }
    
    def __len__(self) -> int:
        return len(self._books)
    
    def __contains__(self, item: Union[Book, str]) -> bool:
        if isinstance(item, Book):
            return item in self._books
        elif isinstance(item, str):
            return item in self._index
        return False
    
    def __repr__(self) -> str:
        return f"Library('{self.name}', книг: {len(self)})"
    
    def __str__(self) -> str:
        stats = self.get_stats()
        return (f"Библиотека '{self.name}'\n"
                f"Книг: {stats['total_books']} | "
                f"Авторов: {stats['unique_authors']} | "
                f"Операций: {stats['total_operations']}")