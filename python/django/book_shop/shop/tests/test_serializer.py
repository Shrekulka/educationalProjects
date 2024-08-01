from django.test import TestCase

from shop.models import Book
from shop.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Book 1', price=504.53)
        book_2 = Book.objects.create(name='Book 2', price=809.27)
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {'id': book_1.id, 'name': 'Book 1', 'price': '504.53', },
            {'id': book_2.id, 'name': 'Book 2', 'price': '809.27', }
        ]
        self.assertEqual(expected_data, data)
