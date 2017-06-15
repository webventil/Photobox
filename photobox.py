#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import datetime
import time
import threading
from subprocess import call
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import *
from time import *

class Example(QWidget):

    path = "images/"
    seconds = 5
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):

        self.center()
        #self.showFullScreen()

        self.originalPic = QLabel(self)
        self.originalPic.setPixmap(QPixmap(self.path + "resources/launch_screen.png").scaled(QSize(723,480), Qt.KeepAspectRatio))
        self.originalPic.show()
        self.originalPic.move(0,0)
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap(self.path + "resources/launch_screen.png").scaled(QSize(723,480), Qt.KeepAspectRatio))
        self.pic.show()
        self.pic.move(0,0)

        btn = QPushButton('', self)
        btn.clicked.connect(self.take_picture)
        btn.setStyleSheet("background-image: url(" + self.path + "resources/foto.png)")
        btn.resize(QSize(76,450))
        btn.move(723,0)
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(quit)
        qbtn.resize(btn.sizeHint())
        qbtn.setShortcut('Esc')
        qbtn.resize(QSize(76,30))
        qbtn.move(723,450)

        self.setFixedSize(800,480)
        self.setWindowTitle('PhotoBox')
        self.show()


    def quit(self):
        QCoreApplication.instance().quit
    
    def change_image(self):
        self.pic.setPixmap(QPixmap(self.path + "resources/" + str(self.seconds) + ".png").scaled(self.originalPic.size(), Qt.KeepAspectRatio))
        if self.seconds == 0:
            self.t = threading.Timer(1.0, self.take_picture_and_display)
            self.t.start()
            self.seconds = 5
        else:
            self.seconds -= 1
            self.t = threading.Timer(1.0, self.change_image)
            self.t.start()
            
    
    def take_picture(self):
        self.t = threading.Timer(1.0, self.change_image)
        self.t.start()

    def take_picture_and_display(self):
        photoPath = self.path + "photo-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        call (["gphoto2","--capture-image-and-download","--filename",photoPath])
        self.pic.setPixmap(QPixmap(photoPath).scaled(self.originalPic.size(), Qt.KeepAspectRatio))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_()) 
