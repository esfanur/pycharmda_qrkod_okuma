import datetime
import time
import cv2
import pyzbar.pyzbar  as pyz
import numpy as np
import os
"""
+++++++++++++++++++++++++++++++++++++++++++++++RESİMDEN QR KOD OKUMA++++++++++++++++++++++++++++++++++++++++++++++++++++++++
res=cv2.imread("kaynaklar/indir.jpg")

#res=cv2.resize(res,None,fx=2,fy=2)

decetor=pyz.decode(res) # resdeki görüntüyü tarar ve içerdiği barkodları çözer
#print(decetor)

for i in decetor:
    data=i.data #burda qrkodun ıcındekı bilgileri hepsını değişkenlere atadık
    rect=i.rect
    pol=i.polygon
    cv2.rectangle(res,(rect.left,rect.top),(rect.left+rect.width,rect.top+rect.height),(255,0,0,),3) #burda qrkod etrafında dıkdortgen oluşturduk
    cv2.polylines(res,[np.array(pol)],True,(0,0,255),1) #burda ıse qrkodun kenarlarını cızdırdık 
cv2.imshow("qrkod",res)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
#+++++++++++++++++++++++++++++++++++++++++++++++++KAMERADAN QR KOD OKUMA +++++++++++++++++++++++++++++++++++++++++++

cam=cv2.VideoCapture(0) #burda kameradan qrkod okumak ıcın Videocapture kullandık.0  varsayılan kamerayı  kullanılır.
oku=[]
with open("okuma.txt", "r") as file: #burada qrkod datasını olsuturudugumuz dosyayı okuyoruz
    for satir in file.readlines(): #Dosyanın satırlarını sırayla al
        oku.append(satir.strip()) #Her satırı boşlukları temizleyerek oku listesine ekliyoruz
    #print(oku)

girisyapanlarliste=[] #daha once gırıs yapanların tutmak ıcın bos bır liste olusturuyoruz
songiris_zamani=0 #Son algılanan QR kodunun zamanını tutmak ıcın

while True:
    _,frame=cam.read()

    if cv2.waitKey(1) ==ord("q"):
        break

    qrkod=pyz.decode(frame)
    #print(qrkod)
    for i in qrkod:

        if len(qrkod)>0 :
            data=i.data
            rect=i.rect
            pol=i.polygon
            #print(data.decode())
            #cv2.putText(frame,data.decode(),(rect.left,rect.top),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
            cv2.rectangle(frame,(rect.left,rect.top),(rect.left+rect.width,rect.top+rect.height),(168,178,215),2)
            cv2.polylines(frame,[np.array(pol)],True,(255,0,0),2)
            if data.decode() in oku and data not in girisyapanlarliste:
                cv2.putText(frame, "BASARILI", (rect.left, rect.top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                if time.time()-songiris_zamani>5: #Aynı QR kodu son 5 saniyede sadece bir kez yazdırmak ıcın
                    with open("gir.txt","a",encoding="utf8") as file:
                        file.write("{} kullanıcı , {} zaman aralıgında giris yapmıstır  \n".format(data.decode(),datetime.datetime.now()))
                    girisyapanlarliste.append(data.decode())#qrkoddan alınan bu veriyi daha önce yazılanlar listesine ekle
                    songiris_zamani=time.time()#Algılama zamanını güncelle

            else: #eger okuma ıslemınde okunan qrkod txt dosyasında yoksa
                cv2.putText(frame, "BASARISIZ", (rect.left, rect.top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)




    cv2.imshow("frame",frame)

cam.release()
cv2.destroyAllWindows()
