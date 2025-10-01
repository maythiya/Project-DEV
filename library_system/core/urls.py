from django.urls import path
from .views import base, register, user_login, user_logout

urlpatterns = [
    path("", base, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    
    #path("books/", book_list, name="book_list"),
]