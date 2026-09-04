# -*- coding: utf-8 -*-
"""
任务2 步骤4：把5张图整合到 Word 文档，并调用 Word 转换为 PDF（学号姓名-2.pdf）
"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

STUDENT = "2025210515 ZHUJIAHE"

doc = Document()

# 标题
t = doc.add_heading("实践任务2：图像字符提取与水印叠加", level=0)
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph("学号姓名：" + STUDENT)
p.runs[0].font.size = Pt(12)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_figure(path, caption, width_in):
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.add_run(caption).bold = True
    cap.runs[0].font.size = Pt(11)
    pic = doc.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.add_run().add_picture(path, width=Inches(width_in))

# 1) 图像A
add_figure("A.png",
           "图1  图像A（从 homework1.png 提取的学号姓名拼音字符）", 6.0)

# 2) 灰度原图
add_figure("images/lena512.bmp",
           "图2  灰度原图像（lena512.bmp）", 4.0)

# 3) 叠加A的灰度图
add_figure("gray_overlay_A.png",
           "图3  叠加图像A的灰度图像（右上角）", 4.0)

# 4) 彩色原图
add_figure("images/peppers.png",
           "图4  彩色原图像（peppers.png）", 4.0)

# 5) 叠加A的彩色图
add_figure("color_overlay_A.png",
           "图5  叠加图像A的彩色图像（右上角）", 4.0)

doc.add_paragraph()

# 说明
note = doc.add_paragraph()
note.add_run("说明：").bold = True
note.add_run(
    "图1 中的图像A，是先从 homework1.png 中用连通域分析自动分割出各个字符，"
    "再按学号 2025210515、姓名拼音 ZHUJIAHE 的顺序拼接而成（数字一行、拼音一行，便于阅读）。"
    "图3、图5 是将图像A按原图宽度约38%缩放后，以半透明白色卡片形式叠加到原图右上角。"
    "文档中的图像均为原始分辨率嵌入，未做压缩。")

doc.save("学号姓名-2.docx")
print("已生成 Word：学号姓名-2.docx")
