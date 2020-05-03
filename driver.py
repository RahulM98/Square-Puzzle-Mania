## Title: driver.py
## Name : 
## @author : Rahul Manna
## Created on : 2020-05-02 22:48:35
## Description : 

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from UI import splashWindow
from backend import Game

class driver():
    def __init__(self):
        self.half_second = 0
        self.timer = QTimer()
        self.init_win = splashWindow()
        self.timer.start(500)
        self.timer.timeout.connect(self.timer_handler)

    def timer_handler(self):
        self.half_second += 1
        if self.half_second == 5: #after 2.5 seconds
            d = self.init_win.hbox.takeAt(0)
            d.widget().deleteLater()
            pass
        elif self.half_second == 7: #after 3.5 seconds
            self.init_win.hbox.addWidget(self.init_win.co_name_lbl)
        elif self.half_second == 10: #after 5 seconds
            self.init_game = Game()
        elif self.half_second == 12: #after 6 seconds
            self.timer.stop()
            self.init_win.close()

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    d = driver()
    sys.exit(app.exec_())