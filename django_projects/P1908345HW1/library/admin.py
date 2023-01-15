from django.contrib import admin

# Register your models here.
from .models import Book, Author, BookCopies

class BookCopiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status', 'due_back')
    list_filter = ('due_back', 'status',)

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookCopies, BookCopiesAdmin)
