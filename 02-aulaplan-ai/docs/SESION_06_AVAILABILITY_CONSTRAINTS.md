# Sesión 06 — Disponibilidad y restricciones

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Representar disponibilidad docente, hard constraints y soft constraints de forma explícita y validable.

## Resultado esperado

El backend puede persistir disponibilidad y restricciones estructuradas listas para ser consumidas por el solver.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Hard vs soft constraints |
| 15–35 | Disponibilidad |
| 35–55 | Constraint schema |
| 55–70 | Endpoints |
| 70–82 | Validación semántica |
| 82–90 | Casos |

## Conceptos

### Hard constraint

Si se viola, el horario no es válido.

Ejemplos:

- Profesor no disponible.
- Grupo doblemente asignado.
- Salón doblemente asignado.
- Salón con capacidad insuficiente.

### Soft constraint

Puede incumplirse, pero genera penalización.

- Preferencia por mañana.
- Evitar huecos.
- Evitar última hora.

## Schema sugerido

```python
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field

class Severity(StrEnum):
    HARD = "HARD"
    SOFT = "SOFT"

class ConstraintCreate(BaseModel):
    type: str
    severity: Severity
    weight: int = Field(default=1, ge=1, le=100)
    target_type: str
    target_id: str | None = None
    parameters: dict[str, Any] = {}
    active: bool = True
```

## Endpoint de disponibilidad

```text
GET /availability/teachers/{teacherId}
PUT /availability/teachers/{teacherId}
```

El `PUT` reemplaza el conjunto completo para facilitar la UI tipo grid.

Request:

```json
{
  "availableTimeBlockIds": ["MON-01", "MON-02", "WED-01"]
}
```

## Constraint catalog inicial

```text
TEACHER_UNAVAILABLE_DAY
TEACHER_PREFERRED_END
ROOM_REQUIRED
MAX_CONSECUTIVE_BLOCKS
MAX_DAILY_BLOCKS
GROUP_NO_GAPS
```

No aceptar un `type` desconocido silenciosamente; validar contra un catálogo.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: implement availability and constraints"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
