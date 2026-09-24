# 12 — Generación, versiones y publicación

**Duración:** 1 hora 30 minutos.

## Objetivo

Convertir el solver en un flujo de negocio completo con versiones inmutables, revisión y publicación.

## Distribución de tiempo

- **00–15 min** — Lifecycle
- **15–35 min** — Persistencia
- **35–55 min** — Versioning
- **55–75 min** — Review/publish
- **75–90 min** — Audit

## Conceptos

- immutable versions
- status transitions
- transactional thinking
- auditability

## Desarrollo

### 1. Guardar versión

Cada ejecución exitosa crea `scheduleVersions` y sus `scheduleEntries`. No sobrescribir una versión anterior.

### 2. Estados

Permitir transiciones válidas `GENERATED → REVIEWED → PUBLISHED → ARCHIVED`.

### 3. Publicación única

Cuando se publica una versión, definir claramente qué ocurre con la versión publicada anterior del mismo periodo.

### 4. Auditoría

Registrar actor, timestamp, versión, acción y metadatos relevantes sin almacenar tokens.

### 5. Frontend

Conectar comparación de versiones, score y botón de publicación al contrato real.

## Endpoints al cierre

- `GET /api/schedules`
- `GET /api/schedules/:id`
- `POST /api/schedules/:id/review`
- `POST /api/schedules/:id/publish`
- `POST /api/schedules/:id/archive`

## Checklist de cierre

- [ ] Versiones son inmutables
- [ ] Transiciones inválidas regresan 409
- [ ] Solo rol permitido publica
- [ ] Auditoría creada
- [ ] Frontend muestra versión publicada

## Commit sugerido

```bash
git add .
git commit -m "feat: implement schedule versioning and publication"
```

## Persistencia de versiones

### Estado

```ts
export type ScheduleStatus =
  | 'GENERATED'
  | 'REVIEWED'
  | 'PUBLISHED'
  | 'ARCHIVED'
```

### Generación

El service debe:

1. cargar `ScheduleProblem` desde repositories;
2. validar preflight;
3. ejecutar solver con `MAX_SOLVER_MS` limitado;
4. rechazar si no existe solución válida;
5. crear un documento `scheduleVersions`;
6. guardar `scheduleEntries` asociados;
7. devolver métricas y versión.

Ejemplo de documento:

```ts
const version = {
  academicPeriodId,
  version: nextVersion,
  status: 'GENERATED',
  score: result.score,
  hardViolations: 0,
  softViolations: result.softViolations,
  solver: {
    nodes: result.nodes,
    elapsedMs: result.elapsedMs,
    timedOut: result.timedOut
  },
  createdBy: user.uid,
  createdAt: new Date().toISOString()
}
```

## Transiciones

```ts
const allowedTransitions = {
  GENERATED: ['REVIEWED', 'ARCHIVED'],
  REVIEWED: ['PUBLISHED', 'ARCHIVED'],
  PUBLISHED: ['ARCHIVED'],
  ARCHIVED: []
} as const
```

Si una transición no está permitida, responder `409 INVALID_SCHEDULE_TRANSITION`.

## Publicación

Usar una transacción Firestore para:

1. localizar la versión publicada actual del mismo periodo;
2. archivarla si existe;
3. marcar la nueva versión como `PUBLISHED`;
4. registrar `publishedAt` y `publishedBy`.

De esta forma nunca existen dos versiones publicadas activas para el mismo periodo.

[Volver al índice](./README.md)
