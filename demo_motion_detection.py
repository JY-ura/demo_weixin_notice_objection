import cv2
import datetime
from demo_weixin_notice_objection import WxTools

camera=cv2.VideoCapture(0)
background = None
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,4))   #形态学膨胀
is_send_msg = False #防止重复发送
app_ID = 'wx8c6505f83a2b9810'
app_secret = '24b248d7c712ee034128b1fba70c9c24'

while True:
    _ , frame = camera.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   #转单通道
    gray_frame =cv2.GaussianBlur(gray_frame, (25,25), 3)    #高斯滤波 消除噪点 （灰度图，高斯分布的高斯核，sigma值）

    if background is None:
        background = gray_frame
        continue

    diff = cv2.absdiff(background, gray_frame)   #灰度图与背景的绝对值差
    diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]       #50：阈值   255：白色像素
    diff = cv2.dilate(diff, es, iterations=3)       #形态学膨胀

    #print(cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #拷贝，外部轮廓，连续

    is_detected = False
    for c in contours:
        if cv2.contourArea(c) < 2000:  #太小忽略
            continue
        (x,y,w,h) = cv2.boundingRect(c)  #获取边界
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        is_detected = True
        if not is_send_msg:
            is_send_msg = True
            wx_tools = WxTools(app_ID,app_secret)
            wx_tools.send_wx_customer_msg('oJz3l6FM6wdMvFi9FNBZGYEfl3bw')

    if is_detected:
        show_text = "motion: detected"
        show_color = (0,0,255)
    else:
        show_text = "motion: Detected"
        show_color = (0, 255, 0)


    cv2.putText(frame,show_text, (10,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, show_color, 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, show_color, 1)

    cv2.imshow('video', frame)
    #cv2.imshow('diff', gray_frame)
    cv2.imshow('diff', diff)


    key = cv2.waitKey(1) & 0xFFf
    if key ==ord('q'):
        break

camera.release()
cv2.destroyAllWindows()