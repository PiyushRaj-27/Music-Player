import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from just_playback import Playback
from pygame import mixer

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        text1 = QLabel(self,text="Music App")
        text1.setStyleSheet("""
            font-size: 30px;
            font-weight: bolder;
            font-family: arial;
        """)
        text1.move(180,50)
        self.openfiledir = ""
        button1 = QPushButton(text="Select A music file!", parent=self)
        button1.clicked.connect(self.openfile)
        button1.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 300px;
            background-color: black;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        button1.move(100,150)

        self.PauseBtn = QPushButton(text="Pause",parent=self)
        self.PauseBtn.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 100px;
            background-color: black;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        self.PauseBtn.move(200,200)
        self.PauseBtn.clicked.connect(self.pauseaud)
        self.Resume = QPushButton(text="Resume",parent=self)
        self.Resume.setStyleSheet("""
            QPushButton{
            font-size : 18px;
            width : 100px;
            background-color: black;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px;
            }
            QPushButton:hover{
                background-color: blue;
            }
        """)
        self.Resume.move(200,200)
        self.Resume.hide()
        self.Resume.clicked.connect(self.continueaud)
        self.setGeometry(100,200,500,400)
        self.setWindowTitle("Music App")
        self.setStyleSheet("""
            background-color: grey;
        """)

    def continueaud(self):
        mixer.music.unpause()
        self.Resume.hide()
    def pauseaud(self):
        mixer.music.pause()
        self.Resume.show()
        
    def openfile(self):
        self.openfiledir = QFileDialog(self).getOpenFileName()[0]
        mixer.init()
        mixer.music.load(self.openfiledir)
        mixer.music.play()
        print(self.openfiledir)
 

#creating a basic application
app = QApplication([])
myapp = MyApplication()
myapp.show()
app.exec()
