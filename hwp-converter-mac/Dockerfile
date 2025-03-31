FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-h2orestart \
    fonts-nanum fonts-unfonts-core \
    locales && \
    locale-gen ko_KR.UTF-8 && \
    update-locale LANG=ko_KR.UTF-8 && \
    fc-cache -fv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR:ko
ENV LC_ALL=ko_KR.UTF-8

WORKDIR /workspace

# 지속 실행 유지
ENTRYPOINT ["/bin/bash", "-c", "while true; do sleep 30; done;"]


