from fastapi import APIRouter
from app.database import db

router = APIRouter(tags=["Admin"])


@router.delete("/drop/departments")
def drop_departments():
    db["Departments"].drop()
    return {
        "message": "Departments collection dropped successfully"
    }


@router.delete("/drop/members")
def drop_members():
    db["Members"].drop()
    return {
        "message": "Members collection dropped successfully"
    }


@router.delete("/drop/books")
def drop_books():
    db["Books"].drop()
    return {
        "message": "Books collection dropped successfully"
    }


@router.delete("/drop/librarians")
def drop_librarians():
    db["Librarians"].drop()
    return {
        "message": "Librarians collection dropped successfully"
    }


@router.delete("/drop/library-cards")
def drop_library_cards():
    db["Library_Cards"].drop()
    return {
        "message": "Library Cards collection dropped successfully"
    }


@router.delete("/drop/issues")
def drop_issues():
    db["Issues"].drop()
    return {
        "message": "Issues collection dropped successfully"
    }