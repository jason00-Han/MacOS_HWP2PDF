FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-h2orestart \
    fonts-nanum fonts-unfonts-core \
    locales python3 python3-pip && \
    locale-gen ko_KR.UTF-8 && \
    update-locale LANG=ko_KR.UTF-8 && \
    fc-cache -fv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR:ko
ENV LC_ALL=ko_KR.UTF-8

# 작업 디렉토리
WORKDIR /workspace

# FastAPI 서버 및 파일 포함
COPY . .

RUN pip3 install --break-system-packages fastapi uvicorn python-multipart

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

