import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox
from PyQt6 import QtCore
from PyQt6.QtCore import QCoreApplication, QTimer
from PyQt6.uic import loadUi
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheets API için kimlik doğrulama bilgileri
creds = 'key.json'
gc=gspread.service_account(filename=creds)

# Kullanıcıların bulunduğu Google Sheets dosyasını açma ve verileri alma
spreadsheet=gc.open('Kullanicilar')
worksheet= spreadsheet.get_worksheet(0)
all_values = worksheet.get_all_values()
del all_values[0]

class ProjeArayuz(QMainWindow):
    def __init__(self):
        super(ProjeArayuz, self).__init__()
        loadUi('proje_arayuz.ui', self)
        self.Uyari.clear()
        self.girisButonu.clicked.connect(self.Giris)
        self.cikisButonu.clicked.connect(QCoreApplication.exit)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

    def mousePressEvent(self, event):
        self.draPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.draPos)
        self.draPos = event.globalPosition().toPoint()
        event.accept()

    def Giris(self):
        kullaniciadi = self.kullaniciAdi.text()
        sifre = self.kullaniciParola.text()

        try:
            for row in all_values:
                k = row[0]
                s = row[1]
                y = row[2]
                if kullaniciadi==k and sifre==s:
                    if y == "admin":
                      tercih_menu_admin.show()  # Admin yetkisi varsa admin menüsünü göster
                    else:
                      tercih_menu.show()  # Admin yetkisi yoksa standart menüyü göster
                      
                    proje_arayuz.hide()
                    self.kullaniciAdi.clear()
                    self.kullaniciParola.clear()
                    self.Uyari.clear()
                    break
                
                elif kullaniciadi!=k or sifre!=s:
                    self.kullaniciAdi.clear()
                    self.kullaniciParola.clear()
                    self.Uyari.setText('Sisteme giriş başarısız ! Kullanıcı adı veya Kullanici sifresi hatalı!')
        except Exception as e:
            pass

class TercihMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('tercih_menu.ui', self)

        self.basvurularButon.clicked.connect(lambda: (basvurular_sayfasi.show(), tercih_menu.hide()))
        self.mentorGorusmesiButon.clicked.connect(lambda: (mentor_gorusme_sayfasi.show(), tercih_menu.hide()))
        self.mulakatlarButonu.clicked.connect(lambda: (mulakatlar.show(), tercih_menu.hide()))
        self.cikisButonu.clicked.connect(QCoreApplication.exit)
        self.geriButonu.clicked.connect(lambda: (proje_arayuz.show(), tercih_menu.hide()))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    def mousePressEvent(self, event):
        self.draPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.draPos)
        self.draPos = event.globalPosition().toPoint()
        event.accept()

class TercihMenuAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('tercih_menu_admin.ui', self)

        self.basvurularButon.clicked.connect(lambda: (basvurular_sayfasi.show(), tercih_menu.hide()))
        self.mentorGorusmesiButon.clicked.connect(lambda: (mentor_gorusme_sayfasi.show(), tercih_menu.hide()))
        self.mulakatlarButonu.clicked.connect(lambda: (mulakatlar.show(), tercih_menu.hide()))
        self.adminMenuButonu.clicked.connect(lambda: (admin_menu.show(), tercih_menu.hide()))
        self.cikisButonu.clicked.connect(QCoreApplication.exit)
        self.geriButonu.clicked.connect(lambda: (proje_arayuz.show(), tercih_menu.hide()))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    def mousePressEvent(self, event):
        self.draPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.draPos)
        self.draPos = event.globalPosition().toPoint()
        event.accept()

spreadsheet=gc.open('Basvurular')
worksheet3= spreadsheet.get_worksheet(0)
all_values3 = worksheet3.get_all_values()
del all_values3[0]

spreadsheet=gc.open('VIT1')
worksheet4= spreadsheet.get_worksheet(0)
all_values4 = worksheet4.get_all_values()
del all_values4[0] 

spreadsheet=gc.open('VIT2')
worksheet5= spreadsheet.get_worksheet(0)
all_values5 = worksheet5.get_all_values()
del all_values5[0] 
class BasvurularSayfasi(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('basvurular.ui', self)
        self.cikisButonu.clicked.connect(QCoreApplication.exit)
        self.geriButonu.clicked.connect(lambda: (self.tableWidget.setRowCount(0), self.aramaKutusu.clear(), tercih_menu.show(), basvurular_sayfasi.hide()))
        self.araButonu.clicked.connect(self.Arama)
        self.tumBasvurularButonu.clicked.connect(self.tumBasvurular)
        self.oncekiVitKontrolButonu.clicked.connect(self.oncekiVitKontrol)
        self.mukerrerKayitButonu.clicked.connect(self.mukerrerKayit)
        self.basvuruFiltreliButonu.clicked.connect(self.basvuruFiltreli)
        self.farkliKayitButonu.clicked.connect(self.farkliKayit)
        self.mentorGorusmesiTanimlananlarButonu.clicked.connect(self.MgTamamlanan)
        self.mentorGorusmesiTanimlanmayanlarButonu.clicked.connect(self.MgTamamlanmayan)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    def mousePressEvent(self, event):
        self.draPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.draPos)
        self.draPos = event.globalPosition().toPoint()
        event.accept()

    def SonucGosterme(self):
        self.tableWidget.setRowCount(0)
        for row_index, (index, row) in enumerate(self.df.iterrows()):
            self.tableWidget.insertRow(row_index)
            for col_index, col_value in enumerate(row):
                item = QTableWidgetItem(str(col_value))
                self.tableWidget.setItem(row_index, col_index, item)
            self.liste_kisi_sayisi.setText(f'Bulunan Kişi Sayısı : {len(self.df)}')
            QTimer.singleShot(3000, lambda: self.liste_kisi_sayisi.clear())

    def Arama(self):
        if self.arama_kutusu.text()!='':
            results= []
            ara= self.arama_kutusu.text()
            for kayit in all_values3:
                if ara.lower() in kayit[1].lower():
                    results.append(kayit)
            if not results:
                    self.arama_negatif.setText('Aradığınız kişi listede bulunmamaktadır!')
                    QTimer.singleShot(3000, lambda: self.arama_negatif.clear())
            self.df = pd.DataFrame(results)
        self.SonucGosterme()

    def tumBasvurular(self):
        self.df = pd.DataFrame(all_values3)
        self.SonucGosterme()

    def oncekiVitKontrol(self):
        results = []
        
        # Başvurular dosyasındaki adayları alın
        for row in all_values3:
            basvuru_adi_soyadi = row[1]  # Adayın kullanıcı adı
            basvuru_mail_adresi = row[2]  # Adayın e-posta adresi

            # VIT1 ve VIT2 dosyalarındaki adaylarla karşılaştırma yapın
            for vit_kaydi in all_values4:
                if basvuru_adi_soyadi == vit_kaydi[1] or basvuru_mail_adresi == vit_kaydi[2]:
                    results.append(row)
                    break
            
            for vit_kaydi in all_values5:
                if basvuru_adi_soyadi == vit_kaydi[1] or basvuru_mail_adresi == vit_kaydi[2]:
                    results.append(row)
                    break

        self.df = pd.DataFrame(results)
        self.SonucGosterme()

    def mukerrerKayit(self):
        results = []
        unique_records = set()  # Tekil kayıtları takip etmek için bir küme oluştur
        for kayit in all_values3:
            aday = (kayit[1], kayit[2])  # İsim ve mail adresi tuple'ını oluştur
            if aday in unique_records:  # Eğer bu kayıt daha önce eklenmişse, mükerrerdir
                results.append(kayit)
            else:
                unique_records.add(aday)  # Eğer daha önce eklenmemişse, set'e ekle
        self.df = pd.DataFrame(results)
        self.SonucGosterme()
    
    def basvuruFiltreli(self):
        results = []
        unique_records = set()  # Tekil kayıtları takip etmek için bir küme oluştur
        for kayit in all_values3:
            aday = (kayit[1], kayit[2])  # İsim ve mail adresi tuple'ını oluştur
            if aday not in unique_records:  # Eğer bu kayıt daha önce eklenmemişse, ekrana getir
                results.append(kayit)
                unique_records.add(aday)  # Set'e ekle
        self.df = pd.DataFrame(results)
        self.SonucGosterme()
    
    def farkliKayit(self):
        results = []

        # Başvurular dosyasındaki adayları alın
        basvurular = set((kayit[1], kayit[2]) for kayit in all_values3)

        # VIT1 dosyasındaki adayları alın
        vit1_adaylar = set((kayit[1], kayit[2]) for kayit in all_values4)

        # VIT2 dosyasındaki adayları alın
        vit2_adaylar = set((kayit[1], kayit[2]) for kayit in all_values5)

        # Başvurular dosyasında ancak VIT1 ve VIT2 dosyalarında olmayan adayları bulun
        for basvuru in basvurular:
            if basvuru not in vit1_adaylar and basvuru not in vit2_adaylar:
                for row in all_values3:
                    if (row[1], row[2]) == basvuru:
                        results.append(row)
                        break

        self.df = pd.DataFrame(results)
        self.SonucGosterme()
    
    def MgTamamlanan(self):
        results= []
        for kayit in all_values3:
            for x in all_values2:
                if kayit[1] == x[1]:
                    results.append(kayit)
        
        self.df = pd.DataFrame(results)
        self.SonucGosterme()

    def MgTamamlanmayan(self):
        results= []
        x=[]
        for kayit in all_values2:
            x.append(kayit[1])
        for kayit in all_values3:
            if not (kayit[1] in x):
                results.append(kayit)
                break
            
        self.df = pd.DataFrame(results)
        self.SonucGosterme()


spreadsheet=gc.open('Mulakatlar')
worksheet1= spreadsheet.get_worksheet(0)
all_values1 = worksheet1.get_all_values()
del all_values1[0]

class Mulakatlar(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('mulakatlar.ui', self)
        self.exitButonu.clicked.connect(QCoreApplication.exit)
        self.tercihlerButonu.clicked.connect(lambda: (self.tableWidget.setRowCount(0), self.aramaKutusu.clear(), tercih_menu.show(), mulakatlar.hide()))
        self.araButonu.clicked.connect(self.Arama)
        self.projesiGonderilmisOlanlarButonu.clicked.connect(self.proje1)
        self.projesiGelmisOlanlarButonu.clicked.connect(self.proje2)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    def mousePressEvent(self, event):
        self.draPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.draPos)
        self.draPos = event.globalPosition().toPoint()
        event.accept()
    def SonucGosterme(self):
        self.tableWidget.setRowCount(0)
        for row_index, (index, row) in enumerate(self.df.iterrows()):
            self.tableWidget.insertRow(row_index)
            for col_index, col_value in enumerate(row):
                item = QTableWidgetItem(str(col_value))
                self.tableWidget.setItem(row_index, col_index, item)
            self.liste_kisi_sayisi.setText(f'Bulunan Kişi Sayısı : {len(self.df)}')
            QTimer.singleShot(3000, lambda: self.liste_kisi_sayisi.clear())

    
    def Arama(self):
        if self.arama_kutusu.text()!='':
            results= []
            ara= self.arama_kutusu.text()
            for kayit in all_values1:
                if ara.lower() in kayit[0].lower():
                    results.append(kayit)
            if not results:
                    self.arama_negatif.setText('Aradığınız kişi listede bulunmamaktadır!')
                    QTimer.singleShot(3000, lambda: self.arama_negatif.clear())
            self.df = pd.DataFrame(results)
        self.SonucGosterme()
       
    def proje1(self):
        results= []
        for kayit in all_values1:
            if kayit[1]!='':
                results.append(kayit)
        
        self.df = pd.DataFrame(results)
        self.SonucGosterme()

    def proje2(self):
        results = []
        for kayit in all_values1:
            if kayit[2]!='':
                results.append(kayit)
        self.df = pd.DataFrame(results)
        self.SonucGosterme()


spreadsheet=gc.open('Mentor')
worksheet2= spreadsheet.get_worksheet(0)
all_values2 = worksheet2.get_all_values()
del all_values2[0]
for kayit in all_values2:
    kayit[4], kayit[5], kayit[6], kayit[7] = kayit[6], kayit[7], kayit[4], kayit[5]

class MentorGorusmeSayfasi(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('mentor_menu.ui', self)
        self.cikisButonu.clicked.connect(QCoreApplication.exit)
        self.tercihlerButonu.clicked.connect(lambda: (self.tableWidget.setRowCount(0), self.aramaKutusu.clear(),
                                                 tercih_menu.show(), mentor_gorusme_sayfasi.hide()))
        self.araButonu.clicked.connect(self.Arama)
        self.tumGorusmelerButonu.clicked.connect(self.TumGorusmeler)
        self.cokluSecenekKutusu.currentIndexChanged.connect(self.update_table)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    def mousePressEvent(self, event):
        self.draPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.draPos)
        self.draPos = event.globalPosition().toPoint()
        event.accept()
    def SonucGosterme(self):
        self.tableWidget.setRowCount(0)
        for row_index, (index, row) in enumerate(self.df.iterrows()):
            self.tableWidget.insertRow(row_index)
            for col_index, col_value in enumerate(row):
                item = QTableWidgetItem(str(col_value))
                self.tableWidget.setItem(row_index, col_index, item)
            self.liste_kisi_sayisi.setText(f'Bulunan Kişi Sayısı : {len(self.df)}')
            QTimer.singleShot(3000, lambda: self.liste_kisi_sayisi.clear())

    def Arama(self):
        if self.aramaKutusu.text()!='':
            results= []
            ara= self.aramaKutusu.text()
            for kayit in all_values2:
                if ara.lower() in kayit[1].lower():
                    results.append(kayit)
            if not results:
                    self.arama_negatif.setText('Aradığınız kişi listede bulunmamaktadır!')
                    QTimer.singleShot(3000, lambda: self.arama_negatif.clear())
            self.df = pd.DataFrame(results)
            self.SonucGosterme()
    
    def TumGorusmeler(self):
        self.df = pd.DataFrame(all_values2)
        self.SonucGosterme()

    def update_table(self):
        results = []
        for kayit in all_values2:
            if self.cokluSecenekKutusu.currentText() == kayit[6]:
                results.append(kayit)
        self.df = pd.DataFrame(results)
        self.SonucGosterme()

class AdminMenu(QMainWindow):
    pass

app = QApplication(sys.argv)
proje_arayuz = ProjeArayuz()
tercih_menu = TercihMenu()
tercih_menu_admin = TercihMenuAdmin()
basvurular_sayfasi = BasvurularSayfasi()
mulakatlar = Mulakatlar()
mentor_gorusme_sayfasi = MentorGorusmeSayfasi()
# admin_menu() = AdminMenu()
proje_arayuz.show()
sys.exit(app.exec())