from django.shortcuts import render
# Create your views here.

# 10-13-2018 from Mozilla Tutorial
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

# 10-27-2018
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# 10-15-2018 from Mozilla Tutorial (Section 6)
class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    '''
    # this option would use a different template
    context_object_name = 'my_book_list'   # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    '''

# 10-17-2018 from Mozilla Tutorial (Section 6)
class BookDetailView(generic.DetailView):
    model = Book

# 10-21-2018 from Mozilla Tutorial (Section 6)
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

# 10-21-2018 from Mozilla Tutorial (Section 6)
class AuthorDetailView(generic.DetailView):
    model = Author

# 10-27-2018 from Mozilla Tutorial (Section 8)
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# 11-4-2018 Section 8 Challenge
class LoanedBooksLibrarianListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')