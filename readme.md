# ☕ Cafe Menu – Django Web Application

A full-featured Django-based web application for managing a coffee shop menu, designed for real-world usage in a café.  
The system allows staff to add, edit, and remove items such as coffee, toasts, and sweets, while also providing a user-friendly and mobile-responsive interface.

## 🚀 Features
- Manage coffee, toast, and sweets menu items.
- Staff dashboard with add/edit/delete options.
- Django admin panel for advanced management.
- Responsive design for mobile and tablets.
- Supports images, modifiers, and preparation methods.

## 🛠️ Tech Stack
- **Backend:** Django 5.2, Python 3.12
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Render
- **Version Control:** Git & GitHub

## ▶️ Run Locally
```bash
git clone https://github.com/iswwimm/untitled_cafe_menu.git
cd cafe_menu
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
