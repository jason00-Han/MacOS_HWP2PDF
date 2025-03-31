import os
import subprocess

class Hwp2Pdf_converter:
    def __init__(self, container_name : str, output_dir: str):
        """
        param container_name: Docker 컨테이너 이름
        param output_dir: 변환된 PDF 파일을 저장할 로컬 경로
        """
        self.container_name = container_name
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def run_command(self, command: list[str]) -> bool:
        """
        :param command: 도커 내부에서 명령어를 실행하는 코드입니다.
        :return: 명령어 실행 결과 True, False 반환
        """
        result = subprocess.run(command, capture_output=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"오류 발생: {result.stderr}")
            return False
        print(f"명령어 실행 성공: {command}")
        return True

    def copy_to_container(self, hwp_file_path: str) -> bool:
        """
        로컬에 있는 .hwp 파일을 Docker 컨테이너로 복사하는 함수.
        :return run_command 명령어 실행
        :param 로컬에 있는 Hwp 파일 주소
        """
        file_name = os.path.basename(hwp_file_path)
        container_path = f"/workspace/Hwp_Folder/{file_name}"
        return self.run_command(["docker", "cp", hwp_file_path, f"{self.container_name}:{container_path}"])

    def convert_file_in_container(self, file_name: str) -> bool:
        """
        Docker 컨테이너 내에서 .hwp 파일을 .pdf로 변환합니다.
        """
        hwp_path = f"/workspace/Hwp_Folder/{file_name}"
        return self.run_command([
            "docker", "exec", self.container_name,
            "libreoffice", "--headless", "--convert-to", "pdf", hwp_path
        ])

    def copy_from_container(self, file_name: str) -> bool:
        """
        변환된 .pdf 파일을 Docker 컨테이너에서 로컬로 복사합니다.
        """
        pdf_name = file_name.replace('.hwp', '.pdf')
        container_path = f"/workspace/{pdf_name}"
        return self.run_command([
            "docker", "cp", f"{self.container_name}:{container_path}", self.output_dir
        ])

    def clean_up_container(self, file_name: str):
        """
        Docker 컨테이너 내에서 변환된 .pdf 파일을 삭제합니다.
        """
        pdf_name = file_name.replace('.hwp', '.pdf')
        self.run_command(["docker", "exec", self.container_name, "rm", f"/workspace/{pdf_name}"])

    def convert_hwp_to_pdf(self, hwp_file_path: str):
        """
        지정된 .hwp 파일을 .pdf로 변환하고 로컬로 저장합니다.
        """
        if not os.path.exists(hwp_file_path):
            raise FileNotFoundError(f"{hwp_file_path} 파일이 존재하지 않습니다.")

        file_name = os.path.basename(hwp_file_path)

        if not self.copy_to_container(hwp_file_path):
            return

        if not self.convert_file_in_container(file_name):
            return

        if not self.copy_from_container(file_name):
            return

        self.clean_up_container(file_name)

        print(f"\n변환 성공: {file_name} → {os.path.join(self.output_dir, file_name.replace('.hwp', '.pdf'))}")
