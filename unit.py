import cv2
import numpy as np


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)  # 每个点的坐标和 x + y
    rect[0] = pts[np.argmin(s)]  # 返回和最小的点，即左上角的点
    rect[2] = pts[np.argmax(s)]  # 返回和最大的点，即右下角的点

    diff = np.diff(pts, axis=1)  # 每个点的坐标差值 y - x
    rect[1] = pts[np.argmin(diff)]  # 差值最小的点，即右上角的点
    rect[3] = pts[np.argmax(diff)]  # 差值最大的点，即左下角的点

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (top_left, top_right, bottom_right, bottom_left) = rect  # 找到四个坐标点(左上, 右上, 右下, 左下)

    widthA = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))  # 下边长
    widthB = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))  # 上边长
    maxWidth = max(int(widthA), int(widthB))  # 取最大边长( 宽 )

    heightA = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))  # 右边长
    heightB = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))  # 左边长
    maxHeight = max(int(heightA), int(heightB))  # 取最大边长( 高 )

    dst = np.array([  # 变换后的新坐标
        [0, 0],  # 左上
        [maxWidth - 1, 0],  # 右上
        [maxWidth - 1, maxHeight - 1],  # 右下
        [0, maxHeight - 1]], dtype="float32")  # 左下

    M = cv2.getPerspectiveTransform(rect, dst)  # 透视变换矩阵(将不规则的四边形映射到3*3矩形中)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))  # 将四边形在矩阵中 "拉正" 为矩形
    # 可以理解成一个不规则的四边形放到一个三维空间里，然后在三维空间里给它拉正为规则的四边形(不严谨！！！只是帮助理解！！！)

    return warped
