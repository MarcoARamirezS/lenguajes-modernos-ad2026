[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 04](./SESION_04_ACADEMIC_CORE.md) · [Sesión 06 →](./SESION_06_AVAILABILITY_CONSTRAINTS.md)

# Sesión 05 — Groups, Rooms & Time Blocks

**Duración:** 1 hora 30 minutos.

## Objetivo

Completar recursos necesarios para generar horarios.

## Distribución de tiempo

```text
00–15  Diseño
15–35  Groups
35–55  Rooms
55–70  Time blocks
70–85  Validaciones
85–90  commit
```


## Groups

Campos:

```text
code
name
student_count
academic_period_id
active
```

## Rooms

```text
code
name
capacity
type
building
active
```

Tipos:

```text
CLASSROOM
LAB
COMPUTER_LAB
AUDITORIUM
```

## Time blocks

```text
day
start_time
end_time
order
active
```

El scheduler no debe trabajar con strings de hora dispersos; debe usar IDs de bloques normalizados.


## Cierre verificable

- [ ] CRUD groups.
- [ ] CRUD rooms.
- [ ] CRUD time blocks.
- [ ] Capacidad validada.
- [ ] Tipo de salón validado.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 04](./SESION_04_ACADEMIC_CORE.md) · [Sesión 06 →](./SESION_06_AVAILABILITY_CONSTRAINTS.md)
