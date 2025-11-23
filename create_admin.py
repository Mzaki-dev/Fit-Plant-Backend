from app.database import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate

db = SessionLocal()

admin = UserCreate(
    full_name="Admin User",
    email="admin@example.com",
    phone=None,
    fields=None,
    role="admin",
    password="adminpass",
    confirm_password="adminpass"
)

create_user(db, admin)

db.close()

print("Admin created")