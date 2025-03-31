from Convert import Hwp2Pdf_converter

converter = Hwp2Pdf_converter(
    container_name="hwp_converter",
    output_dir="/Users/hangyeongmin/PycharmProjects/PythonProject/hwp-converter-mac/PDF_Folder"
)

converter.convert_hwp_to_pdf(r'/Users/hangyeongmin/PycharmProjects/PythonProject/hwp-converter-mac/Hwp_Folder/2025년도 관광서비스 경쟁력 강화 사업 공모(안)_최종.hwp')