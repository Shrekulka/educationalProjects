from django.test import TestCase

from shop.models import Book
from shop.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(title='Book 1', price=504.53, author_name='Author 1')
        book_2 = Book.objects.create(title='Book 2', price=809.27, author_name='Author 2')
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {'id': book_1.id, 'title': 'Book 1', 'slug': 'book-1', 'price': '504.53', 'author_name': 'Author 1'},
            {'id': book_2.id, 'title': 'Book 2', 'slug': 'book-2', 'price': '809.27', 'author_name': 'Author 2'}
        ]
        self.assertEqual(expected_data, data)
