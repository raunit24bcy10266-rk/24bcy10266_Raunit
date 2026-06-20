from pydantic import BaseModel
from datetime import date

class Issue(BaseModel):
    issue_id: str
    member_id: str
    book_id: str
    issue_date: date
    status: str = "Issued"