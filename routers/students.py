from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.database import students_collection
from routers.utils import get_password_hash
from starlette.status import HTTP_302_FOUND, HTTP_400_BAD_REQUEST
from fastapi.templating import Jinja2Templates
from bson.objectid import ObjectId
import os
import re

router = APIRouter()
templates = Jinja2Templates(directory="templates/web/")

upload_folder = "uploads/profile_photos"
os.makedirs(upload_folder, exist_ok=True)

# Helper function to validate email
def validate_email(email: str) -> bool:
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None

# Helper function to validate contact number
def validate_contact_number(contact_number: str) -> bool:
    return (
        contact_number.isdigit() and
        len(contact_number) == 10 and
        contact_number[0] in {'9', '6', '7', '8'}
    )

@router.get("/student_signup", response_class=HTMLResponse)
async def get_student_signup(request: Request):
    return templates.TemplateResponse("student_signup.html", {"request": request})

@router.post("/student_signup")
async def post_student_signup(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    college_name: str = Form(...),
    semester: int = Form(...),
    passing_year: int = Form(...),
    cgpa: float = Form(...),
    branch: str = Form(...),
    contact_number: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    state: str = Form(...),
    nation: str = Form(...),
    profile_photo: UploadFile = File(...),
):
    # Validate passwords
    if password != confirm_password:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    # Validate email
    if not validate_email(email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid email format")

    # Validate contact number
    if not validate_contact_number(contact_number):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid contact number")

    # Validate CGPA
    if not (0.0 <= cgpa <= 10.0):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="CGPA must be between 0.0 and 10.0")

    # Hash the password
    hashed_password = get_password_hash(password)

    # Save profile photo
    photo_path = os.path.join(upload_folder, f"{email}_profile_photo.jpg")
    with open(photo_path, "wb") as f:
        f.write(await profile_photo.read())

    # Insert student data into the database
    student = {
        "first_name": first_name,
        "last_name": last_name,
        "college_name": college_name,
        "semester": semester,
        "passing_year": passing_year,
        "cgpa": cgpa,
        "branch": branch,
        "contact_number": contact_number,
        "email": email,
        "password": hashed_password,
        "state": state,
        "nation": nation,
        "profile_photo_path": photo_path,
    }

    result = await students_collection.insert_one(student)
    student_id = result.inserted_id

    # Redirect to profile page after successful registration
    return RedirectResponse(f"/stdprofile/{student_id}", status_code=HTTP_302_FOUND)

@router.get("/student", response_class=HTMLResponse)
async def get_student(request: Request):
    return templates.TemplateResponse("student.html", {"request": request})

@router.get("/stdsettings", response_class=HTMLResponse)
async def get_stdsettings(request: Request):
    return templates.TemplateResponse("stdsettings.html", {"request": request})

@router.get("/stdprofile/{student_id}", response_class=HTMLResponse)
async def get_stdprofile(request: Request, student_id: str):
    # Fetch the student data from the database using student_id
    student = await students_collection.find_one({"_id": ObjectId(student_id)})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Pass the student data to the template
    return templates.TemplateResponse("student.html", {"request": request, "student": student})
