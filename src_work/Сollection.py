from typing import Union, List, Optional, Iterator
from book import Book


class BookCollection:
    """
    Пользовательская списочная коллекция книг.
    """
    def __init__(self, books: Optional[List[Book]] = None):
        self._books: List[Book] = []
        if books:
            self._books.extend(books)
    
    def __getitem__(self, key: Union[int, slice]) -> Union[Book, 'BookCollection']:
        if isinstance(key, slice):
            return BookCollection(self._books[key])
        else:
            return self._books[key]
    
    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)
    
    def __len__(self) -> int:
        return len(self._books)
    
    def __repr__(self) -> str:
        book_titles = [f"'{book.title}'" for book in self._books[:3]]
        if len(self._books) > 3:
            book_titles.append(f"...(+{len(self._books) - 3})")
        return f"BookCollection([{', '.join(book_titles)}])"
    
    def __contains__(self, item: Book) -> bool:
        return item in self._books
    
    def add_book(self, book: Book) -> None:
        self._books.append(book)
    
    def remove_book(self, book: Book) -> bool:
        try:
            self._books.remove(book)
            return True
        except ValueError:
            return False
    
    def get_random_book(self) -> Optional[Book]:
        import random
        if not self._books:
            return None
        return random.choice(self._books)
    
    def find_by_genre(self, genre: str) -> List[Book]:
        return [book for book in self._books if book.genre == genre]


class IndexDict:
    """
    Пользовательская словарная коллекция книг.
    Индексирует книги по ISBN, автору, году.
    """
    def __init__(self):
        self._isbn_index: dict[str, Book] = {}
        self._author_index: dict[str, List[Book]] = {}
        self._year_index: dict[int, List[Book]] = {}
    
    def __getitem__(self, key: Union[str, int]) -> Union[Book, List[Book]]:
        if isinstance(key, str) and key in self._isbn_index:
            return self._isbn_index[key]
        
        if isinstance(key, str) and key in self._author_index:
            return self._author_index[key]
        
        if isinstance(key, int):
            return self._year_index.get(key, [])
        
        raise KeyError(f"Ключ '{key}' не найден в индексах")
    
    def __iter__(self) -> Iterator[Book]:
        return iter(self._isbn_index.values())
    
    def __len__(self) -> int:
        return len(self._isbn_index)
    
    def __repr__(self) -> str:
        return (f"IndexDict(книг: {len(self)}, "
                f"авторов: {len(self._author_index)}, "
                f"лет: {len(self._year_index)})")
    
    def __contains__(self, item: Union[str, Book]) -> bool:
        if isinstance(item, str):
            return item in self._isbn_index
        elif isinstance(item, Book):
            return item.isbn in self._isbn_index
        return False
    
    def add_book(self, book: Book) -> bool:
        if book.isbn in self._isbn_index:
            print(f"Книга с ISBN {book.isbn} уже существует в индексе")
            return False
        
        self._isbn_index[book.isbn] = book
        
        if book.author not in self._author_index:
            self._author_index[book.author] = []
        self._author_index[book.author].append(book)
        
        if book.year not in self._year_index:
            self._year_index[book.year] = []
        self._year_index[book.year].append(book)
        
        return True
    
    def remove_book(self, book: Book) -> bool:
        if book.isbn not in self._isbn_index:
            return False
        
        del self._isbn_index[book.isbn]
        
        if book.author in self._author_index:
            author_books = self._author_index[book.author]
            author_books.remove(book)
            
            if not author_books:
                del self._author_index[book.author]
        
        if book.year in self._year_index:
            year_books = self._year_index[book.year]
            year_books.remove(book)
            
            if not year_books:
                del self._year_index[book.year]
        
        return True
    
    def rebuild_from_collection(self, collection: BookCollection) -> None:
        self._isbn_index.clear()
        self._author_index.clear()
        self._year_index.clear()
        
        for book in collection:
            self.add_book(book)
        
        print(f"Индексы перестроены. Добавлено {len(collection)} книг")
    
    def search_by_genre(self, genre: str) -> List[Book]:
        result = []
        for book in self:
            if book.genre == genre:
                result.append(book)
        return result
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default