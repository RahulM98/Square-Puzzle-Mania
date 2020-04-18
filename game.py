import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QTableWidgetItem
from UI import gameWindow,splashWindow,gameOverWindow

class Game():
    def __init__(self):
        self.levels = {'easy':3, 'medium':4, 'hard':5}
        self.curr_level = 'medium'
        self.movement_is_final = True
        self.move_count = 0
        self.time_count = 0
        self.hint_count = 0
        self.last_move = 0
        
        #self.init_splashScreen()
        self.init_gameWindow()
        self.init_board()
    
    def init_splashScreen(self):
        self.splash_win = splashWindow()

    def init_gameWindow(self):
        self.game_win = gameWindow(self.levels[self.curr_level])
        self.game_win.pause_btn.clicked.connect(self.pause_btn_func)
        self.game_win.hint_btn.clicked.connect(self.hint_btn_func)
        self.game_win.shuffle_btn.clicked.connect(self.shuffle_btn_func)
        self.game_win.back_btn.clicked.connect(self.return_to_menu)
        for i in range(self.levels[self.curr_level]):
            for j in range(self.levels[self.curr_level]):
                self.game_win.tiles[i][j].clicked.connect(lambda _,x=i,y=j: self.btn_pressed(x,y))

        self.game_win.move_count_lbl.setText(str(self.move_count))
    
    def init_gameOverWindow(self):
        self.gameOver_win = gameOverWindow()
        self.gameOver_win.time_val_lbl.setText(str(self.time_count))
        self.gameOver_win.move_val_lbl.setText(str(self.move_count))
        self.gameOver_win.help_val_lbl.setText(str(self.hint_count))
        self.gameOver_win.score_val_lbl.setText(str(self.calculate_score()))

    def btn_pressed(self,x,y):
        self.last_move = 0
        match_no = 0
        if x == self.blank_i+1 and y == self.blank_j:
            match_no = self.up_move()
            self.move_count+=1
        elif x == self.blank_i-1 and y == self.blank_j:
            match_no = self.down_move()
            self.move_count+=1
        elif x == self.blank_i and y == self.blank_j+1:
            match_no = self.left_move()
            self.move_count+=1
        elif x == self.blank_i and y == self.blank_j-1:
            match_no = self.right_move()
            self.move_count+=1
        else:  #invalid movement
            pass
        self.game_win.move_count_lbl.setText(str(self.move_count))
        if match_no == self.levels[self.curr_level]*self.levels[self.curr_level]:
            print("Game over")
            self.init_gameOverWindow()

    def pause_btn_func(self):
        print("Pause")

    def hint_btn_func(self):
        print("Hint")
        self.movement_is_final = False
        self.move_count += 1
        # {left, right, up, down }
        match_count = {1:-1,2:-1,3:-1,4:-1}
        if self.blank_j != self.levels[self.curr_level]-1 and self.last_move!=2:
            match_count[1] = self.left_move()
        if self.blank_j != 0 and self.last_move!=1:
            match_count[2] = self.right_move()
        if self.blank_i != self.levels[self.curr_level]-1 and self.last_move!=4:
            match_count[3] = self.up_move()
        if self.blank_i != 0 and self.last_move!=3:
            match_count[4] = self.down_move()
        self.movement_is_final = True
        m = max(match_count.values())
        if match_count[1] == m:
            self.left_move()
            self.last_move = 1
        elif match_count[2] == m:
            self.right_move()
            self.last_move = 2
        elif match_count[3] == m:
            self.up_move()
            self.last_move = 3
        elif match_count[4] == m:
            self.down_move()
            self.last_move = 4

        self.game_win.move_count_lbl.setText(str(self.move_count))

    def shuffle_btn_func(self):
        print("Shuffle")

    def return_to_menu(self):
        print("Exit from window")
        sys.exit()


    # Logics for running the game

    #Initializing both game board and result board
    def init_board(self):
        self.board = []
        self.res_board = []
        c = 1
        for i in range(self.levels[self.curr_level]):
            temp = []
            for j in range(self.levels[self.curr_level]):
                if i==self.levels[self.curr_level]-1 and j==self.levels[self.curr_level]-1:
                    c = 0
                temp.append(c)
                self.game_win.tiles[i][j].setText(str(c)) # Filling the tiles
                c+=1
            self.board.append(temp[:])
            self.res_board.append(temp[:])
        #position of the blank tile
        self.blank_i = self.levels[self.curr_level]-1
        self.blank_j = self.levels[self.curr_level]-1
        #blanck tile in UI
        self.game_win.tiles[self.blank_i][self.blank_j].setText('')

    #count no of matches
    def no_of_match(self):
        c = 0
        for i in range(self.levels[self.curr_level]):
            for j in range(self.levels[self.curr_level]):
                if i==j and i==self.levels[self.curr_level]-1:
                    break
                if self.board[i][j] == self.res_board[i][j]:
                    c+=1
        return c

    # When a tile is moving up (in place of the blank tile)
    def up_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i+1][self.blank_j]
        self.board[self.blank_i+1][self.blank_j] = 0
        c = self.no_of_match()
        if self.movement_is_final == False:
            self.board[self.blank_i+1][self.blank_j] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0            
        else:
            self.game_win.tiles[self.blank_i][self.blank_j].setText(self.game_win.tiles[self.blank_i+1][self.blank_j].text())
            self.game_win.tiles[self.blank_i+1][self.blank_j].setText('')
            self.blank_i+=1
        return c

    # When a tile is moving down (in place of the blank tile)
    def down_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i-1][self.blank_j]
        self.board[self.blank_i-1][self.blank_j] = 0
        c = self.no_of_match()
        if self.movement_is_final == False:
            self.board[self.blank_i-1][self.blank_j] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0
        else:
            self.game_win.tiles[self.blank_i][self.blank_j].setText(self.game_win.tiles[self.blank_i-1][self.blank_j].text())
            self.game_win.tiles[self.blank_i-1][self.blank_j].setText('')
            self.blank_i-=1
        return c

    # When a tile is moving left (in place of the blank tile)
    def left_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i][self.blank_j+1]
        self.board[self.blank_i][self.blank_j+1] = 0
        c = self.no_of_match()
        if self.movement_is_final == False:
            self.board[self.blank_i][self.blank_j+1] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0
        else:
            self.game_win.tiles[self.blank_i][self.blank_j].setText(self.game_win.tiles[self.blank_i][self.blank_j+1].text())
            self.game_win.tiles[self.blank_i][self.blank_j+1].setText('')
            self.blank_j+=1
        return c

    # When a tile is moving right (in place of the blank tile)
    def right_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i][self.blank_j-1]
        self.board[self.blank_i][self.blank_j-1] = 0
        c = self.no_of_match()
        if self.movement_is_final == False:
            self.board[self.blank_i][self.blank_j-1] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0
        else:
            self.game_win.tiles[self.blank_i][self.blank_j].setText(self.game_win.tiles[self.blank_i][self.blank_j-1].text())
            self.game_win.tiles[self.blank_i][self.blank_j-1].setText('')
            self.blank_j-=1
        return c


    def calculate_score(self):  #######################
        return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Game()
    #win.show()
    sys.exit(app.exec_())