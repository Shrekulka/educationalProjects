from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Book
from shop.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(title='Book 1', autor_name='Nick 1', price=504.53, slug=slugify('Book 1'))
        self.book_2 = Book.objects.create(title='Book 2', autor_name='Nick 2', price=809.27, slug=slugify('Book 2'))
        self.book_3 = Book.objects.create(title='Book 3', autor_name='Nick 3', price=504.53, slug=slugify('Book 3'))
        self.book_4 = Book.objects.create(title='Book 4', autor_name='Nick 4', price=499.11, slug=slugify('Book 4'))
        self.book_5 = Book.objects.create(title='Book 5', autor_name='Nick 5', price=504.53, slug=slugify('Book 5'))
        self.book_6 = Book.objects.create(title='Book 6 Nick 1', autor_name='Nick 6', price=387.19,
                                          slug=slugify('Book 6 Nick 1'))

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer(
            [self.book_1, self.book_2, self.book_3, self.book_4, self.book_5, self.book_6], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': '504.53'})
        serializer_data = BooksSerializer([self.book_1, self.book_3, self.book_5], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Nick 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_6], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
