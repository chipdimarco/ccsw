from django.contrib import admin

# Register your models here.
# 10-9-2018: Chip
# Added from the Mozilla tutorial
from catalog.models import Author, Genre, Book, BookInstance

# 10-10-2018 edits
# admin.site.register(Author)
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

# register it
# 12/1/2018: 
# admin.site.register(Author, AuthorAdmin)
# AuthorAdmin class
# 12-1-2018: Add decorator
# "use the @register decorator to register the models (this does exactly the same thing 
# as the admin.site.register() syntax)
@admin.register(Author)
class AuthorAdmin (admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


# admin.site.register(Book)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # 10-27-2018 for borrowers
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Genre)
