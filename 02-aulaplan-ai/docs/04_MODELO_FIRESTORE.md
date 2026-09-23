# AulaPlan AI — Modelo Firestore

## Principio

Firestore almacenará datos operativos y versiones de horarios. OR-Tools trabaja en memoria con una representación del dominio; no se ejecutan búsquedas de Firestore dentro del ciclo interno del solver.

## Colecciones

```text
users
academic_periods
teachers
subjects
groups
rooms
time_blocks
teacher_availability
constraints
schedule_versions
```

## `teachers/{teacherId}`

```json
{
  "employeeNumber": "DOC-001",
  "name": "María López",
  "email": "maria@example.edu",
  "active": true,
  "createdAt": "serverTimestamp",
  "updatedAt": "serverTimestamp"
}
```

## `subjects/{subjectId}`

```json
{
  "code": "LAC751",
  "name": "Lenguajes Modernos",
  "weeklyBlocks": 2,
  "roomType": "COMPUTER_LAB",
  "active": true
}
```

## `groups/{groupId}`

```json
{
  "code": "LAC751-A",
  "size": 28,
  "academicPeriodId": "2026-AD",
  "active": true
}
```

## `rooms/{roomId}`

```json
{
  "code": "LAB-03",
  "name": "Laboratorio 3",
  "capacity": 32,
  "type": "COMPUTER_LAB",
  "building": "B",
  "active": true
}
```

## `time_blocks/{blockId}`

```json
{
  "day": "MONDAY",
  "order": 1,
  "start": "08:00",
  "end": "09:30",
  "active": true
}
```

## `teacher_availability/{availabilityId}`

```json
{
  "teacherId": "teacher-1",
  "timeBlockId": "MON-01",
  "available": true
}
```

## `constraints/{constraintId}`

```json
{
  "type": "TEACHER_PREFERRED_END",
  "severity": "SOFT",
  "weight": 10,
  "targetType": "TEACHER",
  "targetId": "teacher-1",
  "parameters": {
    "time": "13:00"
  },
  "active": true
}
```

## `schedule_versions/{scheduleId}`

```json
{
  "academicPeriodId": "2026-AD",
  "version": 3,
  "status": "GENERATED",
  "solverStatus": "FEASIBLE",
  "score": 820,
  "createdBy": "firebase-uid",
  "createdAt": "serverTimestamp",
  "entries": [
    {
      "subjectId": "subject-1",
      "teacherId": "teacher-1",
      "groupId": "group-1",
      "roomId": "room-1",
      "timeBlockId": "MON-01"
    }
  ]
}
```

## Índices esperados

- `teachers`: `active + name`.
- `subjects`: `active + code`.
- `groups`: `academicPeriodId + active`.
- `schedule_versions`: `academicPeriodId + version desc`.
- `constraints`: `active + severity`.

Los índices se agregan a `firebase/firestore.indexes.json` cuando una consulta real los requiera.

## Regla de versionado

Una versión publicada no se sobrescribe.

```text
v1 GENERATED
v2 REVIEWED
v3 PUBLISHED
v4 GENERATED
```

Si se requiere cambiar el horario, se crea una nueva versión.
