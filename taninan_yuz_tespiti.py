import face_recognition
import cv2
import os
import pickle
import tkinter

KAYITLI_YUZLERIN_OLDUGU_KLASOR = "kaydedilen_yuzler"

kayitli_yuzlerin_isim_listesi = []
kayitli_yuzlerin_paket_listesi = []

for dosya in os.listdir(KAYITLI_YUZLERIN_OLDUGU_KLASOR):

    if dosya.endswith(".pkl"):

        sadece_dosya_ismi = os.path.splitext(dosya)[0]

        with open(os.path.join(KAYITLI_YUZLERIN_OLDUGU_KLASOR, dosya), "rb") as d:

            yuz_paketi = pickle.load(d)
        
        kayitli_yuzlerin_isim_listesi.append(sadece_dosya_ismi)
        kayitli_yuzlerin_paket_listesi.append(yuz_paketi)


# print(kayitli_yuzlerin_paket_listesi)
# print(kayitli_yuzlerin_isim_listesi)


def yuzu_tanimaya_calis():
    kayit = cv2.VideoCapture(0)

    while True:

        durum, kare = kayit.read()

        if durum:

            yuz_konumlari = face_recognition.face_locations(kare)
            yuz_paketleri = face_recognition.face_encodings(kare, yuz_konumlari)


            for (ust, sag, alt, sol), yuz_paketi in zip(yuz_konumlari, yuz_paketleri):


                taninan_yuzun_ismi = "Bilinmeyen" 

                if kayitli_yuzlerin_paket_listesi:

                    eslesmeler = face_recognition.compare_faces(kayitli_yuzlerin_paket_listesi, yuz_paketi)
                    yuz_mesafesi = face_recognition.face_distance(kayitli_yuzlerin_paket_listesi, yuz_paketi)

                    if eslesmeler:

                        en_yakin_indeks = yuz_mesafesi.argmin()

                        if eslesmeler[en_yakin_indeks]:

                            taninan_yuzun_ismi = kayitli_yuzlerin_isim_listesi[en_yakin_indeks]


            
                cv2.rectangle(kare, (sol, ust), (sag, alt), (0,255,0), 3)
                cv2.putText(kare, taninan_yuzun_ismi, (sol, ust-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
            
            cv2.imshow("Taninan yuzleri tespit etme", kare)


            if cv2.waitKey(1) & 0xff == ord("q"):
                print("Çıkış yapılıyor...")
                break

        

    kayit.release()
    cv2.destroyAllWindows()


ana_pencere = tkinter.Tk()
ana_pencere.title("Bilinen yuzleri tespit etme")

ana_pencere.geometry("300x170")

tkinter.Label(ana_pencere, text="Yuz tespiti yapmak için tıklayınız").pack(pady=10)
tkinter.Button(ana_pencere, text="Yuzu tespit et", command=yuzu_tanimaya_calis).pack(pady=10)


ana_pencere.mainloop()


