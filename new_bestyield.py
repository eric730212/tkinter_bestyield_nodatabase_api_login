import cv2
import datetime
import os
import time
from PIL import Image, ImageTk
import threading
import serial
import win32api
import win32con
import serial.tools.list_ports
import requests
import json
import sys

import tkinter as tk
import tkinter.messagebox as messagebox

global cap
global COM_PORT

def resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):

        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


COM_PORT = ""
cap = cv2.VideoCapture(0)
tr = ""
T = ""
W = "重量"
b = 1
p = 1
path1 = os.path.dirname(os.path.realpath(__file__))
# path1 = "C:\\Users\\GOD\\Pictures\\"  # 指定資料夾存放位置
token = ""


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Bestyield")
        # self.iconbitmap('%s\\ref\\bestyield1.ico'%path1)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=resource_path('ref\\bestyield.png')))
        print("resource_path: ", resource_path('ref\\bestyield.png'))
        self.config(bg="LightSeaGreen")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):

    def __init__(self, master):
        def log_in():
            global token
            global COM_PORT
            name = nameE.get()
            password = addreddE.get()
            COM_PORT = "COM" + comE.get()
            print(COM_PORT)
            print(name, password)

            my_data = {"system": "ActApi",
                       "Username": name,
                       "Password": password
                       }

            Head = {'Content-Type': 'application/json'}
            x = requests.post('https://byteiotapi.bestyield.com/signin', headers=Head, data=json.dumps(my_data))
            print(x.status_code)
            if x.status_code == 200 and COM_PORT != "":
                loginlab.config(text="登入成功", fg="green")
                token = x.text
                master.switch_frame(PageOne)

            else:
                loginlab.config(text="登入失敗", fg="red")
            print("Token:", x.text)

        tk.Frame.__init__(self, master)

        msg = "歡迎進入 Bestyield 出貨系統"
        self.sseGif = tk.PhotoImage(file="%s\\ref\\bestyield.gif" % path1)
        logo = tk.Label(self, text=msg, image=self.sseGif, compound="bottom", font="Helvetic 10 bold")
        logo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        nameL = tk.Label(self, text="Account")
        nameL.grid(row=1)
        addressL = tk.Label(self, text="Password")
        addressL.grid(row=2)
        comL = tk.Label(self, text="COM")
        comL.grid(row=3)

        nameE = tk.Entry(self)
        addreddE = tk.Entry(self, show="*")
        comE = tk.Entry(self)
        nameE.grid(row=1, column=1)
        addreddE.grid(row=2, column=1, pady=10)
        comE.grid(row=3, column=1)

        nameE.focus()

        loginbtn = tk.Button(self, text="登入", command=log_in)
        loginbtn.grid(row=4, column=1)

        loginlab = tk.Label(self, text="未登入")
        loginlab.grid(row=4, column=0)


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg="LightSeaGreen")

        # tk.Frame.configure(self,bg='blue')

        def cameraShow():
            global cap
            # global logo
            ret, frame = cap.read()
            if p != 0:
                frame = cv2.flip(frame, 1)
                flipimg1 = cv2.cv2.flip(frame, -1)
                flipimg = cv2.cv2.flip(flipimg1, 1)
                cv2image = cv2.cvtColor(flipimg, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                logo.imgtk = imgtk
                logo.configure(image=imgtk)
                logo.after(10, cameraShow)

        def quit():
            global b
            b = 0
            self.quit()

        def tab():
            win32api.keybd_event(9, 0, 0, 0)
            win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
            # time.sleep(0.5)

        def bluetooth():
            global data1
            global COM_PORT
            try:
                """
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    print(p)
                    if "Comm Port" in p.description:
                        # COM_PORT = p.description[34:39]
                        COM_PORT = (p.description.split("(")[-1]).split(")")[0]
                        print("com port:", COM_PORT)
                """
                while (COM_PORT != ""):
                    # COM_PORT = 'COM4'
                    BAUD_RATES = 9600
                    ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=0.5)
                    print("++++++++++")
                    while ser.readline() != b'':
                        data_raw = ser.readline()
                        data = data_raw.decode()
                        data1 = data[6:14]
                        # print('接收到的資料：', data)
                        # print('丟到資料庫的:', data1)
                        weightLR.config(text=data1)

                    weightLR.config(text="重量")
                    messagebox.showerror("錯誤", "錯誤!  沒有偵測到藍芽接收器")
                    ser.close()
                    cv2.waitKey(1000)
                    bluetooth()
            except:
                weightLR.config(text="重量")
                messagebox.showerror("錯誤", "錯誤!  沒有偵測到藍芽接收器")
                # ser.close()
                cv2.waitKey(1000)
                bluetooth()

        def printInfo():
            global tr
            global path1
            global img
            global p
            global T
            global token
            tr = cartE.get()
            totalsnlist = []  # 將有輸入的序號儲存在List
            name_list = [sn1E, sn2E, sn3E, sn4E, sn5E, sn6E, sn7E, sn8E, sn9E, sn10E]
            for i in range(10):
                if name_list[i].get() != "":
                    totalsnlist.append(name_list[i].get())
            seen = set()
            duplicated = set()
            for x in totalsnlist:  # 確認S/N是否有重複或是空的
                if x not in seen:
                    seen.add(x)
                else:
                    duplicated.add(x)
            print(duplicated)
            if tr == "" or seen == set() or T == "上傳成功" or T == "" or T == "上傳失敗":
                print("Empty")
                messagebox.showerror("錯誤", "錯誤!  沒有輸入 Carton ID , S/N 或是 還沒有拍照")
            else:

                if duplicated != set():
                    messagebox.showerror("錯誤", "錯誤!  S/N: %s  重複" % duplicated)
                else:
                    print(tr)
                    # if os.path.isdir(path1 +"\\"+ time.strftime('%Y%m%d') + "\\" + tr):  # 如果沒有,新增今天的目錄
                    if os.path.isdir("%s\\%s\\%s" % (path1, time.strftime('%Y%m%d'), tr)):
                        pass
                    else:
                        os.makedirs("%s\\%s\\%s" % (path1, time.strftime('%Y%m%d'), tr))
                    global path
                    # path = path1 +"\\"+ time.strftime('%Y%m%d') + "\\"  # 定義成今天的資料夾
                    path = "%s\\%s\\%s" % (path1, time.strftime('%Y%m%d'), tr)
                    global person_list
                    person_list = os.listdir(path)
                    person_list.sort()
                    print(person_list)
                    if person_list == []:  # 取出照片編號,沒有的話預設1
                        person_num_latest = 1
                    else:
                        person_num_latest = int((str(person_list[-1]).split("_")[-1]).split(".")[0]) + 1
                    print("person_num_latest:", person_num_latest)
                    person_cnt = person_num_latest
                    print('person_cnt = ', person_cnt)
                    if person_cnt < 10:
                        # current_pic_dir = path + tr + "\\" + tr + "_0" + str(person_cnt)
                        current_pic_dir = path + "\\" + tr + "_0" + str(person_cnt)
                    else:
                        current_pic_dir = path + "\\" + tr + "_" + str(person_cnt)
                    img = cv2.imread("%s\\ref\\test3.png" % path1)
                    cv2.imwrite(current_pic_dir + ".png", img)  # 寫到今天/ s/n /的資料夾裡

                    my_files = {'file': open("%s.png" % current_pic_dir, 'rb')}

                    img = tk.PhotoImage(file="%s\\ref\\test3.png" % path1)
                    logo.config(image=img)
                    print("S/N: %s" % (cartE.get()))

                    my_data1 = {"snList": totalsnlist}
                    y = requests.post('https://byteiotapi.bestyield.com/api/Act18/%s/%s' % (tr, T[1:7]),  # 上傳
                                      headers={'Authorization': 'Bearer ' + token},
                                      files=my_files, data=my_data1)
                    print(y.status_code)
                    print(y.text)

                    if y.status_code == 204 or y.status_code == 201:  # 確認是否有上傳成功
                        # listlabel.insert("end",tr+"  \n"+T+"  \n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n-------------------------------------------------------")
                        listlabel.insert("end", tr)
                        listlabel.insert("end", T)
                        listlabel.insert("end", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        listlabel.insert("end", "-----------------------------------------------------------------")
                        scollbar.config(command=listlabel.yview)
                        print(y.text)
                        clear()  # 清空輸入欄位
                        T = "上傳成功"
                        weightLL.config(text=T, fg="green")
                        p = 1
                        cartE.focus()
                        # tab()         #讓游標回到S/N
                    else:
                        weightLL.config(text="上傳失敗", fg="red")
                        messagebox.showerror("錯誤", y.text)  # 上傳失敗的原因
                        # os.remove("%s.png"%current_pic_dir)

                    tr = ""
                    cameraShow()

        def clear():
            cartE.delete(0, tk.END)
            sn1E.delete(0, tk.END)
            sn2E.delete(0, tk.END)
            sn3E.delete(0, tk.END)
            sn4E.delete(0, tk.END)
            sn5E.delete(0, tk.END)
            sn6E.delete(0, tk.END)
            sn7E.delete(0, tk.END)
            sn8E.delete(0, tk.END)
            sn9E.delete(0, tk.END)
            sn10E.delete(0, tk.END)
            cartE.focus()

        def takepic():
            global img
            global T
            global p
            global data1
            ret, frame = cap.read()
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            flipimg1 = cv2.cv2.flip(frame, -1)
            flipimg = cv2.cv2.flip(flipimg1, 1)

            cv2.imwrite("%s\\ref\\test3.png" % path1, flipimg)
            img = tk.PhotoImage(file="%s\\ref\\test3.png" % path1)

            T = data1
            logo.config(image=img)
            weightLL.config(text=T, fg="black", font="Helvetic 20 bold")
            p = 0

        msg = "歡迎進入 Bestyield 出貨紀錄系統"
        # sseGif=tk.PhotoImage(file="C:\\Users\\GOD\\Pictures\\sse.gif")
        self.sseGif = tk.PhotoImage(file="%s\\ref\\20.png" % path1)
        logo = tk.Label(self, image=self.sseGif, text=msg, compound="bottom", font="Helvetic 20 bold",
                        bg="MediumVioletRed")
        logo.grid(row=0, column=0, columnspan=3, rowspan=11)

        cartL = tk.Label(self, text="Carton ID", font="Helvetic 20 bold", width=8)
        snL1 = tk.Label(self, text="S/N (1)", font="Helvetic 20 bold", width=8)
        snL2 = tk.Label(self, text="S/N (2)", font="Helvetic 20 bold", width=8)
        snL3 = tk.Label(self, text="S/N (3)", font="Helvetic 20 bold", width=8)
        snL4 = tk.Label(self, text="S/N (4)", font="Helvetic 20 bold", width=8)
        snL5 = tk.Label(self, text="S/N (5)", font="Helvetic 20 bold", width=8)
        snL6 = tk.Label(self, text="S/N (6)", font="Helvetic 20 bold", width=8)
        snL7 = tk.Label(self, text="S/N (7)", font="Helvetic 20 bold", width=8)
        snL8 = tk.Label(self, text="S/N (8)", font="Helvetic 20 bold", width=8)
        snL9 = tk.Label(self, text="S/N (9)", font="Helvetic 20 bold", width=8)
        snL10 = tk.Label(self, text="S/N (10)", font="Helvetic 20 bold", width=8)
        weightL = tk.Label(self, text="重量", font="Helvetic 20 bold", width=8)
        cartL.grid(row=0, column=4)
        snL1.grid(row=1, column=4)
        snL2.grid(row=2, column=4)
        snL3.grid(row=3, column=4)
        snL4.grid(row=4, column=4)
        snL5.grid(row=5, column=4)
        snL6.grid(row=6, column=4)
        snL7.grid(row=7, column=4)
        snL8.grid(row=8, column=4)
        snL9.grid(row=9, column=4)
        snL10.grid(row=10, column=4)
        weightL.grid(row=11, column=0)

        weightLR = tk.Label(self, text=W, font="Helvetic 40 bold", height=2)
        weightLR.grid(row=11, column=5, rowspan=2, sticky="N")

        cartE = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        cartE.focus()
        sn1E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn2E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn3E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn4E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn5E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn6E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn7E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn8E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn9E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        sn10E = tk.Entry(self, font="Helvetic 20 bold", width=23, justify="center")
        weightLL = tk.Label(self, text=T, width=20, font="Helvetic 20 bold")
        cartE.grid(row=0, column=5)

        cartE.bind("<Return>", (lambda event: tab()))
        sn1E.bind("<Return>", (lambda event: tab()))
        sn2E.bind("<Return>", (lambda event: tab()))
        sn3E.bind("<Return>", (lambda event: tab()))
        sn4E.bind("<Return>", (lambda event: tab()))
        sn5E.bind("<Return>", (lambda event: tab()))
        sn6E.bind("<Return>", (lambda event: tab()))
        sn7E.bind("<Return>", (lambda event: tab()))
        sn8E.bind("<Return>", (lambda event: tab()))
        sn9E.bind("<Return>", (lambda event: tab()))
        sn10E.bind("<Return>", (lambda event: tab()))

        sn1E.grid(row=1, column=5)
        sn2E.grid(row=2, column=5)
        sn3E.grid(row=3, column=5)
        sn4E.grid(row=4, column=5)
        sn5E.grid(row=5, column=5)
        sn6E.grid(row=6, column=5)
        sn7E.grid(row=7, column=5)
        sn8E.grid(row=8, column=5)
        sn9E.grid(row=9, column=5)
        sn10E.grid(row=10, column=5)
        weightLL.grid(row=11, column=1, padx=10, pady=10)

        scollbar = tk.Scrollbar(self)
        scollbar.grid(row=0, rowspan=13, column=10, sticky="n,s")
        listlabel = tk.Listbox(self, yscrollcommand=scollbar.set)
        listlabel.grid(row=0, rowspan=13, column=9, sticky="n,s")
        listlabel.config(width=30, font="Helvetic 15 bold")

        uploadbtn = tk.Button(self, text="上傳", command=printInfo, cursor="hand2", bg="black", fg="MediumVioletRed",
                              font="Helvetic 20 bold")
        quitbtn = tk.Button(self, text="Quit", command=quit, cursor="hand2", bg="black", fg="white",
                            font="Helvetic 20 bold")
        picbtn = tk.Button(self, text="拍照", command=takepic, cursor="hand2", bg="black", fg="white",
                           font="Helvetic 20 bold")
        clearbtn = tk.Button(self, text="清除", command=clear, cursor="hand2", bg="black", fg="white",
                             font="Helvetic 20 bold")

        quitbtn.grid(row=12, column=2)
        uploadbtn.grid(row=12, column=1)
        picbtn.grid(row=12, column=0)
        clearbtn.grid(row=11, column=4)

        # accountE.insert(0,"GOD")
        # passwordE.insert(0,"pwd")

        c = threading.Thread(target=cameraShow)
        c.daemon = True
        c.start()

        t = threading.Thread(target=bluetooth)
        t.daemon = True
        t.start()

        # root.mainloop()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
