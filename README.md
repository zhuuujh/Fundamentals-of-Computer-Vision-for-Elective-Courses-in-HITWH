# 无人机创新——视觉基础

### Fundamentals of Computer Vision (Drone Innovation) · HITWH

哈尔滨工业大学（威海）于 2026 年春季学期面向大一本科生推出校级跨专业知识体系选修课程《无人机创新——视觉基础》。该课程为首次开设，暂无公开配套学习资源，因此本仓库整理收录了课程的全部实验指导手册、实验源码、实验数据、过程与结果图像以及实验汇报 PPT，可供后续选课同学参考使用。

The interdisciplinary elective course named Fundamentals of Computer Vision (Drone Innovation) was launched for freshmen at Harbin Institute of Technology, Weihai in the Spring 2026 semester. Since this curriculum is newly offered with no pre-existing official learning materials available, this repository collects the laboratory instructions, source code, experimental data, on-site and result images, and presentation slides of this course for reference by future participants.

---

## 课程简介 / About the Course

本课程以无人机视觉任务为背景，面向零基础学生系统讲解计算机视觉的基础概念与 OpenCV 常用操作，涵盖图像滤波、图像分割与字符提取、图像映射（透视变换）、二维码设计与识别等主题，让学生通过动手实践建立"从图像到信息"的完整认知。

This course is oriented around drone vision tasks and introduces computer vision fundamentals and common OpenCV operations to beginners with no prior experience. Topics include image filtering, image segmentation and character extraction, image mapping (perspective transformation), and QR code design & recognition, guiding students through hands-on practice to build a complete understanding from raw images to extracted information.

## 仓库内容 / Repository Contents

| 实践 | 主题 | 主要内容 | 目录 |
|------|------|---------|------|
| Prac1 | 图像滤镜设计 | 基于摄像头实时滤镜；自行设计三种新滤镜并绑定按键切换 | `Prac1/` |
| Prac2 | 图像字符提取与水印叠加 | 连通域分割学号姓名拼音字符、生成图像并叠加到原图右上角 | `Prac2/` |
| Prac3 | 图像映射（透视变换） | 艺术作品映射到公交广告区；广告区提取与透视矫正 | `Prac3/` |
| Prac4 | 二维码设计、生成与识别 | 设计内容+Logo 生成艺术二维码；多二维码图批量识别 | `Prac4/` |

## 实践任务说明 / Experiment Descriptions

### 实践 1：图像滤镜设计（Image Filter Design）

- **任务**：运行例程 `02_Filter.py` 打开摄像头实时显示图像，已有 `Q/Esc` 退出、`C` Canny 边缘检测、`B` 高斯模糊、`P` 预览等模式；在此基础上自行设计三种效果明显、有趣的滤镜并新增对应按键切换。
- **自设计滤镜**：
  - `E` 浮雕 Emboss——`cv2.filter2D` 3×3 卷积核 + delta 偏移；
  - `K` 素描 Sketch——灰度→反色→高斯模糊→颜色减淡（color dodge）；
  - `M` 马赛克 Mosaic——缩小后最近邻放大形成像素方块。
- **提交**：功能、实现方法、原图与滤波后对比，整理为 Word（`学号姓名-1.docx`）。

### 实践 2：图像字符提取与水印叠加（Character Extraction & Watermarking）

- **任务**：从 `homework1.png`（0–9、A–Z 字符表）中提取学号与姓名拼音用到的字符，按顺序拼接生成图像 `A.png`（学号 + 姓名拼音）；将 `A` 缩放后分别叠加到一幅灰度图、一幅彩色图的右上角。
- **方法**：`connectedComponentsWithStats` 分隔字符、按行/列排序对应到 `0123456789/ABCDEFGHIJKLMN/OPQRSTUVWXYZ`；叠加采用半透明白色卡片水印。
- **提交**：A 图、灰度原图、叠加灰度图、彩色原图、叠加彩色图合并为 Word 并导出 PDF（`学号姓名-2.pdf`）。

### 实践 3：图像映射（Image Mapping / Perspective Transform）

- **任务**：例程 `ImgMapping1.py` 将艺术作品透视映射并贴到公交广告区；`ImgMapping2.py` 提取广告区并透视矫正成矩形。使用自行找（自行生成）的图像完成同样任务。
- **方法**：`cv2.getPerspectiveTransform` 求四角透视矩阵 + `cv2.warpPerspective` + `cv2.fillPoly` 掩膜替换 / 区域提取。
- **提交**：两任务的原图、中间结果、最终结果图，合并为 Word 并导出 PDF（`学号姓名-3.pdf`）。

### 实践 4：二维码设计、生成与识别（QR Code Design, Generation & Recognition）

- **任务 1**：设计自己的二维码内容与自己的 Logo，用 `qrcode`（`ERROR_CORRECT_H`）生成带 Logo 的二维码，并识别出内容。
- **任务 2**：制作（或找）一张含 2 个及以上二维码的图像，识别并显示所有二维码内容。
- **方法**：生成用 `qrcode + PIL`；识别用 OpenCV `QRCodeDetector.detectAndDecodeMulti`（可正确解出中文）；绘制用 PIL + 微软雅黑字体。
- **提交**：两任务的原图、中间/最终结果图、识别结果图，合并为 Word 并导出 PDF（`学号姓名-4.pdf`）。

## 环境配置 / Environment

- Python 3.13
- opencv-python（含 `cv2.QRCodeDetector`）
- numpy
- matplotlib
- qrcode
- pyzbar（可选，示例使用；对中文有编码局限）
- python-docx + Microsoft Word（用于导出报告 PDF）

```bash
pip install opencv-python numpy matplotlib qrcode pyzbar python-docx
```

## 使用说明 / Usage

1. 每个实践目录内含任务文档（`实践任务N.docx`）、源码与数据/图像。
2. 直接运行对应脚本即可复现输出；摄像头类程序请允许访问摄像头。
3. 报告导出：用 `make_reportN.py` 生成 Word，再调用本机 Microsoft Word 导出 PDF。

## 提交规范 / Submission Notes

- 报告按 **`学号姓名-N`** 格式命名（如 `2025210515ZHUJIAHE-1.docx`），作为附件在 QQ 群作业提交。
- 报告中的图像请保持**原始分辨率嵌入，不压缩文件中的图像**（Word「文件 → 选项 → 高级」中取消勾选"压缩文件中的图像"）。

## 备注 / Remarks

- 本仓库由选课同学自行整理收录，内容仅供学习交流与后续选课参考；如有疏漏或错误，欢迎指正。
- 示例与实现尽可能贴近课程讲义，个别脚本（如二维码识别）为避免中文乱码已改用 OpenCV 解码器，已在脚本注释中说明。

---

> This repository is maintained by a student for study and reference only. All data and code are for educational purposes.
