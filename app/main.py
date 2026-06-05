import os

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from app.services.extractor import (
    extract_pdf_text,
    extract_docx_text
)

from app.services.groq_service import (
    analyze_contract
)

app = FastAPI(
    title="Contract Intelligence"
)

UPLOAD_DIR = "app/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@app.get("/")
def root():

    return {
        "message":
        "Contract Intelligence Running"
    }


@app.post("/upload")
async def upload_contract(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    if file.filename.endswith(".pdf"):

        text = extract_pdf_text(
            file_path
        )

    elif file.filename.endswith(".docx"):

        text = extract_docx_text(
            file_path
        )

    else:

        return {
            "error":
            "Only PDF and DOCX supported"
        }

    analysis = analyze_contract(
        text[:12000]
    )

    return {
        "filename":
        file.filename,
        "analysis":
        analysis
    }