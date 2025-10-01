from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('loan/<int:pk>/return/', views.return_book, name='return_book'),
    path('me/loans/', views.my_loans, name='my_loans'),
    path("account/delete/", views.account_delete, name="delete_account"),


    # CRUD (staff only)
    path('manage/books/', views.book_manage_list, name='book_manage_list'),
    path('manage/books/create/', views.book_create, name='book_create'),
    path('manage/books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('manage/books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('dashboard/', views.dashboard, name='dashboard'), # Extra charts
    path('register/', views.register, name='register'),
] 