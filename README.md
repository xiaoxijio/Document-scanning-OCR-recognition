# 文档扫描OCR识别

1、导入图片

![image](https://github.com/user-attachments/assets/44f3a28c-8dd4-42be-a3fd-863a8dc1bfb7)


2、转成灰度图 --> 高斯滤波 --> 边缘检测

![image](https://github.com/user-attachments/assets/f2fcea4c-4c11-492c-98c8-4ebb850fbd1d)


3、取出轮廓最大的（用多边形逼近，将其转为四边形）

![image](https://github.com/user-attachments/assets/2c1091d9-4d98-44d2-8c32-3ecd2083286e)


4、透视变换（将其拉伸至原图大小）--> 二值化

![image](https://github.com/user-attachments/assets/49ad570c-3188-473c-969e-82c808193247)


5、灰度处理 --> 中值滤波 --> tesseract识别

<img width="925" alt="09e560efa8af4ed0512f928bfd85d3b" src="https://github.com/user-attachments/assets/a75423a9-90c8-4064-85e8-6bcd7487a7c9">


tesseract下载

[Index of /tesseract](https://digi.bib.uni-mannheim.de/tesseract/)

配置环境变量 --> pip install pytesseract
