from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
workers = db.query(User).filter(User.role == 'worker').all()
for w in workers:
    print(f'ID: {w.id}, Full Name: "{w.full_name}"')
db.close()