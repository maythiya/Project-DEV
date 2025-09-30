from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Book, Category

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]

        if password != confirm:
            messages.error(request, "Password ไม่ตรงกัน")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username ถูกใช้แล้ว")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ")
        return redirect("login")

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # ไปหน้า Dashboard หรือ Home
        else:
            messages.error(request, "Username หรือ Password ไม่ถูกต้อง")
            return redirect("login")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

def book_list(request):
    books = Book.objects.all()

    top_books = Book.objects.order_by('-rating')[:5]  # 5 อันดับยอดนิยม
    new_books = Book.objects.order_by('-created_at')[:5]  # 5 หนังสือใหม่
    categories = Category.objects.all()  # หมวดหมู่ทั้งหมด

    context = {
        'top_books': top_books,
        'new_books': new_books,
        'categories': categories,
    }

    return render(request, "book_list.html", {"books": books})
