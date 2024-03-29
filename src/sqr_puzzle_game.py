## Title: sqr_puzzle_game.py
## Name : Backend
## @author : Rahul Manna
## Created on : 2020-04-15 17:07:08
## Description : It controls running of the game

import sys
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtMultimedia import QSoundEffect
from UI import menuWindow,gameWindow,pauseWindow,gameOverWindow,helpWindow,scoreWindow,dialogWindow
from UI_Settings import settingsWindow
from DB import database
import random
from datetime import datetime

#Node class stores all informations about every states of the puzzle
class Node():
    def __init__(self,data,n,g_score):  #Zero pos is a list having co ordinates of zero
        self.data = data
        self.n = n
        self.parent_node = None
        self.target_co_ordinate = [-1,-1]
        self.g_score = g_score

        # Dictionary to store the positions of the values in data(2d matrix)
        self.position = fill_position_dict(self.n,self.data)

        self.h_score = manhattan_dist(self.n,self.position)  # Calculate h-score by calculating Manhattan distance
        
        self.f_score = self.g_score + self.h_score

        self.blank_i,self.blank_j = self.position[0]

    def copy_matrix(self):
        copy_arr = []
        for i in range(self.n):
            temp = self.data[i][:]
            copy_arr.append(temp)
        return copy_arr

    #Generate all possible children for a node
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

#Game class controls working of the game
class Game():
    def __init__(self):
        self.pc_screen_height = QApplication.desktop().screenGeometry().height()
        self.levels = {'beginner':3,'easy':4, 'medium':5, 'hard':5}
        self.curr_level = 'beginner'
        self.move_count = 0
        self.time_count = 0
        self.hint_count = 0
        self.score = 0
        self.curr_img_no = 1
        self.sound_on = True
        self.curr_volume = 0.5

        self.db = database()   # Initialise database

        self.bg_snd = QSoundEffect()
        self.bg_snd.setSource(QtCore.QUrl.fromLocalFile('audio/join.wav'))
        self.bg_snd.setLoopCount(QSoundEffect.Infinite)
        
        self.menu_snd = QSoundEffect()
        self.menu_snd.setSource(QtCore.QUrl.fromLocalFile('audio/guitar.wav'))
        self.menu_snd.setLoopCount(QSoundEffect.Infinite)

        self.init_menuWindow()

        self.timer = QtCore.QTimer()    # Iintialize timer
        self.timer.timeout.connect(self.timer_handler)

    def init_menuWindow(self):
        def new_game_btn_func():
            self.init_gameWindow()
            self.menu_snd.stop()

        def settings_btn_func():
            self.init_settingsWindow()

        def score_btn_func():
            self.init_scoreWindow()

        def help_btn_func():
            self.init_helpWindow()

        def quit_btn_func():
            def dia_y_btn_func():
                self.dialog_win.close()
                self.menu_win.close()
                self.db.c.close()
                self.db.conn.close()
                sys.exit()

            self.dialog_win = dialogWindow(2,"Exit Game?","Are you sure you want to exit game?")
            self.dialog_win.yes_btn.clicked.connect(dia_y_btn_func)
            self.dialog_win.no_btn.clicked.connect(self.dialog_win.close)
            
        self.menu_win = menuWindow()
        self.menu_win.new_game_btn.clicked.connect(new_game_btn_func)
        self.menu_win.score_btn.clicked.connect(score_btn_func)
        self.menu_win.settings_btn.clicked.connect(settings_btn_func)
        self.menu_win.help_btn.clicked.connect(help_btn_func)
        self.menu_win.quit_btn.clicked.connect(quit_btn_func)

        if self.sound_on == True:
            self.menu_snd.setVolume(self.curr_volume)
        else:
            self.menu_snd.setVolume(0)
        self.menu_snd.play()

    def init_helpWindow(self):
        def back_btn_func():
            self.help_win.close()

        self.help_win = helpWindow()
        self.help_win.img_lbl1.setPixmap(QtGui.QPixmap('images/aa.png').scaled(self.help_win.img_lbl1.width(),self.help_win.img_lbl1.height(),QtCore.Qt.IgnoreAspectRatio))
        self.help_win.img_lbl2.setPixmap(QtGui.QPixmap('images/bb.png').scaled(self.help_win.img_lbl2.width()-50,self.help_win.img_lbl2.height()-50,QtCore.Qt.IgnoreAspectRatio))
        self.help_win.img_lbl3.setPixmap(QtGui.QPixmap('images/cc.png').scaled(self.help_win.img_lbl3.width()-50,self.help_win.img_lbl3.height()-50,QtCore.Qt.IgnoreAspectRatio))
        self.help_win.back_btn.clicked.connect(back_btn_func)
        
        if self.sound_on == True:
            self.menu_snd.setVolume(self.curr_volume)
        else:
            self.menu_snd.setVolume(0)


    def init_pauseWindow(self):
        def resume_btn_func():
            self.timer.start(1000)
            self.pause_win.close()
        
        def settings_btn_func():
            self.dialog_win = dialogWindow(2,"Exit Game?","The Game will be lost. Are you sure you want to quit?")
            self.dialog_win.yes_btn.clicked.connect(dia_y_btn_func_1)
            self.dialog_win.no_btn.clicked.connect(dia_n_btn_func)

        def menu_btn_func():
            self.dialog_win = dialogWindow(2,"Exit Game?","The Game will be lost. Are you sure you want to quit?")
            self.dialog_win.yes_btn.clicked.connect(dia_y_btn_func_2)
            self.dialog_win.no_btn.clicked.connect(dia_n_btn_func)

        def dia_y_btn_func_1():     # yes button (1)
            self.bg_snd.stop()
            if self.sound_on == True:
                self.menu_snd.setVolume(self.curr_volume)
            else:
                self.menu_snd.setVolume(0)
            self.menu_snd.play()
            self.init_settingsWindow()
            self.dialog_win.close()
            self.pause_win.close()
            self.game_win.close()

        def dia_y_btn_func_2():     # yes button (2)
            self.bg_snd.stop()
            if self.sound_on == True:
                self.menu_snd.setVolume(self.curr_volume)
            else:
                self.menu_snd.setVolume(0)
            self.menu_snd.play()
            self.dialog_win.close()
            self.pause_win.close()
            self.game_win.close()

        def dia_n_btn_func():   #No button
            self.dialog_win.close()

        self.pause_win = pauseWindow()
        self.pause_win.resume_btn.clicked.connect(resume_btn_func)
        self.pause_win.settings_btn.clicked.connect(settings_btn_func)
        self.pause_win.menu_btn.clicked.connect(menu_btn_func)
        self.pause_win.sound_on_check.stateChanged.connect(self.checkBox_state_change)
        if self.sound_on == True:
            self.pause_win.sound_on_check.setChecked(True)
        else:
            self.pause_win.sound_on_check.setChecked(False)
        
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

        def return_to_menu():
            def dia_y_btn_func():
                self.dialog_win.close()
                self.bg_snd.stop()
                if self.sound_on == True:
                    self.menu_snd.setVolume(self.curr_volume)
                else:
                    self.menu_snd.setVolume(0)
                self.menu_snd.play()
                self.game_win.close()

            def dia_n_btn_func():
                self.dialog_win.close()
                self.timer.start(1000)

            self.dialog_win = dialogWindow(2,"Exit Game?","The Game will be lost. Are you sure you want to quit?")
            self.dialog_win.yes_btn.clicked.connect(dia_y_btn_func)
            self.dialog_win.no_btn.clicked.connect(dia_n_btn_func)
            self.timer.stop()

        # Initialize all
        self.move_count = 0
        self.time_count = 0
        self.hint_count = 0
        self.score = 0
        
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
            self.game_win.move_lbl.setText('Moves Used :')
            self.game_win.move_count_lbl.setText(str(self.move_count))
        else:
            self.game_win.shuffle_btn.setEnabled(False)
            self.game_win.hint_btn.setEnabled(True)
            self.game_win.msg_lbl.setText('SHUFFLE button is disabled in '+self.curr_level.upper()+' level')
            self.rearrange_all_tiles(10)
            self.game_win.move_lbl.setText('Move Left :')
            self.game_win.move_count_lbl.setText(str(15 - self.move_count))
        self.game_win.msg_lbl.setWordWrap(True)

        #time counter
        self.timer.start(1000)

        #sound
        if self.sound_on == True:
            self.bg_snd.setVolume(self.curr_volume)
        else:
            self.bg_snd.setVolume(0)
        self.bg_snd.play()

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
            self.settings_win.img_no_lbl.setText('{}/24'.format(self.curr_imgShown_no))
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
            self.settings_win.img_no_lbl.setText('{}/24'.format(self.curr_imgShown_no))
            if self.curr_imgShown_no == 24:
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

        self.settings_win.img_no_lbl.setText('{}/24'.format(self.curr_img_no))
        self.settings_win.select_img_btn.setText("Selected")
        self.settings_win.select_img_btn.setChecked(True)

        if self.curr_img_no == 1:
            self.settings_win.left_img_btn.setDisabled(True)
        elif self.curr_img_no == 24:
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
        self.settings_win.sound_on_check.stateChanged.connect(self.checkBox_state_change)
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

    def init_gameOverWindow(self):
        def menu_btn_func():
            self.bg_snd.stop()
            if self.sound_on == True:
                self.menu_snd.setVolume(self.curr_volume)
            else:
                self.menu_snd.setVolume(0)
            self.menu_snd.play()
            self.gameOver_win.close()

        def again_btn_func():
            self.init_gameWindow()
            self.gameOver_win.close()

        self.timer.stop()
        self.gameOver_win = gameOverWindow()
        self.gameOver_win.lvl_val_lbl.setText(self.curr_level.upper())
        self.gameOver_win.time_val_lbl.setText(str(self.get_time_with_format()))
        self.gameOver_win.move_val_lbl.setText(str(self.move_count))
        self.gameOver_win.help_val_lbl.setText(str(self.hint_count))
        self.gameOver_win.score_val_lbl.setText(str(self.score))
        self.gameOver_win.menu_btn.clicked.connect(menu_btn_func)
        self.gameOver_win.again_btn.clicked.connect(again_btn_func)

    def init_scoreWindow(self):
        def back_btn_func():
            self.score_win.close()
 
        self.score_win = scoreWindow()
        self.score_win.back_btn.clicked.connect(back_btn_func)

        c = 0
        for level in self.levels:   # run for all tables
            c+=5
            query_result = self.db.show_table(level)  # query all details about a single table i.e. label [It is a list of tuples]
            for query in query_result:  # single row of of table [It is a tuple]
                for data in query:  # column values in each row
                    if query[1] == None:
                        self.score_win.table_value_lbl[c].setText("--")
                    else:
                        self.score_win.table_value_lbl[c].setText(str(data) if type(data)!=str else data)
                    c+=1

        if self.sound_on == True:
            self.menu_snd.setVolume(self.curr_volume)
        else:
            self.menu_snd.setVolume(0)

    def init_dialogWindow(self,dialog_type,title,message):
        self.dialog_win = dialogWindow(dialog_type,title,message)

    def checkBox_state_change(self,state):
        if state == QtCore.Qt.Checked:
            self.sound_on = True
            self.menu_snd.setVolume(self.curr_volume)
            self.bg_snd.setVolume(self.curr_volume)
        else:
            self.sound_on = False
            self.menu_snd.setVolume(0)
            self.bg_snd.setVolume(0)

    # Function to handle the timer
    def timer_handler(self):
        self.time_count += 1
        self.game_win.time_val_lbl.setText(self.get_time_with_format())

    # Return the time count in appropriate format [HH:MM:SS]
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

    # A Button inside the main game-grid is pressed
    def btn_pressed(self,i,j):
        def dia_ok_btn_func():
            self.init_gameOverWindow()
            self.dialog_win.close()
            self.game_win.close()

        n = self.levels[self.curr_level]

        if i == self.blank_i and j == self.blank_j-1: #0 moves left
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            self.move_count += 1
        elif i == self.blank_i and j == self.blank_j+1: #0 moves right
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            self.move_count += 1
        elif i == self.blank_i-1 and j == self.blank_j: #0 moves up
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            self.move_count += 1
        elif i == self.blank_i+1 and j == self.blank_j: #0 moves down
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            self.move_count += 1
        else:      #invalid move
            pass
        
        # setting text for no of move label in the game window
        if self.curr_level == 'hard':
            self.game_win.move_count_lbl.setText(str(self.move_count))
        else:
            self.game_win.move_count_lbl.setText(str(15 - self.move_count))
        
        # Get positions of all numbers of the game board in a 2d list
        position = fill_position_dict(n,self.board)
        self.blank_i,self.blank_j = position[0]
        if manhattan_dist(n,position) == 0: # Manhattan dist = 0 means the particular state is in the goal state
            #print("game over, winner decided!")
            #Dialog
            self.dialog_win = dialogWindow(1,"Game Over","Congratulations!!You have won this round. Click Ok to proceed...")
            self.dialog_win.ok_btn.clicked.connect(dia_ok_btn_func)
            self.calculateScore_updateDB()      #Update the database with the score
            
        elif self.move_count == 15 and self.curr_level != 'hard': #Out of moves
            #print("Out of moves")
            self.timer.stop()
            self.dialog_win = dialogWindow(1,"Game Over","You are out of moves!! You have lost this round...")
            self.dialog_win.ok_btn.clicked.connect(dia_ok_btn_func)

    #Checks if the current game score is greater than previously stored scores and updates the database
    def calculateScore_updateDB(self):
        self.timer.stop()
        self.score = self.calculate_score()
        scores = self.db.get_scores(self.curr_level)
        for sc in range(3):
            if self.score > scores[sc][0]:
                t = datetime.now().strftime("%d-%m-%y %H:%M:%S")
                total_time = self.get_time_with_format()
                self.db.addition_deletion(self.curr_level,t,self.move_count,self.hint_count,total_time,self.score)
                break
            elif self.score == scores[sc][0]:
                t = datetime.now().strftime("%d-%m-%y %H:%M:%S")
                total_time = self.get_time_with_format()
                self.db.update_table(self.curr_level,t,self.move_count,self.hint_count,total_time,self.score)
                break

    # Moves a tile from (x1,y1) to (x2,y2)
    def shuffle_tiles(self,x1,y1,x2,y2):
        def animation():
            temp = self.game_win.tiles[x1][y1].icon()
            self.game_win.tiles[x1][y1].setIcon(QtGui.QIcon())
            self.game_win.tiles[x2][y2].setIcon(temp)
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

    # Move the zero to any positions by picking a destination randomly from the available moves and repeat the whole process about no_of_repeat
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

    # This function can solve the puzzle when it gets invoked by HINT button in game window
    def auto_solve_puzzle(self):
        n = self.levels[self.curr_level]
        open_list = []
        closed_list = []

        initial = self.board
        #initial = [[2,4,3],[1,0,6],[7,5,8]]        # Testing
        #initial = [[1,2,4],[5,8,7],[6,0,3]]        # Testing
        #initial = [[2,6,4],[1,0,3],[7,5,8]]        # Testing
        #initial = [[8,7,6],[5,4,3],[2,1,0]]        # Testing
        #initial = [[3,0,2],[6,5,1],[4,7,8]]        # Testing
        #initial = [[8,7,4],[3,2,0],[6,5,1]]        # Testing
        #initial = [[8,7,6],[5,4,3],[0,2,1]]        # Testing
        #initial = [[1,2,4,8],[9,5,7,3],[6,14,10,12],[13,0,11,15]]      # Testing
        
        # Set the current node as initial node
        node = Node(initial,n,g_score=0)

        open_list.append(node)
        while len(open_list) > 0:
            if len(open_list) > 1000:   # Can not solve the puzzle
                #print("Halt")
                available_moves = [[self.blank_i,self.blank_j-1],[self.blank_i-1,self.blank_j],[self.blank_i,self.blank_j+1],[self.blank_i+1,self.blank_j]]
                choice = random.randint(0,3)
                while shuffle_nos(self.blank_i,self.blank_j,available_moves[choice][0],available_moves[choice][1],self.board,n) == False:
                    choice = random.randint(0,3)
                self.shuffle_tiles(available_moves[choice][0],available_moves[choice][1],self.blank_i,self.blank_j)
                self.blank_i,self.blank_j = available_moves[choice]
                break
            curr_node = open_list.pop(0)

            if curr_node.h_score == 0:  # It has solved the puzzle
                #print("solved")            
                self.generate_solution(curr_node)       # Asks for the most promising state after current state for the achieved solution
                break       #Stop searching more

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

    # Returns the most promising state after current state for the achieved solution
    def generate_solution(self,curr_node):
        def dia_ok_btn_func():
            self.init_gameOverWindow()
            self.dialog_win.close()
            self.game_win.close()

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
            #Dialog
            self.dialog_win = dialogWindow(1,"Game Over","Congratulations!!You have won this round. Click Ok to proceed...")
            self.dialog_win.ok_btn.clicked.connect(dia_ok_btn_func)
            self.calculateScore_updateDB()

    #Initializing both game board and result board
    def init_board(self):
        size = self.levels[self.curr_level]
        self.board = []
        c = 1
        for i in range(size):
            temp = []
            for j in range(size):
                temp.append(c)
                c+=1
            self.board.append(temp[:])
        
        #position of the blank tile
        self.blank_i = size-1
        self.blank_j = size-1

        #blank tile in board
        self.board[self.blank_i][self.blank_j] = 0

    #Score calculation
    def calculate_score(self):
        completion_score = {'beginner':220,'easy':320,'medium':520,'hard':600}
        if self.curr_level != 'hard':
            x = completion_score[self.curr_level] - self.move_count*3 - self.hint_count*6 - self.time_count*2
        else:
            x = completion_score[self.curr_level] + self.move_count*2
        return x

#In the parallel matrix of numbers
# move tile[x1][y1] to tile[x2][y2], so zero is in tile[x1][y1] at begining of the function
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