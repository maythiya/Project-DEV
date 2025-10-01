from django import forms
from .models import Book


BASE_INPUT = "w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"

class BookForm(forms.ModelForm):
    # ฟิลด์พิเศษ (ไม่ใช่ของโมเดล) สำหรับวาง URL รูปปก
    cover_image_url = forms.URLField(
        required=False,
        label="ปกหนังสือ (URL)",
        widget=forms.URLInput(attrs={"class": BASE_INPUT, "placeholder": "https://...รูปภาพ.jpg"})
    )

    class Meta:
        model = Book
        fields = ["title", "author", "category", "description",
                  "cover_image",     # อัปโหลดจากไฟล์ปกปกติ (ถ้าต้องการ)
                  "total_copies", "available_copies"]
        widgets = {
            "title": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "ชื่อหนังสือ"}),
            "author": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "ผู้แต่ง"}),
            "category": forms.Select(attrs={"class": BASE_INPUT}),
            "description": forms.Textarea(attrs={"class": BASE_INPUT + " h-28", "placeholder": "คำอธิบาย"}),
            "cover_image": forms.ClearableFileInput(attrs={"class": BASE_INPUT}),
            "total_copies": forms.NumberInput(attrs={"class": BASE_INPUT, "min": 0}),
            "available_copies": forms.NumberInput(attrs={"class": BASE_INPUT, "min": 0}),
        }