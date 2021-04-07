import cv2 as cv

camera=cv.VideoCapture(0)
ROI_rect = (100,100,200,200)

while(1):
    ret ,img = camera.read()
    # if(ret):
        # img = cv.resize(img, (480,360))
    # else:
        # break
    k=cv.waitKey(1)
    if(k==27):   #按下Esc键关闭窗口
        break
    # cv.rectangle(img, ROI_rect, (255,0,0),thickness=2) #画矩形框起来
    ROI_img = img[ROI_rect[1]:ROI_rect[1]+ROI_rect[3],ROI_rect[0]:ROI_rect[0]+ROI_rect[2]]
    Guassian_img = cv.GaussianBlur(ROI_img,(5,5),0)
    # cv.imshow("ROI_img", ROI_img)
    # cv.imshow("Guassian_img", Guassian_img)
    cv.imshow("camera", img)

camera.release()



