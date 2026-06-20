from pydantic import BaseModel, EmailStr

class Librarian(BaseModel):
    librarian_id: str
    name: str
    email: EmailStr
    phone: str
    department_id: str