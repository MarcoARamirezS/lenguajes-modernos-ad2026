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
