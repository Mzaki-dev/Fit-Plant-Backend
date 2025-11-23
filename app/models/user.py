from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    fields = Column(String, nullable=True)
    role = Column(String)  # 'admin' or 'worker'
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    image_path = Column(String, nullable=True)