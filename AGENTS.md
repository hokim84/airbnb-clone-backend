## Cursor Cloud specific instructions

### Project Overview
Airbnb Clone Backend — Django REST API + Strawberry GraphQL. Single service, SQLite database (no external DB needed).

### Python Version
This project requires **Python 3.11** (not 3.12). The locked `typing_extensions==4.4.0` and `distutils` usage in `config/settings.py` are incompatible with Python 3.12. Python 3.11 is installed via the `deadsnakes` PPA.

### Running the Dev Server
```
poetry run python manage.py runserver 0.0.0.0:8000
```

### Running Tests
```
poetry run python manage.py test --verbosity 2
```

### Django System Check (lint equivalent)
```
poetry run python manage.py check
```

### Authentication for API Testing
The project supports a `Trust-Me` header for easy API testing:
```
curl -H "Trust-Me: admin" http://localhost:8000/api/v1/rooms/
```

### Key Gotchas
- The `pyproject.toml` references a `README.md` that doesn't exist. Use `poetry install --no-root` to avoid errors.
- The Room POST API has a generic `except Exception` that masks real errors (e.g., missing serializer context). Use GET endpoints or Django admin to verify data.
- `ALLOWED_HOSTS` is empty in settings — use `0.0.0.0:8000` or `localhost:8000` for dev server.
- `LANGUAGE_CODE` is set to `ko-kr` so admin UI and validation messages appear in Korean.
