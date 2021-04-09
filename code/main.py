import cv2 as cv
import numpy as np
import serial
import time
from binascii import unhexlify
from crcmod import mkCrcFun

import picture_process
import control


camera=cv.VideoCapture(2)
ROI_rect = (150,0,640-150,480)

lower_green = np.array([35, 45, 0])
upper_green = np.array([100, 255, 255])

# control.coordinate_write(0, 100, -320)
# control.coordinate_write(0, 100, -380)
# control.coordinate_write(0, 100, -320)
# control.coordinate_write(0, -100, -320)
# control.coordinate_write(0, -100, -380)
# control.coordinate_write(0, 0, -320)
# control.coordinate_read()

P1 = [0, 100, -320, 90, 6, 1]
P2 = [0, 100, -380, 90, 6, 1]
P3 = [0, 100, -320, 90, 6, 1]
P4 = [0, -100, -320, 0, 6, 1]
P5 = [0, -100, -380, 0, 6, 1]
P6 = [0, -100, -320, 0, 6, 0]
P7 = [0,    0, -320, 0, 6, 0]
control.coordinate_write_seven(P1,P2,P3,P4,P5,P6,P7)

def main():

    while(True):
        ret ,img = camera.read()
        # img = cv.resize(img, (480,360))
        img_ROI = img[ROI_rect[1]:ROI_rect[1]+ROI_rect[3],ROI_rect[0]:ROI_rect[2]]
        cv.line(img,(145,0),(145,480),(0,255,255),thickness=2)  #画线
        cv.line(img,(640-145,0),(640-145,480),(0,255,255),thickness=2)

        img_hsv = cv.cvtColor(img_ROI, cv.COLOR_BGR2HSV) # 将图片转为灰度图
        img_mask = cv.inRange(img_hsv, lower_green, upper_green) # 限定范围，转为二值化图片，这里只保留绿色分量
        img_bin = cvbitwise_not(img_mask) #将图片反转，这里只保留除绿色的其他分量

        img_bin = cv.GaussianBlur(img_bin,(5,5),0) #高斯模糊
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(7, 7)) #设置形态学运算所需要的卷积核
        img_bin = cv.erode(img_bin,kernel)          #腐蚀图像
        img_bin = cv.dilate(img_bin,kernel)        #膨胀图像

        contours_list = picture_process.find_contours(img_ROI,img_bin)

        cv.imshow("camera", img)
        cv.imshow("img_bin", img_bin)
        cv.imshow("img_ROI", img_ROI)

        if(cv.waitKey(1)==27):   #按下Esc键关闭窗口
            break
    camera.release()
