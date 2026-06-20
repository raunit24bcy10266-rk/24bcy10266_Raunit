from fastapi import FastAPI

# Import Routers
from app.routes.departments import router as department_router
from app.routes.members import router as member_router
from app.routes.books import router as book_router
from app.routes.librarians import router as librarian_router
from app.routes.library_cards import router as library_card_router
from app.routes.issues import router as issue_router
from app.routes.admin import router as admin_router
from app.routes.reports import router as reports_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title="Library Management System",
    description="Backend-only Library Management System using FastAPI and MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():
    return {
        "message": "Library Management System API Running Successfully"
    }

# Register Routers
app.include_router(department_router, tags=["Departments"])
app.include_router(member_router, tags=["Members"])
app.include_router(book_router, tags=["Books"])
app.include_router(librarian_router, tags=["Librarians"])
app.include_router(library_card_router, tags=["Library Cards"])
app.include_router(issue_router, tags=["Book Issues"])
app.include_router(admin_router, tags=["Admin"])
app.include_router(reports_router, tags=["Reports"])