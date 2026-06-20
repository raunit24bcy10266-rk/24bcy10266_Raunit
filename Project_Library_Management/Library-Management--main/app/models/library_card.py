from pydantic import BaseModel

class LibraryCard(BaseModel):
    card_id: str
    card_number: str
    member_id: str