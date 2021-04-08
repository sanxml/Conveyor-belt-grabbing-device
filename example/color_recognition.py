import cv2 as cv
import numpy as np

camera=cv.VideoCapture(2)
ROI_rect = (150,0,640-150,480)
contours_min_area = 2000

lower_green = np.array([35, 45, 0])
upper_green = np.array([100, 255, 255])

def hsv_trackbar(img_hsv):
    '''通过调节滑动条，得到图片的hsv，输入需为hsv色彩空间的图片'''
    #定义滑动条回调函数，此处pass用作占位语句保持程序结构的完整性
    def nothing(x):
        pass
    #新建窗口
    cv.namedWindow('winName')
    #新建6个滑动条，表示颜色范围的上下边界，这里滑动条的初始化位置即为黄色的颜色范围
    cv.createTrackbar('LowerbH','winName',0,255,nothing)
    cv.createTrackbar('LowerbS','winName',0,255,nothing)
    cv.createTrackbar('LowerbV','winName',0,255,nothing)
    cv.createTrackbar('UpperbH','winName',255,255,nothing)
    cv.createTrackbar('UpperbS','winName',255,255,nothing)
    cv.createTrackbar('UpperbV','winName',255,255,nothing)
    while(1):
        #函数cv.getTrackbarPos()范围当前滑块对应的值
        lowerbH=cv.getTrackbarPos('LowerbH','winName')
        lowerbS=cv.getTrackbarPos('LowerbS','winName')
        lowerbV=cv.getTrackbarPos('LowerbV','winName')
        upperbH=cv.getTrackbarPos('UpperbH','winName')
        upperbS=cv.getTrackbarPos('UpperbS','winName')
        upperbV=cv.getTrackbarPos('UpperbV','winName')
        #得到目标颜色的二值图像，用作cv.bitwise_and()的掩模
        img_target=cv.inRange(img_hsv,(lowerbH,lowerbS,lowerbV),(upperbH,upperbS,upperbV))
        #输入图像与输入图像在掩模条件下按位与，得到掩模范围内的原图像
        img_specifiedColor=cv.bitwise_and(img_hsv,img_hsv,mask=img_target)
        cv.imshow('winName',img_specifiedColor)
        if cv.waitKey(1)==27:
            break
    cv.destroyAllWindows()

def find_contours(img, img_bin):
    '''
    查找面积大于某个值的所有轮廓，并在原图中画出每个轮廓的中点，返回为轮廓中点和面积的列表

    输入：img-原图片， img_bin-原图经过处理后的二值化图片

    返回：contours_list=[cX_1,cY_1,area1,cX_2,cY_2,area2...]

    '''
    contours,hierarchy = cv.findContours(img_bin.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours_list = []
    for index in range(len(contours)) :
        area = cv.contourArea(contours[index])
        if(area < contours_min_area):
            continue
        M = cv.moments(contours[index])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        contours_list.append(cX),contours_list.append(cY),contours_list.append(int(area))
        cv.circle(img, (cX, cY), 3, (0, 0, 255), -1)
        print("(" + str(cX) + "," + str(cY) + ",area=" + str(area) + ")    ", end="")
    print("")
    # print(contours_list)
    return contours_list

def color_recognition(img, point):
    pass

def main():
    while(True):
        ret ,img = camera.read()
        # img = cv.resize(img, (480,360))
        ROI_img = img[ROI_rect[1]:ROI_rect[1]+ROI_rect[3],ROI_rect[0]:ROI_rect[2]]
        cv.line(img,(145,0),(145,480),(0,255,255),thickness=2)  #画线
        cv.line(img,(640-145,0),(640-145,480),(0,255,255),thickness=2)

        hsv_img = cv.cvtColor(ROI_img, cv.COLOR_BGR2HSV) # 将图片转为灰度图

        # gray_img = cv.cvtColor(ROI_img, cv.COLOR_BGR2GRAY) # 将图片转为灰度图
        # ret, img_bin = cv.threshold(gray_img, 100, 255, cv.THRESH_BINARY) # 将灰度图转为二值化图片

        img_mask = cv.inRange(hsv_img, lower_green, upper_green) # 限定范围，转为二值化图片，这里只保留绿色分量
        img_bin = cv.bitwise_not(img_mask) #将图片反转，这里只保留除绿色的其他分量

        img_bin = cv.GaussianBlur(img_bin,(5,5),0) #高斯模糊
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(7, 7)) #设置形态学运算所需要的卷积核
        img_bin = cv.erode(img_bin,kernel)          #腐蚀图像
        img_bin = cv.dilate(img_bin,kernel)        #膨胀图像

        find_contours(ROI_img,img_bin)


        # cv.imshow("img",img)
        # cv.imshow("Guassian_img", Guassian_img)
        # cv.imshow("hsv_img", hsv_img)
        # cv.imshow("out_img", out_img)
        # cv.imshow("mask", img_mask)
        cv.imshow("img_bin", img_bin)
        cv.imshow("camera", ROI_img)


        if(cv.waitKey(1)==27):   #按下Esc键关闭窗口
            break
        elif(cv.waitKey(1)==ord('c')):
            cv.imwrite("hsv_img"+'.png',hsv_img)
    camera.release()

main()

# hsv_img = cv.imread('/run/media/sanxml/data/个人文件夹/浙海大/刘老师/刘老师项目/Conveyor-belt-grabbing-device/example/hsv_img.png')
# cv.imshow("hsv_img", hsv_img)
# hsv_trackbar(hsv_img)
# cv.waitKey(0)