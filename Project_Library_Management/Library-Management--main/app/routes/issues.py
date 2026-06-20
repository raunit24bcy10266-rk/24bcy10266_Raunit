from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.database import db
from app.models.issue import Issue

router = APIRouter(tags=["Issues"])

issues_collection = db["Issues"]
members_collection = db["Members"]
books_collection = db["Books"]


@router.post("/issues")
def issue_book(issue: Issue):

    member = members_collection.find_one(
        {"member_id": issue.member_id}
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    book = books_collection.find_one(
        {"book_id": issue.book_id}
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book["available_copies"] <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book not available"
        )

    existing_issue = issues_collection.find_one(
        {"issue_id": issue.issue_id}
    )

    if existing_issue:
        raise HTTPException(
            status_code=400,
            detail="Issue ID already exists"
        )

    issue_data = issue.model_dump()

    issue_data["issue_date"] = str(
        issue_data["issue_date"]
    )

    if issue_data.get("return_date"):
        issue_data["return_date"] = str(
            issue_data["return_date"]
        )

    issues_collection.insert_one(
        issue_data
    )

    books_collection.update_one(
        {"book_id": issue.book_id},
        {"$inc": {"available_copies": -1}}
    )

    return {
        "message": "Book issued successfully"
    }


@router.get("/issues")
def get_issues():

    issues = []

    for issue in issues_collection.find():
        issue["_id"] = str(issue["_id"])
        issues.append(issue)

    return issues


@router.get("/issues/{issue_id}")
def get_issue(issue_id: str):

    issue = issues_collection.find_one(
        {"issue_id": issue_id}
    )

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue record not found"
        )

    issue["_id"] = str(issue["_id"])

    return issue


@router.put("/issues/return/{issue_id}")
def return_book(issue_id: str):

    issue = issues_collection.find_one(
        {"issue_id": issue_id}
    )

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue record not found"
        )

    if issue.get("status") == "Returned":
        raise HTTPException(
            status_code=400,
            detail="Book already returned"
        )

    issues_collection.update_one(
        {"issue_id": issue_id},
        {
            "$set": {
                "status": "Returned",
                "return_date": str(datetime.now().date())
            }
        }
    )

    books_collection.update_one(
        {"book_id": issue["book_id"]},
        {"$inc": {"available_copies": 1}}
    )

    return {
        "message": "Book returned successfully"
    }


@router.delete("/issues/{issue_id}")
def delete_issue(issue_id: str):

    result = issues_collection.delete_one(
        {"issue_id": issue_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Issue record not found"
        )

    return {
        "message": "Issue record deleted successfully"
    }