# -*- coding: utf-8 -*-
"""实践任务3：把两个任务的原图/中间结果/最终结果整合成Word，并转PDF(学号姓名-3.pdf)"""
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

def section(title):
    doc.add_heading(title, level=1)

# 标题
t = doc.add_heading("实践任务3：图像透视变换（图像映射）", level=0)
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph("学号姓名：" + STUDENT)
p.runs[0].font.size = Pt(12); p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ---------- 任务1 ----------
section("任务1  ImgMapping1：把艺术作品透视映射到公交车广告区")
p = doc.add_paragraph("原图：")
p.runs[0].bold = True
fig("myArt.jpg", "图1-1  原图·艺术作品（自己找的图像 myArt.jpg）", 3.2)
fig("myCar.jpg", "图1-2  原图·带梯形广告牌的公交车（自己找的图像 myCar.jpg）", 4.6)
doc.add_paragraph("中间结果：").runs[0].bold = True
fig("1_ExpandedArt.jpg", "图1-3  中间结果·扩展成公交车大小的艺术图", 4.6)
fig("1_WarpedArt.jpg", "图1-4  中间结果·透视变换后的艺术图（映射到广告区梯形形状）", 4.6)
doc.add_paragraph("最终结果：").runs[0].bold = True
fig("1_BusArt.jpg", "图1-5  最终结果·公交车广告区上贴上艺术图", 4.6)

# ---------- 任务2 ----------
section("任务2  ImgMapping2：提取公交广告区并透视矫正成矩形")
doc.add_paragraph("原图：").runs[0].bold = True
fig("myCar.jpg", "图2-1  原图·带广告区的公交车", 4.6)
doc.add_paragraph("中间结果：").runs[0].bold = True
fig("2_ExtractedAdImg.jpg", "图2-2  中间结果·提取出的广告区域（掩膜保留彩色）", 4.6)
doc.add_paragraph("最终结果：").runs[0].bold = True
fig("2_ADRectified.jpg", "图2-3  最终结果·透视矫正成规则矩形的广告图", 4.6)

# ---------- 说明 ----------
doc.add_heading("说明", level=1)
note = doc.add_paragraph()
note.add_run("原理：").bold = True
note.add_run(
    "两张素材均为自行生成。任务1用 cv2.getPerspectiveTransform 求“艺术图四角→广告区四角”"
    "的透视变换矩阵，再用 cv2.warpPerspective 把艺术图映射为广告区形状，最后用广告区掩膜"
    "(cv2.fillPoly+np.where) 替换到原图上。任务2反其道而行：先用掩膜提取广告区，再求"
    "“广告区四角→矩形四角”的透视矩阵，把梯形广告图矫正成规则矩形。")
note2 = doc.add_paragraph()
note2.add_run("图像：").bold = True
note2.add_run("文档内图像均为原始分辨率嵌入（脚本直接保存 jpg），未做压缩。")

doc.save("学号姓名-3.docx")
print("已生成 Word：学号姓名-3.docx")
