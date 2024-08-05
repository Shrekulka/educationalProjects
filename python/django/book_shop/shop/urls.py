# book_shop/shop/urls.py

from django.urls import path

from shop.views import auth, BookListView, BookDetailView

urlpatterns = [
    path('auth/', auth, name='auth'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='book-detail'),
]
