import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

from app.schema import BillExtractResult
from app.extractor import extract_bill
from app.file_parser import parse_file

load_dotenv()

app = FastAPI(title="Bill Extraction Service", version="1.0.0")

_groq_client: Groq | None = None


def get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")
        _groq_client = Groq(api_key=api_key)
    return _groq_client


class TextRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract/text", response_model=BillExtractResult)
def extract_from_text(body: TextRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")
    client = get_groq_client()
    return extract_bill(client, body.text)


@app.post("/extract/file", response_model=BillExtractResult)
async def extract_from_file(file: UploadFile = File(...)):
    allowed_types = {"application/pdf", "image/png", "image/jpeg", "image/webp", "image/tiff"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    try:
        text = parse_file(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from file")

    client = get_groq_client()
    return extract_bill(client, text)
