import cv2
import time
from PIL import Image , ImageFont,ImageDraw,ImageTk


# img = Image.open('/ref/test3.png')    # 開啟圖片
# font = ImageFont.truetype('Teko-Regular.ttf', 100)   # 設定字型
# draw = ImageDraw.Draw(img)     # 準備在圖片上繪圖
# draw.text((0,0), 'OXXO.STUDIO', fill=(255,255,255), font=font)  # 將文字畫入圖片
# img.save('/ref/ok.jpg')     # 儲存圖片
#




cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    flipimg1 = cv2.flip(frame, -1)
    flipimg = cv2.flip(flipimg1, 1)

    cv2.putText(flipimg1, "AR22001537", (10, 30), cv2.FONT_HERSHEY_PLAIN,
                2, (205, 0, 0), 2, cv2.LINE_AA)
    time_text = time.strftime("%Y-%m-%d %I:%M:%S %p")
    cv2.putText(flipimg1, time_text, (200, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 215, 255), 1, cv2.LINE_AA)
    cv2.imshow("webcam",flipimg1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()