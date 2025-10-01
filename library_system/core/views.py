from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .models import Book, Category, Loan
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from .forms import BookForm
import json
import os, mimetypes
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth import logout

# Public

def _download_cover_to_contentfile(url: str):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    ctype = (r.headers.get("Content-Type") or "").split(";")[0]
    # หานามสกุลไฟล์จาก content-type หรือจาก path
    ext = mimetypes.guess_extension(ctype) or os.path.splitext(urlparse(url).path)[1] or ".jpg"
    filename = f"cover{ext}"
    return filename, ContentFile(r.content)

def book_list(request):
    top_books = Book.objects.order_by('-created_at')[:5]
    new_books = Book.objects.order_by('-created_at')[:10]
    categories = Category.objects.all()
    return render(request, 'book_list.html', {
        'top_books': top_books,
        'new_books': new_books,
        'categories': categories,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

@login_required
@transaction.atomic
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.available_copies <= 0:
        messages.error(request, 'หนังสือเล่มนี้ถูกยืมหมดแล้ว')
        return redirect('book_detail', pk=pk)

    # ไม่ให้ยืมซ้ำถ้ายังไม่คืน
    if Loan.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists():
        messages.warning(request, 'คุณยืมเล่มนี้อยู่แล้ว')
        return redirect('book_detail', pk=pk)

    # คำนวณกำหนดคืน (เช่น 7 วัน)
    due_at = timezone.now() + timezone.timedelta(days=Loan.BORROW_DAYS_DEFAULT)

    # สร้าง Loan พร้อม due_at
    loan = Loan.objects.create(
        user=request.user,
        book=book,
        borrowed_at=timezone.now(),
        due_at=due_at,
    )

    # อัปเดตสต๊อก
    book.available_copies -= 1
    book.save(update_fields=['available_copies'])

    messages.success(request, f'ยืม “{book.title}” สำเร็จ กำหนดคืน {loan.due_at:%d/%m/%Y}')
    return redirect('my_loans')

@login_required
@transaction.atomic
def return_book(request, pk):
    loan = get_object_or_404(Loan, pk=pk, user=request.user)
    if loan.returned_at:
        messages.info(request, 'เล่มนี้ถูกคืนแล้ว')
        return redirect('my_loans')
    loan.returned_at = timezone.now()
    loan.save()
    loan.book.available_copies += 1
    loan.book.save()
    messages.success(request, 'คืนหนังสือสำเร็จ')
    return redirect('my_loans')

@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user).select_related('book').order_by('-borrowed_at')
    return render(request, 'my_loans.html', {'loans': loans})

# Staff only helpers


def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)


@staff_required
def book_manage_list(request):
    books = Book.objects.select_related('category').all()
    return render(request, 'manage/book_manage_list.html', {'books': books})


@staff_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)

            cover_url = form.cleaned_data.get("cover_image_url")
            if cover_url and not book.cover_image:
                try:
                    fname, cfile = _download_cover_to_contentfile(cover_url)
                    base = slugify(book.title) or "cover"
                    _, ext = os.path.splitext(fname)
                    book.cover_image.save(f"{base}{ext}", cfile, save=False)
                except Exception as e:
                    messages.warning(request, f"ดึงปกจาก URL ไม่สำเร็จ: {e}")

            book.save()
            messages.success(request, "เพิ่มหนังสือสำเร็จ")
            return redirect("book_manage_list")
    else:
        form = BookForm()
    return render(request, "manage/book_form.html", {"form": form})


@staff_required
def book_edit(request, pk):
    from .forms import BookForm
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขหนังสือสำเร็จ')
            return redirect('book_manage_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'manage/book_form.html', {'form': form})


@staff_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, 'ลบหนังสือสำเร็จ')
    return redirect('book_manage_list')


@staff_required
def dashboard(request):
    by_cat = list(
        Book.objects.values('category__name')
        .annotate(n=Count('id')).order_by('-n')
    )
    top_borrow = list(
        Loan.objects.values('book__title')
        .annotate(n=Count('id')).order_by('-n')[:10]
    )
    return render(request, 'dashboard.html', {
        'stats_json': json.dumps({'by_cat': by_cat, 'top_borrow': top_borrow}, ensure_ascii=False),
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ เข้าสู่ระบบได้เลย')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@transaction.atomic
def account_delete(request):
    user = request.user

    # กันพลาด: ไม่ให้ลบ superuser (ปรับตามนโยบายคุณได้)
    if user.is_superuser:
        messages.error(request, "บัญชีผู้ดูแลระบบไม่สามารถลบได้")
        return redirect("book_list")  # หรือหน้าอื่น

    open_loans_count = Loan.objects.filter(user=user, returned_at__isnull=True).count()

    if request.method == "POST":
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm", "").strip().upper()  # ให้พิมพ์ DELETE ยืนยัน

        # 1) เช็ครหัสผ่าน
        if not user.check_password(password):
            messages.error(request, "รหัสผ่านไม่ถูกต้อง")
            return render(request, "account/delete_account.html", {"open_loans_count": open_loans_count})

        # 2) กันลบถ้ามีหนังสือค้างยืม
        if open_loans_count > 0:
            messages.error(request, f"ยังมีรายการยืมค้างอยู่ {open_loans_count} รายการ กรุณาคืนก่อนลบบัญชี")
            return render(request, "account/delete_account.html", {"open_loans_count": open_loans_count})

        # 3) เริ่มลบ (ต้องพิมพ์ DELETE)
        if confirm != "DELETE":
            messages.error(request, "กรุณาพิมพ์คำว่า DELETE เพื่อยืนยันการลบ")
            return render(request, "account/delete_account.html", {"open_loans_count": open_loans_count})

        # 4) ออกจากระบบก่อน แล้วลบจริง
        # เก็บอ้างอิง user ไว้ก่อน logout
        u = user
        logout(request)           # เคลียร์ session
        u.delete()                # ลบถาวร (FK ที่ on_delete=CASCADE จะลบตาม)

        messages.success(request, "ลบบัญชีเรียบร้อย ขอบคุณที่ใช้งาน")
        return redirect("book_list")  # หรือหน้าแรก/หน้าล็อกอิน

    return render(request, "account/delete_account.html", {"open_loans_count": open_loans_count})