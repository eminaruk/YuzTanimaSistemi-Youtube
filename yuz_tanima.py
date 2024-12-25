import cv2
import face_recognition

kayit = cv2.VideoCapture(0)


while True:

    durum, kare = kayit.read()

    if durum:

        yuz_konumlari = face_recognition.face_locations(kare)

        for yuz_konumu in yuz_konumlari:

            ust, sag, alt, sol = yuz_konumu

            cv2.rectangle(kare, (sol, ust), (sag, alt), (0,255,0), 3)
            


        cv2.imshow("Yuz Tanima Sistemi", kare)


        if cv2.waitKey(1) & 0xff == ord("q"):

            break
    

kayit.release()
cv2.destroyAllWindows()

