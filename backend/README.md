# HRM Backend

Production-style Flask backend for the Human Resource Payroll system using MySQL, Flask-SQLAlchemy, Flask-Migrate, Alembic, and PyMySQL.

## Create Virtual Environment

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Create MySQL Database

Log in to MySQL as an admin user:

```bash
mysql -u root -p
```

Then run:

```sql
CREATE DATABASE hrm_backend
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'hrm_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON hrm_backend.* TO 'hrm_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Configure Environment

```bash
copy .env.example .env
```

Update `.env` if your MySQL username, password, host, or database name is different.

## Run Migrations

This project already includes an initial migration file at:

```text
migrations/versions/0001_initial_hrm_schema.py
```

If you want to initialize a new migrations folder from scratch, run:

```bash
flask --app wsgi.py db init
```

For the included migration system, run:

```bash
flask --app wsgi.py db upgrade
```

To generate a new migration after changing models:

```bash
flask --app wsgi.py db migrate -m "initial hrm schema"
flask --app wsgi.py db upgrade
```

## Seed Data

Make sure these values are set in `.env`:

```text
ADMIN_NAME=Super Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminPassword123!
EMPLOYEE_NAME=Sok Dara
EMPLOYEE_EMAIL=employee@example.com
EMPLOYEE_PASSWORD=EmployeePassword123!
```

Then run:

```bash
python scripts/seed.py
```

Create a populated Cambodia demo environment covering January 1 through July 10, 2026:

```bash
python scripts/seed_demo.py
```

The demo seed is deterministic and idempotent. It creates Cambodian employees, departments,
positions, shifts, weekday attendance, leave requests, payroll history, adjustments,
performance reviews, public holidays, and company events without duplicating records.

The seed script creates:

- Roles: Super Admin, HR Manager, Department Manager, Employee
- Admin user from environment variables
- Employee user and linked demo employee from environment variables
- Leave types: Annual Leave, Sick Leave, Unpaid Leave
- Salary components: Transport Allowance, Meal Allowance, Tax Deduction, Late Deduction

## Verify Tables In MySQL

```bash
mysql -u hrm_user -p hrm_backend
```

```sql
SHOW TABLES;
DESCRIBE employees;
DESCRIBE payrolls;
```

## Run API

```bash
flask --app wsgi.py run --debug
```

The API starts at:

```text
http://localhost:5000
```

Health check:

```text
GET /health
```

API v1 routes are mounted under:

```text
/api/v1
```
