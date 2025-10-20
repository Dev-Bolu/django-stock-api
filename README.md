# 🍺 Django Inventory Management API

A RESTful API for managing store items, bar stock, and sales tracking using **Django REST Framework (DRF)**.  
Includes authentication, role-based permissions, and daily/weekly/monthly sales reports.

---

## 🚀 Features

✅ CRUD for Store Items, Bar Stock, and Item Values  
✅ Daily stock and sales history auto-tracked via signals  
✅ Role-based access (Manager, Staff, Accountant)  
✅ Token-based authentication for API access  
✅ Sales reports (daily, weekly, monthly)  
✅ Works with both browser session login and REST clients (curl/Postman)

---

## 🧩 Project Structure

django-stock-api/
├── inventory/
│ ├── models.py
│ ├── views.py
│ ├── views_auth.py
│ ├── views_reports.py
│ ├── signals.py
│ ├── serializers.py
│ ├── permissions.py
│ ├── urls.py
│ └── admin.py
├── stock_api_project/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
└── manage.py
---

## ⚙️ Setup Instructions

### 1️⃣ Create and activate a virtual environment

python -m venv venv
source venv/bin/activate        # on Linux/Mac
venv\Scripts\activate           # on Windows

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

4️⃣ Create superuser
python manage.py createsuperuser

5️⃣ Run development server
python manage.py runserver
Server runs at:
👉 http://127.0.0.1:8000/

🔐 Authentication
1️⃣ Register a user
curl -X POST http://127.0.0.1:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"managerbola","password":"   bola2025"}'


2️⃣ Login and get token
curl -X POST http://127.0.0.1:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"managerbola","password":"bola2025"}'


Example response:

{"token": "b97fabe78b0279c4a84cde3573f5def3e82bf870"}

Use that token for subsequent requests.

📦 API Endpoints

🧱 Store Items
Method	Endpoint	Description
1. curl -X GET http://127.0.0.1:8000/api/store-items/     List all items
2. curl -X POST http://127.0.0.1:8000/api/store-items/	Create new item
3. curl -X GET http://127.0.0.1:8000/api/store-items/{id}/	Retrieve item
4. curl -X PUT http://127.0.0.1:8000	/api/store-items/{id}/	Update item
5. curl -X DELETE http://127.0.0.1:8000/api/store-items/{id}/	Delete item

🍾 Bar Stock
Method	Endpoint	Description
1. curl -X GET http://127.0.0.1:8000/api/bar-stock/	List bar stock
2. curl -X POST http://127.0.0.1:8000/api/bar-stock/	Add bar stock record

💰 Item Value
Method	Endpoint Description
1. curl -X GET http://127.0.0.1:8000/api/item-value/	View sales summary per item

🧪 Testing with curl
✅ Create a Store Item

curl -X POST http://127.0.0.1:8000/api/store-items/ \
     -H "Authorization: Token 751069c378c06d0cfd39ec41d0345ab60c649bc3" \
     -H "Content-Type: application/json" \
     -d '{"item": "ball", "store_in": 50, "store_out": 10, "cost_price": 1000, "selling_price": 1500}'

✅ Get all items

curl -X GET http://127.0.0.1:8000/api/store-items/ \
     -H "Authorization: Token 751069c378c06d0cfd39ec41d0345ab60c649bc3"
     
✅ Get daily sales summary

curl -X GET http://127.0.0.1:8000/api/reports/daily/ \
     -H "Authorization: Token 751069c378c06d0cfd39ec41d0345ab60c649bc3"

✅ Get weekly sales summary

curl -X GET http://127.0.0.1:8000/api/reports/weekly/ \
     -H "Authorization: Token b97fabe78b0279c4a84cde3573f5def3e82bf870"

✅ Get monthly sales summary

curl -X GET http://127.0.0.1:8000/api/reports/monthly/ \
     -H "Authorization: Token b97fabe78b0279c4a84cde3573f5def3e82bf870"

👤 Setup Test Users (Optional but Recommended)

To make testing easier, you can create sample users in the Django shell.

1️⃣ Open the shell
python manage.py shell

2️⃣ Paste this code:
from django.contrib.auth.models import User, Group

# Create groups
manager_group, _ = Group.objects.get_or_create(name="BarManager")
staff_group, _ = Group.objects.get_or_create(name="Staff")
accountant_group, _ = Group.objects.get_or_create(name="Accountant")

# Create users
manager = User.objects.create_user(username="manager", password="manager123")
staff = User.objects.create_user(username="staff", password="staff123")
accountant = User.objects.create_user(username="accountant", password="accountant123")

# Assign groups
manager.groups.add(manager_group)
staff.groups.add(staff_group)
accountant.groups.add(accountant_group)

print("✅ Test users created successfully!")
exit()

👥 Roles & Permissions
Role	Permissions
BarManager	Full CRUD
Staff	Can view all items, can only update “sold” field
Accountant	Read-only access

Defined in: inventory/permissions.py

🧠 Tips

Staff cannot view cost or profit fields (secured via permissions)

Signals automatically sync:

StoreItem → StoreItemHistory

StoreItem → BarStock

BarStock → ItemValue

Sales data aggregates automatically each day

🧾 Example Git Commit Message
git add .
git commit -m "Add role-based permissions, reporting views, and curl API tests"
git push origin main








