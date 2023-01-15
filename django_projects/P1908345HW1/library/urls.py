from django.urls import path
from . import views
urlpatterns = [
    path('',views.HomePageView.as_view(), name='home'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/<slug:slug>-<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('myBooks/', views.BookListMyView.as_view(), name='book_mylist'),
    path('book/new/', views.BookCreateView.as_view(), name='book_new'),
    path('allBorrowedbooks', views.BookBorrowedList.as_view(), name="borrowed_book"),
    path('search-form/', views.search_form,name='search_form'),
    path('search/', views.search, name='search'),
    path('changeBookStatus/<int:book_id>', views.changeStatus, name="status"),
    path('book/<int:pk>/result', views.ResultsView.as_view(), name="results"),
]