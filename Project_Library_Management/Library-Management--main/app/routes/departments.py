from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.department import Department

router = APIRouter(tags=["Departments"])

departments_collection = db["Departments"]


@router.post("/departments")
def create_department(department: Department):
    existing = departments_collection.find_one(
        {"department_id": department.department_id}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    departments_collection.insert_one(department.model_dump())

    return {
        "message": "Department created successfully"
    }


@router.get("/departments")
def get_departments():
    departments = []

    for department in departments_collection.find():
        department["_id"] = str(department["_id"])
        departments.append(department)

    return departments


@router.get("/departments/{department_id}")
def get_department(department_id: str):
    department = departments_collection.find_one(
        {"department_id": department_id}
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    department["_id"] = str(department["_id"])

    return department


@router.put("/departments/{department_id}")
def update_department(
    department_id: str,
    department: Department
):
    result = departments_collection.update_one(
        {"department_id": department_id},
        {"$set": department.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return {
        "message": "Department updated successfully"
    }


@router.delete("/departments/{department_id}")
def delete_department(department_id: str):
    result = departments_collection.delete_one(
        {"department_id": department_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return {
        "message": "Department deleted successfully"
    }


@router.delete("/departments/drop/all")
def drop_departments_collection():
    departments_collection.drop()

    return {
        "message": "Departments collection dropped successfully"
    }