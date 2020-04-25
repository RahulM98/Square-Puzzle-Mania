#from PIL import Image
import sys
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect,QPropertyAnimation
from PyQt5.QtMultimedia import QSoundEffect
from UI import menuWindow,gameWindow,pauseWindow,gameOverWindow
from UI_Settings import settingsWindow
from Help import helpWindow
import random

class Node():
    def __init__(self,data,n,g_score):  #Zero pos is a list having co ordinates of zero
        self.data = data
        self.n = n
        self.parent_node = None
        self.target_co_ordinate = [-1,-1]
        self.g_score = g_score

        # Dictionary to store the positions of the values in data(2d matrix)
        self.position = fill_position_dict(self.n,self.data)
        # Fill the dictionary
        #self.fill_position_dict()

        self.h_score = manhattan_dist(self.n,self.position)  # Calculate h-score by calculating Manhattan distance
        
        self.f_score = self.g_score + self.h_score

        self.blank_i,self.blank_j = self.position[0]

    """#Fills the position dictionary :- the positions of the values stored in data
    def fill_position_dict(self):
        for i in range(self.n):
            for j in range(self.n):
                self.position[self.data[i][j]] = [i,j]"""
    
    """#Calculate Manhattan Distance
    def manhattan_dist(self):
        total = 0
        for i in range(1,pow(self.n,2)):
            goal_row,goal_col = divmod(i-1,self.n)
            total = total + (abs(goal_row-self.position[i][0])+abs(goal_col-self.position[i][1]))
        return total"""

    def copy_matrix(self):
        copy_arr = []
        for i in range(self.n):
            temp = self.data[i][:]
            copy_arr.append(temp)
        return copy_arr

    """def shuffle(self,x1,y1,arr):
        if x1 >= 0 and x1 < self.n and y1 >= 0 and y1 < self.n:
            arr[self.blank_x][self.blank_y] = arr[x1][y1]
            arr[x1][y1] = 0
            return True
        else:
            return False"""

    def generate_children(self,g):
        # available moves for zero
        #                           Left                            Right                           Up                            Down
        available_moves = [[self.blank_i,self.blank_j-1],[self.blank_i,self.blank_j+1],[self.blank_i-1,self.blank_j],[self.blank_i+1,self.blank_j]]
        children = []
        
        for zero_pos in available_moves:
            temp_arr = self.copy_matrix()
            if shuffle_nos(self.blank_i,self.blank_j,zero_pos[0],zero_pos[1],temp_arr,self.n) == True:
                child = Node(temp_arr,self.n,g)
                child.parent_node = self
                child.target_co_ordinate = zero_pos
                children.append(child)

        return children

class Game():
    def __init__(self):
        self.pc_screen_height = QApplication.desktop().screenGeometry().height()
        self.levels = {'beginner':3,'easy':4, 'medium':5, 'hard':5}
        self.curr_level = 'beginner'
        self.move_count = 15
        self.time_count = 0
        self.hint_count = 0
        self.curr_img_no = 1
        self.sound_on = True
        self.curr_volume = 0.5
        #self.path = []
        #self.idx_path = -1

        self.bg_snd = QSoundEffect()
        self.bg_snd.setSource(QtCore.QUrl.fromLocalFile('audio/join.wav'))
        self.bg_snd.setLoopCount(QSoundEffect.Infinite)
        #self.bg_snd.setVolume(0)
        
        self.menu_snd = QSoundEffect()
        self.menu_snd.setSource(QtCore.QUrl.fromLocalFile('audio/guitar.wav'))
        self.menu_snd.setLoopCount(QSoundEffect.Infinite)
        #self.menu_snd.setVolume(0)

        #clk_snd1 = QSoundEffect()
        #clk_snd1.setSource(QtCore.QUrl.fromLocalFile('audio/click1.wav'))
        #self.clk_snd1.setLoopCount(QSoundEffect.Infinite)
        #clk_snd2 = QSoundEffect()
        #clk_snd2.setSource(QtCore.QUrl.fromLocalFile('audio/click2.wav'))
        #self.click_sounds = [clk_snd1,clk_snd2]
        #self.volume = 1

        self.init_menuWindow()
        #self.init_gameWindow()
        #self.init_board()

        self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.timer_handler)
        #self.timer.start(1000)

    def init_menuWindow(self):
        def new_game_btn_func():
            self.init_gameWindow()
            self.menu_snd.stop()
            #self.menu_win.close()

        def settings_btn_func():
            self.init_settingsWindow()

        def help_btn_func():
            self.init_helpWindow()
            
        self.menu_win = menuWindow()
        self.menu_win.new_game_btn.clicked.connect(new_game_btn_func)
        self.menu_win.score_btn.clicked.connect(self.blank_func)
        self.menu_win.settings_btn.clicked.connect(settings_btn_func)
        self.menu_win.help_btn.clicked.connect(help_btn_func)
        self.menu_win.quit_btn.clicked.connect(sys.exit)

        if self.sound_on == True:
            self.menu_snd.setVolume(self.curr_volume)
        else:
            self.menu_snd.setVolume(0)
        self.menu_snd.play()

    def init_helpWindow(self):
        def back_btn_func():
            self.help_win.close()

        self.help_win = helpWindow()
        self.help_win.back_btn.clicked.connect(back_btn_func)
        
        if self.sound_on == True:
            self.menu_snd.setVolume(self.curr_volume)
        else:
            self.menu_snd.setVolume(0)


    def init_pauseWindow(self):
        self.pause_win = pauseWindow()
        self.pause_win.time_val_lbl.setText(self.get_time_with_format())
        self.pause_win.move_val_lbl.setText(str(self.move_count))
        self.pause_win.help_val_lbl.setText(str(self.hint_count))
        self.pause_win.resume_btn.clicked.connect(self.resume_btn_func)
        self.pause_win.menu_btn.clicked.connect(self.blank_func)
        
    def init_gameWindow(self):
        def pause_btn_func():
            self.timer.stop()
            self.init_pauseWindow()
        
        def hint_btn_func():
            self.hint_count += 1
            self.game_win.hint_count_lbl.setText(str(self.hint_count))
            self.auto_solve_puzzle()

        def shuffle_btn_func():
            self.rearrange_all_tiles(20)
            #self.game_win.update()

        def return_to_menu():
            print("Exit from window")
            self.bg_snd.stop()
            if self.sound_on == True:
                self.menu_snd.setVolume(self.curr_volume)
            else:
                self.menu_snd.setVolume(0)
            self.menu_snd.play()
            self.game_win.close()

        self.move_count = 15
        self.time_count = 0
        self.hint_count = 0
        
        self.init_board()
        self.game_win = gameWindow(self.levels[self.curr_level])
        self.game_win.pause_btn.clicked.connect(pause_btn_func)
        self.game_win.hint_btn.clicked.connect(hint_btn_func)
        self.game_win.shuffle_btn.clicked.connect(shuffle_btn_func)
        self.game_win.back_btn.clicked.connect(return_to_menu)
        for i in range(self.levels[self.curr_level]):
            for j in range(self.levels[self.curr_level]):
                self.game_win.tiles[i][j].clicked.connect(lambda _,x=i,y=j: self.btn_pressed(x,y))
        height = self.pc_screen_height // 2.4
        self.game_win.img_lbl.setPixmap(QtGui.QPixmap('squared/{}.jpg'.format(self.curr_img_no)).scaled(height,height,QtCore.Qt.KeepAspectRatio))
        #Fill Message area
        if self.curr_level == 'hard':
            self.game_win.shuffle_btn.setEnabled(True)
            self.game_win.hint_btn.setEnabled(False)
            self.game_win.msg_lbl.setText('HINT button is disabled in '+self.curr_level.upper()+' level')
            self.rearrange_all_tiles(20)
        else:
            self.game_win.shuffle_btn.setEnabled(False)
            self.game_win.hint_btn.setEnabled(True)
            self.game_win.msg_lbl.setText('SHUFFLE button is disabled in '+self.curr_level.upper()+' level')
            self.rearrange_all_tiles(10)
        self.game_win.msg_lbl.setWordWrap(True)
        self.game_win.move_count_lbl.setText(str(self.move_count))
        print("Backend : ",self.game_win.tiles[0][0].size())

        #self.rearrange_all_tiles(10)

        #time counter
        self.timer.timeout.connect(self.timer_handler)
        self.timer.start(1000)

        #sound
        if self.sound_on == True:
            self.bg_snd.setVolume(self.curr_volume)
        else:
            self.bg_snd.setVolume(0)
        self.bg_snd.play()

    def init_gameOverWindow(self):
        self.timer.stop()
        self.gameOver_win = gameOverWindow()
        self.gameOver_win.time_val_lbl.setText(str(self.get_time_with_format()))
        self.gameOver_win.move_val_lbl.setText(str(self.move_count))
        self.gameOver_win.help_val_lbl.setText(str(self.hint_count))
        self.gameOver_win.score_val_lbl.setText(str(self.calculate_score()))

    def get_time_with_format(self):
        s = self.time_count
        m,s = divmod(s,60)
        h,m = divmod(m,60)
        if s<10:
            s = '0'+str(s)
        if m<10:
            m = '0'+str(m)
        if h<10:
            h = '0'+str(h)
        return '{}:{}:{}'.format(h,m,s)

    def timer_handler(self):
        self.time_count += 1
        
        self.game_win.time_val_lbl.setText(self.get_time_with_format())
        #print("A")

    """def pause_btn_func(self):
        self.timer.stop()
        self.init_pauseWindow()"""

    def resume_btn_func(self):
        self.timer.start(1000)
        self.pause_win.close()

    """def hint_btn_func(self):
        self.hint_count += 1
        self.game_win.hint_count_lbl.setText(str(self.hint_count))
        self.auto_solve_puzzle()"""

    """def shuffle_btn_func(self):
        pass"""

    """def return_to_menu(self):
        print("Exit from window")
        self.bg_snd.stop()
        self.menu_snd.play()
        self.game_win.close()"""

    def blank_func(self):
        pass

    """def new_game_btn_func(self):
        self.init_gameWindow()
        self.menu_snd.stop()
        #self.menu_win.close()"""
    
    def btn_pressed(self,i,j):
        n = self.levels[self.curr_level]

        if i == self.blank_i and j == self.blank_j-1: #0 moves left
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_j = self.blank_j-1
            self.move_count -= 1
        elif i == self.blank_i and j == self.blank_j+1: #0 moves right
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_j = self.blank_j+1
            self.move_count -= 1
        elif i == self.blank_i-1 and j == self.blank_j: #0 moves up
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_i = self.blank_i-1
            self.move_count -= 1
        elif i == self.blank_i+1 and j == self.blank_j: #0 moves down
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_i = self.blank_i+1
            self.move_count -= 1
        else:      #invalid move
            pass
        
        position = fill_position_dict(n,self.board)
        self.blank_i,self.blank_j = position[0]
        if manhattan_dist(n,position) == 0:
            print("game over, winner decided!")
            self.init_gameOverWindow()

        """for x in range(3):
            for y in range(3):
                print(self.board[x][y],end=" ")
            print()
        print()"""

        self.game_win.move_count_lbl.setText(str(self.move_count))
        if self.move_count == 0:
            print("Out of moves")

    def shuffle_tiles(self,x1,y1,x2,y2):
        
        print(self.game_win.tiles[1][1].geometry())
        def animation():
            temp = self.game_win.tiles[x1][y1].icon()
            self.game_win.tiles[x1][y1].setIcon(QtGui.QIcon())
            self.game_win.tiles[x2][y2].setIcon(temp)
            #a
            self.anim2 = QPropertyAnimation(self.game_win.tiles[x2][y2], b"geometry")
            self.anim2.setDuration(250)
            self.anim2.setStartValue(b)
            self.anim2.setEndValue(a)
            self.anim2.start()
            
            
        # animation part 1
        self.anim1 = QPropertyAnimation(self.game_win.tiles[x2][y2], b"geometry")
        self.anim1.setDuration(1)
        #store geometry of both buttons
        a = self.game_win.tiles[x2][y2].geometry()
        b = self.game_win.tiles[x1][y1].geometry()
        self.anim1.setStartValue(a)
        self.anim1.setEndValue(b)
        self.anim1.start()
        self.anim1.finished.connect(animation)

        #self.game_win.tiles[x2][y2].setText(self.game_win.tiles[x1][y1].text())
        #self.game_win.tiles[x1][y1].setText("")

    def rearrange_all_tiles(self,no_of_repeat):
        n = self.levels[self.curr_level]
        available_moves = [[self.blank_i,self.blank_j-1],[self.blank_i-1,self.blank_j],[self.blank_i,self.blank_j+1],[self.blank_i+1,self.blank_j]]
        number = 1
        #do
        prev_choice = choice = random.randint(0,3)
        #only one legal shuffle is allowed here
        while shuffle_nos(self.blank_i,self.blank_j,available_moves[choice][0],available_moves[choice][1],self.board,n) == False:
            prev_choice = choice = random.randint(0,3)
        self.blank_i,self.blank_j = available_moves[choice]
        number += 1
        
        available_moves = [[self.blank_i,self.blank_j-1],[self.blank_i-1,self.blank_j],[self.blank_i,self.blank_j+1],[self.blank_i+1,self.blank_j]]
        #rest of the legal shuffles are done here
        while number <= no_of_repeat:
            choice = random.randint(0,3)
            #print('from : ',(self.blank_i,self.blank_j),' to : ',available_moves[choice])
            
            if abs(prev_choice-choice)!=2 and shuffle_nos(self.blank_i,self.blank_j,available_moves[choice][0],available_moves[choice][1],self.board,n) == True:
                self.blank_i,self.blank_j = available_moves[choice]
                available_moves = [[self.blank_i,self.blank_j-1],[self.blank_i-1,self.blank_j],[self.blank_i,self.blank_j+1],[self.blank_i+1,self.blank_j]]
                
                prev_choice = choice
                number += 1
        
        btn_w = self.game_win.tiles[0][0].width()
        btn_h = self.game_win.tiles[0][0].height()
        #place images on appropriate tiles
        for i in range(n):
            for j in range(n):
                c = self.board[i][j]
                if c != 0:
                    self.game_win.tiles[i][j].setIcon(QtGui.QIcon('{}/{}/{}.jpg'.format(self.curr_level,self.curr_img_no,c)))
                else:
                    self.game_win.tiles[i][j].setIcon(QtGui.QIcon())
                self.game_win.tiles[i][j].setIconSize(QtCore.QSize(btn_w-5,btn_h-5))

    def auto_solve_puzzle(self):
        n = self.levels[self.curr_level]
        open_list = []
        closed_list = []

        initial = self.board
        #initial = [[2,4,3],[1,0,6],[7,5,8]]
        #initial = [[1,2,4],[5,8,7],[6,0,3]]
        #initial = [[2,6,4],[1,0,3],[7,5,8]]
        #initial = [[8,7,6],[5,4,3],[2,1,0]]
        #initial = [[3,0,2],[6,5,1],[4,7,8]]
        #initial = [[8,7,4],[3,2,0],[6,5,1]]
        #initial = [[8,7,6],[5,4,3],[0,2,1]]
        #initial = [[1,2,4,8],[9,5,7,3],[6,14,10,12],[13,0,11,15]]
        node = Node(initial,n,g_score=0)

        t = self.time_count

        open_list.append(node)
        while len(open_list) > 0:
            #print("AA")
            if len(open_list) > 1000:   # Can not solve the puzzle
                print("Halt")
                available_moves = [[self.blank_i,self.blank_j-1],[self.blank_i-1,self.blank_j],[self.blank_i,self.blank_j+1],[self.blank_i+1,self.blank_j]]
                choice = random.randint(0,3)
                while shuffle_nos(self.blank_i,self.blank_j,available_moves[choice][0],available_moves[choice][1],self.board,n) == False:
                    choice = random.randint(0,3)
                self.shuffle_tiles(available_moves[choice][0],available_moves[choice][1],self.blank_i,self.blank_j)
                self.blank_i,self.blank_j = available_moves[choice]
                break
            curr_node = open_list.pop(0)

            if curr_node.h_score == 0:
                print("solved")
                ##########
            
                self.generate_solution(curr_node)
                #self.show_solution_path(first_child)
                break

            new_children = curr_node.generate_children(curr_node.g_score+1)

            for child in new_children:
                idx_open = get_index(child,open_list)
                idx_closed = get_index(child,closed_list)
                if idx_open == -1 and idx_closed == -1:
                    open_list.append(child)
                elif idx_open > -1:
                    if child.f_score < open_list[idx_open].f_score:
                        open_list[idx_open].g_score = child.g_score
                        open_list[idx_open].h_score = child.h_score
                        open_list[idx_open].f_score = child.f_score
                elif idx_closed > -1:
                    if child.f_score < closed_list[idx_closed].f_score:
                        closed_list.pop(idx_closed)
                        open_list.append(child)

            open_list.sort(key= lambda node:node.f_score)
            closed_list.append(curr_node)

    def generate_solution(self,curr_node):
        size = self.levels[self.curr_level]
        goal = curr_node
        while(curr_node.parent_node != None):
            prev = curr_node
            curr_node = curr_node.parent_node
        x,y = prev.target_co_ordinate
        shuffle_nos(self.blank_i,self.blank_j,x,y,self.board,size)
        self.shuffle_tiles(x,y,self.blank_i,self.blank_j)
        self.blank_i,self.blank_j = x,y
        if goal.parent_node == curr_node:
            
            self.init_gameOverWindow()

    #Initializing both game board and result board
    def init_board(self):
        size = self.levels[self.curr_level]
        self.board = []
        #self.res_board = []
        c = 1
        for i in range(size):
            temp = []
            for j in range(size):
                temp.append(c)
                #self.game_win.tiles[i][j].setText(str(c)) # Filling the tiles
                #img = Image.open('{}/{}/{}.jpg'.format(self.curr_level,self.img_no,c))
                #img = img.resize((self.game_win.tiles[i][j].width(),self.game_win.tiles[i][j].height()))
                #self.game_win.tiles[i][j].setIcon(QtGui.QIcon('{}/{}/{}.jpg'.format(self.curr_level,self.img_no,c)))
                #self.game_win.tiles[i][j].setIconSize(QtCore.QSize(self.game_win.tiles[i][j].width(),self.game_win.tiles[i][j].height()))
                #self.game_win.tiles[i][j].setStyleSheet('image:url({}/{}/{}.jpg) 5;border-width:5px'.format(self.curr_level,self.img_no,c))
                c+=1
            self.board.append(temp[:])
            #self.res_board.append(temp[:])
        
        #position of the blank tile
        self.blank_i = size-1
        self.blank_j = size-1

        #blank tile in board
        self.board[self.blank_i][self.blank_j] = 0
        #blank tile in UI
        #self.game_win.tiles[self.blank_i][self.blank_j].setText('')
        #self.game_win.tiles[i][j].setIcon(QtGui.QIcon())
        #self.game_win.tiles[i][j].adjustSize()
        #print("Icon size : ",self.game_win.tiles[i][j].iconSize())

    def calculate_score(self):
        return 0

    # Settings area
    def init_settingsWindow(self):
        def left_side_toggle():
            source = self.settings_win.sender()
            if source.text() == "Change Picture":
                self.settings_win.pic_btn.setChecked(True)
                self.settings_win.level_btn.setChecked(False)
                self.settings_win.sound_btn.setChecked(False)
                self.settings_win.stackedWidget.setCurrentIndex(0)
            elif source.text() == "Change Level":
                self.settings_win.pic_btn.setChecked(False)
                self.settings_win.level_btn.setChecked(True)
                self.settings_win.sound_btn.setChecked(False)
                self.settings_win.stackedWidget.setCurrentIndex(1)
            elif source.text() == "Sound":
                self.settings_win.pic_btn.setChecked(False)
                self.settings_win.level_btn.setChecked(False)
                self.settings_win.sound_btn.setChecked(True)
                self.settings_win.stackedWidget.setCurrentIndex(2)
        
        #Right side part 1
        def select_img_func():
            self.settings_win.select_img_btn.setText("Selected")
            self.settings_win.select_img_btn.setChecked(True)
            self.curr_img_no = self.curr_imgShown_no

        def left_img_func():
            h = self.pc_screen_height // 1.6
            self.curr_imgShown_no -= 1
            self.settings_win.img_lbl.setPixmap(QtGui.QPixmap('squared/{}.jpg'.format(self.curr_imgShown_no)).scaled(h,h,QtCore.Qt.KeepAspectRatio))
            if self.curr_imgShown_no == 1:
                self.settings_win.left_img_btn.setDisabled(True)
            else:
                self.settings_win.left_img_btn.setEnabled(True)
            self.settings_win.right_img_btn.setEnabled(True)
            if self.curr_imgShown_no == self.curr_img_no:
                self.settings_win.select_img_btn.setText("Selected")
                self.settings_win.select_img_btn.setChecked(True)
            else:
                self.settings_win.select_img_btn.setText("Select")
                self.settings_win.select_img_btn.setChecked(False)

        def right_img_func():
            h = self.pc_screen_height // 1.6
            self.curr_imgShown_no += 1
            self.settings_win.img_lbl.setPixmap(QtGui.QPixmap('squared/{}.jpg'.format(self.curr_imgShown_no)).scaled(h,h,QtCore.Qt.KeepAspectRatio))
            if self.curr_imgShown_no == 22:
                self.settings_win.right_img_btn.setDisabled(True)
            else:
                self.settings_win.right_img_btn.setEnabled(True)
            self.settings_win.left_img_btn.setEnabled(True)
            if self.curr_imgShown_no == self.curr_img_no:
                self.settings_win.select_img_btn.setText("Selected")
                self.settings_win.select_img_btn.setChecked(True)
            else:
                self.settings_win.select_img_btn.setText("Select")
                self.settings_win.select_img_btn.setChecked(False)

        #Right side Part 2
        def right_side_toggle():
            source = self.settings_win.sender()
            if source.text() == 'Beginner':
                self.settings_win.beginner_level_btn.setChecked(True)
                self.settings_win.easy_level_btn.setChecked(False)
                self.settings_win.medium_level_btn.setChecked(False)
                self.settings_win.hard_level_btn.setChecked(False)
                self.curr_level = 'beginner'
                self.settings_win.level_msg_lbl.setText("""You get 8 tiles to solve where number of movements is limited. Hint 
                                                        functionality is available for this level.""")
            elif source.text() == 'Easy':
                self.settings_win.beginner_level_btn.setChecked(False)
                self.settings_win.easy_level_btn.setChecked(True)
                self.settings_win.medium_level_btn.setChecked(False)
                self.settings_win.hard_level_btn.setChecked(False)
                self.curr_level = 'easy'
                self.settings_win.level_msg_lbl.setText("""You have 15 tiles to arrange with a limited number of movements. Hint 
                                                        functionality is available for this level.""")
            elif source.text() == 'Medium':
                self.settings_win.beginner_level_btn.setChecked(False)
                self.settings_win.easy_level_btn.setChecked(False)
                self.settings_win.medium_level_btn.setChecked(True)
                self.settings_win.hard_level_btn.setChecked(False)
                self.curr_level = 'medium'
                self.settings_win.level_msg_lbl.setText("""You get 24 tiles to arrange properly in a limited number of movements. Hint 
                                                        functionality is available for this level.""")
            elif source.text() == 'Hard':
                self.settings_win.beginner_level_btn.setChecked(False)
                self.settings_win.easy_level_btn.setChecked(False)
                self.settings_win.medium_level_btn.setChecked(False)
                self.settings_win.hard_level_btn.setChecked(True)
                self.curr_level = 'hard'
                self.settings_win.level_msg_lbl.setText("""You have 24 tiles where the number of movements are not limited. Shuffle feature 
                                                        is available for this level""")

        #Right side Part3
        def checkBox_state_change(state):
            #source = self.settings_win.sender()
            if state == QtCore.Qt.Checked:
                self.sound_on = True
                self.menu_snd.setVolume(self.curr_volume)
            else:
                self.sound_on = False
                self.menu_snd.setVolume(0)

        def slider_value_change():
            self.curr_volume = self.settings_win.slider.value()/100
            self.settings_win.vol_value.setText(str(int(self.curr_volume*100)))
            self.menu_snd.setVolume(self.curr_volume)
            self.bg_snd.setVolume(self.curr_volume)

        self.curr_imgShown_no = self.curr_img_no
        self.settings_win = settingsWindow()
        #left side
        self.settings_win.pic_btn.clicked.connect(left_side_toggle)
        self.settings_win.level_btn.clicked.connect(left_side_toggle)
        self.settings_win.sound_btn.clicked.connect(left_side_toggle)
        self.settings_win.back_btn.clicked.connect(self.settings_win.close)

        #right side
        h = self.pc_screen_height // 1.6
        self.settings_win.img_lbl.setPixmap(QtGui.QPixmap('squared/{}.jpg'.format(self.curr_img_no)).scaled(h,h,QtCore.Qt.KeepAspectRatio))

        self.settings_win.left_img_btn.clicked.connect(left_img_func)
        self.settings_win.right_img_btn.clicked.connect(right_img_func)
        self.settings_win.select_img_btn.clicked.connect(select_img_func)

        self.settings_win.select_img_btn.setText("Selected")
        self.settings_win.select_img_btn.setChecked(True)

        if self.curr_img_no == 1:
            self.settings_win.left_img_btn.setDisabled(True)
        elif self.curr_img_no == 22:
            self.settings_win.right_img_btn.setDisabled(True)

        #Part2
        self.settings_win.beginner_level_btn.clicked.connect(right_side_toggle)
        self.settings_win.easy_level_btn.clicked.connect(right_side_toggle)
        self.settings_win.medium_level_btn.clicked.connect(right_side_toggle)
        self.settings_win.hard_level_btn.clicked.connect(right_side_toggle)

        if self.curr_level == 'beginner':
            self.settings_win.beginner_level_btn.setChecked(True)
            self.settings_win.level_msg_lbl.setText("""You get 8 tiles to solve where number of movements is limited. Hint 
                                                        functionality is available for this level.""")
        elif self.curr_level == 'easy':
            self.settings_win.easy_level_btn.setChecked(True)
            self.settings_win.level_msg_lbl.setText("""You have 15 tiles to arrange with a limited number of movements. Hint 
                                                        functionality is available for this level.""")
        elif self.curr_level == 'medium':
            self.settings_win.medium_level_btn.setChecked(True)
            self.settings_win.level_msg_lbl.setText("""You get 24 tiles to arrange properly in a limited number of movements. Hint 
                                                        functionality is available for this level.""")
        elif self.curr_level == 'hard':
            self.settings_win.hard_level_btn.setChecked(True)
            self.settings_win.level_msg_lbl.setText("""You have 24 tiles where the number of movements are not limited. Shuffle feature 
                                                        is available for this level""")

        #Part3
        self.settings_win.sound_on_check.stateChanged.connect(checkBox_state_change)
        self.settings_win.slider.valueChanged.connect(slider_value_change)

        if self.sound_on == True:
            self.settings_win.sound_on_check.setChecked(True)
        else:
            self.settings_win.sound_on_check.setChecked(False)
        self.settings_win.vol_value.setText(str(int(self.curr_volume*100)))
        self.settings_win.slider.setValue(int(self.curr_volume*100))

        if self.sound_on == True:
            self.menu_snd.setVolume(self.curr_volume)
        else:
            self.menu_snd.setVolume(0)


# move tile[x1][y1] to tile[x2][y2], so zero is in tile[x1][y1] now
def shuffle_nos(x1,y1,x2,y2,arr,n):
    if x2 >= 0 and x2 < n and y2 >= 0 and y2 < n:
        arr[x1][y1] = arr[x2][y2]
        arr[x2][y2] = 0
        return True
    else:
        return False

def get_index(item,seq):   # Get index of the item in seq (sequence i.e. list)
    for i in range(len(seq)):
        if item.data == seq[i].data:
            return i
    return -1

#Fills the position dictionary :- the positions of the values stored in data
def fill_position_dict(n,arr):
    position = {}
    for i in range(n):
        for j in range(n):
            position[arr[i][j]] = [i,j]
    return position

#Calculate Manhattan Distance
def manhattan_dist(n,position):
    #position = fill_position_dict(n,arr)
    total = 0
    for i in range(1,pow(n,2)):
        goal_row,goal_col = divmod(i-1,n)
        total = total + (abs(goal_row-position[i][0])+abs(goal_col-position[i][1]))
    return total

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Game()
    #a.auto_solve_puzzle()
    #win.show()
    sys.exit(app.exec_())