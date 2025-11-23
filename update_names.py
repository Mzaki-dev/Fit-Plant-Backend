from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("UPDATE users SET full_name = 'Unknown' WHERE full_name IS NULL OR full_name = ''"))
    conn.commit()
    print(f'Updated {result.rowcount} rows')