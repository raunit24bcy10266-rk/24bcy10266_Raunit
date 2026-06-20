from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.librarian import Librarian

router = APIRouter(tags=["Librarians"])

librarians_collection = db["Librarians"]
departments_collection = db["Departments"]


@router.post("/librarians")
def create_librarian(librarian: Librarian):

    department = departments_collection.find_one(
        {"department_id": librarian.department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )

    existing = librarians_collection.find_one(
        {"librarian_id": librarian.librarian_id}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Librarian already exists"
        )

    librarians_collection.insert_one(
        librarian.model_dump()
    )

    return {
        "message": "Librarian created successfully"
    }


@router.get("/librarians")
def get_librarians():

    librarians = []

    for librarian in librarians_collection.find():
        librarian["_id"] = str(librarian["_id"])
        librarians.append(librarian)

    return librarians


@router.get("/librarians/{librarian_id}")
def get_librarian(librarian_id: str):

    librarian = librarians_collection.find_one(
        {"librarian_id": librarian_id}
    )

    if not librarian:
        raise HTTPException(
            status_code=404,
            detail="Librarian not found"
        )

    librarian["_id"] = str(librarian["_id"])

    return librarian


@router.put("/librarians/{librarian_id}")
def update_librarian(
    librarian_id: str,
    librarian: Librarian
):

    department = departments_collection.find_one(
        {"department_id": librarian.department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )

    result = librarians_collection.update_one(
        {"librarian_id": librarian_id},
        {"$set": librarian.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Librarian not found"
        )

    return {
        "message": "Librarian updated successfully"
    }


@router.delete("/librarians/{librarian_id}")
def delete_librarian(librarian_id: str):

    result = librarians_collection.delete_one(
        {"librarian_id": librarian_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Librarian not found"
        )

    return {
        "message": "Librarian deleted successfully"
    }