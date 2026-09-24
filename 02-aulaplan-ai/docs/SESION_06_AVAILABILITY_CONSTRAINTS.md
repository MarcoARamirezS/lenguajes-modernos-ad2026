[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 05](./SESION_05_GROUPS_ROOMS_BLOCKS.md) · [Sesión 07 →](./SESION_07_FIREBASE_AUTH_RBAC.md)

# Sesión 06 — Availability & Constraints

**Duración:** 1 hora 30 minutos.

## Objetivo

Representar disponibilidad y reglas del problema de horarios.

## Distribución de tiempo

```text
00–20  Hard vs soft
20–40  Availability
40–60  Constraint catalog
60–80  API
80–90  pruebas
```


## Hard constraints

Nunca pueden incumplirse:

- profesor ocupado;
- grupo ocupado;
- salón ocupado;
- profesor no disponible;
- capacidad insuficiente;
- tipo de salón incorrecto.

## Soft constraints

Se puntúan:

- preferencia de mañana;
- evitar huecos;
- evitar última hora;
- distribuir sesiones;
- compactar agenda.

## Catálogo

```text
TEACHER_UNAVAILABLE
TEACHER_PREFERRED
ROOM_REQUIRED
MAX_CONSECUTIVE
MAX_DAILY_BLOCKS
AVOID_GAPS
```

Cada constraint tiene:

```text
type
target_id
priority
weight
params
```


## Cierre verificable

- [ ] Disponibilidad persistida.
- [ ] Hard/soft diferenciados.
- [ ] Catálogo validado.
- [ ] Payloads inválidos rechazados.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 05](./SESION_05_GROUPS_ROOMS_BLOCKS.md) · [Sesión 07 →](./SESION_07_FIREBASE_AUTH_RBAC.md)
