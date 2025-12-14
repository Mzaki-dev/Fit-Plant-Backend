from pydantic import BaseModel, Field

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: str
    phone: str | None = None
    fields: str | None = None
    role: str
    image_path: str | None = None

class UserCreate(UserBase):
    password: str
    confirm_password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    fields: str | None = None
    role: str | None = None
    is_active: bool | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class PaginatedWorkers(BaseModel):
    workers: list[User]
    total: int
    page: int
    limit: int
    total_pages: int

    class Config:
        from_attributes = True

class TaskCounts(BaseModel):
    pending: int
    completed: int
    total: int