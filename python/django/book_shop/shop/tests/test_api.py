from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Book
from shop.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Book 1', price=504.53)
        book_2 = Book.objects.create(name='Book 2', price=809.27)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

