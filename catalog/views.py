from django.shortcuts import render
# Create your views here.

# 10-13-2018 from Mozilla Tutorial
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

# 10-27-2018
from django.contrib.auth.mixins import LoginRequiredMixin

# 11-8-2018: Section 9
import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm

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

# 11-8-2018: Section 9 Forms
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
