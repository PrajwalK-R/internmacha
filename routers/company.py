from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.database import companies_collection
from routers.utils import get_password_hash
from starlette.status import HTTP_302_FOUND
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates/web/")
upload_folder = Path("uploads/company_logos")
os.makedirs(upload_folder, exist_ok=True)

@router.get("/company_signup", response_class=HTMLResponse)
async def get_company_signup(request: Request):
    return templates.TemplateResponse("company_signup.html", {"request": request})

@router.post("/company_signup")
async def post_company_signup(
    request: Request,
    company_name: str = Form(...),
    industry: str = Form(...),
    location: str = Form(...),
    company_size: int = Form(...),
    website: str = Form(...),
    contact_email: str = Form(...),
    contact_number: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    company_logo: UploadFile = File(...)
):
    if password != confirm_password:
        return templates.TemplateResponse("company_signup.html", {"request": request, "error": "Passwords do not match"})

    hashed_password = get_password_hash(password)

    # Create a unique logo filename
    logo_filename = f"{contact_email}_logo.jpg"
    logo_path = os.path.join(upload_folder, logo_filename)

    # Save the logo file
    with open(logo_path, "wb") as f:
        shutil.copyfileobj(company_logo.file, f)

    company_data = {
        "company_name": company_name,
        "industry": industry,
        "location": location,
        "website": website,
        "contact_email": contact_email,
        "contact_number": contact_number,
        "password": hashed_password,
        "company_logo": str(logo_path)
    }

    # Insert the company data into the database
    result = await companies_collection.insert_one(company_data)
    if result.inserted_id:
        return RedirectResponse("/login", status_code=HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("company_signup.html", {"request": request, "error": "Failed to register company"})

@router.get("/company", response_class=HTMLResponse)
async def get_company_page(request: Request):
    return templates.TemplateResponse("company.html", {"request": request})
