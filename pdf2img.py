import os
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_to_png(pdf_path, output_folder):
    # 读取PDF文件
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    # 拆分每一页并转换为PNG
    for i in range(num_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        # 临时保存单页PDF
        temp_pdf_path = f"{output_folder}/temp_page.pdf"
        with open(temp_pdf_path, "wb") as f:
            writer.write(f)

        # 将单页PDF转换为PNG
        images = convert_from_path(temp_pdf_path, dpi=300,poppler_path="C:/Users/11707/Downloads/Release-24.02.0-0/poppler-24.02.0/Library/bin")
        for image in images:
            image.save(f"{output_folder}/{os.path.basename(pdf_path).replace('.pdf', '')}_page_{i+1}.png", 'PNG')

        # 删除临时PDF文件
        os.remove(temp_pdf_path)

# 设置PDF文件夹和输出文件夹
pdf_folder = 'Patents'
output_folder = 'Pictures'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中的所有PDF文件
for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file)
        split_pdf_to_png(pdf_path, output_folder)
        print(f"Processed {file}")
