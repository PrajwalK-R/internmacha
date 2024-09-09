from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the correct environment variable name
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize the MongoDB client
client = AsyncIOMotorClient(DATABASE_URL)

# Access the specific database
db = client.get_database("userdatabase")

# Define collections
students_collection = db.students
companies_collection = db.companies
