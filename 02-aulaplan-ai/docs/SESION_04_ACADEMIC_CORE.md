# Sesión 04 — Academic Core: periodos, profesores y materias

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Implementar los primeros módulos reales con Pydantic, Service y Repository para practicar una arquitectura consistente sobre Firestore.

## Resultado esperado

Los endpoints CRUD de periodos, profesores y materias funcionan contra Firestore y aparecen documentados en Swagger.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–10 | Modelo de datos |
| 10–30 | Schemas Pydantic |
| 30–50 | Repositories |
| 50–70 | Services |
| 70–82 | Routers |
| 82–90 | Swagger |

## Estructura por módulo

```text
app/
├── schemas/teacher.py
├── repositories/teacher_repository.py
├── services/teacher_service.py
└── api/v1/routes/teachers.py
```

## Schema ejemplo

`app/schemas/teacher.py`:

```python
from pydantic import BaseModel, EmailStr, Field


class TeacherCreate(BaseModel):
    employee_number: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    active: bool = True


class TeacherResponse(TeacherCreate):
    id: str
```

Agregar `email-validator` si Pydantic lo solicita:

```bash
pip install email-validator
```

## Repository

```python
from firebase_admin import firestore
from app.core.firebase import get_db


class TeacherRepository:
    collection_name = "teachers"

    def __init__(self):
        self.db = get_db()

    def create(self, data: dict) -> dict:
        ref = self.db.collection(self.collection_name).document()
        payload = {**data, "createdAt": firestore.SERVER_TIMESTAMP}
        ref.set(payload)
        return {"id": ref.id, **data}

    def list(self) -> list[dict]:
        return [{"id": doc.id, **doc.to_dict()} for doc in self.db.collection(self.collection_name).stream()]
```

## Service

El Service contiene reglas de negocio, por ejemplo evitar `employee_number` repetido. No se duplica validación de formato que ya pertenece a Pydantic.

## Endpoints mínimos

```text
GET/POST/PATCH/DELETE /academic-periods
GET/POST/PATCH/DELETE /teachers
GET/POST/PATCH/DELETE /subjects
```

## Pruebas manuales

Usar Swagger para crear:

1. Periodo `2026-AD`.
2. Profesor `DOC-001`.
3. Materia `LAC751`.

Consultar Firestore Emulator UI y verificar documentos.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: implement academic core catalogs"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
