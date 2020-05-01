## Title: 15 sqr puzzle.py
## Name : 
## @author : Rahul Manna
## Created on : 2020-04-10 20:28:33
## Description : 

class puzzle():
    def __init__(self):
        self.size = 3
        self.board = [[2,4,3],[1,0,6],[7,5,8]]
        self.res_board = [[1,2,3],[4,5,6],[7,8,0]]
        self.movement_is_final = True
        self.blank_i = self.size-2
        self.blank_j = self.size-2
        self.last_move = 0

    def show_board(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j],end=' ')
            print()

    def count_h_val(self):
        c = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]!=self.res_board[i][j] and self.board[i][j]!=0:
                        c+=1
        return c

    # When a tile is moving up (in place of the blank tile)
    def up_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i+1][self.blank_j]
        self.board[self.blank_i+1][self.blank_j] = 0
        c = self.count_h_val()
        if self.movement_is_final == False:
            self.board[self.blank_i+1][self.blank_j] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0            
        else:
            self.blank_i+=1
        return c

    # When a tile is moving down (in place of the blank tile)
    def down_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i-1][self.blank_j]
        self.board[self.blank_i-1][self.blank_j] = 0
        c = self.count_h_val()
        if self.movement_is_final == False:
            self.board[self.blank_i-1][self.blank_j] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0
        else:
            self.blank_i-=1
        return c

    # When a tile is moving left (in place of the blank tile)
    def left_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i][self.blank_j+1]
        self.board[self.blank_i][self.blank_j+1] = 0
        c = self.count_h_val()
        if self.movement_is_final == False:
            self.board[self.blank_i][self.blank_j+1] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0
        else:
            self.blank_j+=1
        return c

    # When a tile is moving right (in place of the blank tile)
    def right_move(self):
        self.board[self.blank_i][self.blank_j] = self.board[self.blank_i][self.blank_j-1]
        self.board[self.blank_i][self.blank_j-1] = 0
        c = self.count_h_val()
        if self.movement_is_final == False:
            self.board[self.blank_i][self.blank_j-1] = self.board[self.blank_i][self.blank_j]
            self.board[self.blank_i][self.blank_j] = 0
        else:
            self.blank_j-=1
        return c

    def solve(self):
        val = -1
        while val!=0:
            print("Hint")
            self.movement_is_final = False
            #self.move_count += 1
            # {left, right, up, down }
            match_count = {1:999,2:999,3:999,4:999}
            if self.blank_j != self.size-1 and self.last_move!=3:
                match_count[1] = self.left_move()
            if self.blank_j != 0 and self.last_move!=1:
                match_count[3] = self.right_move()
            if self.blank_i != self.size-1 and self.last_move!=4:
                match_count[2] = self.up_move()
            if self.blank_i != 0 and self.last_move!=2:
                match_count[4] = self.down_move()
            self.movement_is_final = True
            print("h values = ",match_count.values())
            m = min(match_count.values())
            if match_count[1] == m:
                self.left_move()
                self.last_move = 1
            elif match_count[3] == m:
                self.right_move()
                self.last_move = 3
            elif match_count[2] == m:
                self.up_move()
                self.last_move = 2
            elif match_count[4] == m:
                self.down_move()
                self.last_move = 4
            self.show_board()
            val = self.count_h_val()
            print(val)
            input()

if __name__ == "__main__":
    a = puzzle()
    a.show_board()
    #b=a.left_move()
    print("val = ",a.count_h_val())
    a.solve()
    print("End")
    a.show_board()
        