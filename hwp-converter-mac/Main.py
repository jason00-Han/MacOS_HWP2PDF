from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import subprocess
import uuid

app = FastAPI()

UPLOAD_DIR = "/workspace/Hwp_Folder"
OUTPUT_DIR = "/workspace/PDF_Folder"

@app.post("/convert/")
async def convert_hwp(file: UploadFile = File(...)):

    temp_filename = f"{uuid.uuid4().hex}.hwp"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)

    output_pdf_path = os.path.join(OUTPUT_DIR, temp_filename.replace('.hwp', '.pdf'))

    max_len = 100
    base_name, ext = os.path.splitext(file.filename)
    safe_filename = base_name[:max_len] + '.pdf'

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", file_path, "--outdir", OUTPUT_DIR
    ], capture_output=True, encoding='utf-8')

    if result.returncode != 0:
        return {"error": "PDF 변환 실패", "details": result.stderr}


    return FileResponse(
        output_pdf_path,
        media_type="application/pdf",
        filename=safe_filename
    )

