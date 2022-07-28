
import tkinter as tk
from tkinter import ttk, messagebox
import  numpy as np
import  os
import pickle, sqlite3
import cv2
from PIL import Image


def Thu_lap_du_lieu():
    def insertOrUpdate(id, name, age, gender):# 4 truong

        conn = sqlite3.connect('duydata.db') #ket noi sql

        query = "SELECT * FROM People WHERE ID=" + str(id)# truy van thong qua id

        cusror = conn.execute(query)# lay bang tu tren

        isRecordExit = 0 # kiem tra xem neu co trong data thi update = 1
        for row in cusror:# for tung hang tren bang
            isRecordExit = 1 # neu ton tai chuyen thanh = 1

        if (isRecordExit == 0):# neu chua co thi insert

            query = "INSERT INTO People(ID,Name,Age,Gender) VALUES(" + str(id) + " , " + str(name) + "," + str(
                age) + "," + str(gender) + ")"
        else:
            query = "UPDATE People SET Name= '" + str(name) + "' , Age= '" + str(age) + "', Gender= '" + str(
                gender) + "' Where ID = " + str(id)
        conn.execute(query)
        conn.commit()# thuc thi csdl va close
        conn.close()
        # insertOrUpdate(10,"ABC")

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')# load thu vien
    cap = cv2.VideoCapture(0)# mở camera
    #insert data
    id=id1.get()
    name="'"+name1.get()+"'"
    age=age1.get()
    gender="'"+gen1.get()+"'"
    insertOrUpdate(id,name,age,gender)
    so_anh = 0

    while (True):
        ret, frame = cap.read()#load hinh anh tu camare, ret tra ve gia tri true
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)# #chuyen mau anh thanh xam de nhan dien nhanh hon anh mau
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)#sau khi anh thu ve tu camare se ket hop voi thu vien face.xml cho ra khuon mat,1.3,5 lay nhung diem gan mat nhat
        for (x, y, w, h) in faces:#vong lap tao hinh vuong bao quanh mat nhan dien duoc
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,255), 2)# ve hinh theo truc toa do x ,y , w ,h, 2 do day

            if not os.path.exists('DATABASE'):#tao thu muc
                os.makedirs('DATABASE')
            so_anh += 1#tang anh
            cv2.imwrite('DATABASE/User.' + str(id) + '.' + str(so_anh) + '.jpg', gray[y:y + h, x:x + w])#ghi them anh tang dan, anh cắt theo hình vuông
        cv2.imshow('camera', frame)#ten hien thi
        cv2.waitKey(1)# hien thi k bi tat
        if (so_anh >= 100) :
            cap.release()
            messagebox.showinfo(title='Thông báo', message="Đã lấy dữ liệu xong!")
            cv2.destroyAllWindows()
            break
    edit_ButID.delete(0,"end")
    edit_ButStr.delete(0,"end")
    edit_ButAge.delete(0, "end")
    edit_ButGen.delete(0,"end")



def Huan_luyen():
    recognizer = cv2.face.LBPHFaceRecognizer_create()# thu vien train khuon mat
    path = 'DATABASE'# lay duong dan

    def getImagesWithId(path):
        immagePaths = [os.path.join(path, f) for f in os.listdir(path)]# lu duong dan,os truy cap toi duong dan,list dir truy cap toi tat ca file trong database
        #print(immagePaths)
        faces = [] #luu du lieu anh
        IDs = [] #luu list id trong data
        for immagePath in immagePaths:# for tat ca cac duong dan
            faceImg = Image.open(immagePath).convert('L')# dung thu vien image mo len va con covert L la grayscale
            faceNP = np.array(faceImg,'uint8')# su dung mang numpy de lay du lieu sang dang ma tran
            #print(faceNP)
            Id = int(immagePath.split('/')[-1].split('.')[1])# dung split cat layid cua pthu 1 sau dau / va dau .
            faces.append(faceNP)# them vao mang
            IDs.append(Id)#them vao mang
            cv2.imshow('camera', faceNP)
            cv2.waitKey(10)
            return faces, IDs # retrun lai

    faces, IDs = getImagesWithId(path)# luu hai bien lai
    recognizer.train(faces, np.array(IDs))# train du lieu anh la faces va id anh

    if not os.path.exists('recognizer'):# sau khi train xong se tra ve file dang yml va se giong voi khuon mat cua minh
        os.makedirs('recognizer')
    recognizer.save('recognizer/trainingData.yml')
    messagebox.showinfo(title='Thông báo', message="Đã huấn luyện xong!")
    cv2.destroyAllWindows()




def nhan_dien():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizer/trainingData.yml')# doc file yml

    def getProfile(id):# lay thong tin id
        conn = sqlite3.connect("duydata.db")
        query = "SELECT * FROM people WHERE ID =" + str(id) #select
        cusror = conn.execute(query)# thuc thi query
        profile = None # luu gia tri lay tu data ve
        for row in cusror:
            profile = row
        conn.close() # dong
        return profile
    # lay duoc thonng tin thong qua id
    cap = cv2.VideoCapture(0) # truy cap toi cam
    fontface = cv2.FONT_HERSHEY_SIMPLEX# font chu
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)#anh xam
        faces = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces:# ve hinh vuong tren khuon mat
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]# cat anh tren cam so sanh vs tap du lieu
            id, confidence = recognizer.predict(roi_gray)#nhan dien khuon mat dang hien tren cam va tra ve id va do chinh xac
            if confidence < 100:
                profile = getProfile(id)# neu id co trong profile thi in ra
                aa= "{:0.2f}".format(confidence)
                display_string = str(aa)
                if (profile != None):
                    cv2.putText(frame, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    print(aa)
                    cv2.putText(frame, "Name: " + str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                    cv2.putText(frame, "Age: " + str(profile[2]), (x + 18, y + h + 60), fontface, 1, (0, 255, 0), 2)
                    cv2.putText(frame, "Gender: " + str(profile[3]), (x + 10, y + h + 98), fontface, 1, (0, 255, 0), 2)

            else:
                cv2.putText(frame, "Khong Biet", (x + 10, y + h +30), fontface, 1, (0, 0, 255), 2)
        cv2.imshow('camera', frame)
        if (cv2.waitKey(1)) & 0xFF == ord('a'):
            break
    cv2.destroyAllWindows()



win = tk.Tk()

win.title("Login")
win.geometry('500x300')
win.configure(bg='#263D42')
label = ttk.Label(win,text="Hệ Thống Nhận Diện Khuôn Mặt",background="Blue",foreground="white",font=50)
label.grid(column =1, row =0)
label.place(x=110,y=20)


label1 = ttk.Label(win,text="Input Your ID:",background="#263D42",foreground="white")
label1.grid(column =0, row =2)
label1.place(y=80)

label2 = ttk.Label(win,text="Input Your Name:",background="#263D42",foreground="white")
label2.grid(column =0, row =3)
label2.place(y=110)

label3 = ttk.Label(win,text="Age:",background="#263D42",foreground="white")
label3.grid(column =0, row =4)
label3.place(y=140)

label4 = ttk.Label(win,text="Gender:",background="#263D42",foreground="white")
label4.grid(column =0, row =5)
label4.place(y=170)


id1 =tk.IntVar()
edit_ButID=ttk.Entry(win,textvariable=id1, width=50)
edit_ButID.grid(column =1, row =2)
edit_ButID.focus()
edit_ButID.place(x=110,y=80)

name1 =tk.StringVar()
edit_ButStr=ttk.Entry(win,textvariable=name1,width=50)
edit_ButStr.grid(column =1, row =3)
edit_ButStr.place(x=110,y=110)

age1 =tk.IntVar()
edit_ButAge=ttk.Entry(win,textvariable=age1, width=50)
edit_ButAge.grid(column =1, row =4)
edit_ButAge.focus()
edit_ButAge.place(x=110,y=140)

gen1 =tk.StringVar()
edit_ButGen=ttk.Entry(win,textvariable=gen1,width=50)
edit_ButGen.grid(column =1, row =5)
edit_ButGen.place(x=110,y=170)


btlaydulieu= ttk.Button(win, text ="Lấy Dữ Liệu", command=Thu_lap_du_lieu)
btlaydulieu.grid(column =0, row =4)

bttrain= ttk.Button(win, text ="Training", command=Huan_luyen)
bttrain.grid(column =1, row =4)

btnhandien= ttk.Button(win, text ="Nhận Diện", command=nhan_dien)
btnhandien.grid(column =2, row =4)
bttrain.place(x=200,y=220)
btnhandien.place(x=350,y=220)
btlaydulieu.place(x=50,y=220)
win.mainloop()

