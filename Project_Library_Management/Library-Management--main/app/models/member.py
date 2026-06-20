from pydantic import BaseModel, EmailStr

class Member(BaseModel):
    member_id: str
    name: str
    email: EmailStr
    phone: str
    department_id: str