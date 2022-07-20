import tkinter

import cv2
import datetime
import os
import time
from PIL import Image, ImageTk, ImageFont, ImageDraw
import threading
import serial
import win32api
import win32con
import serial.tools.list_ports
import requests
import json
import sys

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

global cap
global COM_PORT
global WebCam
global A
global c_terminate
global t_terminate
global stop_precamerashow
global count
global auto_count
global auto_count_arr
global name
global password


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):

        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


name = ""
password = ""
WebCam = "10"
COM_PORT = ""
A = 0
c_terminate = 0
t_terminate = 0
stop_precamerashow = 0
count = 0
auto_count = 0
auto_count_arr = []
cap0 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap1 = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2 + cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(0)
tr = ""
T = ""
W = "重量"
b = 1
p = 1
path1 = os.path.dirname(os.path.realpath(__file__))
# path1 = "C:\1\Users\\GOD\\Pictures\\"  # 指定資料夾存放位置
token = ""


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Bestyield-V1.7.9")
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
            global name
            global password

            name = nameE.get()
            password = addreddE.get()
            COM_PORT = "COM" + comE.get()

            print(WebCam)
            print(COM_PORT)
            print(name, password)

            my_data = {"system": "WebActHp",
                       "Username": name,
                       "Password": password
                       }
            # my_data = {"system": "WebActHp",
            #            "Username": 'TST410',
            #            "Password": '0410'
            #            }

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
        self.sseGif = tk.PhotoImage(file=resource_path("ref\\bestyield.gif"))
        logo = tk.Label(self, text=msg, image=self.sseGif, compound="bottom", font="Helvetic 10 bold")
        logo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        nameL = tk.Label(self, text="Account")
        nameL.grid(row=1)
        addressL = tk.Label(self, text="Password")
        addressL.grid(row=2)
        comL = tk.Label(self, text="COM")
        comL.grid(row=3)
        # cameraSeclectL = tk.Label(self, text="Camera")
        # cameraSeclectL.grid(row=4)

        nameE = tk.Entry(self)
        addreddE = tk.Entry(self, show="*")
        # comE = tk.Entry(self)
        comE = ttk.Combobox(self, values=['1', '2', '3', '4', '5', '6', '7', '8', '9', ], state="readonly")
        nameE.grid(row=1, column=1)
        addreddE.grid(row=2, column=1, pady=10)
        comE.grid(row=3, column=1)
        comE.current(4)
        # cameraSecectE = tk.Entry(self)
        # cameraSeclectE = ttk.Combobox(self, values=['0', '1', '2'], state="readonly")
        # cameraSeclectE.grid(row=4, column=1, pady=10)
        # cameraSeclectE.current(0)

        nameE.focus()

        loginbtn = tk.Button(self, text="登入", command=log_in)
        loginbtn.grid(row=5, column=1)

        loginlab = tk.Label(self, text="未登入")
        loginlab.grid(row=5, column=0)


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.config(bg="LightSeaGreen")

        # tk.Frame.configure(self,bg='blue')

        def preCameraShow():
            global A
            global WebCam
            global cap0
            global cap1
            global cap2
            global stop_precamerashow

            while stop_precamerashow != 1:
                WebCam = cameraSeclectE.get()
                # print("webcam:", WebCam)
                # print('stop_precamerashow:', stop_precamerashow)
                if WebCam == "0":
                    # cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
                    ret, frame = cap0.read()
                    frame = cv2.flip(frame, 1)
                    flipimg1 = cv2.flip(frame, -1)
                    flipimg = cv2.flip(flipimg1, 1)
                    cv2image = cv2.cvtColor(flipimg, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image=img)
                    logo.imgtk = imgtk
                    logo.configure(image=imgtk)

                if WebCam == "1":
                    try:
                        ret, frame = cap1.read()
                        frame = cv2.flip(frame, 1)
                        flipimg1 = cv2.flip(frame, -1)
                        flipimg = cv2.flip(flipimg1, 1)
                        cv2image = cv2.cvtColor(flipimg, cv2.COLOR_BGR2RGBA)
                        img = Image.fromarray(cv2image)
                        imgtk = ImageTk.PhotoImage(image=img)
                        logo.imgtk = imgtk
                        logo.configure(image=imgtk)
                        # logo.after(10, cameraShow)
                    except:
                        logo.config(image=self.sseGif)
                if WebCam == "2":
                    try:
                        ret, frame = cap2.read()
                        frame = cv2.flip(frame, 1)
                        flipimg1 = cv2.flip(frame, -1)
                        flipimg = cv2.flip(flipimg1, 1)
                        cv2image = cv2.cvtColor(flipimg, cv2.COLOR_BGR2RGBA)
                        img = Image.fromarray(cv2image)
                        imgtk = ImageTk.PhotoImage(image=img)
                        logo.imgtk = imgtk
                        logo.configure(image=imgtk)
                        # logo.after(10, cameraShow)
                    except:
                        logo.config(image=self.sseGif)

                if stop_precamerashow == 1:
                    # d = threading.Thread(target=cameraShow)
                    # d.daemon = True
                    # d.start()
                    break

        def cameraShow():
            global cap
            global A
            global WebCam
            # global logo
            A = 1
            if WebCam == "0":
                ret, frame = cap0.read()
            if WebCam == "1":
                ret, frame = cap1.read()
            if WebCam == "2":
                ret, frame = cap2.read()

            if p != 0 and A != 0:
                frame = cv2.flip(frame, 1)
                flipimg1 = cv2.flip(frame, -1)
                flipimg = cv2.flip(flipimg1, 1)
                cv2image = cv2.cvtColor(flipimg, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                logo.imgtk = imgtk
                logo.configure(image=imgtk)
                logo.after(10, cameraShow)
                # print('webcom:', WebCam)
                # print('cameraShow()')
            else:
                print('else')
                pass

        def quit_bluetooth():
            global b
            global A
            global t_terminate
            global stop_precamerashow
            global ser
            try:
                A = 0
                b = 0
                t_terminate = 1
                print('t.join()')
                # t.join(t_terminate)
                stop_precamerashow = 1
                print('c.join()')
                c.join(stop_precamerashow)
                print('sys.exit()')
                ser.close()
                print(t_terminate)
                cap0.release()
                cap1.release()
                cap2.release()
                print('self.quit()')
                self.quit()
                print('app.destroy()')
                app.destroy()
            except:
                cap0.release()
                cap1.release()
                cap2.release()
                self.quit()
                app.destroy()

        def quit():
            global b
            global A
            global t_terminate
            global stop_precamerashow
            global ser
            try:
                A = 0
                b = 0
                t_terminate = 1
                print('t.join()')
                t.join(t_terminate)
                stop_precamerashow = 1
                print('c.join()')
                c.join(stop_precamerashow)
                print('ser.close()')
                ser.close()
                print(t_terminate)
                cap0.release()
                cap1.release()
                cap2.release()
                print('self.quit()')
                self.quit()
                print('app.destroy()')
                app.destroy()
            except:
                self.quit()
                app.destroy()

        def tab():
            win32api.keybd_event(9, 0, 0, 0)
            win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
            # time.sleep(0.5)

        def bluetooth():
            global data1
            global COM_PORT
            global t_terminate
            global ser
            print('bluetooth()com:', COM_PORT)
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

                while (True):
                    # COM_PORT = 'COM4'
                    BAUD_RATES = 9600
                    ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=1)
                    print("++++++++++")
                    print(ser.readline())
                    # while ser.readline() != b'' and t_terminate != 1:
                    while ser.isOpen() and t_terminate != 1:

                        data_raw = ser.readline()
                        data = data_raw.decode()
                        data1 = data[6:14].replace(" ", "")

                        # print('接收到的資料：', data)
                        # print('丟到資料庫的:', data1)
                        weightLR.config(text=data1)
                        # print('bluetooth()')
                        # print('whileloop1 t_terminate:', t_terminate)
                        # ser.close()
                        if t_terminate == 1:
                            print('t_termainal_break')
                            break

                    if t_terminate == 0:
                        weightLR.config(text="重量")
                        messagebox.showerror("錯誤", "錯誤!  沒有偵測到秤重機COM PORT")
                        # ser.close()
                        cv2.waitKey(1000)
                        print('bluetooth()outside')
                        bluetooth()
                    if t_terminate == 1:
                        # ser.close()
                        print('blooth()close')
                        break




            except:
                weightLR.config(text="重量")
                messagebox.showerror("錯誤", "錯誤!  沒有偵測到秤重機COM PORT, 程式關閉")
                # ser.close()
                cv2.waitKey(1000)
                # bluetooth()
                quit_bluetooth()

        def printInfo():
            global tr
            global path1
            global img
            global p
            global T
            global token
            global count
            global name
            global password
            tr = cartE.get()
            totalsnlist = []  # 將有輸入的序號儲存在List
            name_list = [sn1E, sn2E, sn3E, sn4E, sn5E, sn6E, sn7E, sn8E, sn9E, sn10E]
            for i in range(10):
                if name_list[i].get() != "":
                    # print('name_list[%d].get()'%i,name_list[i].get())
                    totalsnlist.append(name_list[i].get())
                    # print('sn%dE.get'%i,totalsnlist[i])
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
                    if os.path.isdir("%s\\%s" % ("C:\\HP_LOG\\PK2", time.strftime('%Y%m%d'))):
                        pass
                    else:
                        os.makedirs("%s\\%s" % ("C:\\HP_LOG\\PK2", time.strftime('%Y%m%d')))
                    # global path
                    # path = path1 +"\\"+ time.strftime('%Y%m%d') + "\\"  # 定義成今天的資料夾
                    path = "%s\\%s" % ("C:\\HP_LOG\\PK2", time.strftime('%Y%m%d'))
                    global person_list
                    person_list = os.listdir(path)
                    person_list.sort()
                    print('person_list', person_list)
                    # if person_list == []:  # 取出照片編號,沒有的話預設1
                    #     person_num_latest = 1
                    # else:
                    #     person_num_latest = int((str(person_list[-1]).split("_")[-1]).split(".")[0]) + 1
                    # print("person_num_latest:", person_num_latest)
                    # person_cnt = person_num_latest
                    # print('person_cnt = ', person_cnt)
                    # if person_cnt < 10:
                    #     # current_pic_dir = path + tr + "\\" + tr + "_0" + str(person_cnt)
                    #     current_pic_dir = path + "\\" + tr +"_PK_"+ time.strftime('%Y%m%d%H%M%S') + "_0" + str(person_cnt)
                    # else:
                    #     current_pic_dir = path + "\\" + tr +"_PK_"+ time.strftime('%Y%m%d%H%M%S') +  str(person_cnt)
                    img = cv2.imread(resource_path("ref\\test3.png"))
                    # cv2.imwrite(current_pic_dir + ".png", img)  # 寫到今天/ s/n /的資料夾裡
                    #
                    # my_files = {'file': open("%s.png" % current_pic_dir, 'rb')}
                    path_time = time.strftime('%Y%m%d%H%M%S')
                    if sn1E.get() != "" and sn2E.get() != "":
                        # print("sn2E.get():", sn2E.get())
                        cv2.imwrite(path + "\\" + tr + "_PK_" + path_time + ".png",
                                    img)  # 寫到今天/ s/n /的資料夾裡
                        my_files = {
                            'file': open(path + "\\" + tr + "_PK_" + path_time + '.png', 'rb')}
                        print('my_files_path:', path + "\\" + tr + "_PK_" + path_time + '.png')
                    else:
                        # print("sn2E.get():空白")
                        cv2.imwrite(path + "\\" + tr + '_' + sn1E.get() + "_PK_" + path_time + ".png",
                                    img)  # 寫到今天/ s/n /的資料夾裡
                        my_files = {
                            'file': open(path + "\\" + tr + '_' + sn1E.get() + "_PK_" + path_time + '.png', 'rb')}
                        print('my_files_path:', path + "\\" + tr + '_' + sn1E.get() + "_PK_" + path_time + '.png')
                    # cv2.imwrite("/ref/test4.png", img)

                    # my_files = {'file': open('ref\\test3.png', 'rb')}
                    img = tk.PhotoImage(file=resource_path("ref\\test3.png"))

                    logo.config(image=img)
                    print("S/N: %s" % (cartE.get()))

                    my_data1 = {"snList": totalsnlist}

                    y = requests.post(
                        'https://byteiotapi.bestyield.com/api/Act18/%s/%s' % (tr, T.replace(" ", "")[:-1]),  # 上傳
                        headers={'Authorization': 'Bearer ' + token},
                        files=my_files, data=my_data1)

                    print('y.status_code:', y.status_code)
                    print('y.text:', y.text)
                    print('T:', T.replace(" ", "")[:-1])

                    if y.status_code == 401:

                        print(name, password)

                        my_data = {"system": "WebActHp",
                                   "Username": name,
                                   "Password": password
                                   }
                        # my_data = {"system": "WebActHp",
                        #            "Username": 'ActApi',
                        #            "Password": 'Act2022'
                        #            }

                        Head = {'Content-Type': 'application/json'}
                        x = requests.post('https://byteiotapi.bestyield.com/signin', headers=Head,
                                          data=json.dumps(my_data))
                        print(x.status_code)
                        if x.status_code == 200 and COM_PORT != "":
                            token = x.text
                            y = requests.post(
                                'https://byteiotapi.bestyield.com/api/Act18/%s/%s' % (tr, T.replace(" ", "")[:-1]),
                                # 上傳
                                headers={'Authorization': 'Bearer ' + token},
                                files=my_files, data=my_data1)
                            print("重新登入", y.status_code)
                            print("重新登入", y.text)

                    if y.status_code == 204 or y.status_code == 201:  # 確認是否有上傳成功
                        # listlabel.insert("end",tr+"  \n"+T+"  \n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n-------------------------------------------------------")
                        count += 1
                        listlabel.insert(0, "-----------------------------------------------------------------")
                        listlabel.insert(0, "累計數量:", count)
                        listlabel.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        listlabel.insert(0, T)
                        listlabel.insert(0, tr)
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
                        messagebox.showerror("錯誤", y.text.split("{")[-1].split("}")[0])  # 上傳失敗的原因
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
            if cartE.get() != "" and sn1E.get() != "":
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                flipimg1 = cv2.flip(frame, -1)
                flipimg = cv2.flip(flipimg1, 1)

                # add text function
                cv2.putText(flipimg, cartE.get(), (10, 30), cv2.FONT_HERSHEY_PLAIN,
                            2, (205, 0, 0), 2, cv2.LINE_AA)
                str_entry = []
                if sn1E.get() != "":
                    str_entry.append(sn1E.get())
                if sn2E.get() != "":
                    str_entry.append(sn2E.get())
                if sn3E.get() != "":
                    str_entry.append(sn3E.get())
                if sn4E.get() != "":
                    str_entry.append(sn4E.get())
                if sn5E.get() != "":
                    str_entry.append(sn5E.get())
                if sn6E.get() != "":
                    str_entry.append(sn6E.get())
                if sn7E.get() != "":
                    str_entry.append(sn7E.get())
                if sn8E.get() != "":
                    str_entry.append(sn8E.get())
                if sn9E.get() != "":
                    str_entry.append(sn9E.get())
                if sn10E.get() != "":
                    str_entry.append(sn10E.get())

                print("str_entry:", str_entry)
                for i in range(len(str_entry)):
                    cv2.putText(flipimg, str_entry[i], (10, 30 + (i + 1) * 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (205, 0, 0), 2, cv2.LINE_AA)
                    if i == len(str_entry) - 1:
                        cv2.putText(flipimg, data1[:-1].replace(" ", "") + "(g)", (10, 30 + (i + 2) * 30),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2, (205, 0, 0), 2, cv2.LINE_AA)
                # time
                # time_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # cv2.putText(flipimg, time_text, (200, 450), cv2.FONT_HERSHEY_COMPLEX,
                #             1, (0, 215, 255), 1, cv2.LINE_AA)

                cv2.imwrite(resource_path("ref\\test3.png"), flipimg)
                img = tk.PhotoImage(file=resource_path("ref\\test3.png"))

                T = data1
                logo.config(image=img)
                weightLL.config(text=T, fg="black", font="Helvetic 20 bold")
                p = 0
            else:
                messagebox.showerror("錯誤","錯誤! 尚未輸入 Carton ID , SN !")

        def repic():
            global p
            global A
            global T
            try:
                if p == 1:
                    weightLL.config(text="", fg="black", font="Helvetic 20 bold")
                    T = ""
                    print('repic camerashow')
                    # cameraShow()
                else:
                    p = 1
                    weightLL.config(text="", fg="black", font="Helvetic 20 bold")
                    T = ""
                    print('repic camerashow')
                    cameraShow()
            except:
                print('repic error')
                pass

        def camerashow_thread():
            global WebCam
            global cap
            global cap0
            global cap1
            global cap2
            global stop_precamerashow
            global p

            stop_precamerashow = 1

            WebCam = cameraSeclectE.get()
            print("thread_webcam:", WebCam)
            if WebCam == "0":
                # cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
                cap = cap0
            if WebCam == "1":
                # cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
                cap = cap1
            if WebCam == "2":
                # cap = cv2.VideoCapture(2 + cv2.CAP_DSHOW)
                cap = cap2

            p = 1
            cameraShow()
            # c = threading.Thread(target=cameraShow)
            # c.daemon = True
            # c.start()

        def auto_takepic():
            global auto_count
            global data1
            global auto_count_arr
            global T
            global ser
            global cap
            global stop_precamerashow
            time.sleep(3)
            while ser.isOpen():
                while stop_precamerashow == 1:
                    while cartE.get()!="":
                        time.sleep(0.1)
                        if len(auto_count_arr) <= 10:
                            auto_count_arr.append(data1)
                            print("auto_count_arr<10:",auto_count_arr)
                        else:
                            auto_count_arr.pop(0)
                            auto_count_arr.append(data1)
                            print("auto_count_arr:", auto_count_arr)

                            for i in range(10):
                                if auto_count_arr[0] == auto_count_arr[i]:
                                    auto_count += 1
                                else:
                                    auto_count = 0

                            print("auto_count:", auto_count)

                            if auto_count == 10:
                                if auto_count_arr[0] == "0g" and T == "上傳成功":
                                    print("data1:", data1)
                                    time.sleep(3)
                                    weightLL.config(text="")

                                    auto_count = 0
                                    auto_count_arr = []
                                elif auto_count_arr[0] != "0g"  and cartE.get() != "" and sn1E.get() != "":
                                    repic()
                                    takepic()
                                    auto_count = 0
                                    auto_count_arr = []
                                    T = data1
                                auto_count = 0
                                auto_count_arr = []
                                print("T:",T)
                    # print("cartE="" T=:",T)
                    if T == "上傳成功":
                        if data1 == "0g":
                            T = ""
                            weightLL.config(text=T)

        msg = "歡迎進入 Bestyield 出貨紀錄系統"
        # sseGif=tk.PhotoImage(file="C:\\Users\\GOD\\Pictures\\sse.gif")
        self.sseGif = tk.PhotoImage(file=resource_path("ref\\20.png"))
        logo = tk.Label(self, image=self.sseGif, text=msg, compound="bottom", font="Helvetic 20 bold",
                        bg="MediumVioletRed")
        logo.grid(row=0, column=0, columnspan=3, rowspan=11)

        # piclogo = tk.Label(self, image=self.sseGif, text=msg, compound="bottom", font="Helvetic 20 bold",
        #                 bg="MediumVioletRed")
        # piclogo.grid(row=10, column=0, columnspan=3, rowspan=11)

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
        repicbtn = tk.Button(self, text="重拍", command=repic, cursor="hand2", bg="black", fg="white",
                             font="Helvetic 20 bold")

        quitbtn.grid(row=12, column=2)
        uploadbtn.grid(row=12, column=1)
        picbtn.grid(row=12, column=0)
        clearbtn.grid(row=11, column=4)
        repicbtn.grid(row=12, column=3)

        quitbtn.grid_forget()
        uploadbtn.grid_forget()
        picbtn.grid_forget()
        repicbtn.grid_forget()
        clearbtn.grid_forget()

        startbtn = tk.Button(self, text="開始", command=lambda: [camerashow_thread(), cameraSeclectE.grid_forget(),
                                                               cameraSeclectL.grid_forget(), startbtn.grid_forget(),
                                                               quitbtn.grid(row=12, column=2),
                                                               uploadbtn.grid(row=12, column=1),
                                                               picbtn.grid(row=12, column=0),
                                                               clearbtn.grid(row=11, column=4)
            , repicbtn.grid(row=12, column=3)],
                             cursor="hand2",
                             bg="black", fg="white",
                             font="Helvetic 20 bold")
        startbtn.grid(row=12, column=2)
        cameraSeclectL = tk.Label(self, text="Camera Select", font="Helvetic 20 bold", bg='red')
        cameraSeclectL.grid(row=12, column=0)
        cameraSeclectE = ttk.Combobox(self, values=["0", "1", "2"], state="readonly", font="Helvetic 20 bold")
        cameraSeclectE.grid(row=12, column=1)
        cameraSeclectE.current(0)
        # accountE.insert(0,"GOD")
        # passwordE.insert(0,"pwd")

        t = threading.Thread(target=bluetooth)
        t.daemon = True
        t.start()

        c = threading.Thread(target=preCameraShow)
        c.daemon = True
        c.start()

        auto = threading.Thread(target=auto_takepic)
        auto.daemon = True
        auto.start()

        # root.mainloop()
        app.protocol('WM_DELETE_WINDOW', quit)


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
