# Product CRUD Flow Documentation

This document explains how the project works from the browser to the database.

## 1. Data model

File:

```text
products/models.py
```

The `Product` model contains:

- `name`
- `description`
- `price`
- `quantity`
- `created_at`
- `updated_at`

Django creates the database table from this model through migrations.

## 2. Serializer

File:

```text
products/serializers.py
```

`ProductSerializer` has two responsibilities:

1. Convert `Product` objects into JSON for API responses.
2. Validate incoming JSON before creating or updating a product.

Current validation includes:

- Product name cannot be blank.
- Product name must be unique ignoring letter case.
- Price cannot be negative.
- Quantity cannot be negative.

Example incoming JSON:

```json
{
  "name": "Keyboard",
  "description": "USB keyboard",
  "price": "850.00",
  "quantity": 15
}
```

## 3. REST API views

File:

```text
products/views.py
```

Two DRF generic API views are used.

### ProductListCreateAPIView

Handles:

```text
GET  /api/products/
POST /api/products/
```

GET returns a paginated list.

POST validates the request with `ProductSerializer` and creates the record when valid.

### ProductDetailAPIView

Handles:

```text
GET    /api/products/<id>/
PUT    /api/products/<id>/
PATCH  /api/products/<id>/
DELETE /api/products/<id>/
```

DRF automatically handles 404 responses if the requested product does not exist.

## 4. Pagination

File:

```text
products/pagination.py
```

The API returns 5 records per page by default.

Example:

```text
GET /api/products/?page=2&page_size=5
```

Typical API response:

```json
{
  "count": 13,
  "next": "http://127.0.0.1:8000/api/products/?page=3&page_size=5",
  "previous": "http://127.0.0.1:8000/api/products/?page=1&page_size=5",
  "results": []
}
```

The browser calculates the total number of pages from `count`.

## 5. URL routing

File:

```text
products/urls.py
```

There are two groups of routes.

Browser routes:

```text
/products/
/products/add/
/products/<id>/edit/
```

API routes:

```text
/api/products/
/api/products/<id>/
```

The project-level `crud_api/urls.py` includes all product URLs and redirects `/` to the product list page.

## 6. Product list page

File:

```text
products/templates/products/list.html
```

When the page opens:

1. JavaScript calls `GET /api/products/?page=1&page_size=5`.
2. The API returns JSON.
3. JavaScript creates the table rows.
4. Pagination buttons are generated from the API `count`.

When Delete is clicked:

1. Standard browser `confirm()` asks the user to confirm.
2. JavaScript sends `DELETE /api/products/<id>/`.
3. On success, standard browser `alert()` is shown.
4. The current list page reloads from the API.
5. If the last record on the final page was deleted, the UI automatically moves back to the previous valid page.

## 7. Add product flow

File:

```text
products/templates/products/form.html
```

For `/products/add/`:

```text
User fills form
    ↓
JavaScript creates JSON
    ↓
POST /api/products/
    ↓
Serializer validates data
    ↓
Product saved
    ↓
201 Created JSON response
    ↓
Browser alert
    ↓
Redirect to /products/
```

If validation fails, the API returns HTTP 400 and errors are displayed below the related fields.

## 8. Edit product flow

For `/products/<id>/edit/`:

1. The page receives the product ID from Django.
2. JavaScript calls `GET /api/products/<id>/`.
3. Returned values fill the form.
4. User changes the data and submits.
5. JavaScript sends `PUT /api/products/<id>/`.
6. Serializer validates the updated values.
7. On success, the user sees a normal browser alert and returns to the list.

## 9. Why the API and HTML are separated

This project intentionally keeps the UI and data layer separate.

The HTML pages do not call `Product.objects` directly. They consume the API. That means the same REST endpoints can later be reused by:

- a React/Vue frontend,
- a mobile application,
- another internal system,
- Postman/API clients.

## 10. Database configuration

File:

```text
crud_api/settings.py
```

SQLite is the default because it makes the ZIP immediately runnable.

For MySQL, set:

```text
DB_ENGINE=mysql
DB_NAME=crud_api_db
DB_USER=root
DB_PASSWORD=...
DB_HOST=127.0.0.1
DB_PORT=3306
```

No application code needs to change when switching databases.

## 11. Tests

File:

```text
products/tests.py
```

Tests cover:

- paginated list
- product creation
- duplicate-name validation
- update
- delete
- negative price/quantity validation

Run:

```bash
python manage.py test
```

## 12. API testing examples

### Create

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Mouse","description":"Wireless mouse","price":"599.00","quantity":20}'
```

### List

```bash
curl "http://127.0.0.1:8000/api/products/?page=1&page_size=5"
```

### Update

```bash
curl -X PUT http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Mouse Pro","description":"Updated","price":"799.00","quantity":10}'
```

### Delete

```bash
curl -X DELETE http://127.0.0.1:8000/api/products/1/
```
