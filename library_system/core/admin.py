from django.contrib import admin
from .models import Category, Book, Loan, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'available_copies', 'total_copies')
    list_filter = ('category',)
    search_fields = ('title', 'author')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'borrowed_at', 'due_at', 'returned_at')
    list_filter = ('returned_at', 'book__category')
    search_fields = ('book__title', 'user__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'book')
    search_fields = ('book__title', 'user__username', 'comment')