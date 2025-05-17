from django.urls import path
from . import views

urlpatterns = [ path('' , views.index, name='index'),
                path('books/' , views.BookListView.as_view() , name='books' ),
                path('authors/', views.AuthorListView.as_view(), name='authors'),
                path('book/<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
                path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail') ,
                path('resetlogin/<path:next>', views.resetlogin, name='resetlogin') ,
                path('loaned_books/', views.AllLoanedBooksListView.as_view(), name='all-loaned-books'),
                path('book/<uuid:pk>/renew/', views.renew_book_librarian,name='renew-book-librarian') ,
                path('signup/<path:next>', views.user_signup, name='signup'),
                path('search_book_librarian', views.search_book_librarian, name='search-book-librarian'),
                path('set_book_on_maintenance/<uuid:pk>',views.set_book_on_maintenance,name='set-book-on-maintenance')  ]
