[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 05](./SESION_05_SUBJECTS_GROUPS_OFFERINGS.md) · [Sesión 07 →](./SESION_07_AVAILABILITY_CONSTRAINTS.md)

# Sesión 06 — Salones y bloques horarios

**Duración:** 1 h 30 min  
**Objetivo:** crear los recursos físicos y temporales que el scheduler necesita.

## Distribución

```text
00–15  Diseño de recursos
15–35  Rooms
35–55  TimeBlocks
55–70  seed
70–82  pruebas
82–90  commit
```

## 1. Salones

El schema `RoomCreate` obliga a registrar capacidad y tipo:

```text
CLASSROOM
LAB
COMPUTER_LAB
AUDITORIUM
```

## 2. Crear salón

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/rooms   -H "Content-Type: application/json"   -d '{
    "code":"COMP1",
    "name":"Laboratorio de Cómputo 1",
    "capacity":32,
    "type":"COMPUTER_LAB",
    "building":"A",
    "active":true
  }'
```

## 3. Crear bloque

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/time-blocks   -H "Content-Type: application/json"   -d '{
    "day":"MONDAY",
    "start_time":"08:00",
    "end_time":"09:30",
    "order":1,
    "active":true
  }'
```

## 4. Seed opcional

### `apps/api/scripts/seed_demo.py`

```python
from firebase_admin import firestore, initialize_app

initialize_app()
db = firestore.client()

days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
times = [
    ("08:00", "09:30"), ("09:30", "11:00"), ("11:00", "12:30"),
    ("12:30", "14:00"), ("14:00", "15:30"), ("15:30", "17:00"),
]
for day in days:
    for index, (start, end) in enumerate(times, start=1):
        document_id = f"{day[:3]}-{index:02d}"
        db.collection("time_blocks").document(document_id).set({
            "day": day, "start_time": start, "end_time": end,
            "order": index, "active": True,
        })

rooms = [
    ("A101", "Aula 101", 35, "CLASSROOM"),
    ("A102", "Aula 102", 40, "CLASSROOM"),
    ("LAB1", "Laboratorio 1", 30, "LAB"),
    ("COMP1", "Cómputo 1", 32, "COMPUTER_LAB"),
]
for code, name, capacity, room_type in rooms:
    db.collection("rooms").document(code).set({
        "code": code, "name": name, "capacity": capacity,
        "type": room_type, "building": "A", "active": True,
    })
print("Demo seed completed")
```


### Ejecutar contra Emulator Suite

macOS/Linux:

```bash
export FIRESTORE_EMULATOR_HOST=127.0.0.1:8080
export GCLOUD_PROJECT=PROJECT_ID
PYTHONPATH=. python scripts/seed_demo.py
```

Windows PowerShell:

```powershell
$env:FIRESTORE_EMULATOR_HOST="127.0.0.1:8080"
$env:GCLOUD_PROJECT="PROJECT_ID"
$env:PYTHONPATH="."
python scripts/seed_demo.py
```

## 5. Por qué `order`

Permite detectar última hora, huecos y secuencia de clases.

## Checklist

- [ ] Salones con capacidad y tipo.
- [ ] Bloques por día.
- [ ] Seed probado.
- [ ] `order` consistente.

## Commit

```bash
git add .
git commit -m "feat: implement rooms time blocks and demo seed"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 05](./SESION_05_SUBJECTS_GROUPS_OFFERINGS.md) · [Sesión 07 →](./SESION_07_AVAILABILITY_CONSTRAINTS.md)
