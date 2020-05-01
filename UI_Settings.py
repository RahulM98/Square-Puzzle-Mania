## Title: UI_Settings.py
## Name : 
## @author : Rahul Manna
## Created on : 2020-04-23 17:34:47
## Description : 

import sys
import PyQt5
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication,QWidget,QCheckBox,QSlider,QPushButton,QLabel,QFrame,QStackedWidget,QVBoxLayout,QHBoxLayout,QGridLayout

class settingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        #print("height",height,"width",width)
        self.setFixedSize(self.width,self.height)
        #self.setWindowTitle("Puzzle game")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.initUI()

    l_style = """
    QPushButton{
        border: 0px solid white;
        padding: 15px;
        color: white;
    }
    QPushButton:hover{
        border: 0px solid rgb(119,136,153);
        padding: 15px;
        color: rgb(119,136,153);
    }
    QPushButton:checked{
        border: 5px solid white;
        border-radius: 20px;
        padding: 15px;
        color: white;
    }
    """

    r_style1 = """
    QPushButton{
        border: 3px solid rgb(0,0,128);
        border-radius: 20px;
        color: rgb(0,0,128);
        font: 30px Arial Bold;
    }
    QPushButton:hover{
        border: 3px solid rgb(148,0,211);
        border-radius: 20px;
        color: rgb(148,0,211);
        font: 30px Arial Bold;
    }
    QPushButton:pressed,:checked{
        border: 3px solid rgb(148,0,211);
        border-radius: 20px;
        background-color : rgb(0,0,128);
        color: white;
        font: 30px Arial Bold;
    }
    QPushButton:disabled{
        border: 3px solid rgb(128,128,128);
        border-radius: 20px;
        color: rgb(128,128,128);
        font: 30px Arial Bold;
    }
    """
    
    r_style2 = """
    QLabel{
        background-color:rgb(49,52,58);
        color:white;
        border:5px solid rgb(139,69,19);
        border-radius: 10px;
        padding: 20px;
    }
    QPushButton{
        border: 3px solid rgb(0,0,128);
        padding: 10px;
        border-radius: 20px;
        color: rgb(0,0,128);
    }
    QPushButton:hover{
        border: 3px solid rgb(148,0,211);
        padding: 10px;
        border-radius: 20px;
        color: rgb(139,69,19);
    }
    QPushButton:pressed,:checked{
        border: 3px solid rgb(148,0,211);
        padding: 10px;
        border-radius: 20px;
        background-color : rgb(189,183,107);
        color: rgb(139,69,19);
    }
    """

    r_style3 = """
    QFrame#f{
        background-color:rgb(238,232,170);
        border:3px solid rgb(139,69,19);
        border-radius: 5px;
        padding: 10px;
    }
    QCheckBox::indicator:checked{
        height: 35px;
        width: 35px;
        image: url('images/check.png');
    }
    QCheckBox::indicator:unchecked{
        height: 35px;
        width: 35px;
        image: url('images/uncheck.png');
    }
    QCheckBox::indicator:checked:pressed{
        height: 35px;
        width: 35px;
        image: url('images/check.png');
    }
    QCheckBox::indicator:unchecked:pressed{
        height: 35px;
        width: 35px;
        image: url('images/uncheck.png');
    }
    """

    def initUI(self):
        win_name_lbl = QLabel("Settings")
        win_name_lbl.setFont(QtGui.QFont("Segoe Print",30,QtGui.QFont.Bold))
        win_name_lbl.setStyleSheet('color: rgb(230,230,250);padding-left: 100px;padding-right: 10px;')

        #This is left side
        l_frame = QFrame()
        self.pic_btn = QPushButton("Change Picture")
        self.level_btn = QPushButton("Change Level")
        self.sound_btn = QPushButton("Sound")
        self.back_btn = QPushButton("Return to Menu")

        self.pic_btn.setCheckable(True)
        self.level_btn.setCheckable(True)
        self.sound_btn.setCheckable(True)

        self.pic_btn.setChecked(True)

        #self.back_btn.clicked.connect(sys.exit)##############

        l_grid = QGridLayout()
        l_grid.addWidget(self.pic_btn,0,1)
        l_grid.addWidget(self.level_btn,2,1)
        l_grid.addWidget(self.sound_btn,4,1)
        l_grid.addWidget(self.back_btn,6,1)

        for i in range(7):
            l_grid.setRowStretch(i,1)
        l_grid.setColumnStretch(0,1)
        l_grid.setColumnStretch(1,1)
        l_grid.setColumnStretch(2,1)
        
        l_frame.setLayout(l_grid)

        self.pic_btn.setFont(QtGui.QFont("MV Boli",25,QtGui.QFont.Bold))
        self.level_btn.setFont(QtGui.QFont("MV Boli",25,QtGui.QFont.Bold))
        self.sound_btn.setFont(QtGui.QFont("MV Boli",25,QtGui.QFont.Bold))
        self.back_btn.setFont(QtGui.QFont("MV Boli",25,QtGui.QFont.Bold))

        self.pic_btn.setStyleSheet(self.l_style)
        self.level_btn.setStyleSheet(self.l_style)
        self.sound_btn.setStyleSheet(self.l_style)
        self.back_btn.setStyleSheet(self.l_style)

        bg_img = QtGui.QPixmap('images/7.jpg')
        bg_img = bg_img.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(bg_img))
        self.setPalette(palette)

        #This is right side
        r_frame_img = QtGui.QPixmap('images/bg1.jpg')
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(r_frame_img))

        self.frame1 = QFrame()
        self.frame1.setAutoFillBackground(True)
        #palette.setBrush(self.backgroundRole(),QtGui.QBrush(r_frame_img))
        self.frame1.setPalette(palette)

        self.frame2 = QFrame()
        self.frame2.setAutoFillBackground(True)
        #palette.setBrush(self.backgroundRole(),QtGui.QBrush(r_frame_img))
        self.frame2.setPalette(palette)

        self.frame3 = QFrame()
        self.frame3.setAutoFillBackground(True)
        #palette.setBrush(self.backgroundRole(),QtGui.QBrush(r_frame_img))
        self.frame3.setPalette(palette)
        
        self.init_frame1()
        self.init_frame2()
        self.init_frame3()

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.frame1)
        self.stackedWidget.addWidget(self.frame2)
        self.stackedWidget.addWidget(self.frame3)

        #Part 1
        """self.img_lbl = QLabel("")
        self.left_img_btn = QPushButton("<")
        self.right_img_btn = QPushButton(">")
        self.select_img_btn = QPushButton("Select")

        self.r_grid_1 = QGridLayout()
        self.r_grid_1.addWidget(self.img_lbl,1,0,1,5)
        self.r_grid_1.addWidget(self.left_img_btn,3,1,1,1)
        self.r_grid_1.addWidget(self.select_img_btn,3,2,1,1)
        self.r_grid_1.addWidget(self.right_img_btn,3,3,1,1)
        
        self.r_grid_1.setColumnStretch(0,3)
        self.r_grid_1.setColumnStretch(1,1)
        self.r_grid_1.setColumnStretch(2,2)
        self.r_grid_1.setColumnStretch(3,1)
        self.r_grid_1.setColumnStretch(4,3)
        self.r_grid_1.setRowStretch(0,1)
        self.r_grid_1.setRowStretch(1,4)
        self.r_grid_1.setRowStretch(2,1)
        self.r_grid_1.setRowStretch(3,1)
        self.r_grid_1.setRowStretch(4,1)

        self.r_frame.setLayout(self.r_grid_1)

        self.select_img_btn.setCheckable(True)
        self.select_img_btn.setChecked(True)

        self.img_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.img_lbl.setStyleSheet('padding: 10px;border-top: 5px solid rgb(139,69,19);border-bottom: 5px solid rgb(139,69,19)')
        self.left_img_btn.setStyleSheet(self.r_style)
        self.right_img_btn.setStyleSheet(self.r_style)
        self.select_img_btn.setStyleSheet(self.r_style)"""

        #Part 2
        """level_lbl = QLabel("Choose Level")
        self.beginner_level_btn = QPushButton("Beginner")
        self.easy_level_btn = QPushButton("Easy")
        self.medium_level_btn = QPushButton("Medium")
        self.hard_level_btn = QPushButton("Hard")
        self.level_msg_lbl = QLabel("")

        self.r_grid_2 = QGridLayout()
        self.r_grid_2.addWidget(level_lbl,0,0)"""

        #Part 3

        main_grid = QGridLayout()
        main_grid.addWidget(win_name_lbl,0,0,1,1)
        main_grid.addWidget(l_frame,2,0,1,1)
        main_grid.addWidget(self.stackedWidget,1,1,2,1)

        main_grid.setRowStretch(0,1)
        main_grid.setRowStretch(1,1)
        main_grid.setRowStretch(2,7)

        main_grid.setColumnStretch(0,3)
        main_grid.setColumnStretch(1,5)

        self.setLayout(main_grid)

        self.show()

    def init_frame1(self):
        self.img_no_lbl = QLabel("00/22")
        self.img_lbl = QLabel("")
        self.left_img_btn = QPushButton("<")
        self.right_img_btn = QPushButton(">")
        self.select_img_btn = QPushButton("Select")

        r_grid_1 = QGridLayout()
        r_grid_1.addWidget(self.img_no_lbl,0,2,1,1)
        r_grid_1.addWidget(self.img_lbl,1,0,1,5)
        r_grid_1.addWidget(self.left_img_btn,3,1,1,1)
        r_grid_1.addWidget(self.select_img_btn,3,2,1,1)
        r_grid_1.addWidget(self.right_img_btn,3,3,1,1)
        
        r_grid_1.setColumnStretch(0,3)
        r_grid_1.setColumnStretch(1,1)
        r_grid_1.setColumnStretch(2,2)
        r_grid_1.setColumnStretch(3,1)
        r_grid_1.setColumnStretch(4,3)
        r_grid_1.setRowStretch(0,1)
        r_grid_1.setRowStretch(1,4)
        r_grid_1.setRowStretch(2,1)
        r_grid_1.setRowStretch(3,1)
        r_grid_1.setRowStretch(4,1)

        self.frame1.setLayout(r_grid_1)

        self.select_img_btn.setCheckable(True)

        self.img_no_lbl.setFont(QtGui.QFont("MV Boli",20,QtGui.QFont.Bold))

        self.img_no_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.img_no_lbl.setStyleSheet('color: rgb(0,0,128);border-color:rgb(139,69,19);border-style:solid;border-width:0 5px 0 5px;')
        self.img_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.img_lbl.setStyleSheet('padding: 10px;border-top: 5px solid rgb(139,69,19);border-bottom: 5px solid rgb(139,69,19);')
        self.left_img_btn.setStyleSheet(self.r_style1)
        self.right_img_btn.setStyleSheet(self.r_style1)
        self.select_img_btn.setStyleSheet(self.r_style1)

    def init_frame2(self):
        level_lbl = QLabel("Choose Level")
        self.beginner_level_btn = QPushButton("Beginner")
        self.easy_level_btn = QPushButton("Easy")
        self.medium_level_btn = QPushButton("Medium")
        self.hard_level_btn = QPushButton("Hard")
        self.level_msg_lbl = QLabel("")

        r_grid_2 = QGridLayout()
        r_grid_2.addWidget(level_lbl,0,0,1,6)
        r_grid_2.addWidget(self.beginner_level_btn,2,1,1,1)
        r_grid_2.addWidget(self.easy_level_btn,2,2,1,1)
        r_grid_2.addWidget(self.medium_level_btn,2,3,1,1)
        r_grid_2.addWidget(self.hard_level_btn,2,4,1,1)
        r_grid_2.addWidget(self.level_msg_lbl,4,1,2,4)

        for i in range(6):
            r_grid_2.setRowStretch(i,1)
            r_grid_2.setColumnStretch(i,1)
        r_grid_2.setRowStretch(6,1)

        r_grid_2.setSpacing(15)

        self.beginner_level_btn.setCheckable(True)
        self.easy_level_btn.setCheckable(True)
        self.medium_level_btn.setCheckable(True)
        self.hard_level_btn.setCheckable(True)

        self.beginner_level_btn.setStyleSheet(self.r_style2)
        self.easy_level_btn.setStyleSheet(self.r_style2)
        self.medium_level_btn.setStyleSheet(self.r_style2)
        self.hard_level_btn.setStyleSheet(self.r_style2)
        self.level_msg_lbl.setStyleSheet(self.r_style2)

        level_lbl.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))
        self.beginner_level_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.easy_level_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.medium_level_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.hard_level_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.level_msg_lbl.setFont(QtGui.QFont("Ink Free",25,QtGui.QFont.Bold))

        level_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.level_msg_lbl.setWordWrap(True)
        self.level_msg_lbl.setTextFormat(QtCore.Qt.RichText)

        self.frame2.setLayout(r_grid_2)

    def init_frame3(self):
        self.sound_on_check = QCheckBox("Sound")
        #self.sound_on_check.toggle()
        vol = QLabel("Volume : ")
        self.vol_value = QLabel("0")
        minimum = QLabel("0")
        maximum = QLabel("100")
        self.slider = QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)

        f = QFrame()
        f.setObjectName("f")
        f.setAutoFillBackground(True)
        h = QHBoxLayout()
        h.addWidget(self.slider)
        f.setLayout(h)
        f.setStyleSheet(self.r_style3)

        h1 = QHBoxLayout()
        h1.addStretch(1)
        h1.addWidget(self.sound_on_check,3)
        h1.addStretch(1)

        r_grid_3 = QGridLayout()
        r_grid_3.addLayout(h1,1,2,1,3)
        r_grid_3.addWidget(vol,3,2,1,2)
        r_grid_3.addWidget(self.vol_value,3,4,1,1)
        r_grid_3.addWidget(minimum,5,1,1,1)
        r_grid_3.addWidget(f,5,2,1,3)
        r_grid_3.addWidget(maximum,5,5,1,1)

        for i in range(7):
            r_grid_3.setRowStretch(i,1)
            r_grid_3.setColumnStretch(i,1)

        self.sound_on_check.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        vol.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.vol_value.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        minimum.setFont(QtGui.QFont("MV Boli",16,QtGui.QFont.Bold))
        maximum.setFont(QtGui.QFont("MV Boli",16,QtGui.QFont.Bold))
        self.slider.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))

        vol.setAlignment(QtCore.Qt.AlignCenter)
        minimum.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.vol_value.setAlignment(QtCore.Qt.AlignCenter)

        self.sound_on_check.setStyleSheet(self.r_style3)

        self.frame3.setLayout(r_grid_3)
        pass

'''
app = QApplication(sys.argv)
win = settingsWindow()
win.stackedWidget.setCurrentIndex(2)
sys.exit(app.exec_())'''