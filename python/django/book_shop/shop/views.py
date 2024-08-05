# book_shop/shop/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from shop.models import Book
from shop.serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['price']
    search_fields = ['title', 'autor_name']
    ordering_fields = ['title', 'autor_name', 'price']


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'
    slug_url_kwarg = 'slug'


def auth(request):
    return render(request, "oauth.html")
