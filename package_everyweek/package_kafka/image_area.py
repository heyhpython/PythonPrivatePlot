# coding=utf-8
# builtins
# third party package
import cv2
import numpy as np
# self built


def main():
    # 1.导入图片
    img_src = cv2.imread("./测试图片1.jpg")

    # 2.灰度化与二值化
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    ret, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # 3.连通域分析
    img_contour, *_ = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 4.轮廓面积打印
    img_contours = []
    for i in range(len(img_contour)):
        area = cv2.contourArea(img_contour[i])
        print("轮廓 %d 的面积是:%d" % (i, area))

        img_temp = np.zeros(img_src.shape, np.uint8)
        img_contours.append(img_temp)

        cv2.drawContours(img_contours[i], contours, i, (255, 255, 255), -1)
        cv2.imshow("%d" % i, img_contours[i])

    # 5.显示结果
    cv2.imshow("img_bin", img_bin)
    cv2.imshow("img_src", img_src)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    from PIL import Image