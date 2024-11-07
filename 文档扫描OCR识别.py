import cv2
from unit import cv_show, resize, four_point_transform


image = cv2.imread('img/page.jpg')
ratio = image.shape[0] / 500.0
orig = image.copy()
image = resize(image, height=500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度图
gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯滤波
edged = cv2.Canny(gray, 75, 200)  # 边缘检测
# cv_show('gray', edged)

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:3]  # 对轮廓面积排序，取最大的

for c in cnts:
    peri = cv2.arcLength(c, True)  # 计算轮廓周长(True表示轮廓是闭合的)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # 多边形逼近(0.02 * peri越小，逼近的轮廓与原始轮廓越接近)

    if len(approx) == 4:  # 当轮廓被判断为四边形时, 那么！
        screenCnt = approx
        break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
# cv_show('image', image)

warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)  # 透视变换 (去对应函数里有详细讲解)
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)  # 灰度图
# cv_show('warped', warped)
ref = cv2.threshold(warped, 155, 255, cv2.THRESH_BINARY)[1]  # 二值化
cv2.imwrite('scan.jpg', ref)

# cv_show('orig', orig)  # 对比一下看看
# cv_show('ref', ref)
