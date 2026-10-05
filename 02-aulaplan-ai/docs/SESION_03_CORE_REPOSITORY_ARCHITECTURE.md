[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 02](./SESION_02_FIREBASE_FUNCTIONS_FIRESTORE.md) · [Sesión 04 →](./SESION_04_PERIODS_TEACHERS.md)

# Sesión 03 — Core, errores, Repository y Service

**Duración:** 1 h 30 min  
**Objetivo:** construir la arquitectura reutilizable antes de crear módulos académicos.

## 1. Estructura

```bash
mkdir -p src/firebase src/repositories src/schemas src/services
```

En Windows usa `New-Item -ItemType Directory -Force`.

## 2. Código

### `apps/api/src/core/errors.py`

```python
class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400, code: str = "API_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
```


### `apps/api/src/firebase/client.py`

```python
from functools import lru_cache
from google.cloud.firestore_v1 import Client
from firebase_admin import firestore


@lru_cache(maxsize=1)
def get_db() -> Client:
    return firestore.client()
```


### `apps/api/src/http/responses.py`

```python
from datetime import date, datetime
from flask import jsonify
from pydantic import ValidationError

from src.core.errors import ApiError


def to_jsonable(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    return value


def register_error_handlers(app) -> None:
    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return jsonify({"error": error.code, "message": error.message}), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": "VALIDATION_ERROR", "details": error.errors()}), 422

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify({"error": "NOT_FOUND", "message": "Resource not found"}), 404

    @app.errorhandler(Exception)
    def handle_unexpected(error: Exception):
        app.logger.exception(error)
        return jsonify({"error": "INTERNAL_ERROR", "message": "Unexpected server error"}), 500
```


### `apps/api/src/repositories/base.py`

```python
from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1.base_query import FieldFilter

from src.core.errors import ApiError
from src.firebase.client import get_db


class FirestoreRepository:
    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name

    @property
    def collection(self):
        return get_db().collection(self.collection_name)

    def list(self, filters: dict[str, Any] | None = None) -> list[dict]:
        query = self.collection
        for key, value in (filters or {}).items():
            query = query.where(filter=FieldFilter(key, "==", value))

        result = []
        for snapshot in query.stream():
            row = snapshot.to_dict() or {}
            row["id"] = snapshot.id
            result.append(row)
        return result

    def get(self, document_id: str) -> dict:
        snapshot = self.collection.document(document_id).get()
        if not snapshot.exists:
            raise ApiError("Resource not found", 404, "NOT_FOUND")
        data = snapshot.to_dict() or {}
        data["id"] = snapshot.id
        return data

    def create(self, data: dict) -> dict:
        now = datetime.now(timezone.utc)
        document = self.collection.document()
        payload = {**data, "created_at": now, "updated_at": now}
        document.set(payload)
        return self.get(document.id)

    def update(self, document_id: str, data: dict) -> dict:
        self.get(document_id)
        payload = {**data, "updated_at": datetime.now(timezone.utc)}
        self.collection.document(document_id).update(payload)
        return self.get(document_id)

    def delete(self, document_id: str) -> None:
        self.get(document_id)
        self.collection.document(document_id).delete()

    def exists_by_field(self, field: str, value: Any, exclude_id: str | None = None) -> bool:
        query = self.collection.where(filter=FieldFilter(field, "==", value)).limit(2)
        for snapshot in query.stream():
            if snapshot.id != exclude_id:
                return True
        return False
```


### `apps/api/src/services/crud.py`

```python
from typing import Type
from pydantic import BaseModel

from src.core.errors import ApiError
from src.repositories.base import FirestoreRepository


class CrudService:
    def __init__(
        self,
        repository: FirestoreRepository,
        create_schema: Type[BaseModel],
        update_schema: Type[BaseModel],
        unique_fields: tuple[str, ...] = (),
    ) -> None:
        self.repository = repository
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.unique_fields = unique_fields

    def list(self, filters: dict | None = None) -> list[dict]:
        return self.repository.list(filters)

    def get(self, document_id: str) -> dict:
        return self.repository.get(document_id)

    def create(self, raw: dict) -> dict:
        model = self.create_schema.model_validate(raw)
        data = model.model_dump()
        self._assert_unique(data)
        return self.repository.create(data)

    def update(self, document_id: str, raw: dict) -> dict:
        model = self.update_schema.model_validate(raw)
        data = model.model_dump()
        self._assert_unique(data, document_id)
        return self.repository.update(document_id, data)

    def delete(self, document_id: str) -> None:
        self.repository.delete(document_id)

    def _assert_unique(self, data: dict, exclude_id: str | None = None) -> None:
        for field in self.unique_fields:
            if field in data and self.repository.exists_by_field(field, data[field], exclude_id):
                raise ApiError(f"{field} already exists", 409, "DUPLICATE_VALUE")
```


## 3. Actualizar `app.py`

```python
from flask import Flask
from src.http.responses import register_error_handlers
from src.http.routes_health import health_bp

def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing
    register_error_handlers(app)
    app.register_blueprint(health_bp)
    return app
```

## 4. Prueba

```bash
PYTHONPATH=. pytest tests -q
```

## Concepto

```text
Route → Service → Repository → Firestore
```

## Checklist

- [ ] `ApiError`.
- [ ] cliente Firestore central.
- [ ] repository genérico.
- [ ] CrudService.
- [ ] error handlers.

## Commit

```bash
git add .
git commit -m "feat: add backend core repository architecture"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 02](./SESION_02_FIREBASE_FUNCTIONS_FIRESTORE.md) · [Sesión 04 →](./SESION_04_PERIODS_TEACHERS.md)
