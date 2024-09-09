from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.database import students_collection, companies_collection
from routers.utils import verify_password, sanitize_input
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

router = APIRouter()
templates = Jinja2Templates(directory="templates/web/")

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def post_login(request: Request, email: str = Form(...), password: str = Form(...)):
    email = sanitize_input(email)
    password = sanitize_input(password)
    
    student = await students_collection.find_one({"email": email})
    company = await companies_collection.find_one({"contact_email": email})
    
    if student and verify_password(password, student["password"]):
        student_id = str(student["_id"])  # Convert ObjectId to string for URL
        return RedirectResponse(f"/stdprofile/{student_id}", status_code=HTTP_302_FOUND)
    elif company and verify_password(password, company["password"]):
        company_id = str(company["_id"])  # Convert ObjectId to string for URL
        return RedirectResponse(f"/company/{company_id}", status_code=HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "message": "Incorrect email or password. Please try again."
        })
