Finance Dashboard Backend

A robust Django REST Framework backend for a Finance Dashboard with Role-Based Access Control (RBAC)

This backend is built as part of the **Backend Developer Intern Assignment** for a finance dashboard system. It supports user management, financial records CRUD, dashboard analytics, and strict role-based permissions.

Features

- Role-Based Access Control (RBAC): Three roles — `Viewer`, `Analyst`, and `Admin`
- Financial Records Management: Full CRUD operations with filtering, pagination, and soft delete
- Dashboard Analytics: Rich summary with visualization-ready data
  - Total Income / Expenses / Net Balance
  - Category-wise breakdown (Pie Chart ready)
  - Monthly trend (Line/Bar Chart ready)
  - Type distribution (Income vs Expense)
  - Recent activity
- JWT Authentication with custom claims (role included in token)
- Clean Architecture: Services layer, reusable permissions, filters, and consistent API responses
- Data Isolation: Every user can only access their own financial records
- API Documentation: Built-in Swagger UI

---
Tech Stack

- Framework: Django 5.1 + Django REST Framework
- Authentication: SimpleJWT
- Database: SQLite (easily switchable to PostgreSQL)
- Filtering: django-filter
- API Documentation: drf-spectacular (Swagger)
- Python: 3.11+

---

Roles & Permissions

| Role      | View Records | Create / Update / Delete Records | View Dashboard | Access Admin |
|-----------|--------------|----------------------------------|----------------|--------------|
|  Viewer   | Yes          | No                               | Yes            | No           |
|  Analyst  | Yes          | Yes                              | Yes            | No           |
|  Admin    | Yes          | Yes                              | Yes            | Yes          |

---

API Structure & Endpoints

All API endpoints are prefixed with `/api/`.

1. Authentication

| Method | Endpoint                  | Description                  | Access       |
|--------|---------------------------|------------------------------|--------------|
| POST   | `/api/users/register/`    | Register new user            | Public       |
| POST   | `/api/users/login/`       | Login and get JWT tokens     | Public       |

2. Financial Records

| Method | Endpoint                     | Description                              | Access                  |
|--------|------------------------------|------------------------------------------|-------------------------|
| GET    | `/api/records/`              | List all own records (with filters)      | All authenticated users |
| POST   | `/api/records/`              | Create new financial record              | Analyst + Admin         |
| GET    | `/api/records/{id}/`         | Get single record                        | Owner only              |
| PUT    | `/api/records/{id}/`         | Update record                            | Analyst + Admin         |
| PATCH  | `/api/records/{id}/`         | Partial update                           | Analyst + Admin         |
| DELETE | `/api/records/{id}/`         | Soft delete record                       | Analyst + Admin         |
| GET    | `/api/records/stats/`        | Basic stats (income, expenses)           | All authenticated users |

Supported Query Filters:
- `record_type=income` / `expense`
- `category=salary`
- `start_date=2026-04-01`
- `end_date=2026-04-30`
- `min_amount=1000`
- `max_amount=50000`

 3. Dashboard Analytics (Visualization Ready)

| Method | Endpoint                        | Description                                      | Access                  |
|--------|---------------------------------|--------------------------------------------------|-------------------------|
| GET    | `/api/dashboard/summary/`       | Full dashboard summary with viz-ready data       | All authenticated users |

Response includes:
- `total_income`, `total_expenses`, `net_balance`
- `category_breakdown` → Perfect for **Pie Chart**
- `monthly_trend` → Perfect for **Line / Bar Chart**
- `type_distribution` → Perfect for **Donut Chart**
- `recent_activity`
- `currency`, `last_updated`


Installation & Setup

Prerequisites
- Python 3.11 or higher
- Git

Step-by-Step Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Shubham12sharma/Finance-Data-Processing-and-Access-Control-.git
   cd finance-backend

2.Create virtual environment:

python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4.Make .env

  DEBUG=True
  SECRET_KEY="Your-sec-key"
  ALLOWED_HOSTS=localhost,127.0.0.1
  
  DATABASE_URL=sqlite:///db.sqlite3

5.Run database migrationsBash
  python manage.py makemigrations
  python manage.py migrate

6.Start the development serverBash
  python manage.py runserver

7.Open API Documentation
Go to: http://127.0.0.1:8000/api/docs/
  

