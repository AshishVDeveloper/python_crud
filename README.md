# Django Product CRUD with REST API

A small, clean Django + Django REST Framework project demonstrating CRUD operations for products.

The browser UI does **not** save directly to the database. It calls the REST API with JavaScript. This makes the project easy to understand as a basic **Model → Serializer → API → View/UI** flow.

## Features

- Product list with API pagination
- Add product form
- Edit product form
- Delete with normal browser `confirm()`
- Success/error messages with normal browser `alert()`
- REST API for list, create, retrieve, update, partial update, and delete
- Validation for duplicate product names, negative price, and negative quantity
- SQLite by default for easy setup
- Optional MySQL configuration using environment variables
- Automated API tests
- Django admin registration

## Project flow

```text
Browser page
   ↓ fetch()
REST API URL
   ↓
APIView / DRF Generic View
   ↓
Serializer validation
   ↓
Product model
   ↓
Database
   ↓
JSON response
   ↓
Browser renders result
```

For a detailed explanation, read [`docs/FLOW.md`](docs/FLOW.md).

## URLs

### Browser pages

| URL | Purpose |
|---|---|
| `/` | Redirects to product list |
| `/products/` | Product list with pagination |
| `/products/add/` | Add product form |
| `/products/<id>/edit/` | Edit product form |

### REST API

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/products/` | Paginated product list |
| POST | `/api/products/` | Create product |
| GET | `/api/products/<id>/` | Get one product |
| PUT | `/api/products/<id>/` | Full update |
| PATCH | `/api/products/<id>/` | Partial update |
| DELETE | `/api/products/<id>/` | Delete product |

Pagination example:

```text
/api/products/?page=2&page_size=5
```

## Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Run tests

```bash
python manage.py test
```

### 5. Start the server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/products/
```

## Optional MySQL setup

SQLite works without any extra configuration. The project also supports a local `.env` file through `python-dotenv`.

For SQLite, copy `.env.example` to `.env` and keep `DB_ENGINE=sqlite` (or simply do not create `.env`).

To use MySQL, install a compatible MySQL Python driver, copy `.env.example` to `.env`, and use values like:

```text
DB_ENGINE=mysql
DB_NAME=crud_api_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Then run:

```bash
python manage.py migrate
python manage.py runserver
```

## Main files

```text
crud_api/
├── crud_api/
│   ├── settings.py
│   └── urls.py
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── pagination.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── templates/products/
│       ├── base.html
│       ├── list.html
│       └── form.html
├── docs/
│   └── FLOW.md
├── manage.py
└── requirements.txt
```

## Important note

This is intentionally a simple CRUD project. There is no SweetAlert dependency. Delete uses the standard browser confirmation dialog and create/update/delete success messages use the standard browser alert dialog.


## Troubleshooting

### `ModuleNotFoundError: No module named 'dotenv'`
Run:

```bash
pip install -r requirements.txt
```

The requirements file includes `python-dotenv`.

### `IndentationError` in `settings.py`
Do not indent the top-level `DATABASES` `if/else` block. Use the `settings.py` supplied with this ZIP unchanged unless you need to alter database credentials.
