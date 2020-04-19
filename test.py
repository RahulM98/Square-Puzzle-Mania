# https://pythonprogramminglanguage.com/pyqt5-hello-world/
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    

class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer")
        self.resize(900,900)

        self.label = QLabel("Time",self)
        self.label.move(100,100)

        self.c = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.func)
        self.timer.start(1000)

        if self.c == 10:
            self.timer.stop()

    def func(self):
        print("a")
        self.c += 1
        self.label.setText(str(self.c))
        if self.c == 5:
            self.timer.stop()
            self.timer.start(2000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )


"""import os
import shutil
try:
    path = 'images/new'
    #os.mkdir(path)
    shutil.rmtree(path)
except OSError as e:
    print(e)"""