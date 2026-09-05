# 无人机创新——视觉基础

### Fundamentals of Computer Vision 

哈尔滨工业大学（威海）于 2026 年春季学期面向大一本科生推出校级跨专业知识体系选修课程《无人机创新——具身智能基础》。该课程为首次开设，暂无公开配套学习资源，因此本仓库整理收录了课程的全部实验指导手册、实验源码、实验数据、过程与结果图像，可供后续选课同学参考使用。

The interdisciplinary elective course named Fundamentals of Computer Vision (Drone Innovation) was launched for freshmen at Harbin Institute of Technology at Weihai in the Spring 2026 semester. Since this curriculum is newly offered with no pre-existing official learning materials available, this repository collects the laboratory instructions, source code, experimental data, on-site and result images of this course for reference by future participants.

---

## 仓库内容 / Repository Contents

| 实践 | 主题 | 主要内容 | 目录 |
|------|------|---------|------|
| Prac1 | 图像滤镜实践与应用 | 基于摄像头实时滤镜；自行设计三种新滤镜并绑定按键切换 | `Prac1/` |
| Prac2 | 图像字符提取与水印叠加 | 连通域分割学号姓名拼音字符、生成图像并叠加到原图右上角 | `Prac2/` |
| Prac3 | 图像映射与透视变换 | 艺术作品映射到公交广告区；广告区提取与透视矫正 | `Prac3/` |
| Prac4 | 二维码设计、生成与识别 | 设计内容+Logo 生成艺术二维码；多二维码图批量识别 | `Prac4/` |

## 实践任务说明 / Experiment Descriptions

### 实践 1：图像滤镜设计（Image Filter Design）

- **任务**：运行例程 `02_Filter.py` 打开摄像头实时显示图像，已有 `Q/Esc` 退出、`C` Canny 边缘检测、`B` 高斯模糊、`P` 预览等模式；在此基础上自行设计三种效果明显、有趣的滤镜并新增对应按键切换。
- **自设计滤镜**：
  - `E` 浮雕 Emboss——`cv2.filter2D` 3×3 卷积核 + delta 偏移；
  - `K` 素描 Sketch——灰度→反色→高斯模糊→颜色减淡；
  - `M` 马赛克 Mosaic——缩小后最近邻放大形成像素方块。

### 实践 2：图像字符提取与水印叠加（Character Extraction & Watermarking）

- **任务**：从 `homework1.png`（0–9以及 A–Z 字符表）中提取学号与姓名拼音用到的字符，按顺序拼接生成图像 `A.png`（学号 + 姓名拼音）；将 `A` 缩放后分别叠加到一幅灰度图、一幅彩色图的右上角。
- **方法**：`connectedComponentsWithStats` 分隔字符、按行/列排序对应到 `0123456789/ABCDEFGHIJKLMN/OPQRSTUVWXYZ`；叠加采用半透明白色卡片水印。

### 实践 3：图像映射（Image Mapping / Perspective Transform）

- **任务**：例程 `ImgMapping1.py` 将艺术作品透视映射并贴到公交广告区；`ImgMapping2.py` 提取广告区并透视矫正成矩形。使用自行生成的图像完成同样任务。
- **方法**：`cv2.getPerspectiveTransform` 求四角透视矩阵 + `cv2.warpPerspective` + `cv2.fillPoly` 掩膜替换以及区域提取。

### 实践 4：二维码设计、生成与识别（QR Code Design, Generation & Recognition）

- **任务 1**：设计自己的二维码内容与自己的 Logo，用 `qrcode`（`ERROR_CORRECT_H`）生成带 Logo 的二维码，并识别出内容。
- **任务 2**：制作或寻找一张含 2 个及以上二维码的图像，识别并显示所有二维码内容。
- **方法**：生成用 `qrcode + PIL`；识别用 OpenCV `QRCodeDetector.detectAndDecodeMulti`可正确解出中文；绘制用 PIL + 微软雅黑字体。

- 本仓库由本人自行整理收录，内容仅供学习交流与后续选课参考；如有疏漏或错误，欢迎指正。
- 示例与实现尽可能贴近课程讲义，个别脚本（如二维码识别）为避免中文乱码已改用 OpenCV 解码器，已在脚本注释中说明。

---

> This repository is maintained by a student for study and reference only. All data and code are for educational purposes.
