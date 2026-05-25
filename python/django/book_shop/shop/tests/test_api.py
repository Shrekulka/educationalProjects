import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Book
from shop.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(title='Book 1', author_name='Nick 1', price=504.53, slug=slugify('Book 1'))
        self.book_2 = Book.objects.create(title='Book 2', author_name='Nick 2', price=809.27, slug=slugify('Book 2'))
        self.book_3 = Book.objects.create(title='Book 3', author_name='Nick 3', price=504.53, slug=slugify('Book 3'))
        self.book_4 = Book.objects.create(title='Book 4', author_name='Nick 4', price=499.11, slug=slugify('Book 4'))
        self.book_5 = Book.objects.create(title='Book 5', author_name='Nick 5', price=504.53, slug=slugify('Book 5'))
        self.book_6 = Book.objects.create(title='Book 6 Nick 1', author_name='Nick 6', price=387.19,
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

    def test_create(self):
        self.assertEqual(6, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "title": "Hemingway: The Paris Years",
            "author_name": "Michael S. Reynolds",
            "price": 773.37
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(7, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "author_name": self.book_1.author_name,
            "price": 999.99,
            "slug": self.book_1.slug
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()  # или self.book_1 = Book.objects.get(id=self.book_1.id)
        self.assertEqual(Decimal('999.99'), self.book_1.price)
