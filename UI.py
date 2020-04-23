import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QGridLayout,QHBoxLayout,QVBoxLayout,QFrame,QCheckBox,QGraphicsDropShadowEffect
import math

class splashWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,350)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()
    
    def initUI(self):
        lbl = QLabel("Puzzle Game")
        hb = QHBoxLayout()
        hb.addWidget(lbl)
        self.setLayout(hb)
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
    QLabel{
        padding-left: 10px;
        padding-right: 10px;
        color: white;
    }
    """

    def initUI(self):
        lbl = QLabel("Square Puzzle Mania")
        self.new_game_btn = QPushButton("New Game")
        self.score_btn = QPushButton("View Score")
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

        """grid = QGridLayout()
        grid.addWidget(lbl,0,0,1,5)
        grid.addWidget(self.new_game_btn,2,2,1,1)
        grid.addWidget(self.score_btn,4,2,1,1)
        grid.addWidget(self.settings_btn,6,2,1,1)
        grid.addWidget(self.help_btn,8,2,1,1)
        grid.addWidget(self.quit_btn,10,2,1,1)

        grid.setRowStretch(0,2)
        for i in range(1,12):
            grid.setRowStretch(i,1)
        for i in range(5):
            grid.setColumnStretch(i,1)"""

        hbox = QHBoxLayout()
        hbox.addWidget(lbl,5)
        hbox.addStretch(1)
        hbox.addLayout(vbox,2)
        hbox.addStretch(2)

        self.setLayout(hbox)

        self.quit_btn.clicked.connect(sys.exit)

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
        #print("height",height,"width",width)
        self.setFixedSize(self.width,self.height)
        #self.setWindowTitle("Puzzle game")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #self.showFullScreen()
        self.initUI(no_of_tiles)

    right_style = """
    QPushButton{
        border: 0px solid black;
        font: 40px bold;
        font-family: MV Boli;
        color: white;
    }
    QLabel#obj_1{
        border : 3px solid white;
        border-radius : 5px;
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
                #if i==j and i==no_of_tiles-1:
                #    break
                temp.append(QPushButton(''))#temp.append(QPushButton('{}X{}'.format(i,j)))
            self.tiles.append(temp)

        print(self.tiles[0][0].width(),self.tiles[0][0].height())

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
        self.r_grid.setRowStretch(0,1)
        self.r_grid.setRowStretch(1,1)
        self.r_grid.setRowStretch(2,1)
        self.r_grid.setRowStretch(3,1)
        self.r_grid.setRowStretch(4,1)
        self.r_grid.setRowStretch(5,1)
        self.r_grid.setRowStretch(6,1)
        self.r_grid.setRowStretch(7,1)
        self.r_grid.setRowStretch(8,1)
        self.r_grid.setRowStretch(9,1)
        self.r_grid.setRowStretch(10,1)
        self.r_grid.setRowStretch(11,1)
        self.r_grid.setRowStretch(12,1)
        self.r_grid.setRowStretch(13,1)
        self.r_grid.setRowStretch(14,1)
        self.r_grid.setRowStretch(15,1)
        self.r_grid.setRowStretch(16,1)

        self.r_frame = QFrame()
        self.r_frame.setLayout(self.r_grid)
        
        #self.setStyleSheet(open('Style.css').read())

        # For game tiles
        self.grid = QGridLayout()

        for i in range(no_of_tiles):
            for j in range(no_of_tiles):
                #if i==j and i==no_of_tiles-1:
                #    break
                self.tiles[i][j].setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
                self.tiles[i][j].setFlat(True)
                self.tiles[i][j].setStyleSheet('border:0px solid black')
                self.grid.addWidget(self.tiles[i][j],i,j,1,1)

        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)
        
        #self.back_btn.clicked.connect(self.func)


        #g = math.gcd(self.width(),self.height())
        #x = self.width()//g
        #y = self.height()//g

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.grid,8)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.r_frame,5)
        self.setLayout(self.hbox)

        #self.img_lbl.setMaximumSize(450,450)
        #self.img_lbl.setPixmap(QtGui.QPixmap('images/flower.jpg').scaled(450,450,QtCore.Qt.KeepAspectRatio))
        self.img_lbl.setAlignment(QtCore.Qt.AlignHCenter)

        image = QtGui.QPixmap('images/bg01.jpg')
        #image = image.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(image))
        self.setPalette(palette)

        image = QtGui.QPixmap('images/bg02.jpg')
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
        print(self.tiles[0][0].size())
        print(self.tiles[0][0].width(),self.tiles[0][0].height())
        

    #def func(self):
    #    sys.exit()

class pauseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,550)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()
    
    def initUI(self):
        lbl = QLabel("Game Paused")
        time_lbl = QLabel("Time Taken : ")
        self.time_val_lbl = QLabel("")
        move_lbl = QLabel("No of Moves : ")
        self.move_val_lbl = QLabel("")
        help_lbl = QLabel("No of Help Taken : ")
        self.help_val_lbl = QLabel("")
        self.menu_btn = QPushButton("Main Menu")
        self.resume_btn = QPushButton("Resume Game")
        self.sound_on = QCheckBox("Sound")

        #self.menu_btn.clicked.connect(sys.exit)#################

        grid = QGridLayout()
        grid.addWidget(lbl,0,1,1,3)
        grid.addWidget(time_lbl,1,1,1,1)
        grid.addWidget(self.time_val_lbl,1,3,1,1)
        grid.addWidget(move_lbl,2,1,1,1)
        grid.addWidget(self.move_val_lbl,2,3,1,1)
        grid.addWidget(help_lbl,3,1,1,1)
        grid.addWidget(self.help_val_lbl,3,3,1,1)
        #grid.addWidget(score_lbl,4,1,1,1)
        #grid.addWidget(self.score_val_lbl,4,3,1,1)
        grid.addWidget(self.sound_on,4,2,1,1)
        grid.addWidget(self.resume_btn,6,1,1,1)
        grid.addWidget(self.menu_btn,6,3,1,1)
        self.setLayout(grid)

        for i in range(8):
            grid.setRowStretch(i,1)
        for i in range(5):
            grid.setColumnStretch(i,1)

        self.show()

class gameOverWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,550)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.initUI()
    
    def initUI(self):
        lbl = QLabel("Game Over")
        time_lbl = QLabel("Time Taken : ")
        self.time_val_lbl = QLabel("")
        move_lbl = QLabel("No of Moves : ")
        self.move_val_lbl = QLabel("")
        help_lbl = QLabel("No of Help Taken : ")
        self.help_val_lbl = QLabel("")
        score_lbl = QLabel("Total Score : ")
        self.score_val_lbl = QLabel("")
        self.again_btn = QPushButton("Play Again")
        self.menu_btn = QPushButton("Return to Main Menu")

        self.menu_btn.clicked.connect(sys.exit)#################

        grid = QGridLayout()
        grid.addWidget(lbl,0,1,1,3)
        grid.addWidget(time_lbl,1,1,1,1)
        grid.addWidget(self.time_val_lbl,1,3,1,1)
        grid.addWidget(move_lbl,2,1,1,1)
        grid.addWidget(self.move_val_lbl,2,3,1,1)
        grid.addWidget(help_lbl,3,1,1,1)
        grid.addWidget(self.help_val_lbl,3,3,1,1)
        grid.addWidget(score_lbl,4,1,1,1)
        grid.addWidget(self.score_val_lbl,4,3,1,1)
        grid.addWidget(self.again_btn,6,1,1,1)
        grid.addWidget(self.menu_btn,6,3,1,1)
        self.setLayout(grid)

        for i in range(8):
            grid.setRowStretch(i,1)
        for i in range(5):
            grid.setColumnStretch(i,1)

        self.show()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = menuWindow()   #gameWindow(4)
    #win.show()
    sys.exit(app.exec_())
