import cv2
import face_recognition
import pickle
import tkinter
from tkinter import messagebox, simpledialog
import os





def kaydet():

    isim = simpledialog.askstring("Yuz kaydetme", "Kaydetmek istediginiz yuzun ismini giriniz")

    if not isim:
        messagebox.showwarning("Uyari", "Herhangi bir isim girmediniz!")
        return

    messagebox.showinfo("Bilgi","Yuzunuzu kaydetmek icin 's' tusuna basiniz!")
    kayit = cv2.VideoCapture(0)
    while True:

        durum, kare = kayit.read()

        if durum:

            yuz_konumlari = face_recognition.face_locations(kare)

            if yuz_konumlari:

                for yuz_konumu in yuz_konumlari:

                    ust, sag, alt, sol = yuz_konumu

                    cv2.rectangle(kare, (sol, ust), (sag, alt), (0,255,0), 3)


            cv2.imshow("Yuz kaydetme", kare)

            # print("Yuzunuzu kaydetmek icin 's' tusuna basiniz!")
            

            if cv2.waitKey(1) & 0xff == ord("s"):

                if yuz_konumlari:

                    kaydedilecek_yuz_paketi = face_recognition.face_encodings(kare, yuz_konumlari)

                    with open(f"kaydedilen_yuzler\\{isim}.pkl", "wb") as dosya:

                        pickle.dump(kaydedilecek_yuz_paketi[0], dosya)

                        # print("yuzunuz basarili bir sekilde kaydedildi")
                        messagebox.showinfo("Bilgi", "yuzunuz basarili bir sekilde kaydedildi")

    kayit.release()
    cv2.destroyAllWindows()


def sil():

    isim = simpledialog.askstring("Yuz silme", "Silmek istediginiz yuzun ismini giriniz")

    if not isim: 
        messagebox.showwarning("Uyari", "Herhangi bir isim girmediniz!")
        return

    yuz_dosyasi_konumu = f"kaydedilen_yuzler\\{isim}.pkl"

    if os.path.exists(yuz_dosyasi_konumu):

        os.remove(yuz_dosyasi_konumu)

        messagebox.showinfo("Bilgi", "yuz dosyaniz basarili bir sekilde silindi!")
    
    else:

        messagebox.showwarning("Uyari", "Boyle bir dosya bulunmamaktadir!")


ana_pencere = tkinter.Tk()

ana_pencere.title("Yuz kaydetme sistemi")

ana_pencere.geometry("500x300")

tkinter.Label(ana_pencere, text="Yuz kaydetmek veya silmek icin secim yapiniz!").pack(pady=10)
tkinter.Button(ana_pencere, text="Yeni yuz kaydet", width=30, command=kaydet).pack(pady=10)
tkinter.Button(ana_pencere, text="Mevcut yuz sil", width=30, command=sil).pack(pady=10)

ana_pencere.mainloop()
