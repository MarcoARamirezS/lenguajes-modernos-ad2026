# Sesión 08 — Dominio del problema de scheduling

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Transformar documentos Firestore en un modelo de dominio limpio que no dependa de Firebase y preparar una instancia del problema para OR-Tools.

## Resultado esperado

Existe una estructura `SchedulingProblem` validada con profesores, asignaciones, salones, bloques y restricciones.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | CSP vs optimización |
| 15–35 | Modelo in-memory |
| 35–50 | Asignaciones académicas |
| 50–65 | Problem builder |
| 65–80 | Prevalidaciones |
| 80–90 | Dataset pequeño |

## Por qué separar Firestore del solver

No usar consultas Firestore dentro de bucles del solver. Primero cargar y normalizar:

```text
Firestore → repositories → problem builder → SchedulingProblem → solver
```

## Asignación académica

Se agrega el concepto que faltaba:

```json
{
  "subjectId": "subject-1",
  "teacherId": "teacher-1",
  "groupId": "group-1",
  "requiredBlocks": 2
}
```

Colección sugerida: `teaching_assignments`.

## Dataclasses

`app/scheduling/domain.py`:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TeachingAssignment:
    id: str
    subject_id: str
    teacher_id: str
    group_id: str
    required_blocks: int

@dataclass(frozen=True)
class SchedulingProblem:
    assignments: list[TeachingAssignment]
    room_ids: list[str]
    time_block_ids: list[str]
```

La implementación real crecerá para incluir mapas por ID, capacidades, tipos y disponibilidad.

## Prevalidaciones

Antes de OR-Tools detectar:

- asignación sin profesor;
- materia inexistente;
- grupo inexistente;
- `requiredBlocks <= 0`;
- cero salones compatibles;
- profesor sin disponibilidad;
- grupo mayor que todos los salones compatibles.

Si una prevalidación falla, devolver 422 con un código comprensible en lugar de ejecutar un solver destinado a fallar.

## Dataset de clase

Crear manualmente:

- 3 profesores;
- 4 materias;
- 2 grupos;
- 3 salones;
- 10 bloques;
- 4 teaching assignments.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: create scheduling domain model"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
