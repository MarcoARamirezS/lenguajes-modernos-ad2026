[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 06](./SESION_06_ROOMS_TIME_BLOCKS.md) · [Sesión 08 →](./SESION_08_AUTH_RBAC.md)

# Sesión 07 — Disponibilidad y restricciones

**Duración:** 1 h 30 min  
**Objetivo:** capturar las reglas que controlarán el problema de horarios.

## Distribución

```text
00–20  Hard vs Soft
20–40  Disponibilidad
40–60  Constraints
60–78  pruebas
78–90  análisis
```

## Hard constraints

Nunca pueden violarse: profesor/grupo/salón ocupado, no disponibilidad, capacidad, tipo de salón y máximos de carga.

## Soft constraints

Modifican el score: preferencias, evitar últimas horas y reducir huecos.

## Disponibilidad

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/availability   -H "Content-Type: application/json"   -d '{
    "teacher_id":"TEACHER_ID",
    "time_block_id":"MON-01",
    "available":true,
    "preference_weight":10
  }'
```

## Hard constraint

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/constraints   -H "Content-Type: application/json"   -d '{
    "type":"TEACHER_UNAVAILABLE",
    "priority":"HARD",
    "target_type":"TEACHER",
    "target_id":"TEACHER_ID",
    "weight":0,
    "params":{"time_block_id":"TUE-03"},
    "active":true
  }'
```

## Soft constraint

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/constraints   -H "Content-Type: application/json"   -d '{
    "type":"TEACHER_PREFERRED",
    "priority":"SOFT",
    "target_type":"TEACHER",
    "target_id":"TEACHER_ID",
    "weight":15,
    "params":{"time_block_id":"MON-01"},
    "active":true
  }'
```

## Regla

```text
HARD → filtra candidatos o impide place()
SOFT → puntúa soluciones
```

## Checklist

- [ ] disponibilidad.
- [ ] hard constraint.
- [ ] soft constraint.
- [ ] pesos coherentes.

## Commit

```bash
git add .
git commit -m "feat: implement availability and scheduling constraints"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 06](./SESION_06_ROOMS_TIME_BLOCKS.md) · [Sesión 08 →](./SESION_08_AUTH_RBAC.md)
