# -*- coding: utf-8 -*-
"""实践任务4：把两个任务的原图/中间结果/最终结果整合成Word，并转PDF(学号姓名-4.pdf)"""
import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

STUDENT = "2025210515 ZHUJIAHE"
BASE = os.path.dirname(os.path.abspath(__file__))

doc = Document()

def fig(path, caption, width_in):
    cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.add_run(caption).bold = True; cap.runs[0].font.size = Pt(11)
    pic = doc.add_paragraph(); pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.add_run().add_picture(os.path.join(BASE, path), width=Inches(width_in))

def section(t):
    doc.add_heading(t, level=1)

t = doc.add_heading("实践任务4：二维码设计、生成与识别", level=0)
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph("学号姓名：" + STUDENT); p.runs[0].font.size = Pt(12)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ---------- 任务1 ----------
section("任务1  设计内容与logo，生成带logo二维码并识别")
doc.add_paragraph("原图：").runs[0].bold = True
fig("1a_my_logo.png", "图1-1  原图·自己设计的logo(蓝色圆徽标+姓名缩写ZJH)", 2.2)
doc.add_paragraph("中间结果：").runs[0].bold = True
fig("1b_qrcode_nologo.png", "图1-2  中间结果·生成的二维码(未加logo)", 2.6)
doc.add_paragraph("最终结果：").runs[0].bold = True
fig("1c_qrcode_with_logo.png", "图1-3  最终结果·嵌入自己logo的艺术二维码", 2.6)
doc.add_paragraph("识别结果：").runs[0].bold = True
fig("1d_qrcode_decoded.png", "图1-4  识别结果·正确解出二维码内容(底部)", 2.6)

# ---------- 任务2 ----------
section("任务2  含多个二维码图像的全部二维码识别")
doc.add_paragraph("原图：").runs[0].bold = True
fig("2a_multi_qrcodes.png", "图2-1  原图·含3个二维码的图像", 4.6)
doc.add_paragraph("最终结果：").runs[0].bold = True
fig("2b_multi_result.png", "图2-2  最终结果·全部二维码均被识别并显示内容", 4.6)

# ---------- 说明 ----------
doc.add_heading("说明", level=1)
note = doc.add_paragraph()
note.add_run("二维码内容：").bold = True
note.add_run(
    "任务1编码内容为“2025210515 朱嘉和 ZHUJIAHE”，logo为自己用OpenCV设计的圆形“ZJH”徽标。"
    "生成时采用 qrcode（ERROR_CORRECT_H 30%容错，保证嵌logo仍可读），并把logo以alpha透明方式叠加到中心。")
note2 = doc.add_paragraph()
note2.add_run("识别：").bold = True
note2.add_run(
    "使用 OpenCV 的 QRCodeDetector.detectAndDecodeMulti 解码——相较 pyzbar，它能正确处理中文内容。"
    "识别结果用绿色边框标注编号，并在图下方显示各二维码内容。")
note3 = doc.add_paragraph()
note3.add_run("图像：").bold = True
note3.add_run("文档内图像均为原始分辨率嵌入，未做压缩。")

doc.save("学号姓名-4.docx")
print("已生成 Word：学号姓名-4.docx")
