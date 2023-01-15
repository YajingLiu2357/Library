import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    summary = models.CharField(max_length=500)
    ISBN = models.CharField(max_length=100)
    slug = models.SlugField(max_length = 250, null = True, blank = True, allow_unicode=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Book, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.slug, self.id])






class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        return name

class BookCopies(models.Model):
    """Model representing a specific copy of a book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book across whole library')
    book = models.ForeignKey('Book', on_delete=models.PROTECT)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
        )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
        )
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'




