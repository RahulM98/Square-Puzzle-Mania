## Title: UI.py
## Name : UI
## @author : Rahul Manna
## Created on : 2020-04-07 17:58:12
## Description : Contains UI for several windows

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QGridLayout,QHBoxLayout,QVBoxLayout,QFrame,QCheckBox,QScrollArea,QGraphicsDropShadowEffect

class splashWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        self.setFixedSize(self.width,self.height)        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()
    
    def initUI(self):
        self.game_name_lbl = QLabel("Square Puzzle\nMania")
        self.game_name_lbl.resize(500,350)
        self.game_name_lbl.setFont(QtGui.QFont("Segoe Print",46,QtGui.QFont.Bold))
        self.game_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.game_name_lbl.setStyleSheet("color: white;")

        effect = QGraphicsDropShadowEffect()
        effect.setColor(QtGui.QColor(QtCore.Qt.gray))
        effect.setBlurRadius(15)
        self.game_name_lbl.setGraphicsEffect(effect)
        self.game_name_lbl.setWordWrap(True)

        self.co_name_lbl = QLabel("")
        self.co_name_lbl.setTextFormat(QtCore.Qt.RichText)
        self.co_name_lbl.setText("a<br><b>ManR</b><br>creation")
        self.co_name_lbl.setFont(QtGui.QFont("Gabriola",56))
        self.co_name_lbl.setStyleSheet('color:rgb(255,2,11)')
        self.co_name_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.game_name_lbl)
        self.setLayout(self.hbox)
        
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
        self.setPalette(palette)
        self.show()

class menuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        self.setFixedSize(self.width,self.height)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()

    style = """
    QPushButton{
        border: 5px solid white;
        padding: 8px;
        border-radius: 10px;
        color: white;
    }
    QPushButton:hover{
        border: 5px solid rgb(176,196,222);
        padding: 8px;
        border-radius: 10px;
        color: rgb(176,196,222);
    }
    QLabel{
        padding-left: 10px;
        padding-right: 10px;
        color: white;
    }
    """

    def initUI(self):
        lbl = QLabel("Square Puzzle Mania")
        self.new_game_btn = QPushButton("New Game")
        self.score_btn = QPushButton("High Scores")
        self.settings_btn = QPushButton("Settings")
        self.help_btn = QPushButton("Help")
        self.quit_btn = QPushButton("Quit Game")

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(self.new_game_btn,1)
        vbox.addStretch(1)
        vbox.addWidget(self.score_btn,1)
        vbox.addStretch(1)
        vbox.addWidget(self.settings_btn,1)
        vbox.addStretch(1)
        vbox.addWidget(self.help_btn,1)
        vbox.addStretch(1)
        vbox.addWidget(self.quit_btn,1)
        vbox.addStretch(2)

        hbox = QHBoxLayout()
        hbox.addWidget(lbl,5)
        hbox.addStretch(1)
        hbox.addLayout(vbox,2)
        hbox.addStretch(2)

        self.setLayout(hbox)

        effect = QGraphicsDropShadowEffect()
        effect.setColor(QtGui.QColor(QtCore.Qt.lightGray))
        effect.setBlurRadius(15)
        lbl.setGraphicsEffect(effect)
        lbl.setWordWrap(True)
        lbl.setAlignment(QtCore.Qt.AlignCenter)

        lbl.setFont(QtGui.QFont("Segoe Print",72,QtGui.QFont.Bold))
        self.new_game_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.score_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.settings_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.help_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.quit_btn.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))

        self.setStyleSheet(self.style)

        image = QtGui.QPixmap('images/menu_bg.jpg')
        image = image.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(image))
        self.setPalette(palette)

        self.show()

class gameWindow(QWidget):
    def __init__(self,no_of_tiles):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        self.setFixedSize(self.width,self.height)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI(no_of_tiles)

    right_style = """
    QPushButton{
        border: 0px solid black;
        font: 40px bold;
        font-family: MV Boli;
        color: white;
    }
    QPushButton:hover{
        border: 0px solid rgb(176,196,222);
        font: 40px bold;
        font-family: MV Boli;
        color: rgb(176,196,222);
    }
    QLabel#obj_1{
        border : 3px solid white;
        border-radius : 5px;
        background: rgb(112,128,144);
        font: 24px bold;
        font-family: MV Boli;
        color: white;
    }
    QLabel#obj_2{
        font: 26px bold;
        font-family: MV Boli;
        color: white;
    }
    QLabel#obj_3{
        border : 3px solid white;
        border-radius : 10px;
        font: 26px bold;
        font-family: MV Boli;
        color: white;
    }
    """

    def initUI(self,no_of_tiles):
        self.tiles = []
        for i in range(no_of_tiles):
            temp = []
            for j in range(no_of_tiles):
                temp.append(QPushButton(''))
            self.tiles.append(temp)

        self.img_lbl = QLabel("Image show")
        self.pause_btn = QPushButton("")
        self.hint_btn = QPushButton("")
        self.shuffle_btn = QPushButton("")
        self.time_lbl = QLabel("Time :")
        self.time_val_lbl = QLabel("00:00:00")
        self.move_lbl = QLabel("Move Left :")
        self.move_count_lbl = QLabel("0")
        self.hint_lbl = QLabel("Help Taken :")
        self.hint_count_lbl = QLabel("0")
        self.msg_lbl = QLabel("label")
        self.back_btn = QPushButton("Back to Main Menu")
        
        self.pause_btn.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        self.hint_btn.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        self.shuffle_btn.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        self.back_btn.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        self.pause_btn.setToolTip("Pause Game")
        self.hint_btn.setToolTip("Get Help By One Step")
        self.shuffle_btn.setToolTip("Shuffle Again")

        self.msg_lbl.setObjectName("obj_1")
        self.time_lbl.setObjectName("obj_2")
        self.time_val_lbl.setObjectName("obj_3")
        self.move_lbl.setObjectName("obj_2")
        self.hint_lbl.setObjectName("obj_2")
        self.move_count_lbl.setObjectName("obj_3")
        self.hint_count_lbl.setObjectName("obj_3")

        self.pause_btn.setFlat(True)
        self.hint_btn.setFlat(True)
        self.shuffle_btn.setFlat(True)
        self.back_btn.setFlat(True)

        #For right side panel
        self.r_grid = QGridLayout()
        self.r_grid.addWidget(self.img_lbl,1,1,3,3)
        self.r_grid.addWidget(self.pause_btn,5,1,1,1)
        self.r_grid.addWidget(self.hint_btn,5,2,1,1)
        self.r_grid.addWidget(self.shuffle_btn,5,3,1,1)
        self.r_grid.addWidget(self.msg_lbl,7,1,1,3)
        self.r_grid.addWidget(self.time_lbl,9,1,1,1)
        self.r_grid.addWidget(self.time_val_lbl,9,2,1,2)
        self.r_grid.addWidget(self.move_lbl,11,1,1,1)
        self.r_grid.addWidget(self.hint_lbl,11,3,1,1)
        self.r_grid.addWidget(self.move_count_lbl,13,1,1,1)
        self.r_grid.addWidget(self.hint_count_lbl,13,3,1,1)
        self.r_grid.addWidget(self.back_btn,15,1,1,3)
        #set column stretch
        self.r_grid.setColumnStretch(0,1)
        self.r_grid.setColumnStretch(1,2)
        self.r_grid.setColumnStretch(2,2)
        self.r_grid.setColumnStretch(3,2)
        self.r_grid.setColumnStretch(4,1)
        #set row stretch
        for i in range(17):
            self.r_grid.setRowStretch(i,1)

        self.r_frame = QFrame()
        self.r_frame.setLayout(self.r_grid)

        # For game tiles
        self.grid = QGridLayout()

        for i in range(no_of_tiles):
            for j in range(no_of_tiles):
                self.tiles[i][j].setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
                self.tiles[i][j].setFlat(True)
                self.tiles[i][j].setStyleSheet('border:0px solid black')
                self.grid.addWidget(self.tiles[i][j],i,j,1,1)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.grid,8)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.r_frame,5)
        self.setLayout(self.hbox)

        self.img_lbl.setAlignment(QtCore.Qt.AlignHCenter)

        image = QtGui.QPixmap('images/bg2.jpg')
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(image))
        self.setPalette(palette)

        image = QtGui.QPixmap('images/bg3.jpg')
        image = image.scaled(self.r_frame.width(),self.r_frame.height())
        palette.setBrush(self.r_frame.backgroundRole(),QtGui.QBrush(image))
        self.r_frame.setAutoFillBackground(True)
        self.r_frame.setPalette(palette)

        self.pause_btn.setIcon(QtGui.QIcon('images/pause.png'))
        self.hint_btn.setIcon(QtGui.QIcon("images/hint.png"))
        self.shuffle_btn.setIcon(QtGui.QIcon("images/shuffle.png"))
        self.pause_btn.setIconSize(QtCore.QSize(50,50))
        self.hint_btn.setIconSize(QtCore.QSize(50,50))
        self.shuffle_btn.setIconSize(QtCore.QSize(50,50))

        self.pause_btn.setStyleSheet(self.right_style)
        self.hint_btn.setStyleSheet(self.right_style)
        self.shuffle_btn.setStyleSheet(self.right_style)
        self.back_btn.setStyleSheet(self.right_style)

        self.move_lbl.setStyleSheet(self.right_style)
        self.move_count_lbl.setStyleSheet(self.right_style)
        self.time_lbl.setStyleSheet(self.right_style)
        self.time_val_lbl.setStyleSheet(self.right_style)
        self.hint_lbl.setStyleSheet(self.right_style)
        self.hint_count_lbl.setStyleSheet(self.right_style)
        self.msg_lbl.setStyleSheet(self.right_style)
        
        self.time_val_lbl.setAlignment(QtCore.Qt.AlignRight)

        self.show()

class pauseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,500)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()
    
    style = '''
    QWidget{
        background: rgb(240,230,140);
    }
    QLabel{
        color: rgb(107,37,4);
    }
    QPushButton{
        border: 5px solid rgb(165,81,5);
        padding: 15px;
        border-radius: 10px;
        color: rgb(107,37,4);
    }
    QPushButton:hover{
        border: 5px solid rgb(107,37,4);
        padding: 15px;
        border-radius: 10px;
        color: rgb(165,81,5);
    }
    QCheckBox{
        color: rgb(107,37,4);
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
    '''

    def initUI(self):
        lbl = QLabel("Game Paused")
        self.sound_on_check = QCheckBox("Sound")
        self.resume_btn = QPushButton("Resume")
        self.settings_btn = QPushButton("Settings")
        self.menu_btn = QPushButton("Main Menu")

        grid = QGridLayout()
        grid.addWidget(lbl,0,2,2,3)
        grid.addWidget(self.sound_on_check,3,3,1,1)
        grid.addWidget(self.resume_btn,5,1,1,1)
        grid.addWidget(self.settings_btn,5,3,1,1)
        grid.addWidget(self.menu_btn,5,5,1,1)
        self.setLayout(grid)

        for i in range(7):
            grid.setRowStretch(i,1)
            grid.setColumnStretch(i,1)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.setFont(QtGui.QFont("MV Boli",30,QtGui.QFont.Bold))
        self.sound_on_check.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))
        self.resume_btn.setFont(QtGui.QFont("MV Boli",16,QtGui.QFont.Bold))
        self.settings_btn.setFont(QtGui.QFont("MV Boli",16,QtGui.QFont.Bold))
        self.menu_btn.setFont(QtGui.QFont("MV Boli",16,QtGui.QFont.Bold))

        self.resume_btn.setToolTip("Resume Game")
        self.settings_btn.setToolTip("Change Level and Image")
        self.menu_btn.setToolTip("Return to Main Menu")

        self.setStyleSheet(self.style)

        self.show()

class gameOverWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        self.setFixedSize(self.width,self.height)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()
    
    style = '''
    QLabel#blue_text{
        color: rgb(0,0,139);
    }
    QLabel#white_text{
        padding: 4px;
        color: rgb(243,243,244);
    }
    QPushButton#blue_text{
        padding: 5px;
        color: rgb(0,0,139);
        border:5px solid rgb(0,0,139);
        border-radius: 8px;
    }
    QPushButton#blue_text:hover{
        padding: 5px;
        color: rgb(0,0,255);
        border:5px solid rgb(0,0,255);
        border-radius: 8px;
    }
    QPushButton#white_text{
        padding: 5px;
        color: rgb(243,243,244);
        border:5px solid rgb(243,243,244);
        border-radius: 8px;
    }
    QPushButton#white_text:hover{
        padding: 5px;
        color: rgb(176,196,222);
        border:5px solid rgb(176,196,222);
        border-radius: 8px;
    }
    '''
    def initUI(self):
        lbl = QLabel("Game Over")
        lvl_lbl= QLabel("Level")
        self.lvl_val_lbl = QLabel("")
        time_lbl = QLabel("Time Taken")
        self.time_val_lbl = QLabel("")
        move_lbl = QLabel("Moves Used")
        self.move_val_lbl = QLabel("")
        help_lbl = QLabel("Help Taken")
        self.help_val_lbl = QLabel("")
        score_lbl = QLabel("Total Score")
        self.score_val_lbl = QLabel("")
        self.again_btn = QPushButton("Play Again")
        self.menu_btn = QPushButton("Main Menu")

        grid = QGridLayout()
        grid.addWidget(lbl,1,2,1,1)
        grid.addWidget(lvl_lbl,3,1,1,1)
        grid.addWidget(self.lvl_val_lbl,3,3,1,1)
        grid.addWidget(time_lbl,4,1,1,1)
        grid.addWidget(self.time_val_lbl,4,3,1,1)
        grid.addWidget(move_lbl,5,1,1,1)
        grid.addWidget(self.move_val_lbl,5,3,1,1)
        grid.addWidget(help_lbl,6,1,1,1)
        grid.addWidget(self.help_val_lbl,6,3,1,1)
        grid.addWidget(score_lbl,7,1,1,1)
        grid.addWidget(self.score_val_lbl,7,3,1,1)
        grid.addWidget(self.menu_btn,9,1,1,1)
        grid.addWidget(self.again_btn,9,3,1,1)
        self.setLayout(grid)
        for i in range(11):
            grid.setRowStretch(i,1)
        for i in range(5):
            grid.setColumnStretch(i,1)

        lbl.setObjectName("white_text")
        lvl_lbl.setObjectName("blue_text")
        time_lbl.setObjectName("blue_text")
        move_lbl.setObjectName("blue_text")
        help_lbl.setObjectName("blue_text")
        score_lbl.setObjectName("blue_text")
        self.lvl_val_lbl.setObjectName("white_text")
        self.time_val_lbl.setObjectName("white_text")
        self.move_val_lbl.setObjectName("white_text")
        self.help_val_lbl.setObjectName("white_text")
        self.score_val_lbl.setObjectName("white_text")
        self.again_btn.setObjectName("white_text")
        self.menu_btn.setObjectName("blue_text")

        lbl.setFont(QtGui.QFont("MV Boli",40,QtGui.QFont.Bold))
        lvl_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        time_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        move_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        help_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        score_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.lvl_val_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.time_val_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.move_val_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.help_val_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.score_val_lbl.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.again_btn.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))
        self.menu_btn.setFont(QtGui.QFont("MV Boli",28,QtGui.QFont.Bold))

        lbl.setAlignment(QtCore.Qt.AlignRight)
        lvl_lbl.setAlignment(QtCore.Qt.AlignCenter)
        time_lbl.setAlignment(QtCore.Qt.AlignCenter)
        move_lbl.setAlignment(QtCore.Qt.AlignCenter)
        help_lbl.setAlignment(QtCore.Qt.AlignCenter)
        score_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lvl_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.time_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.move_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.help_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.score_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        
        image = QtGui.QPixmap('images/bg6.jpg')
        image = image.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(image))
        self.setPalette(palette)
        self.setStyleSheet(self.style)
        self.show()


class scoreWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        self.setFixedSize(self.width,self.height)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()

    style = """
    QFrame{
        background-color: transparent;
        border: 0px solid white;
    }
    QScrollArea{
        border-top: 5px ridge rgb(240,240,240);
        border-bottom: 5px ridge rgb(240,240,240);
        border-left: 5px ridge rgb(240,240,240);
        border-right: 1px ridge rgb(240,240,240);
    }
    QLabel{
        padding: 5px;
        color: white;
    }
    QLabel#header{
        padding: 20px;
        color: rgb(230,230,250);
    }
    QLabel#underline{
        padding: 20px;
        color: white;
        text-decoration: underline;
    }
    QPushButton{
        padding: 10px;
        color: white;
        border: 5px solid white;
        border-radius:6px;
    }
    QPushButton:hover{
        border: 5px solid rgb(119,136,153);
        border-radius:6px;
        padding: 10px;
        color: rgb(119,136,153);
    }
    """

    def initUI(self):
        lbl = QLabel("High Scores")
        lbl.setFont(QtGui.QFont("Segoe Print",30,QtGui.QFont.Bold))
        lbl.setObjectName('header')

        beginner_lbl = QLabel("Beginner")
        easy_lbl = QLabel("Easy")
        medium_lbl = QLabel("Medium")
        hard_lbl = QLabel("Hard")
        self.back_btn = QPushButton("Return to Menu")

        headers = ['High Score','Moves Used','Hints Taken','Time Taken','Played On']

        self.table_value_lbl = []
        for i in range(80):
            self.table_value_lbl.append(QLabel("A"))
            self.table_value_lbl[i].setAlignment(QtCore.Qt.AlignCenter)
            self.table_value_lbl[i].setFont(QtGui.QFont("MV Boli",20))
        
        beginner_lbl.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))
        easy_lbl.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))
        medium_lbl.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))
        hard_lbl.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))
        self.back_btn.setFont(QtGui.QFont("MV Boli",24,QtGui.QFont.Bold))

        c = 0   #table val lbl count

        grid = QGridLayout()
        #Beginner level
        grid.addWidget(beginner_lbl,3,1,2,1)
        #header
        for i in range(len(headers)):
            self.table_value_lbl[c].setText(headers[i])
            grid.addWidget(self.table_value_lbl[c],5,i+1,1,1)
            self.table_value_lbl[c].setObjectName('underline')
            c+=1
        for i in range(3):
            for j in range(5):
                grid.addWidget(self.table_value_lbl[c],i+6,j+1,1,1)
                c+=1
        
        #easy level
        grid.addWidget(easy_lbl,11,1,2,1)
        #header
        for i in range(len(headers)):
            self.table_value_lbl[c].setText(headers[i])
            grid.addWidget(self.table_value_lbl[c],13,i+1,1,1)
            self.table_value_lbl[c].setObjectName('underline')
            c+=1
        for i in range(3):
            for j in range(5):
                grid.addWidget(self.table_value_lbl[c],i+14,j+1,1,1)
                c+=1

        #medium level
        grid.addWidget(medium_lbl,18,1,2,1)
        #header
        for i in range(len(headers)):
            self.table_value_lbl[c].setText(headers[i])
            grid.addWidget(self.table_value_lbl[c],20,i+1,1,1)
            self.table_value_lbl[c].setObjectName('underline')
            c+=1
        for i in range(3):
            for j in range(5):
                grid.addWidget(self.table_value_lbl[c],i+21,j+1,1,1)
                c+=1
        
        #hard level
        grid.addWidget(hard_lbl,25,1,2,1)
        #header
        for i in range(len(headers)):
            self.table_value_lbl[c].setText(headers[i])
            grid.addWidget(self.table_value_lbl[c],27,i+1,1,1)
            self.table_value_lbl[c].setObjectName('underline')
            c+=1
        for i in range(3):
            for j in range(5):
                grid.addWidget(self.table_value_lbl[c],i+28,j+1,1,1)
                c+=1

        for i in range(31):
            grid.setRowStretch(i,1)
        for i in range(7):
            grid.setColumnStretch(i,7)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(6,1)

        frame = QFrame()
        frame.setLayout(grid)

        scroll_page = QScrollArea()
        scroll_page.setWidget(frame)
        scroll_page.setWidgetResizable(True)

        main_grid = QGridLayout()
        main_grid.addWidget(lbl,1,1,2,2)
        main_grid.addWidget(scroll_page,3,1,24,7)
        main_grid.addWidget(self.back_btn,28,5,1,2)

        for i in range(30):
            main_grid.setRowStretch(i,1)

        self.setLayout(main_grid)

        image = QtGui.QPixmap('images/6.jpg')
        image = image.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(image))
        self.setPalette(palette)

        self.setStyleSheet(self.style)

        self.show()

class helpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        self.setFixedSize(self.width,self.height)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.initUI()

    style = '''
    QLabel#textLabel{
        color : white;
        padding: 10px;
    }
    QFrame{
        background: transparent;
    }
    QScrollArea{
        border-top: 3px solid rgb(240,240,240);
        border-bottom: 3px solid rgb(240,240,240);
        border-left: 3px solid rgb(240,240,240);
        border-right: 0px solid rgb(240,240,240);
    }
    QPushButton{
        padding: 10px;
        border: 3px solid white;
        border-radius: 5px;
        color: white;
    }
    QPushButton:hover{
        padding: 10px;
        border: 3px solid rgb(176,196,222);
        border-radius: 5px;
        color: rgb(176,196,222);
    }
    '''

    def initUI(self):
        self.back_btn = QPushButton("Return to Menu")
        name_lbl = QLabel("Help")
        name_lbl.setFont(QtGui.QFont("Segoe Print",30,QtGui.QFont.Bold))
        name_lbl.setStyleSheet('color: rgb(230,230,250);padding-left: 100px;padding-right: 10px;')
        
        self.img_lbl1 = QLabel("")
        self.img_lbl2 = QLabel("")
        self.img_lbl3 = QLabel("")
        
        self.back_btn.setFont(QtGui.QFont("MV Boli",22,QtGui.QFont.Bold))
        self.back_btn.setStyleSheet(self.style)
        txt_lbl = []
        for i in range(20):
            a = QLabel("")
            txt_lbl.append(a)
            txt_lbl[i].setObjectName('textLabel')
            txt_lbl[i].setWordWrap(True)
            txt_lbl[i].setTextFormat(QtCore.Qt.RichText)
            txt_lbl[i].setFont(QtGui.QFont("MV Boli",20))
            txt_lbl[i].setAlignment(QtCore.Qt.AlignTop)

        txt_lbl[0].setText('''<b><u>Square Puzzle Mania</u></b> is a classical sliding puzzle game consisting of a puzzle that has been divided in 
                            N x N tiles. One tile is taken out and the others are shuffled. The objective is to rearrange the puzzle into its
                             correct original order by moving the tiles.''')
        txt_lbl[1].setText('''<b><u>Movement</u> : </b>''')
        txt_lbl[2].setText('''To move a tile, all you need to do is just a click on the tile and the tile will be moved to the blank space at once.''')
        txt_lbl[3].setText('''The game comes with four difficulty levels.''')
        txt_lbl[4].setText('''<b>1. <u>Beginner</u> : </b>''')
        txt_lbl[5].setText('''You will get 8 tiles to solve where number of movements is limited. If you have never played puzzle before this 
                            level is recommended for you to start.''')
        txt_lbl[6].setText('''<b>2. <u>Easy</u> : </b>''')
        txt_lbl[7].setText('''You have 15 number of tiles to arrange with a limited number of movements.''')
        txt_lbl[8].setText('''<b>3. <u>Medium</u> : </b>''')
        txt_lbl[9].setText('''The difficulty level gets higher as you get 24 tiles to arrange properly in a limited number of movements. 
                            However, the score gets higher with a higher level of difficulty.''')
        txt_lbl[10].setText('''<b>4. <u>Hard</u> : </b>''')
        txt_lbl[11].setText('''If you are pro at solving puzzles, this level is just for you. You get 24 tiles where the number of movements 
                            is not limited at all. If you find this level easy, the game has another feature <b><u>Shuffle</u></b> to increase difficulty.''')
        txt_lbl[12].setText('''<b><u>Shuffle Feature</u> : </b>''')
        txt_lbl[13].setText('''The game is too easy ?? Just click on the <b><u>Shuffle</u></b> button to reshuffle the tiles to increase difficulty. The more
                             number of shuffling the more score. However, this feature is available only at <b><u>Hard</u></b> level.''')
        txt_lbl[14].setText('''<b><u>Hint Feature</u> : </b>''')
        txt_lbl[15].setText('''Got stuck in a game? Never mind, just click on the <b><u>Hint</u></b> button, you will get help for a movement. This feature 
                            is not available in <b><u>Hard</u></b> level.''')
        txt_lbl[16].setText('''<b><u>Score Calculation</u> : </b>''')
        txt_lbl[17].setText('''The score is calculated using a hidden formula. The more number of Hint used the less score. The lesser number of 
                            moves used the more score.''')
        txt_lbl[18].setText('''Thank you very much for reading this much. Hope you like the game. <b>:D</b>''')
        txt_lbl[19].setText('''<font face="Gabriola" size="12"><b>~~ ManR</b></font>''')

        grid = QGridLayout()
        grid.addWidget(txt_lbl[0],0,1,1,3)
        grid.addWidget(txt_lbl[1],1,1,1,1)
        grid.addWidget(txt_lbl[2],1,2,1,1)
        grid.addWidget(self.img_lbl1,1,3,1,1)   #Add image
        grid.addWidget(txt_lbl[3],2,1,1,3)
        grid.addWidget(txt_lbl[4],3,1,1,1)
        grid.addWidget(txt_lbl[5],3,2,1,2)
        grid.addWidget(txt_lbl[6],4,1,1,1)
        grid.addWidget(txt_lbl[7],4,2,1,2)
        grid.addWidget(txt_lbl[8],5,1,1,1)
        grid.addWidget(txt_lbl[9],5,2,1,2)
        grid.addWidget(txt_lbl[10],6,1,1,1)
        grid.addWidget(txt_lbl[11],6,2,1,2)
        grid.addWidget(txt_lbl[12],7,1,1,1)
        grid.addWidget(txt_lbl[13],7,2,1,1)
        grid.addWidget(self.img_lbl2,7,3,1,1)   #Add image
        grid.addWidget(txt_lbl[14],8,1,1,1)
        grid.addWidget(txt_lbl[15],8,2,1,1)
        grid.addWidget(self.img_lbl3,8,3,1,1)   #Add image
        grid.addWidget(txt_lbl[16],9,1,1,1)
        grid.addWidget(txt_lbl[17],9,2,1,2)
        grid.addWidget(txt_lbl[18],10,1,1,3)
        grid.addWidget(txt_lbl[19],12,3,1,1)

        grid.setVerticalSpacing(50)

        for i in range(15):
            grid.setRowStretch(i,1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,3)
        grid.setColumnStretch(2,5)
        grid.setColumnStretch(3,3)
        grid.setColumnStretch(4,1)
        
        frame = QFrame()
        frame.setLayout(grid)

        scroll_page = QScrollArea()
        scroll_page.setWidgetResizable(True)
        scroll_page.setWidget(frame)

        scroll_page.setStyleSheet(self.style)

        hbox = QHBoxLayout()
        hbox.addStretch(3)
        hbox.addWidget(self.back_btn,1)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(name_lbl,2)
        vbox.addWidget(scroll_page,20)
        vbox.addLayout(hbox,1)

        self.setLayout(vbox)

        img = QtGui.QPixmap("images/bg4.jpg")
        img = img.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(img))
        self.setPalette(palette)

        self.show()

class dialogWindow(QWidget):
    #type1 = ok dialog | type2=y/n dialog
    def __init__(self,dlg_type,title,message):
        super().__init__()
        self.setFixedSize(450,250)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI(dlg_type,title,message)
    
    style = '''
    QWidget{
        padding: 15px;
    }
    QLabel{
        padding: 5px;
        color: rgb(107,37,4);
    }
    QPushButton{
        padding: 4px;
        color: rgb(107,37,4);
        border: 4px solid rgb(107,37,4);
        border-radius: 4px;
    }
    QPushButton:hover{
        padding: 4px;
        color: rgb(132,66,4);
        border: 4px solid rgb(132,66,4);
        border-radius: 4px;
    }
    '''

    def initUI(self,dlg_type,title,message):
        title_lbl = QLabel(title)
        msg_lbl = QLabel(message)
        self.ok_btn = QPushButton("Okay")
        self.yes_btn = QPushButton("Yes")
        self.no_btn = QPushButton("No")
        
        grid = QGridLayout()
        grid.addWidget(title_lbl,0,1,1,4)
        grid.addWidget(msg_lbl,1,0,2,6)
        if dlg_type == 2:
            grid.addWidget(self.yes_btn,4,1,1,1)
            grid.addWidget(self.no_btn,4,4,1,1)
        else:    # dlg_type == 1
            grid.addWidget(self.ok_btn,4,4,1,1)

        for i in range(6):
            grid.setColumnStretch(i,1)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)
        grid.setRowStretch(4,1)

        self.setLayout(grid)

        title_lbl.setFont(QtGui.QFont("MV Boli",20,QtGui.QFont.Bold))
        msg_lbl.setFont(QtGui.QFont("MV Boli",15,QtGui.QFont.Bold))
        self.ok_btn.setFont(QtGui.QFont("MV Boli",14,QtGui.QFont.Bold))
        self.yes_btn.setFont(QtGui.QFont("MV Boli",14,QtGui.QFont.Bold))
        self.no_btn.setFont(QtGui.QFont("MV Boli",14,QtGui.QFont.Bold))

        title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        msg_lbl.setAlignment(QtCore.Qt.AlignCenter)
        msg_lbl.setWordWrap(True)

        image = QtGui.QPixmap('images/dialog.jpg')
        image = image.scaled(450,250,QtCore.Qt.IgnoreAspectRatio)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(image))
        self.setPalette(palette)

        self.setStyleSheet(self.style)

        self.show()
