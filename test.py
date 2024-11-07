import os
import cv2
from PIL import Image

from unit import cv_show, sort_contours, resize, four_point_transform
import pytesseract

image = cv2.imread('scan.jpg')
# cv_show('image', image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
gray = cv2.medianBlur(gray, 3)  # 中值滤波
# cv_show('gray', gray)
filename = '{}.png'.format(os.getpid())
cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
print(text)
os.remove(filename)
