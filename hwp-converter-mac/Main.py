from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import subprocess

app = FastAPI()

UPLOAD_DIR = "/workspace/Hwp_Folder"
OUTPUT_DIR = "/workspace/PDF_Folder"

@app.post("/convert/")
async def convert_hwp(file: UploadFile = File(...)):
    # 1. 저장 경로 설정
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    pdf_name = file.filename.replace('.hwp', '.pdf')
    pdf_path = os.path.join(OUTPUT_DIR, pdf_name)

    # 2. 파일 저장
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 3. LibreOffice 실행
    result = subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", file_path, "--outdir", OUTPUT_DIR
    ], capture_output=True, encoding='utf-8')

    if result.returncode != 0:
        return {"error": "PDF 변환 실패", "details": result.stderr}

    # 4. 클라이언트에게 PDF 반환
    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_name)