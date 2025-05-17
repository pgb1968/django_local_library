from django.db import models

# Create your models here.

from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a genre" )

    class Meta:
       ordering = ['name']

    def __str__(self):
       return self.name


class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter language")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    date_of_birth = models.DateField('Born', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    

class Book(models.Model):
    title  = models.CharField(max_length = 200)
    author = models.ForeignKey(Author,
                null = True,
                on_delete = models.SET_NULL)
    summary = models.TextField(max_length = 1000,
                help_text = 'Describe the book')
    isbn    = models.CharField('ISBN', max_length = 13,
                unique = True, help_text = 'ISBN code')
    genre   = models.ForeignKey(Genre,
                                on_delete = models.SET_NULL,
                                null = True)
    language = models.ForeignKey(Language,
                                 on_delete = models.SET_NULL,
                                 null = True)

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
 

import uuid
from datetime import date
from django.contrib.auth.models import User

class BookInstance(models.Model):
    id = models.UUIDField(primary_key = True,
                          default = uuid.uuid4,
                          help_text = "Unique ID for book")
    book = models.ForeignKey(Book, 
                             on_delete = models.RESTRICT,
                             null = True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User,
                                 on_delete = models.SET_NULL,
                                 null = True,
                                 blank = True)
    LOAN_STATUS = ( ('d', 'Maintenance'),
                    ('o', 'On loan'),
                    ('a', 'Available'),
                    ('r', 'Reserved'),)
    status = models.CharField(max_length = 1,
                              choices = LOAN_STATUS,
                              blank = True,
                              default = 'd',
                              help_text = 'Book availability')

    def is_overdue(self):
        return bool(self.due_back and (date.today() > self.due_back))

    class Meta:
        ordering = ['due_back', 'book']
        permissions = ( ("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    