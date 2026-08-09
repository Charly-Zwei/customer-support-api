# Customer Support API

Flask REST API for customer management, document types, purchases, loyalty reports, and Excel exports.

## Technologies

- Python 3.14
- Flask
- SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pandas
- OpenPyXL
- Bootstrap
- JavaScript
- Docker
- Gunicorn

## Features

- Customer creation, search, listing, and update
- Document type management
- Customer purchase management
- Loyal customer report
- Individual customer Excel export
- Loyal customer report Excel export
- Request validation and response serialization with Marshmallow
- Database migrations with Flask-Migrate
- Seed data for local development and demonstration

## Project Organization

The application follows a layered structure:

- `app/models/` — database models
- `app/schemas/` — request validation and response serialization
- `app/services/` — business logic and Excel export logic
- `app/routes/` — HTTP endpoints
- `app/templates/` — frontend HTML
- `app/static/` — CSS and JavaScript
- `migrations/` — database migration history
- `seed.py` — sample data
- `run.py` — application entry point

## Requirements

The project can be run either with Docker or directly with Python.

### Docker

Install Docker Desktop.

### Without Docker

Install Python 3.14 and Git. The project uses SQLite, so no external database server is required.

Verify Python:

```bash
python --version
```

Expected:

```text
Python 3.14.x
```

## Environment Configuration

Both setup options require a `.env` file in the project root.

Use `.env-example` as a reference or rename it to `.env`:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
```

Replace `your-secret-key` with a secret value of your choice.

The `.env` file must not be committed to version control.

The SQLite database is stored locally at:

```text
instance/database.db
```

The database file is not included in the repository. Its structure is recreated through the existing Flask-Migrate migrations.
The database is stored in Flask’s instance directory to keep local data separate from the application code.

## Setup

### Option 1: Run with Docker

Clone the repository:

```bash
git clone <repository-url>
cd customer-support-api
```

Create the `.env` file as described in the Environment Configuration section.

Build and start the application:

```bash
docker compose up --build
```

The Docker setup builds the Python 3.14 image, installs the dependencies, loads the environment configuration, applies the existing migrations, and starts the Flask application using Gunicorn.

Open:

```text
http://localhost:5000
```

To stop the application:

```bash
docker compose down
```

The `instance/` directory is mounted into the container, so the SQLite database persists when the container is stopped or recreated.

#### Seed Data

Sample data is optional.

To populate an empty database, keep the application running and open a **second terminal** in the project directory:

```bash
docker compose exec app python seed.py
```

Do not stop the running container before executing the command.

Run the seed script only on an empty database. Running it again against an already populated database may create duplicate records or violate database constraints.

## Production Deployment Notes

This project uses Gunicorn as the WSGI server (see Docker Configuration above), 
which is production-ready by default — the Flask development server is never used.

For a production deployment:

- Generate a strong `SECRET_KEY` (do not reuse the development value):
  python -c "import secrets; print(secrets.token_hex(32))"
- Ensure `FLASK_DEBUG` (or equivalent) is disabled/unset.
- Run `flask --app run.py db upgrade` (or let Docker apply migrations automatically, 
  as described above) before starting the application.
- Place the container behind a reverse proxy (e.g. Nginx) if exposing it over HTTPS.
- Back up the `instance/database.db` file periodically, since SQLite has no 
  built-in replication or automated backups.

### Option 2: Run Without Docker

Clone the repository:

```bash
git clone <repository-url>
cd customer-support-api
```

Create the `.env` file as described in the Environment Configuration section.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Apply the existing database migrations:

```bash
flask --app run.py db upgrade
```

This creates the database tables defined by the migration history.

#### Seed Data

Sample data is optional.

To populate an empty database:

```bash
python seed.py
```

Run the seed script only on an empty database. Running it again against an already populated database may create duplicate records or violate database constraints.

Start the application:

```bash
flask --app run.py run
```

Open:

```text
http://127.0.0.1:5000
```

## Main Endpoints

### Customers

```text
POST   /customers
GET    /customers
GET    /customers/<document_type>/<document_number>
PUT    /customers/<customer_id>
GET    /customers/<customer_id>/purchases
GET    /customers/<customer_id>/export
```

Customer lookup uses document type and document number. A document number is unique within its document type, allowing the same number to exist under different document types.

### Document Types

```text
GET    /document-types/
```

### Purchases

```text
POST   /purchases
GET    /purchases/<purchase_id>
GET    /purchases
```

### Reports

```text
GET    /reports/loyal-customers
GET    /reports/loyal-customers/export
```

The loyalty report is based on the loyalty threshold and period configured in `ReportService`.

## Excel Exports

Excel generation is centralized in `ExportService` and uses Pandas and OpenPyXL.

### Individual Customer

```text
GET /customers/<customer_id>/export
```

Exports the selected customer's information to an Excel file.

### Loyal Customers

```text
GET /reports/loyal-customers/export
```

Exports the loyal customer report to an Excel file.

The files are generated in memory using `BytesIO`, so temporary Excel files do not need to be stored on the server.

## Frontend

The frontend is served by Flask and communicates with the API through JavaScript.

Main page:

```text
app/templates/index.html
```

Frontend assets:

```text
app/static/css/
app/static/js/
```

The interface allows users to search for customers, view customer information and purchases, consult the loyal customer report, and export individual or loyal-customer information.

## Database Migrations

After modifying a database model, create a new migration with:

```bash
flask --app run.py db migrate -m "describe the change"
```

Review the generated migration before applying it:

```bash
flask --app run.py db upgrade
```

Migration files are stored in:

```text
migrations/versions/
```

When using Docker, existing migrations are applied automatically when the application starts.

## Docker Configuration

The Docker setup consists of:

- `Dockerfile` — application image, database migration, and Gunicorn startup process
- `docker-compose.yml` — container, environment variables, port, and SQLite persistence
- `.dockerignore` — excludes local and unnecessary files from the Docker build context

The Docker configuration runs the Flask application using Gunicorn, a production WSGI server.

Gunicorn starts the application with:

```text
gunicorn --bind 0.0.0.0:5000 run:app
```

SQLite is retained for this technical test, with the database persisted through the mounted `instance/` directory.

## Notes

The application uses the Flask application factory pattern through `create_app()`.

The project separates HTTP handling, request validation and serialization, business logic, database models, and export operations into different modules.

Database credentials, application secrets, and other environment-specific configuration should be provided through environment variables rather than hard-coded in the source code.

The SQLite database is intentionally excluded from version control. Database structure is recreated through Flask-Migrate migrations, while optional sample data can be inserted using `seed.py`.
