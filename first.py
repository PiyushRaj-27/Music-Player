
#Basic Imports
from cgitb import text
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QPropertyAnimation,QPoint,QSize,QTimer
from just_playback import Playback
# from pygame import mixer,error

#the main class
class MyApplication(QWidget):
    def __init__(self):
        super().__init__()

        #playback instance
        self.playback = Playback()
        #currently opened file directory
        self.openfiledir = ""
        #previouly opened file directory
        self.prev = ""

        #Default lable configuration
        text1 = QLabel(self,text="MUSIC")
        text1.setObjectName("txt1")
        text1.move(10,10)

        #select file button configuration
        button1 = QPushButton(text="  Select File",parent=self)
        pixmap4 = QPixmap("music-file.png")
        button1.clicked.connect(self.openfile)
        button1.setIcon(pixmap4)
        button1.setObjectName("filebtn")
        button1.move(10,350)

        #Pause button configuration
        self.PauseBtn = QPushButton(parent=self)
        self.pixmap2 = QPixmap("pause-64.png")
        self.PauseBtn.setIcon(self.pixmap2)
        self.PauseBtn.setObjectName("Resume")
        self.PauseBtn.move(238,270)
        self.PauseBtn.clicked.connect(self.pauseaud)

        #Resume button configuration
        self.Resume = QPushButton(parent=self)
        self.pixmap1 = QPixmap("play-64.png")
        self.Resume.setIcon(self.pixmap1)
        self.Resume.setObjectName("Resume")
        self.Resume.move(238,270)
        self.Resume.hide()
        self.Resume.clicked.connect(self.continueaud)

        #seek forward button configuration
        self.seekfor = QPushButton(text=">>",parent=self)
        self.seekfor.setObjectName("seekf")
        self.seekfor.move(350,270)
        self.seekfor.clicked.connect(self.moveforward)

        #seek backward button configuration
        self.seekback = QPushButton(text="<<", parent=self)
        self.seekback.setObjectName("seekb")
        self.seekback.move(125, 270)
        self.seekback.clicked.connect(self.movebackward)

        #Timeline configuration
        ghost_timeline = QWidget(self)
        ghost_timeline.setObjectName("gsttime")
        ghost_timeline.resize(530,10)
        ghost_timeline.move(0,230)
        self.timeline = QWidget(self)
        self.timeline.setObjectName("timeline")
        self.timeline.move(0,230)
        self.timeline.resize(0,10)
        
        #Total duration lable configuration:
        self.totalduration = QLabel(self,text= f"{int(self.playback.duration/60)}:{self.playback.duration%60}")
        self.totalduration.setObjectName("totaldur")
        self.totalduration.move(490,250)

        #Timestamp lable configuration
        self.timestamp = QLabel(self, text= "0:00")
        self.timestamp.setObjectName("timestamp")
        self.timestamp.move(10,250)

        #Central logo configuration
        self.frame = QLabel(self)
        self.frame.resize(120,120)
        self.frame.setObjectName("frame")
        self.frame.move(200,70)
        self.pixmap3 = QPixmap("music.png")
        self.pixmap3 = self.pixmap3.scaledToWidth(120)
        self.frame.setPixmap(self.pixmap3)

        #Application window allingment.
        self.setGeometry(100,200,500,420)
        self.setMaximumSize(530,400)
        self.setMinimumSize(530,400)
        self.setWindowTitle("Music App")
        self.windowico = QPixmap("note.png")
        self.setWindowIcon(self.windowico)
        self.setObjectName("main")


    #seek forward:
    def movebackward(self):
        self.playback.seek(self.playback.curr_pos - 10.0)
        self.anim1.setCurrentTime(self.anim1.currentTime() - 10000)

    #seek backward:
    def moveforward(self):
        self.playback.seek(self.playback.curr_pos + 10.0)
        self.anim1.setCurrentTime( self.anim1.currentTime() + 10000)

    #Resume/Continue audio
    def continueaud(self):
        try:
            self.playback.resume()
            self.Resume.hide()
            self.anim1.resume()
            self.timer.timeout.connect(self.update_time)
        except:
            print("Please select a music file!")
    
    #pause Audio
    def pauseaud(self):
        try:
            self.playback.pause()
            self.Resume.show()
            self.anim1.pause()
            self.timer.timeout.disconnect()
        except:
            print("Please select a music file!")

    #Select file
    def openfile(self):

        #setting previous file directory
        if self.openfiledir != "":
            self.prev = self.openfiledir

        #Open file dialog
        self.filedil = QFileDialog(self)
        self.openfiledir = self.filedil.getOpenFileName(options=QFileDialog.DontUseNativeDialog)[0]
        self.filedil.close()
        self.Resume.hide() #Hinding the resume button by default as this is not required during play!

        #stoping previous playback
        if(self.playback.active):
            self.playback.stop()
        
        #loading music file and running
        self.playback.load_file(path_to_file=self.openfiledir)
        self.playback.play()
        self.playback.loop_at_end(True)

        #setting the initial value of previous file directory
        if self.prev == "":
            self.prev = self.openfiledir
        
        #Timeline animation
        self.timeline.resize(0,10)
        self.anim1 = QPropertyAnimation(self.timeline,b"size")
        self.anim1.setEndValue(QSize(530,10))
        self.anim1.setDuration(self.playback.duration * 1000)
        self.anim1.start()
        self.anim1.setLoopCount(100) #selecting a high value just for safety !

        #Totalduration lable setup
        self.totalduration.setText(f"{int(self.playback.duration/60)}:{int(self.playback.duration%60)}")

        #Timestamp lable setup/updation
        self.minute = 0
        self.second = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timestamp.setText(f"{self.minute}:{self.second}")
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

        print(self.prev) #now we just need to use this previous file to load the previous file separately. Maybe a hard task!
        #TODO: Leaving this to future me, to implement the previous music with the previous button.
        print(f"Currently playing {self.openfiledir}") #for testing
    
    #update Timestamp lable
    def update_time(self):
        self.minute = int(self.playback.curr_pos/60)
        self.second = int(self.playback.curr_pos%60)
        self.timestamp.setText(f"{self.minute}:{self.second}")

#creating an instance of application
app = QApplication([])
myapp = MyApplication()
myapp.show()
with open("style.qss","r") as f:
    _style = f.read()
    app.setStyleSheet(_style)
app.exec()
