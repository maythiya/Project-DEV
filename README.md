# 📚 Library Management System  

ระบบจัดการห้องสมุดออนไลน์ พัฒนาด้วย **Django + TailwindCSS + HTMX**  
รองรับการยืม-คืนหนังสือ, จัดการสมาชิก, และดูสถิติการใช้งาน  

---

## 🚀 Features
- ✅ สมัครสมาชิก / Login / Logout  
- ✅ ค้นหาและยืม-คืนหนังสือ  
- ✅ ระบบจัดการหนังสือสำหรับผู้ดูแล (Admin)  
- ✅ Dashboard แสดงสถิติการใช้งาน  
- ✅ UI/UX ใช้ง่าย รองรับมือถือ  

---

## 🏗️ System Architecture
```mermaid
flowchart TD
    A[Frontend (Tailwind + HTMX)] -->|Request| B[Django Views & Controllers]
    B --> C[Database (SQLite/MySQL)]
    C -->|Data| B
    B -->|Response (HTML/JSON)| A
Frontend → TailwindCSS + HTMX ใช้ทำ UI/UX และ Dynamic Interaction

Backend → Django ทำหน้าที่จัดการ Business Logic และ API

Database → เก็บข้อมูลหนังสือ, ผู้ใช้, การยืมคืน

🔄 Workflow
mermaid
Copy code
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant S as Django Server
    participant DB as Database

    U->>F: Search Book
    F->>S: GET /search
    S->>DB: Query หนังสือ
    DB-->>S: ส่งผลลัพธ์
    S-->>F: แสดงผลลัพธ์
    U->>F: Click "Borrow"
    F->>S: POST /borrow
    S->>DB: บันทึกการยืม
    DB-->>S: OK
    S-->>F: ยืนยันการยืมสำเร็จ
⚙️ Tech Stack
Backend: Django (Python)

Frontend: TailwindCSS, HTMX

Database: SQLite (Dev) / MySQL (Production)

Deployment: Docker / Heroku

📂 Project Structure
Copy code
project-root/
│── core/              # Django App หลัก
│── templates/         # HTML Templates
│── static/            # Static files (CSS, JS, Images)
│── theme/             # Tailwind + PostCSS
│── db.sqlite3         # Database (dev)
│── manage.py          # Django CLI
│── requirements.txt   # Dependencies
│── README.md          # Documentation

🛠️ Installation
Copy code
# Clone repo
git clone https://github.com/username/library-system.git
cd library-system

# สร้าง Virtual Env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ติดตั้ง dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
📊 Example Screenshots
(เพิ่มภาพ Screenshot ของหน้า Login, Dashboard, Borrow Book ฯลฯ เพื่อให้ README ดูสวยขึ้น)

👨‍💻 Contributors
พัชรพล ยินดีรัมย์
เมย์ธิญา แกมนิล

