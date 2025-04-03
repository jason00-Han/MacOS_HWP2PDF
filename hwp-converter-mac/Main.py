from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import shutil
import subprocess
import re
from minio import Minio
from urllib.parse import quote, unquote

app = FastAPI()

UPLOAD_DIR = "/workspace/Hwp_Folder"
OUTPUT_DIR = "/workspace/PDF_Folder"
ENDPOINT = os.getenv("ENDPOINT_URL").replace("https://", "")
S3_BUCKET = "datahubtest1"

# MinIO 클라이언트 설정
minio_client = Minio(
    endpoint=ENDPOINT,
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    secure=True
)

def truncate_utf8(text, max_bytes):
    encoded = text.encode('utf-8')
    if len(encoded) <= max_bytes:
        return text
    while len(encoded) > max_bytes:
        text = text[:-1]
        encoded = text.encode('utf-8')
    return text

@app.post("/convert/")
async def convert_hwp(
    file: UploadFile = File(..., description="HWP 원본 파일"),
    site_name: str = Form(..., description="공고 사이트 명"),
    notice_uuid: str = Form(..., description="공고 UUID 값"),
    file_name : str = Form(..., description="파일 이름")
):
    clean_file_name = re.sub(r'[\\/:"*?<>|]', '_', file_name)
    # 파일명 안전히 생성 (UTF-8 byte 기준 자막기)
    base_name, _ = os.path.splitext(clean_file_name)
    safe_base = truncate_utf8(base_name, 150)
    hwp_filename = safe_base + ".hwp"
    pdf_filename = safe_base + ".pdf"

    # 파일 경로 설정
    file_path = os.path.join(UPLOAD_DIR, hwp_filename)
    output_pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    #  파일 저장
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    cmd = f'libreoffice --headless --convert-to pdf "{file_path}" --outdir "{OUTPUT_DIR}"'

    result = subprocess.run(cmd, shell=True, capture_output=True, encoding='utf-8')

    if result.returncode != 0:
        return {"error": "PDF 변환 실패", "details": result.stderr}

    #  S3 업로드 경로 (디코딩된 이름 사용)
    raw_object_key = f"{site_name}/{notice_uuid}/{pdf_filename}"
    s3_object_key = raw_object_key  # 인코딩 없이 저장에 사용

    try:
        minio_client.fput_object(
            bucket_name=S3_BUCKET,
            object_name=s3_object_key,
            file_path=output_pdf_path,
            content_type="application/pdf"
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "S3 업로드 실패", "details": str(e)})

    # URL만 인코딩 처리
    encoded_url_key = quote(s3_object_key)
    user_friendly_url = f"https://{ENDPOINT}/{S3_BUCKET}/{encoded_url_key}"

    # 업로드 성공 후 로컬 파일 삭제
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
    except Exception as e:
        # 파일 삭제 실패 로그 출력 (삭제 실패해도 동작은 계속)
        print(f"파일 삭제 실패: {str(e)}")

    return {
        "message": "PDF 변환 및 업로드 성공",
        "s3_bucket": S3_BUCKET,
        "s3_object_key": s3_object_key,  # 한글 포함된 원본 키 반환
        "s3_url": user_friendly_url       # URL은 인코딩됨
    }
