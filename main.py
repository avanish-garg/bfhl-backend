from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import base64
import imghdr
import mimetypes
import math

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # for dev: allow all; later you can restrict to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, OPTIONS, etc
    allow_headers=["*"],            # Accept all headers
)

class InputModel(BaseModel):
    data: List[str]
    file_b64: Optional[str] = None

@app.get("/bfhl")
def get_operation_code():
    return {"operation_code": 1}

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

@app.post("/bfhl")
def process_data(input_data: InputModel):
    numbers = [i for i in input_data.data if i.isdigit()]
    alphabets = [i for i in input_data.data if i.isalpha()]
    lowercase = [i for i in alphabets if i.islower()]
    highest_lowercase = [max(lowercase)] if lowercase else []

    prime_found = any(is_prime(int(i)) for i in numbers)

    file_valid = False
    file_mime_type = ""
    file_size_kb = ""

    if input_data.file_b64:
        try:
            file_bytes = base64.b64decode(input_data.file_b64)
            file_valid = True
            ext = imghdr.what(None, file_bytes)
            file_mime_type = mimetypes.guess_type(f"file.{ext}")[0] or "application/octet-stream"
            file_size_kb = round(len(file_bytes) / 1024)
        except:
            file_valid = False

    return {
        "is_success": True,
        "user_id": "your_fullname_ddmmyyyy",
        "email": "your_email@college.com",
        "roll_number": "YOUR_ROLL_NO",
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": highest_lowercase,
        "is_prime_found": prime_found,
        "file_valid": file_valid,
        "file_mime_type": file_mime_type,
        "file_size_kb": file_size_kb
    }
