from pydoc import plain
from struct import unpack_from
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QPropertyAnimation,QPoint,QSize,QTimer
from just_playback import Playback
from pygame import mixer,error

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.playback = Playback()
        self.windowico = QPixmap("note.png")
        #lable configurations
        text1 = QLabel(self,text="MUSIC")
        text1.setStyleSheet("""
            font-size: 30px;
            font-weight: bolder;
            font-family: Candara;
            color: white;
        """)
        text1.move(10,10)

        #file directory of opened file!
        self.openfiledir = ""

        #button1 configuration. Not declared as a class property, rather a local variable in this method.
        button1 = QPushButton(text="Select file", parent=self)
        button1.clicked.connect(self.openfile)
        button1.setStyleSheet("""
            QPushButton{
            font-size : 12px;
            background-color: Red;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px;
            font-family: Candara;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        button1.move(10,350)

        #Pause button configuration
        # self.PauseBtn = QPushButton(text="Pause",parent=self)
        self.PauseBtn = QPushButton(parent=self)
        self.pixmap2 = QPixmap("pause-64.png")
        self.PauseBtn.setIcon(self.pixmap2)
        self.PauseBtn.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 50px;
            height: 50px;
            background-color: Red;
            color: white;
            border: none;
            border-radius: 25%;
            font-family: Candara;
            padding: 0px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        self.PauseBtn.move(238,270)
        self.PauseBtn.clicked.connect(self.pauseaud)

        #Resume button configuration
        # self.Resume = QPushButton(text="Resume",parent=self)
        self.Resume = QPushButton(parent=self)
        self.pixmap1 = QPixmap("play-64.png")
        self.Resume.setIcon(self.pixmap1)
        self.Resume.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 50px;
            height: 50px;
            background-color: Red;
            color: white;
            border: none;
            border-radius: 25%;
            font-family: Candara;
            padding: 0px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        self.Resume.move(238,270)
        self.Resume.hide()
        self.Resume.clicked.connect(self.continueaud)

        #seek forward button

        self.seekfor = QPushButton(text=">>",parent=self)
        self.seekfor.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 50px;
            background-color: Red;
            color: white;
            border: none;
            border-radius: 10px;
            font-family: Candara;
            padding: 10px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        self.seekfor.move(350,270)
        self.seekfor.clicked.connect(self.moveforward)

        #seek backward button

        self.seekback = QPushButton(text="<<", parent=self)
        self.seekback.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 50px;
            background-color: Red;
            color: white;
            border: none;
            border-radius: 10px;
            font-family: Candara;
            padding: 10px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        self.seekback.move(100, 270)
        self.seekback.clicked.connect(self.movebackward)

        #Timeline!
        self.timeline = QWidget(self)
        self.timeline.setStyleSheet("""
            background-color : red;
        """)
        self.timeline.move(0,230)
        self.timeline.resize(0,10)
        
        #timestamp:
        self.totalduration = QLabel(self,text= f"{int(self.playback.duration/60)}:{self.playback.duration%60}")
        self.totalduration.setStyleSheet("""
            background-color: black;
            color: white;
            font-size: 12px;
            font-family: Candara;
        """)
        self.totalduration.move(490,250)

        self.timestamp = QLabel(self, text= "0:00")
        self.timestamp.setStyleSheet("""
            background-color: black;
            width: 150px;
            color: white;
            font-size: 12px;
            font-family: Candara;
        """)
        self.timestamp.move(10,250)

        #logo
        self.frame = QLabel(self)
        self.frame.resize(90,90)
        self.frame.setStyleSheet("""
            background-color: rgba(255,0,0,1)
        """)
        self.frame.move(220,100)
        self.pixmap3 = QPixmap("music-64.png")
        self.frame.setPixmap(self.pixmap3)
        #Application window allingment.
        self.setGeometry(100,200,500,420)
        self.setMaximumSize(530,400)
        self.setMinimumSize(530,400)
        self.setWindowTitle("Music App")
        self.setWindowIcon(self.windowico)
        self.setStyleSheet("""
            background-color: black;
            border: none;
            border-radius: 10px;
        """)
        

    def movebackward(self):
        self.playback.seek(self.playback.curr_pos - 10.0)
        self.anim1.setCurrentTime(self.anim1.currentTime() - 10000)
    def moveforward(self):
        self.playback.seek(self.playback.curr_pos + 10.0)
        self.anim1.setCurrentTime( self.anim1.currentTime() + 10000)
    def continueaud(self):
        try:
            
            self.playback.resume()
            self.Resume.hide()
            self.anim1.resume()
            self.timer.timeout.connect(self.update_time)
        except error :
            print("Please select a music file!")
    
    def pauseaud(self):
        try:
            
            self.playback.pause()
            self.Resume.show()
            self.anim1.pause()
            self.timer.timeout.disconnect()
        except:
            print("Please select a music file!")


    def openfile(self):
        self.filedil = QFileDialog(self)
        self.openfiledir = self.filedil.getOpenFileName(options=QFileDialog.DontUseNativeDialog)[0]
        self.filedil.close()
        self.Resume.hide()
        self.playback = Playback()
        if(self.playback.active):
            self.playback.stop()
        self.playback.load_file(path_to_file=self.openfiledir)
        self.playback.play()
        self.playback.loop_at_end(True)
        self.timeline.resize(0,10)
        self.anim1 = QPropertyAnimation(self.timeline,b"size")
        self.anim1.setEndValue(QSize(530,10))
        self.anim1.setDuration(self.playback.duration * 1000)
        self.anim1.start()
        self.anim1.setLoopCount(100) #selecting a high value just for safety !
        self.totalduration.setText(f"{int(self.playback.duration/60)}:{int(self.playback.duration%60)}")
        self.minute = 0
        self.second = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timestamp.setText(f"{self.minute}:{self.second}")
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        print(f"Currently playing {self.openfiledir}")
    
    def update_time(self):
        
        self.minute = int(self.playback.curr_pos/60)
        self.second = int(self.playback.curr_pos%60)
        self.timestamp.setText(f"{self.minute}:{self.second}")

#creating a basic application
app = QApplication([])
myapp = MyApplication()
myapp.show()
app.exec()
