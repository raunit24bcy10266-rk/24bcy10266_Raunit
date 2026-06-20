from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.member import Member

router = APIRouter(tags=["Members"])

members_collection = db["Members"]
departments_collection = db["Departments"]


@router.post("/members")
def create_member(member: Member):

    department = departments_collection.find_one(
        {"department_id": member.department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )

    existing = members_collection.find_one(
        {"member_id": member.member_id}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Member already exists"
        )

    members_collection.insert_one(
        member.model_dump()
    )

    return {
        "message": "Member created successfully"
    }


@router.get("/members")
def get_members():

    members = []

    for member in members_collection.find():
        member["_id"] = str(member["_id"])
        members.append(member)

    return members


@router.get("/members/{member_id}")
def get_member(member_id: str):

    member = members_collection.find_one(
        {"member_id": member_id}
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    member["_id"] = str(member["_id"])

    return member


@router.put("/members/{member_id}")
def update_member(
    member_id: str,
    member: Member
):

    department = departments_collection.find_one(
        {"department_id": member.department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )

    result = members_collection.update_one(
        {"member_id": member_id},
        {"$set": member.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return {
        "message": "Member updated successfully"
    }


@router.delete("/members/{member_id}")
def delete_member(member_id: str):

    result = members_collection.delete_one(
        {"member_id": member_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return {
        "message": "Member deleted successfully"
    }