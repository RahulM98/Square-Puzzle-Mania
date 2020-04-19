from PIL import Image
import sys
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication
from UI import gameWindow,pauseWindow,gameOverWindow

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
        self.levels = {'beginner':3,'easy':4, 'medium':5, 'hard':5}
        self.curr_level = 'beginner'
        self.move_count = 0
        self.time_count = 0
        self.hint_count = 0
        self.img_no = 1
        #self.path = []
        #self.idx_path = -1
        
        self.init_gameWindow()
        self.init_board()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_handler)
        self.timer.start(1000)

    def init_pauseWindow(self):
        self.pause_win = pauseWindow()
        self.pause_win.time_val_lbl.setText(self.get_time_with_format())
        self.pause_win.move_val_lbl.setText(str(self.move_count))
        self.pause_win.help_val_lbl.setText(str(self.hint_count))
        self.pause_win.resume_btn.clicked.connect(self.resume_btn_func)
        self.pause_win.menu_btn.clicked.connect(self.return_to_menu)
        
    def init_gameWindow(self):
        self.move_count = 0
        self.time_count = 0
        self.hint_count = 0
        
        self.game_win = gameWindow(self.levels[self.curr_level])
        self.game_win.pause_btn.clicked.connect(self.pause_btn_func)
        self.game_win.hint_btn.clicked.connect(self.hint_btn_func)
        self.game_win.shuffle_btn.clicked.connect(self.shuffle_btn_func)
        self.game_win.back_btn.clicked.connect(self.return_to_menu)
        for i in range(self.levels[self.curr_level]):
            for j in range(self.levels[self.curr_level]):
                self.game_win.tiles[i][j].clicked.connect(lambda _,x=i,y=j: self.btn_pressed(x,y))
        #Fill Message area
        if self.curr_level == 'hard':
            self.game_win.shuffle_btn.setEnabled(True)
            self.game_win.hint_btn.setEnabled(False)
            self.game_win.msg_lbl.setText('HINT button is disabled in '+self.curr_level.upper()+' level')
        else:
            self.game_win.shuffle_btn.setEnabled(False)
            self.game_win.hint_btn.setEnabled(True)
            self.game_win.msg_lbl.setText('SHUFFLE button is disabled in '+self.curr_level.upper()+' level')
        self.game_win.msg_lbl.setWordWrap(True)
        self.game_win.move_count_lbl.setText(str(self.move_count))
        print("Backend : ",self.game_win.tiles[0][0].size())

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

    def pause_btn_func(self):
        self.timer.stop()
        self.init_pauseWindow()

    def resume_btn_func(self):
        self.timer.start(1000)
        self.pause_win.close()

    def hint_btn_func(self):
        self.hint_count += 1
        self.game_win.hint_count_lbl.setText(str(self.hint_count))
        self.auto_solve_puzzle()

    def shuffle_btn_func(self):
        pass

    def return_to_menu(self):
        print("Exit from window")
        sys.exit()

    def btn_pressed(self,i,j):
        n = self.levels[self.curr_level]

        if i == self.blank_i and j == self.blank_j-1: #0 moves left
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_j = self.blank_j-1
            self.move_count += 1
        elif i == self.blank_i and j == self.blank_j+1: #0 moves right
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_j = self.blank_j+1
            self.move_count += 1
        elif i == self.blank_i-1 and j == self.blank_j: #0 moves up
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_i = self.blank_i-1
            self.move_count += 1
        elif i == self.blank_i+1 and j == self.blank_j: #0 moves down
            shuffle_nos(self.blank_i,self.blank_j,i,j,self.board,n)
            self.shuffle_tiles(i,j,self.blank_i,self.blank_j)
            #self.blank_i = self.blank_i+1
            self.move_count += 1
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

    def shuffle_tiles(self,x1,y1,x2,y2):
        self.game_win.tiles[x2][y2].setIcon(self.game_win.tiles[x1][y1].icon())
        self.game_win.tiles[x1][y1].setIcon(QtGui.QIcon())
        print(self.game_win.tiles[1][1].geometry())
        #self.game_win.tiles[x2][y2].setText(self.game_win.tiles[x1][y1].text())
        #self.game_win.tiles[x1][y1].setText("")

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
            if len(open_list) > 1000:
                print("Halt")
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
                self.game_win.tiles[i][j].setIcon(QtGui.QIcon('{}/{}/{}.jpg'.format(self.curr_level,self.img_no,c)))
                self.game_win.tiles[i][j].setIconSize(QtCore.QSize(self.game_win.tiles[i][j].width(),self.game_win.tiles[i][j].height()))
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
        self.game_win.tiles[i][j].setIcon(QtGui.QIcon())
        #self.game_win.tiles[i][j].adjustSize()
        #print("Icon size : ",self.game_win.tiles[i][j].iconSize())

    def calculate_score(self):
        return 0

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