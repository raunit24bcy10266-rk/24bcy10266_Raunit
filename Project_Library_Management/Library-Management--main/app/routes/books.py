from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.book import Book

router = APIRouter(tags=["Books"])

books_collection = db["Books"]
departments_collection = db["Departments"]


@router.post("/books")
def create_book(book: Book):

    department = departments_collection.find_one(
        {"department_id": book.department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )

    existing = books_collection.find_one(
        {"book_id": book.book_id}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Book already exists"
        )

    books_collection.insert_one(
        book.model_dump()
    )

    return {
        "message": "Book created successfully"
    }


@router.get("/books")
def get_books():

    books = []

    for book in books_collection.find():
        book["_id"] = str(book["_id"])
        books.append(book)

    return books


@router.get("/books/{book_id}")
def get_book(book_id: str):

    book = books_collection.find_one(
        {"book_id": book_id}
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book["_id"] = str(book["_id"])

    return book


@router.put("/books/{book_id}")
def update_book(book_id: str, book: Book):

    department = departments_collection.find_one(
        {"department_id": book.department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )

    result = books_collection.update_one(
        {"book_id": book_id},
        {"$set": book.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book updated successfully"
    }


@router.delete("/books/{book_id}")
def delete_book(book_id: str):

    result = books_collection.delete_one(
        {"book_id": book_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book deleted successfully"
    }