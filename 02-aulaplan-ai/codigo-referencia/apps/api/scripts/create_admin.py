import os
from firebase_admin import auth, firestore, initialize_app

initialize_app()
email = os.environ["ADMIN_EMAIL"]
user = auth.get_user_by_email(email)
firestore.client().collection("users").document(user.uid).set({
    "email": user.email,
    "display_name": user.display_name or "Administrator",
    "role": "ADMIN",
    "active": True,
})
print(f"ADMIN ready: {email} ({user.uid})")
