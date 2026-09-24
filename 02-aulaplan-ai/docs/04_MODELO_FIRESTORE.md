# 04 — Modelo Firestore

## Colecciones

```text
users
academicPeriods
teachers
subjects
groups
rooms
timeBlocks
teachingAssignments
availabilityRules
constraints
scheduleVersions
scheduleEntries
auditLogs
```

## users

```json
{
  "uid": "firebase-auth-uid",
  "email": "coordinator@example.edu",
  "displayName": "Coordinador",
  "role": "COORDINATOR",
  "active": true
}
```

Roles:

```text
ADMIN
COORDINATOR
VIEWER
```

## academicPeriods

Campos principales:

- `name`.
- `startDate`.
- `endDate`.
- `status`: `DRAFT | ACTIVE | CLOSED`.

## teachers

- `code`.
- `name`.
- `email`.
- `active`.
- `maxDailyBlocks`.
- `maxWeeklyBlocks`.

## subjects

- `code`.
- `name`.
- `weeklyBlocks`.
- `requiredRoomType`.
- `active`.

## groups

- `code`.
- `name`.
- `studentCount`.
- `academicPeriodId`.

## rooms

- `code`.
- `name`.
- `capacity`.
- `type`.
- `building`.
- `active`.

Tipos sugeridos:

```text
CLASSROOM
LAB
COMPUTER_LAB
AUDITORIUM
```

## timeBlocks

- `day`.
- `startTime`.
- `endTime`.
- `order`.
- `active`.

## teachingAssignments

Une:

```text
teacher + subject + group + academicPeriod
```

Campos:

- `teacherId`.
- `subjectId`.
- `groupId`.
- `weeklyBlocks`.
- `preferredRoomType`.

## availabilityRules

- `teacherId`.
- `day`.
- `timeBlockId`.
- `available`.
- `preferenceWeight`.

## constraints

- `type`.
- `scope`.
- `targetId`.
- `hard`.
- `weight`.
- `parameters`.

## scheduleVersions

- `academicPeriodId`.
- `version`.
- `status`.
- `score`.
- `hardViolations`.
- `softViolations`.
- `createdBy`.
- `createdAt`.
- `publishedAt`.

## scheduleEntries

- `scheduleVersionId`.
- `assignmentId`.
- `teacherId`.
- `subjectId`.
- `groupId`.
- `roomId`.
- `timeBlockId`.

## Índices

Crear índices compuestos solo cuando una consulta real los necesite. Registrar cada índice en `firebase/firestore.indexes.json` para que el proyecto sea reproducible.

## Regla de acceso

El frontend no escribe estas colecciones de negocio directamente. Las escrituras pasan por `/api/*`, donde Firebase Admin aplica autorización y validación.
