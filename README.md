# Siegecode HRM

Siegecode HRM is a full-stack Human Resource Management and payroll system. It includes employees, attendance, shifts, leave, payroll, reports, performance reviews, events, and account management.

## Start the project

If you have already completed the first-time setup, open two PowerShell terminals in the project folder.

**Terminal 1 — backend**

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
flask --app wsgi.py run --debug
```

**Terminal 2 — frontend**

```powershell
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

| Service | Address |
| --- | --- |
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:5000 |
| Backend health check | http://127.0.0.1:5000/health |

Keep both terminals running while you use the application.

## First-time setup

### 1. Install the required software

You need:

- Python 3.10 or newer
- Node.js 18 or newer (includes npm)
- MySQL 8, either installed locally or hosted by Aiven
- A Cloudinary account only if you need employee photo uploads

### 2. Set up the backend

From the project folder, run:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

On macOS or Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

### 3. Configure MySQL

Choose either local MySQL or Aiven.

#### Option A: Local MySQL

Log in to MySQL as an administrator and run:

```sql
CREATE DATABASE hrm_backend
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'hrm_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON hrm_backend.* TO 'hrm_user'@'localhost';
FLUSH PRIVILEGES;
```

Then open `backend/.env` and set:

```dotenv
DATABASE_URL=mysql+pymysql://hrm_user:strong_password@localhost:3306/hrm_backend?charset=utf8mb4
MYSQL_SSL_CA=
```

#### Option B: Aiven MySQL

Copy your connection values from the Aiven service overview into `backend/.env`:

```dotenv
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE?charset=utf8mb4
MYSQL_SSL_CA=certs/aiven-ca.pem
```

Download the Aiven CA certificate and save it as `backend/certs/aiven-ca.pem`.

If the database password contains characters such as `@`, `:`, `/`, `?`, or `#`, URL-encode the password before adding it to `DATABASE_URL`.

### 4. Configure backend settings

Still in `backend/.env`, replace the example secrets and login details:

```dotenv
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=replace-with-a-long-random-secret
JWT_SECRET_KEY=replace-with-a-long-random-jwt-secret

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

ADMIN_NAME=Super Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=replace-with-a-secure-admin-password

EMPLOYEE_NAME=Sok Dara
EMPLOYEE_EMAIL=employee@example.com
EMPLOYEE_PASSWORD=replace-with-a-secure-employee-password
```

Cloudinary is optional unless you use employee photo uploads:

```dotenv
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

Do not commit `.env`, passwords, secret keys, Cloudinary credentials, or production certificates.

### 5. Create the database tables and sample users

Run these commands from `backend` while the virtual environment is active:

```powershell
flask --app wsgi.py db upgrade
python scripts\seed.py
```

The seed creates the admin and employee accounts defined in `backend/.env`, along with the required roles, leave types, and salary components.

To add the full Cambodia demo dataset, run:

```powershell
python scripts\seed_demo.py
```

The demo seed can safely be run again without duplicating its records. It adds employees, departments, shifts, attendance, leave, payroll, performance reviews, holidays, events, and report data.

Do not run `flask db init`. The migrations folder is already included in this repository.

### 6. Set up the frontend

Return to the project folder and run:

```powershell
cd ..\frontend
npm install
Copy-Item .env.example .env
npm run dev
```

The frontend environment should contain:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:5000
```

Finally, start the backend in a second terminal using the commands in [Start the project](#start-the-project).

## Useful commands

Run backend tests:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

Build the frontend:

```powershell
cd frontend
npm run build
```

After changing SQLAlchemy models, create and apply a migration:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
flask --app wsgi.py db migrate -m "describe the schema change"
flask --app wsgi.py db upgrade
```

Review generated migrations before applying them, and back up production data first.

## Troubleshooting

### PowerShell blocks virtual environment activation

Allow local scripts for your user, then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### `getaddrinfo failed`

The database host cannot be found. Check that the Aiven service is running and copy its current hostname into `DATABASE_URL`.

### `CERTIFICATE_VERIFY_FAILED`

Download the current CA certificate for your Aiven service and replace `backend/certs/aiven-ca.pem`.

### `Access denied for user`

Check the MySQL username and password in `DATABASE_URL`. URL-encode special characters in the password.

### Browser shows a CORS error

Add the exact frontend address to `CORS_ORIGINS` in `backend/.env`, then restart Flask.

### Frontend cannot reach the backend

Check http://127.0.0.1:5000/health. If it works, confirm that `frontend/.env` uses the same backend address, then restart Vite.

## Technology

- Frontend: React 18, TypeScript, Vite, and Tailwind CSS
- Backend: Flask, SQLAlchemy, Flask-Migrate, and JWT
- Database: MySQL 8
- Media storage: Cloudinary

## Project structure

```text
Human-Resource-Payroll/
|-- backend/          Flask API, migrations, models, and seed scripts
|-- frontend/         React and Vite application
`-- README.md         Project setup and startup guide
```

## Production notes

- Do not use Flask's development server in production.
- Run Flask through a production WSGI server and reverse proxy.
- Build the frontend with `npm run build` and deploy `frontend/dist`.
- Set the production URLs in `VITE_API_BASE_URL` and `CORS_ORIGINS`.
- Use strong, unique secrets and keep database TLS verification enabled.
- Back up MySQL before migrations or large seed operations.
- Never run the demo seed against a real production database.

## Live demo

[Explore the HRM system](https://hrm-five-nu.vercel.app/)
