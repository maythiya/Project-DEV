from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


    def can_borrow(self):
        return self.available_copies > 0


class Loan(models.Model):
    BORROW_DAYS_DEFAULT = 7

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)


def save(self, *args, **kwargs):
    if not self.due_at:
        self.due_at = (self.borrowed_at or timezone.now()) + timezone.timedelta(days=self.BORROW_DAYS_DEFAULT)
    super().save(*args, **kwargs)


    @property
    def is_overdue(self):
        return not self.returned_at and timezone.now() > self.due_at