cd 명령로 hwp-converter-mac 폴더 안으로 들어가서 도커 이미지 hwp_converter이라는 이름으로 빌드한 다음에 docker run -dit --name hwp_converter -v "$PWD":/workspace hwp_converter로 로컬 환경과 도커환경 동기화 하고
main.py에 자기가 원하는 hwp 폴더 경로 놓고 바꾸면 됌
