from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QApplication,QWidget,QFrame,QLabel,QPushButton,QScrollArea,QVBoxLayout,QGridLayout

class helpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.height = QApplication.desktop().screenGeometry().height()
        self.width = QApplication.desktop().screenGeometry().width()
        #print("height",height,"width",width)
        self.setFixedSize(self.width,self.height)
        #self.setWindowTitle("Puzzle game")
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
        border: 3px solid white;
        border-radius: 5px;
        color: white;
    }
    QPushButton:hover{
        border: 3px solid rgb(176,196,222);
        border-radius: 5px;
        color: rgb(176,196,222);
    }
    '''

    def initUI(self):
        self.back_btn = QPushButton("Back to Main Menu")
        name_lbl = QLabel("Help")
        name_lbl.setFont(QtGui.QFont("Segoe Print",30,QtGui.QFont.Bold))
        name_lbl.setStyleSheet('color: rgb(230,230,250);padding-left: 100px;padding-right: 10px;')

        self.back_btn.setFont(QtGui.QFont("MV Boli",22,QtGui.QFont.Bold))
        txt_lbl = []
        for i in range(19):
            a = QLabel("")
            txt_lbl.append(a)
            txt_lbl[i].setObjectName('textLabel')
            txt_lbl[i].setWordWrap(True)
            txt_lbl[i].setTextFormat(QtCore.Qt.RichText)
            txt_lbl[i].setFont(QtGui.QFont("MV Boli",20))
            txt_lbl[i].setAlignment(QtCore.Qt.AlignTop)
            #txt_lbl[i].setStyleSheet(self.style)

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

        grid = QGridLayout()
        grid.addWidget(txt_lbl[0],0,1,1,3)
        grid.addWidget(txt_lbl[1],1,1,1,1)
        grid.addWidget(txt_lbl[2],1,2,1,1)
        #grid.addWidget(txt_lbl[])   #Add image
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
        #grid.addWidget(txt_lbl[])   #Add image
        grid.addWidget(txt_lbl[14],8,1,1,1)
        grid.addWidget(txt_lbl[15],8,2,1,1)
        #grid.addWidget(txt_lbl[])   #Add image
        grid.addWidget(txt_lbl[16],9,1,1,1)
        grid.addWidget(txt_lbl[17],9,2,1,2)
        grid.addWidget(txt_lbl[18],10,1,1,3)
        grid.addWidget(self.back_btn,12,3,1,1)

        #grid.setSpacing(20)
        grid.setVerticalSpacing(50)

        for i in range(15):
            grid.setRowStretch(i,1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,3)
        grid.setColumnStretch(2,5)
        grid.setColumnStretch(3,3)
        grid.setColumnStretch(4,1)
        

        ##################
        #grid.addWidget(self.back_btn,4,4,1,1)
        frame = QFrame()
        frame.setLayout(grid)

        scroll_page = QScrollArea()
        scroll_page.setWidgetResizable(True)
        #scroll_page.(True)
        scroll_page.setWidget(frame)

        scroll_page.setStyleSheet(self.style)

        vbox = QVBoxLayout()
        vbox.addWidget(name_lbl,2)
        vbox.addWidget(scroll_page,20)
        #vbox.addStretch(1)

        self.setLayout(vbox)

        img = QtGui.QPixmap("images/3.jpg")
        img = img.scaled(self.width,self.height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(img))
        self.setPalette(palette)

        self.show()

'''
app = QApplication(sys.argv)
win = helpWindow()
win.show()
sys.exit(app.exec_())'''