# Sesión 05 — Grupos, salones y bloques horarios

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Agregar recursos académicos que posteriormente se transformarán en variables y dominios del solver.

## Resultado esperado

Existen grupos asociados a un periodo, salones tipados y bloques horarios ordenados por día.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Relaciones por ID |
| 15–35 | Groups |
| 35–55 | Rooms |
| 55–70 | Time blocks |
| 70–82 | Validaciones cruzadas |
| 82–90 | Prueba |

## Group

Campos mínimos:

```json
{
  "code": "LAC751-A",
  "size": 28,
  "academicPeriodId": "period-id",
  "active": true
}
```

## Room

Tipos válidos:

```python
from enum import StrEnum

class RoomType(StrEnum):
    CLASSROOM = "CLASSROOM"
    LAB = "LAB"
    COMPUTER_LAB = "COMPUTER_LAB"
    AUDITORIUM = "AUDITORIUM"
```

Reglas:

- `capacity > 0`.
- `code` único.
- tipo conocido.

## TimeBlock

No almacenar una fecha; almacenar la posición semanal reutilizable:

```json
{
  "day": "MONDAY",
  "order": 1,
  "start": "08:00",
  "end": "09:30",
  "active": true
}
```

## Validaciones de servicio

Antes de crear un grupo:

1. Verificar que `academicPeriodId` existe.
2. Verificar código único dentro del periodo.

Antes de asignar un salón a una materia más adelante:

1. Capacidad del salón >= tamaño del grupo.
2. Tipo del salón compatible con `roomType`.

## Datos semilla manuales

Crear al menos:

- 2 grupos.
- 3 salones.
- 10 bloques horarios distribuidos en lunes y martes.

Esto permite iniciar la sesión 08 sin depender de UI todavía.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: implement groups rooms and time blocks"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
