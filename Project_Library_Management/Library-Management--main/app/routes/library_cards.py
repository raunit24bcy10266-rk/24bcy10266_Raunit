from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.library_card import LibraryCard

router = APIRouter(tags=["Library Cards"])

cards_collection = db["Library_Cards"]
members_collection = db["Members"]


@router.post("/library-cards")
def create_library_card(card: LibraryCard):

    member = members_collection.find_one(
        {"member_id": card.member_id}
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member does not exist"
        )

    existing_card = cards_collection.find_one(
        {"member_id": card.member_id}
    )

    if existing_card:
        raise HTTPException(
            status_code=400,
            detail="Member already has a library card"
        )

    cards_collection.insert_one(
        card.model_dump()
    )

    return {
        "message": "Library Card created successfully"
    }


@router.get("/library-cards")
def get_cards():

    cards = []

    for card in cards_collection.find():
        card["_id"] = str(card["_id"])
        cards.append(card)

    return cards


@router.get("/library-cards/{card_id}")
def get_card(card_id: str):

    card = cards_collection.find_one(
        {"card_id": card_id}
    )

    if not card:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )

    card["_id"] = str(card["_id"])

    return card


@router.put("/library-cards/{card_id}")
def update_card(card_id: str, card: LibraryCard):

    member = members_collection.find_one(
        {"member_id": card.member_id}
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member does not exist"
        )

    result = cards_collection.update_one(
        {"card_id": card_id},
        {"$set": card.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )

    return {
        "message": "Library Card updated successfully"
    }


@router.delete("/library-cards/{card_id}")
def delete_card(card_id: str):

    result = cards_collection.delete_one(
        {"card_id": card_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )

    return {
        "message": "Library Card deleted successfully"
    }