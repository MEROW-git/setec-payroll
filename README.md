# Siegecode HRM

Siegecode HRM is a full-stack Human Resource Management and payroll system for employees, attendance, shifts, leave, payroll, reports, performance, events, and account management.

## Technology

- Frontend: React 18, TypeScript, Vite, Tailwind CSS
- Backend: Flask, SQLAlchemy, Flask-Migrate, JWT
- Database: MySQL 8
- Media storage: Cloudinary

## Project Structure

```text
Human-Resource-Payroll/
|-- backend/          Flask API, migrations, models, and seed scripts
|-- frontend/         React and Vite application
`-- README.md
```

## Prerequisites

Install these tools before starting:

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- MySQL 8 locally, or an Aiven MySQL service
- Cloudinary account if employee photo uploads are required

## 1. Backend Setup

Open PowerShell from the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## 2. Backend Environment

Create the private backend environment file:

```powershell
Copy-Item .env.example .env
```

Update `backend/.env`:

```dotenv
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=replace-with-a-long-random-secret
JWT_SECRET_KEY=replace-with-a-long-random-jwt-secret

DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE?charset=utf8mb4
MYSQL_SSL_CA=certs/aiven-ca.pem

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

ADMIN_NAME=Super Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=replace-with-a-secure-admin-password

EMPLOYEE_NAME=Sok Dara
EMPLOYEE_EMAIL=employee@example.com
EMPLOYEE_PASSWORD=replace-with-a-secure-employee-password

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

Do not commit `.env`, database passwords, JWT secrets, Cloudinary secrets, or production certificates.

### Aiven MySQL

Copy the connection values from the Aiven service overview into `DATABASE_URL`. Download the Aiven **CA certificate** and save it as:

```text
backend/certs/aiven-ca.pem
```

Keep `MYSQL_SSL_CA=certs/aiven-ca.pem` enabled so the application verifies the database TLS certificate.

If the password contains reserved URL characters such as `@`, `:`, `/`, `?`, or `#`, URL-encode the password before placing it in `DATABASE_URL`.

### Local MySQL

Create a local database if Aiven is not being used:

```sql
CREATE DATABASE hrm_backend
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'hrm_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON hrm_backend.* TO 'hrm_user'@'localhost';
FLUSH PRIVILEGES;
```

Then use:

```dotenv
DATABASE_URL=mysql+pymysql://hrm_user:strong_password@localhost:3306/hrm_backend?charset=utf8mb4
MYSQL_SSL_CA=
```

## 3. Database Migrations

Run migrations from the `backend` directory with the virtual environment active:

```powershell
flask --app wsgi.py db upgrade
```

This creates or updates all required tables. Do not run `flask db init`; the repository already contains the Alembic migration environment.

After intentionally changing SQLAlchemy models, generate and review a migration:

```powershell
flask --app wsgi.py db migrate -m "describe the schema change"
flask --app wsgi.py db upgrade
```

Never apply a destructive production migration without reviewing the generated migration file and taking a database backup.

Useful migration commands:

```powershell
flask --app wsgi.py db current
flask --app wsgi.py db history
```

## 4. Seed Data

Run the base seed first. It creates roles, login accounts, leave types, and salary components using values from `backend/.env`:

```powershell
python scripts\seed.py
```

Then create the full Cambodia demo dataset:

```powershell
python scripts\seed_demo.py
```

The demo seed is deterministic and idempotent, so it can be run again without duplicating its records. It creates:

- Cambodian employees and organizational departments
- Positions and shift assignments
- Attendance from January 1 through July 10, 2026
- Leave requests and holidays
- Payroll periods and payroll records through July 2026
- Allowances and deductions
- Performance reviews
- Events and schedules
- Data used by dashboard charts and all standard reports

To refresh only demo attendance records:

```powershell
python scripts\seed_demo.py --attendance-only
```

The seeded login emails and passwords are the `ADMIN_*` and `EMPLOYEE_*` values configured in `backend/.env`.

## 5. Start the Backend

From `backend`, with `.venv` active:

```powershell
flask --app wsgi.py run --debug
```

The API runs at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/health
```

API routes are mounted under `/api/v1`.

## 6. Frontend Setup

Open a second terminal from the project root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

The frontend environment should contain:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:5000
```

Vite normally starts at:

```text
http://localhost:5173
```

Keep both the Flask and Vite terminals running while developing.

## Quick Start

After the first installation, normal development startup only requires two terminals.

Terminal 1:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
flask --app wsgi.py run --debug
```

Terminal 2:

```powershell
cd frontend
npm run dev
```

## Build and Test

Build the frontend for production:

```powershell
cd frontend
npm run build
```

Run backend tests:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

Compile-check backend modules:

```powershell
python -m compileall app
```

## Production Notes

- Do not use the Flask development server in production.
- Serve Flask through a production WSGI server and reverse proxy.
- Build the frontend with `npm run build` and deploy `frontend/dist`.
- Set production frontend and backend URLs in `VITE_API_BASE_URL` and `CORS_ORIGINS`.
- Use strong, unique secrets and rotate any credential that has been exposed.
- Keep database TLS verification enabled.
- Back up MySQL before migrations and large seed operations.
- Do not run demo seed scripts against a real production database.

## Troubleshooting

### `getaddrinfo failed`

The database hostname cannot be resolved. Confirm the Aiven service is running and copy its latest host name into `DATABASE_URL`.

### `CERTIFICATE_VERIFY_FAILED`

The CA certificate does not belong to the configured Aiven service. Download the current CA certificate and replace `backend/certs/aiven-ca.pem`.

### `Access denied for user`

The MySQL username or password is incorrect. Copy the service URI directly instead of reading ambiguous characters from a screenshot.

### Browser CORS error

Ensure the exact frontend URL is included in `CORS_ORIGINS`, then restart Flask.

### Frontend cannot reach the API

Confirm Flask is running on port `5000` and `frontend/.env` points to the same URL. Restart Vite after changing its environment file.

## Live Demo

[Explore the HRM system](https://hrm-five-nu.vercel.app/)
