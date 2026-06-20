from pydantic import BaseModel

class Book(BaseModel):
    book_id: str
    title: str
    author: str
    isbn: str
    available_copies: int
    department_id: str