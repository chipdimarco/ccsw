from django.contrib import admin

# Register your models here.
# 10-9-2018: Chip
# Added from the Mozilla tutorial
from catalog.models import Author, Genre, Book, BookInstance


# 10-10-2018 edits
# admin.site.register(Author)
# AuthorAdmin class
class AuthorAdmin (admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
# register it
admin.site.register(Author, AuthorAdmin)

# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

# admin.site.register(BookInstance)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre)
