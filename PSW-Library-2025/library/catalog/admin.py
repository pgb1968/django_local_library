from django.contrib import admin

# Register your models here.

from .models import Author, Book, Genre, Language, BookInstance

class BooksInline(admin.TabularInline):
    extra = 0
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name',
                  ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]
    
class BooksInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre')
    inlines = [BooksInstanceInline]
    
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    fieldsets    = (
                        (None, {'fields': ('book', 'imprint', 'id')}),
                        ('Availability', {'fields': ('status', 'due_back', 'borrower')}),
                   )



admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

