import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Book, Category, Loan


@pytest.mark.django_db
def test_borrow_and_return_flow(client):
    u = User.objects.create_user('alice', password='pass1234')
    cat = Category.objects.create(name='Test')
    b = Book.objects.create(title='T', author='A', category=cat, total_copies=1, available_copies=1)


    client.login(username='alice', password='pass1234')
    # ยืม
    resp = client.get(f'/book/{b.id}/borrow/')
    b.refresh_from_db()
    assert b.available_copies == 0
    loan = Loan.objects.get(user=u, book=b, returned_at__isnull=True)


    # คืน
    resp = client.get(f'/loan/{loan.id}/return/')
    b.refresh_from_db(); loan.refresh_from_db()
    assert b.available_copies == 1
    assert loan.returned_at is not None
