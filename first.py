from pydoc import plain
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QPropertyAnimation,QPoint,QSize
from just_playback import Playback
from pygame import mixer,error

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.playback = Playback()
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
        self.PauseBtn = QPushButton(text="Pause",parent=self)
        self.PauseBtn.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 100px;
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
        self.PauseBtn.move(200,270)
        self.PauseBtn.clicked.connect(self.pauseaud)

        #Resume button configuration
        self.Resume = QPushButton(text="Resume",parent=self)
        self.Resume.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 100px;
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
        self.Resume.move(200,270)
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
        # self.anim1 = QPropertyAnimation(self.timeline,b"size")
        # self.anim1.setEndValue(QSize(200,10))
        # self.anim1.setDuration(self.playback.duration * 1000)

        #Application window allingment.
        self.setGeometry(100,200,500,420)
        self.setMaximumSize(530,400)
        self.setMinimumSize(530,400)
        self.setWindowTitle("Music App")
        self.setStyleSheet("""
            background-color: black;
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
        except error :
            print("Please select a music file!")
    
    def pauseaud(self):
        try:
            
            self.playback.pause()
            self.Resume.show()
            self.anim1.pause()
        except:
            print("Please select a music file!")


    def openfile(self):
        self.filedil = QFileDialog(self)
        self.openfiledir = self.filedil.getOpenFileName(options=QFileDialog.DontUseNativeDialog)[0]
        self.filedil.close()
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
        print(f"Currently playing {self.openfiledir}")
 

#creating a basic application
app = QApplication([])
myapp = MyApplication()
myapp.show()
app.exec()
