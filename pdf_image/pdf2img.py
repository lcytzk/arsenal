import io

import fitz
from PIL import Image


def pdf_to_images(pdf_path, image_folder):
    # 打开 PDF 文件
    print(pdf_path, image_folder)

    pdf_document = fitz.open(pdf_path)

    # 遍历每一页
    for page_number in range(pdf_document.page_count):
        # 获取页面
        page = pdf_document[page_number]

        # 获取页面的图像
        image_list = page.get_images(full=True)

        # 遍历每个图像
        for img_info in image_list:
            image_index = img_info[0]
            base_image = pdf_document.extract_image(image_index)
            image_bytes = base_image["image"]

            # 使用 Pillow 保存图像
            img = Image.open(io.BytesIO(image_bytes))
            print(page_number, image_index)
            rgb_im = img.convert('RGB')
            rgb_im.save(f"{image_folder}/page_{page_number + 1}.jpg")
            # img.save(f"{image_folder}/page_{page_number + 1}.png")

    # 关闭 PDF 文件
    pdf_document.close()

import os
import sys

pdf_file_path = sys.argv[1]
output_folder = pdf_file_path.split('.')[-2]

os.mkdir(output_folder)
pdf_to_images(pdf_file_path, output_folder)

