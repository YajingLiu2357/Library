from django.views.generic import TemplateView, ListView, DetailView
from .models import Book, Author, BookCopies
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse



class HomePageView(TemplateView):
    template_name = 'home.html'
class BookListView(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'library_BookList'

    def get_context_data(self, **kwargs):
        #Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        #Create any data add it to the context
        context['section']='dashboard'
        return context
class AuthorListView(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'library_AuthorList'
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_detail.html'
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
class BookListMyView(LoginRequiredMixin, ListView):
    template_name='bookcopies_list.html'
    paginate_by = 2
    def get_queryset(self):
        return models.BookCopies.objects.filter(borrower=self.request.user)

    def get_context_data(self, **kwargs):
        #Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        #Create any data add it to the context
        context['section']='myBooks'
        return context

class BookCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'library.add_book'
    model = models.Book
    template_name = 'book_new.html'
    fields = ['title','author','summary','ISBN']

    def get_context_data(self, **kwargs):
        #Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        #Create any data add it to the context
        context['section']='newBooks'
        return context

class BookBorrowedList(PermissionRequiredMixin, ListView):
    template_name='bookcopies_list.html'
    permission_required = 'library.add_book'
    paginate_by = 2
    def get_queryset(self):
        return models.BookCopies.objects.filter(status="o")

    def get_context_data(self, **kwargs):
        #Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        #Create any data add it to the context
        context['section']='borrowedBooks'
        return context


def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    error = False
    # print("DEBUG: SEARCH")
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if not q:
            error = True
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html', {'books': books, 'query': q})
    return render (request, 'search_form.html', {'error': error})

def changeStatus(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        selected_bookcopy=book.bookcopies_set.get(pk=request.POST['choice'])
    except(KeyError, BookCopies.DoesNotExist):
        return render(request, 'book_detail.html', {
            'book': book,
            'error_message': "You didn't select a bookcopy.",})
    else:
        selected_bookcopy.status = 'o'
        selected_bookcopy.borrower=request.user
        selected_bookcopy.save()
        return HttpResponseRedirect(reverse('results', args=(book.id,)))

class ResultsView(DetailView):
    model = Book
    template_name = 'results.html'


