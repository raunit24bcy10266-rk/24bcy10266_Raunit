from fastapi import APIRouter
from app.database import db

router = APIRouter(tags=["Reports"])

books_collection = db["Books"]
issues_collection = db["Issues"]
members_collection = db["Members"]


@router.get("/reports/books-by-department")
def books_by_department():

    pipeline = [
        {
            "$group": {
                "_id": "$department_id",
                "total_books": {"$sum": 1}
            }
        }
    ]

    result = list(
        books_collection.aggregate(pipeline)
    )

    for item in result:
        item["_id"] = str(item["_id"])

    return result


@router.get("/reports/most-borrowed-books")
def most_borrowed_books():

    pipeline = [
        {
            "$group": {
                "_id": "$book_id",
                "borrow_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "borrow_count": -1
            }
        }
    ]

    result = list(
        issues_collection.aggregate(pipeline)
    )

    for item in result:
        item["_id"] = str(item["_id"])

    return result


@router.get("/reports/members-by-department")
def members_by_department():

    pipeline = [
        {
            "$group": {
                "_id": "$department_id",
                "total_members": {"$sum": 1}
            }
        }
    ]

    result = list(
        members_collection.aggregate(pipeline)
    )

    for item in result:
        item["_id"] = str(item["_id"])

    return result