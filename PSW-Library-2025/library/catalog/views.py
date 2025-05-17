from django.shortcuts import render

# Create your views here.
from .models import Book, Author

def index(request):
    n_books   = Book.objects.all().count()
    n_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    num_visits = num_visits + 1
    request.session['num_visits'] = num_visits
    request.session.modified = True
    ctx = {
             'num_books'    : n_books,
             'num_authors'  : n_authors,
             'num_visits'   : num_visits,
          }
    return render(request, 'index.html',context=ctx)


from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(LoginRequiredMixin,generic.ListView):
    login_url = '/accounts/login/'
    model = Book
    paginate_by = 3
    
class AuthorListView(LoginRequiredMixin,generic.ListView):
    login_url = '/accounts/login/'
    model = Author
    paginate_by = 3
   
class BookDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/accounts/login/'
    model = Book

class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/accounts/login/'
    model = Author

from django.http import HttpResponseRedirect
from django.urls import reverse

def resetlogin(request, next):
    request.session['num_visits'] = 0
    request.session.modified = True
    return HttpResponseRedirect(reverse('login') + "?next=" + next)
    
from .models import BookInstance
from django.contrib.auth.mixins import PermissionRequiredMixin

class AllLoanedBooksListView (LoginRequiredMixin,
                              PermissionRequiredMixin,
                              generic.ListView):
    login_url = '/accounts/login/'
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_loaned.html'
    paginate_by = 3

    def get_queryset(self):
        all_l = BookInstance.objects.filter(status__exact='o')
        return all_l.order_by('due_back')


import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception = True)
def renew_book_librarian(request, pk):
    # Retrieve the book instance (or raise an error)
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is the first request (i.e. not a POST) then:
    # create the default form and render it
    if request.method != 'POST':
       p = datetime.date.today() + datetime.timedelta(weeks=3)
       form = RenewBookForm(initial={'renewal_date': p })
       ctx = { 'form': form, 'book_instance': book_instance }
       return render(request, 'catalog/book_renew_librarian.html', ctx)

    # ...otherwise...

    # ...this is a POST request,so:
    # - create a form instance and bind it with the POST data
    # - validate the form
    # - if the form is valid, process the data in cleaned_data
    #   and redirect to the page "exiting the form entry"
    # - if the form is not valid, re-render the page with errors

    form = RenewBookForm(request.POST)

    if form.is_valid():
       book_instance.due_back = form.cleaned_data['renewal_date']
       book_instance.save()
       return HttpResponseRedirect(reverse('all-loaned-books'))
    else:
       ctx = { 'form': form, 'book_instance': book_instance }
       return render(request, 'catalog/book_renew_librarian.html', ctx)


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .forms import SignupForm

def user_signup(request, next):
  if request.method != 'POST':
     form = SignupForm()
     return render(request, 'catalog/signup.html', {'form': form})
  else:
    form = SignupForm(request.POST)
    if form.is_valid():
       form.save()
       auth_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
       login(request, auth_user)
       gruppo_utenti = Group.objects.get(name='Utenti')
       auth_user.groups.add(gruppo_utenti)
       return HttpResponseRedirect(next)
    else:
       return render(request, 'catalog/signup.html', {'form': form})


from catalog.forms import SearchBookTitleForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception = True)
def search_book_librarian(request):
    # If this is the first request then:
    # create and render the default form.
    if request.method != 'POST':
       form = SearchBookTitleForm(initial={'title': ''})
       ctx = { 'form': form }
       return render(request, 'catalog/search_book_librarian.html', ctx)

    # otherwise...
    
    form = SearchBookTitleForm(request.POST)
    if form.is_valid(): # Form is valid: search, and render
       s = form.cleaned_data['title']
       #### Raw SQL formulation of query
       ###search_SQL = s + '%'
       ###found_books = Book.objects.raw( \
       ####       'SELECT * FROM catalog_book WHERE title LIKE %s', [search_SQL])

       ##### Equivalent filter-based formulation
       #####found_books = Book.objects.filter(title__startswith = s)    
       
       search_SQL = s.replace("*","%")
       found_books = Book.objects.raw( \
          'SELECT * FROM catalog_book WHERE title LIKE %s',
           [search_SQL])
       ctx = { 'search_title': s, 'found_books' : found_books }
       return render(request, 'catalog/searched_book_librarian.html', ctx)
    else:
       # Form is not valid: re-render it
       ctx = { 'form': form }
       return render(request, 'catalog/search_book_librarian.html', ctx)


from django.http import JsonResponse

def set_book_on_maintenance (request,pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.status = 'd'
    book_instance.save()
    return JsonResponse({'outcome' : 'OK',
                         'new_status': 'Maintenance',
                         'new_style' : 'text-warning',
                         'new_button': ''})


