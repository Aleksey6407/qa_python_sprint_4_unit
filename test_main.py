import pytest
from main import BooksCollector


class TestBooksCollector:

# ----- Тесты для add_new_book -----
    def test_add_new_book():
        collector = BooksCollector()
        collector.add_new_book("Новая книга")
        assert "Новая книга" in collector.books_genre
        assert collector.books_genre["Новая книга"] == ""

    def test_add_new_book_too_long():
        collector = BooksCollector()
        long_name = "a" * 50
        collector.add_new_book(long_name)
        assert long_name not in collector.books_genre

    def test_add_new_book_empty():
        collector = BooksCollector()
        collector.add_new_book("")
        assert "" not in collector.books_genre

    # ----- Тесты для set_book_genre -----
    def test_set_book_genre():
        collector = BooksCollector()
        collector.books_genre["Книга"] = ""   # прямой доступ
        collector.set_book_genre("Книга", "Фантастика")
        assert collector.books_genre["Книга"] == "Фантастика"

    def test_set_book_genre_invalid_genre():
        collector = BooksCollector()
        collector.books_genre["Книга"] = ""
        collector.set_book_genre("Книга", "Не жанр")
        assert collector.books_genre["Книга"] == ""

    def test_set_book_genre_nonexistent_book():
        collector = BooksCollector()
        collector.set_book_genre("Нет книги", "Фантастика")
        assert collector.books_genre == {}

    # ----- Отдельный позитивный тест для get_book_genre -----
    def test_get_book_genre():
        collector = BooksCollector()
        collector.books_genre["Книга"] = "Ужасы"   # прямой доступ
        assert collector.get_book_genre("Книга") == "Ужасы"

    def test_get_book_genre_nonexistent():
        collector = BooksCollector()
        assert collector.get_book_genre("Нет") is None

    # ----- Тесты для get_books_with_specific_genre -----
    def test_get_books_with_specific_genre_success():
        collector = BooksCollector()
        collector.books_genre = {
            "Чужой": "Ужасы",
            "Книга2": "Фантастика",
            "Книга3": "Ужасы"
        }
        result = collector.get_books_with_specific_genre("Ужасы")
        assert result == ["Чужой", "Книга3"]

    def test_get_books_with_specific_genre_missing():
        collector = BooksCollector()
        collector.books_genre = {"Чужой": "Ужасы"}
        result = collector.get_books_with_specific_genre("Приключения")
        assert result == []

    def test_get_books_with_specific_genre_empty():
        collector = BooksCollector()
        assert collector.get_books_with_specific_genre("Фантастика") == []

    # ----- Тесты для get_books_for_children -----
    def test_get_books_for_children_success():
        collector = BooksCollector()
        collector.books_genre = {
            "Властелин колец": "Фантастика",
            "Король лев": "Мультфильмы",
            "Сон в летнюю ночь": "Комедии",
            "Чужой": "Ужасы"   # Ужасы – возрастной рейтинг, не попадёт
        }
        result = collector.get_books_for_children()
        # Только книги с жанром не из genre_age_rating
        assert result == ["Властелин колец", "Король лев", "Сон в летнюю ночь"]

    def test_get_books_for_children_only_age_rating():
        collector = BooksCollector()
        collector.books_genre = {
            "Страшная": "Ужасы",
            "Детектив": "Детективы"
        }
        result = collector.get_books_for_children()
        assert result == []

    # ----- Тесты для избранного -----
    def test_add_book_in_favorites():
        collector = BooksCollector()
        collector.books_genre = {"Книга": "Фантастика"}
        collector.add_book_in_favorites("Книга")
        assert "Книга" in collector.favorites

    def test_add_book_in_favorites_already():
        collector = BooksCollector()
        collector.books_genre = {"Книга": "Фантастика"}
        collector.favorites = ["Книга"]
        collector.add_book_in_favorites("Книга")
        assert collector.favorites == ["Книга"]   # не дублируется

    def test_delete_book_from_favorites():
        collector = BooksCollector()
        collector.favorites = ["Книга1", "Книга2"]
        collector.delete_book_from_favorites("Книга1")
        assert collector.favorites == ["Книга2"]

    def test_get_list_of_favorites_books():
        collector = BooksCollector()
        collector.favorites = ["Книга1", "Книга2"]
        assert collector.get_list_of_favorites_books() == ["Книга1", "Книга2"]

    def test_get_books_genre():
        collector = BooksCollector()
        # Наполняем словарь напрямую, потому что тестируем только get_books_genre()
        test_dict = {
            "Книга1": "Фантастика",
            "Книга2": "Ужасы",
            "Книга3": ""
        }
        collector.books_genre = test_dict.copy()
        # Проверяем, что метод возвращает точно такой же словарь
        assert collector.get_books_genre() == test_dict

    def test_get_books_genre_empty():
        collector = BooksCollector()
        # Изначально словарь пуст
        assert collector.get_books_genre() == {}