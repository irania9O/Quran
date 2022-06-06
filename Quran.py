# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog,QWidget,QSlider,QComboBox,QLabel,QApplication,QColorDialog,QPushButton,QSpinBox
from PyQt5.QtGui import QFont,QFontDatabase,QIcon
from PyQt5.QtCore import QObject,pyqtSignal,QRunnable,QThreadPool,QSize,Qt
from mutagen.mp3 import MP3 
from requests import get
from os import path,mkdir
import sys,sqlite3,time,pygame
def r_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()
#---------- SQL ---------------
conn_q = sqlite3.connect(r_path('data/Quran.db'))
cq = conn_q.cursor()
soure = cq.execute("SELECT * FROM 'ChapterProperty'").fetchall()
#---------- SQL ---------------
conn = sqlite3.connect(r_path('data/data.dll'))
c = conn.cursor()
#--------- MAIN TABLE  SQL -----------
c.execute('''CREATE TABLE IF NOT EXISTS app (
    ID varchar(255) NOT NULL,
    VALUE varchar(255),
    PRIMARY KEY (ID)
);''')
conn.commit()
#---------- SET DEFULT THEM -------------
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("theme", "bp"))
except:
    pass
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("font", "20"))
except:
    pass
conn.commit()
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("theme_t", "white"))
except:
    pass
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("soure", "1"))
except:
    c.execute(f"UPDATE 'app' set 'VALUE' = '1' where ID = 'soure'")
    pass
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("aye", "1"))
except:
    c.execute(f"UPDATE 'app' set 'VALUE' = '1' where ID = 'aye'")
    pass
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("qari", "Parhizgar"))
except:
    pass
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("type", "AR"))
except:
    pass
try:
    c.execute("insert into app (ID, VALUE) values(?,?)",("P_S", "1"))
except:
    pass
conn.commit()
#------------------------
class Signals(QObject):
    finished = pyqtSignal()

class Runnable(QRunnable):
    def __init__(self,see,length,aye):
        super().__init__()
        self.s = see
        self.length = length
        self.aye = aye
        self.signal = Signals()
    def run(self):
        pos  = int(pygame.mixer.music.get_pos())
        while(pos > -0.00000000001):
            pos  = int(pygame.mixer.music.get_pos())
            if int(pos/self.length) > 100:
                self.s.slider.setValue(int((pos/self.length)/10))
            else:
                self.s.slider.setValue(int(pos/self.length))
            time.sleep(1)
        self.signal.finished.emit()
class Window(QDialog):
    def __init__(self):
        super().__init__()

        # setting title
    
        self.setWindowTitle("Python ")
    
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.them_bar = """\n#them_bar {
                    background-color: rgb(30,50,100);
                    border-radius: 20px;
                    opacity: 100;               
                }
                """
        self.setStyleSheet("""
                        #MAIN {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 red, stop:1 yellow);
                            border-radius: 20px;
                            opacity: 100;               
                        }
                        """+self.them_bar)
        #setting geometry
        #self.setGeometry(100, 100, 1024, 1024)
        self.resize(1350,900)
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):
        theme = c.execute("SELECT * FROM 'app' where ID = 'theme'").fetchall()[0][1]
        if theme == "bp":
            self.change_tehm_bp()
        elif theme == "ry":
            self.change_tehm_ry()
        elif theme == "rb":
            self.change_tehm_rb()
        elif theme == "gb":
            self.change_tehm_gb()
        elif theme == "gbl":
            self.change_tehm_gbl()
        else:
            self.setStyleSheet("""
                    #MAIN {
                        background-color: """+theme+""";
                        border-radius: 20px;
                        opacity: 100;
                                     
                    }"""+self.them_bar)            
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        self.widget = QWidget(self)
        self.widget.resize(1200,900)
        self.widget.setObjectName('MAIN')
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        self.slider = QSlider(Qt.Horizontal,self.widget)
        self.slider.setGeometry(200, 800, 400,40)
        self.slider.setStyleSheet('''
QSlider::groove:horizontal {
    background-color: white;
    border: 1px solid;
    height: 10px;
    margin: 0px;
    border-radius : 5;
    }
QSlider::handle:horizontal {
    
    border: 1px solid;
    height: 26px;
    width: 26px;
    margin: -15px 0px;
    border-radius : 13;
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(255, 242, 0,255), stop:1 rgba(0, 234, 255,255));
    }
''')
        self.sliderv = QSlider(Qt.Horizontal,self.widget)
        self.sliderv.setGeometry(900, 800, 200,40)
        self.sliderv.setValue(99)
        self.sliderv.valueChanged.connect(self.set_vol)
        self.sliderv.setStyleSheet('''
QSlider::groove:horizontal {
    background-color: white;
    border: 1px solid;
    height: 10px;
    margin: 0px;
    border-radius : 5;
    }
QSlider::handle:horizontal {
    
    border: 1px solid;
    height: 26px;
    width: 26px;
    margin: -15px 0px;
    border-radius : 13;
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(255, 242, 0,255), stop:1 rgba(0, 234, 255,255));
    }
''')
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        self.soure_list = QComboBox(self.widget)
        self.soure_list.setStyleSheet('''QComboBox {font-size:  18px;border-radius: 5px;border: 2px solid rgb(255, 69, 0);color: rgb(0, 0, 255);}    
                                         QComboBox::drop-down {subcontrol-origin: padding;subcontrol-position: top right;width: 20px;}''')
        self.soure_list.setGeometry(10, 10, 125, 50)
        for i in soure:
            self.soure_list.addItem(i[1])
        self.soure_list.currentTextChanged.connect(self.add_aye)

        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        self.aye_list = QComboBox(self.widget)
        self.aye_list.setStyleSheet('''QComboBox {font-size:  18px;border-radius: 5px;border: 2px solid rgb(255, 69, 0);color: rgb(0, 0, 255);}    
                                       QComboBox::drop-down {subcontrol-origin: padding;subcontrol-position: top right;width: 20px;}''')
        self.aye_list.setGeometry(155, 10, 100, 50)
        for x in range(1,8):
            self.aye_list.addItem(str(x))
        self.aye_list.currentTextChanged.connect(self.change_aye)
        global AllItems
        AllItems = [self.aye_list.itemText(i) for i in range(self.aye_list.count())]
        #---------------------------------------------
        self.qari_list = QComboBox(self.widget)
        self.qari_list.setStyleSheet('''QComboBox {font-size:  18px;border-radius: 5px;border: 2px solid rgb(255, 69, 0);color: rgb(0, 0, 255);}    
                                       QComboBox::drop-down {subcontrol-origin: padding;subcontrol-position: top right;width: 20px;}''')
        self.qari_list.setGeometry(900, 10, 250, 50)
        qari = cq.execute("SELECT * FROM 'Audio'").fetchall()
        for i in qari:
            self.qari_list.addItem(i[1])
        self.qari_list.currentTextChanged.connect(self.change_qari)
        esm_qari = c.execute(f"SELECT * FROM 'app' WHERE ID='qari'").fetchall()[0][1]
        self.qari_list.setCurrentText(esm_qari)
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        fatehe = cq.execute("SELECT * FROM 'Quran'  WHERE Chapter='1'").fetchall()
        self.aye_a = QLabel(fatehe[0][1],self.widget)
        theme_t = c.execute("SELECT * FROM 'app' where ID = 'theme_t'").fetchall()[0][1]
        self.aye_a.setStyleSheet('QLabel{color:'+theme_t+';}')
        self.aye_a.setAlignment(Qt.AlignCenter)
        self.aye_a.setWordWrap(True)
        self.aye_a.setGeometry(100, 100, 1000, 700)
        QFontDatabase.addApplicationFont(r_path("data/font/QuranTaha.ttf"))
        font_size = c.execute("SELECT * FROM 'app' where ID = 'font'").fetchall()[0][1]
        font = QFont('QuranTaha', int(font_size))
        self.aye_a.setFont(font)
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        self.name_app_1= QLabel("کلام نور",self.widget)
        self.name_app_1.setStyleSheet('QLabel{color:'+theme_t+';}')
        self.name_app_1.setAlignment(Qt.AlignCenter)
        self.name_app_1.setWordWrap(True)
        self.name_app_1.setGeometry(500,0, 200, 100)
        font = QFont('QuranTaha', 30)
        self.name_app_1.setFont(font)
        
        self.name_app_2= QLabel("Seyed Ali Kamali",self.widget)
        self.name_app_2.setStyleSheet('QLabel{color:'+theme_t+';}')
        self.name_app_2.setAlignment(Qt.AlignCenter)
        self.name_app_2.setWordWrap(True)
        self.name_app_2.setGeometry(0,835, 150, 100)
        font = QFont('QuranTaha', 10)
        self.name_app_2.setFont(font)
        
        self.name_app_3= QLabel("V1",self.widget)
        self.name_app_3.setStyleSheet('QLabel{color:'+theme_t+';}')
        self.name_app_3.setAlignment(Qt.AlignCenter)
        self.name_app_3.setWordWrap(True)
        self.name_app_3.setGeometry(1075,835, 200, 100)
        font = QFont('QuranTaha', 10)
        self.name_app_3.setFont(font)
         
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*--*-*--*
        self.play_stop = QPushButton("",  self.widget)
        self.play_stop.setIcon(QIcon(r_path('data/icon/play.png')))
        self.play_stop.setIconSize(QSize(60,60))  
        self.play_stop.setGeometry(20,790, 60, 60)
        self.play_stop.setStyleSheet("""border-radius : 20;""")
        self.play_stop.clicked.connect(self.play_sound)
        
        self.play_stop = QPushButton("",  self.widget)
        self.play_stop.setIcon(QIcon(r_path('data/icon/stop.png')))
        self.play_stop.setIconSize(QSize(60,60))  
        self.play_stop.setGeometry(100,790, 60, 60)
        self.play_stop.setStyleSheet("""border-radius : 20;""")
        self.play_stop.clicked.connect(self.stop_sound)

        self.vlumeee = QPushButton("",  self.widget)
        self.vlumeee.setIcon(QIcon(r_path('data/icon/volum.png')))
        self.vlumeee.setIconSize(QSize(60,60))  
        self.vlumeee.setGeometry(825,790, 60, 60)
        self.vlumeee.setStyleSheet("""border-radius : 20;""")
        self.vlumeee.clicked.connect(self.stop_sound)


        
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        self.widgets = QWidget(self)
        self.widgets.setGeometry(1205,0, 60, 900)
        self.widgets.setObjectName('them_bar')
        
        self.change_bp = QPushButton("",  self.widgets)
        self.change_bp.setGeometry(10, 10, 40, 40)
        self.change_bp.setStyleSheet("""border : 2px solid black;border-radius : 20;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0, 61, 166, 255), stop:1 rgba(166, 0, 135, 255));""")
        self.change_bp.clicked.connect(self.change_tehm_bp)
        
        self.change_ry = QPushButton("",  self.widgets)
        self.change_ry.setGeometry(10, 60, 40, 40)
        self.change_ry.setStyleSheet("""border : 2px solid black;border-radius : 20;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0,150,45,255), stop:1 rgba(150, 0, 18,255));""")
        self.change_ry.clicked.connect(self.change_tehm_ry)
        
        self.change_rb = QPushButton("",  self.widgets)
        self.change_rb.setGeometry(10, 110, 40, 40)
        self.change_rb.setStyleSheet("""border : 2px solid black;border-radius : 20;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(207, 13, 60,255), stop:1 rgba(3, 0, 47,255));""")
        self.change_rb.clicked.connect(self.change_tehm_rb)
        
        self.change_gb = QPushButton("",  self.widgets)
        self.change_gb.setGeometry(10, 160, 40, 40)
        self.change_gb.setStyleSheet("""border : 2px solid black;border-radius : 20;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 gray, stop:1 black);""")
        self.change_gb.clicked.connect(self.change_tehm_gb)

        self.change_gbl = QPushButton("",  self.widgets)
        self.change_gbl.setGeometry(10, 210, 40, 40)
        self.change_gbl.setStyleSheet("""border : 2px solid black;border-radius : 20;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0, 86, 156, 255), stop:1 rgba(1, 125, 28, 255));""")
        self.change_gbl.clicked.connect(self.change_tehm_gbl)
        
        self.change_gbl = QPushButton("",  self.widgets)
        self.change_gbl.setIcon(QIcon(r_path('data/icon/rgb.png')))
        self.change_gbl.setIconSize(QSize(40,40))  
        self.change_gbl.setGeometry(10, 260, 40, 40)
        self.change_gbl.setStyleSheet("""border-radius : 20;""")
        self.change_gbl.clicked.connect(self.pick_color)

        
        self.spin = QSpinBox(self.widgets)
        self.spin.setGeometry(10, 640, 40, 40)
        self.spin.valueChanged.connect(self.change_font)
        self.spin.setValue(int(font_size))
        self.spin.setMinimum(1)
        self.spin.setMaximum(50)
        self.spin.setStyleSheet("""border : 2px solid gold;border-radius : 10;""")

        self.change_gbl = QPushButton("",  self.widgets)
        self.change_gbl.setIcon(QIcon(r_path('data/icon/rgb.png')))
        self.change_gbl.setIconSize(QSize(40,40))  
        self.change_gbl.setGeometry(10, 700, 40, 40)
        self.change_gbl.setStyleSheet("""border-radius : 20;""")
        self.change_gbl.clicked.connect(self.pick_t_color)

        """
        self.spin = QSpinBox(self.widgets)
        self.spin.setGeometry(10, 750, 40, 40)
        self.spin.setObjectName('QSpinBox')
        self.spin.setRange(0, 100)
        self.spin.setStyleSheet('''QSpinBox {
        border-radius : 5;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0, 255, 238, 255), stop:1 rgba(2, 245, 107, 255));
         }
        ''') 
        """
        c.execute(f"UPDATE 'app' set 'VALUE' = 'AR' where ID = 'type'")
        conn.commit()
        self.lang_t = QPushButton("AR",  self.widgets)
        self.lang_t.setGeometry(10, 750, 40, 40)
        self.lang_t.setStyleSheet("""color:red;border : 2px solid black;border-radius : 20;background-color:white;""")
        self.lang_t.setFont(QFont('QuranTaha', 12))
        self.lang_t.clicked.connect(self.change_lang)
        
        self.change_gbl = QPushButton("",  self.widgets)
        self.change_gbl.setIcon(QIcon(r_path('data/icon/minimize.png')))
        self.change_gbl.setIconSize(QSize(50,50))  
        self.change_gbl.setGeometry(10, 800, 40, 40)
        self.change_gbl.setStyleSheet("""border-radius : 20;""")
        self.change_gbl.clicked.connect(self.minmizie_window)
        
        self.change_gbl = QPushButton("",  self.widgets)
        self.change_gbl.setIcon(QIcon(r_path('data/icon/exit.png')))
        self.change_gbl.setIconSize(QSize(50,50))   
        self.change_gbl.setGeometry(10, 850, 40, 40)
        self.change_gbl.setStyleSheet("""border-radius : 20;""")
        self.change_gbl.clicked.connect(self.close_window)

    def change_font(self):
        value = self.spin.value()
        c.execute(f"UPDATE 'app' set 'VALUE' = '{value}' where ID = 'font'")
        conn.commit()
        font = QFont('QuranTaha', value)
        self.aye_a.setFont(font)
        
    def add_aye(self,name):
        shomare = 0
        for i in soure:
            if i[1] == name:
                aye = i[3]
                soure_n = i[0]
                c.execute(f"UPDATE 'app' set 'VALUE' = '{soure_n}' where ID = 'soure'")
                conn.commit()               
        self.aye_list.clear()        
        for x in range(1,aye+1):
            self.aye_list.addItem(str(x))
        c.execute(f"UPDATE 'app' set 'VALUE' = '1' where ID = 'aye'")
        conn.commit()
        global AllItems
        AllItems = [self.aye_list.itemText(i) for i in range(self.aye_list.count())]        
    def change_aye(self,shomare):
        c.execute(f"UPDATE 'app' set 'VALUE' = '{shomare}' where ID = 'aye'")
        conn.commit()
        try:
            esm_soure = self.soure_list.currentText()
            soure_n = cq.execute(f"SELECT * FROM 'ChapterProperty' WHERE Name='{esm_soure}'").fetchall()[0][0]
            types = c.execute("SELECT * FROM 'app' WHERE ID='type'").fetchall()[0][1]
            ayat = cq.execute(f"SELECT * FROM 'Quran'  WHERE Chapter='{soure_n}' AND verse='{shomare}'").fetchall()
            mani = cq.execute(f"SELECT * FROM 'fa.fooladvand'  WHERE ID='{ayat[0][0]}'").fetchall()
            if types == "AR":
                 self.aye_a.setText(ayat[0][1])
            elif types == "FA":
                self.aye_a.setText(mani[0][1])
           
        except:
            pass

    def change_lang(self):
        try:
            shomare = self.aye_list.currentText()
            esm_soure = self.soure_list.currentText()
            soure_n = cq.execute(f"SELECT * FROM 'ChapterProperty' WHERE Name='{esm_soure}'").fetchall()[0][0]
            types = c.execute("SELECT * FROM 'app' WHERE ID='type'").fetchall()[0][1]
            ayat = cq.execute(f"SELECT * FROM 'Quran'  WHERE Chapter='{soure_n}' AND verse='{shomare}'").fetchall()
            mani = cq.execute(f"SELECT * FROM 'fa.fooladvand'  WHERE ID='{ayat[0][0]}'").fetchall()
            if types == "AR":
                c.execute(f"UPDATE 'app' set 'VALUE' = 'FA' where ID = 'type'")
                self.aye_a.setText(mani[0][1])
                self.lang_t.setText("FA")
            elif types == "FA":
                c.execute(f"UPDATE 'app' set 'VALUE' = 'AR' where ID = 'type'")
                self.aye_a.setText(ayat[0][1])
                self.lang_t.setText("AR")
            
            conn.commit()
        except:
            pass        
    def change_qari(self,esm_qari):
        c.execute(f"UPDATE 'app' set 'VALUE' = '{esm_qari}' where ID = 'qari'")
        conn.commit()

    def close_window(self):
        self.close()
    def minmizie_window(self):
        self.showMinimized()

    def set_vol(self,p):
        pygame.mixer.music.set_volume(p/100)
    def check(self): 
        state = c.execute("SELECT * FROM 'app' WHERE ID='P_S'").fetchall()[0][1]
        aye = int(c.execute(f"SELECT * FROM 'app' WHERE ID='aye'").fetchall()[0][1])+1
        if str(aye) in AllItems and state == "1":
            self.aye_list.setCurrentText(str(aye))
            self.change_aye(aye)
            self.play_sound()

    def play_sound(self):
        aye = c.execute(f"SELECT * FROM 'app' WHERE ID='aye'").fetchall()[0][1]
        soure = c.execute(f"SELECT * FROM 'app' WHERE ID='soure'").fetchall()[0][1]
        esm_qari = c.execute(f"SELECT * FROM 'app' WHERE ID='qari'").fetchall()[0][1]
        audio_id = cq.execute(f"SELECT * FROM 'Quran'  WHERE Chapter='{soure}' AND verse='{aye}'").fetchall()[0][7]
        base_url = cq.execute(f"SELECT * FROM 'Audio' WHERE Name='{esm_qari}'").fetchall()[0][3]
        types = c.execute("SELECT * FROM 'app' WHERE ID='type'").fetchall()[0][1]
        if types == "FA":
            esm_qari = "Fooladvand"
            base_url = "https://everyayah.com/data/translations/Fooladvand_Hedayatfar_40Kbps/"
            
        if not path.exists(r_path('data/audio/'+esm_qari)):
            mkdir(r_path('data/audio/'+esm_qari))
            
        urlss = r_path('data/audio/'+esm_qari+'/'+str(audio_id)+'.mp3')
        
        if not path.exists(urlss):
            mp3 = base_url+audio_id+'.mp3'
            file = get(mp3).content
            with open(urlss,'wb') as f:
                f.write(file)
                f.close()          
        audio = MP3(urlss)
        length = int(audio.info.length)

        c.execute(f"UPDATE 'app' set 'VALUE' = '1' where ID = 'P_S'")
        conn.commit()      
    
        pygame.mixer.music.stop()
        pygame.mixer.music.load(urlss)
        pygame.mixer.music.play()

        runnable = Runnable(self,length,aye)
        runnable.signal.finished.connect(self.check)
        global pool
        pool = QThreadPool.globalInstance()
        pool.setMaxThreadCount(1)
        pool.start(runnable)
        
        
    def stop_sound(slef):
        pool.clear()
        c.execute(f"UPDATE 'app' set 'VALUE' = '0' where ID = 'P_S'")
        conn.commit()
        pygame.mixer.music.stop()    
         
    def pick_color(self):
        self.widget.hide()
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet("""
                    #MAIN {
                        background-color: """+color.name()+""";
                        border-radius: 20px;
                        opacity: 100;
                                     
                    }"""+self.them_bar)
            c.execute(f"UPDATE 'app' set 'VALUE' = '{color.name()}' where ID = 'theme'")
            conn.commit()
        self.widget.show()
        
    def pick_t_color(self):
        self.widget.hide()
        color = QColorDialog.getColor()
        if color.isValid():
            self.aye_a.setStyleSheet('QLabel{color:'+color.name()+';}')
            self.name_app_1.setStyleSheet('QLabel{color:'+color.name()+';}')
            self.name_app_2.setStyleSheet('QLabel{color:'+color.name()+';}')
            self.name_app_3.setStyleSheet('QLabel{color:'+color.name()+';}')
            
            c.execute(f"UPDATE 'app' set 'VALUE' = '{color.name()}' where ID = 'theme_t'")
            conn.commit()
        self.widget.show()
        
    def change_tehm_bp(self):
        c.execute("UPDATE 'app' set 'VALUE' = 'bp' where ID = 'theme'")
        conn.commit()
        self.setStyleSheet("""
                #MAIN {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0, 61, 166, 255), stop:1 rgba(166, 0, 135, 255));
                    border-radius: 20px;
                    opacity: 100;
                                 
                }"""+self.them_bar)
        
    def change_tehm_ry(self):
        c.execute("UPDATE 'app' set 'VALUE' = 'ry' where ID = 'theme'")
        conn.commit()
        self.setStyleSheet("""
                #MAIN {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0,150,45,255), stop:1 rgba(150, 0, 18,255));
                    border-radius: 20px;
                    opacity: 100;
                                 
                }"""+self.them_bar)
    
    def change_tehm_rb(self):
        c.execute("UPDATE 'app' set 'VALUE' = 'rb' where ID = 'theme'")
        conn.commit()
        self.setStyleSheet("""
                #MAIN {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(207, 13, 60,255), stop:1 rgba(3, 0, 47,255));
                    border-radius: 20px;
                    opacity: 100;
                                 
                }"""+self.them_bar)
    def change_tehm_gb(self):
        c.execute("UPDATE 'app' set 'VALUE' = 'gb' where ID = 'theme'")
        conn.commit()
        self.setStyleSheet("""
                #MAIN {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 gray, stop:1 black);
                    border-radius: 20px;
                    opacity: 100;
                                 
                }"""+self.them_bar)
    def change_tehm_gbl(self):
        c.execute("UPDATE 'app' set 'VALUE' = 'gbl' where ID = 'theme'")
        conn.commit()
        self.setStyleSheet("""
                #MAIN {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, stop:0 rgba(0, 86, 156, 255), stop:1 rgba(1, 125, 28, 255));
                    border-radius: 20px;
                    opacity: 100;
                                 
                }"""+self.them_bar)

        

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()
#--------------
# start the app
sys.exit(App.exec())
