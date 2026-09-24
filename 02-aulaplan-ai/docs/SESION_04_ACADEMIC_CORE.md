[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 03](./SESION_03_FIREBASE_FUNCTIONS_FIRESTORE.md) · [Sesión 05 →](./SESION_05_GROUPS_ROOMS_BLOCKS.md)

# Sesión 04 — Academic Core

**Duración:** 1 hora 30 minutos.

## Objetivo

Implementar periodos académicos, profesores y materias.

## Distribución de tiempo

```text
00–15  Modelo
15–35  Pydantic schemas
35–55  Repositories
55–75  Services
75–85  Routes
85–90  commit
```


## Schemas

Ejemplo:

```python
from pydantic import BaseModel, EmailStr, Field

class TeacherCreate(BaseModel):
    code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    max_daily_blocks: int = Field(ge=1, le=8)
    max_weekly_blocks: int = Field(ge=1, le=40)
```

Instalar email validator:

```bash
pip install email-validator
pip freeze > requirements.txt
```

## Capas

Crear:

```text
src/schemas/teacher.py
src/repositories/teacher_repository.py
src/services/teacher_service.py
src/http/routes/teachers.py
```

Repetir para:

- academic periods;
- subjects.

## Regla

Los códigos académicos deben ser únicos.


## Cierre verificable

- [ ] CRUD teachers.
- [ ] CRUD subjects.
- [ ] CRUD academic periods.
- [ ] Pydantic rechaza payloads inválidos.
- [ ] Duplicados devuelven 409.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 03](./SESION_03_FIREBASE_FUNCTIONS_FIRESTORE.md) · [Sesión 05 →](./SESION_05_GROUPS_ROOMS_BLOCKS.md)
