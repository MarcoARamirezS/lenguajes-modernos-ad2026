[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 04](./SESION_04_PERIODS_TEACHERS.md) · [Sesión 06 →](./SESION_06_ROOMS_TIME_BLOCKS.md)

# Sesión 05 — Materias, grupos y ofertas académicas

**Duración:** 1 h 30 min  
**Objetivo:** definir qué profesor imparte qué materia a qué grupo.

## 1. Relación central

```text
course_offerings
├── academic_period_id
├── subject_id
├── group_id
├── teacher_id
└── active
```

Los schemas y services ya se crearon en la sesión anterior.

## 2. Materia

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/subjects   -H "Content-Type: application/json"   -d '{
    "code":"LM-401",
    "name":"Lenguajes Modernos",
    "weekly_blocks":2,
    "required_room_type":"COMPUTER_LAB",
    "active":true
  }'
```

## 3. Grupo

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/groups   -H "Content-Type: application/json"   -d '{
    "code":"LAC751",
    "name":"LAC751",
    "student_count":28,
    "academic_period_id":"PERIOD_ID",
    "active":true
  }'
```

## 4. Oferta académica

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/offerings   -H "Content-Type: application/json"   -d '{
    "academic_period_id":"PERIOD_ID",
    "subject_id":"SUBJECT_ID",
    "group_id":"GROUP_ID",
    "teacher_id":"TEACHER_ID",
    "active":true
  }'
```

## 5. Razón técnica

El scheduler no debe intentar adivinar relaciones entre profesores, grupos y materias. `course_offerings` es su entrada explícita.

## Checklist

- [ ] Materia creada.
- [ ] Grupo creado.
- [ ] Offering creado.
- [ ] Relaciones usan IDs.

## Commit

```bash
git add .
git commit -m "feat: implement subjects groups and course offerings"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 04](./SESION_04_PERIODS_TEACHERS.md) · [Sesión 06 →](./SESION_06_ROOMS_TIME_BLOCKS.md)
