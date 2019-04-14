#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:54:26 2019

@author: khushboogoyal
"""

"""this is the fucntion which check whether the board is full or not 
and return true and false, if it finds aleast one zero on the board"""

import time, os , psutil
count = 0

def BoradisFull(board):
 
    for x in range(0,9):
        for y in range(0,9):
            if board[x][y] == 0:
                
                return False
            

    print("board is filled")
    
    return True

    
    print("board is yet to be solved")
    


def possibleEntry(board , i, j):
        
    k=0
    l = 0
    
    
    
    """this is the list to fill possible Array"""
    possibleArray = {}
    for x in range (1, 10):
        
        possibleArray[x] = 0
    #print('count is----',count)    
        
    # for horizontal values
    for y in range (0, 9):
        
        if not board[i][y] == 0: 
            
            possibleArray[board[i][y]] = 1
    
    # for vertical values
    
    for x in range (0, 9):
        if not board[x][j] == 0: 
            possibleArray[board[x][j]] = 1
    
    #For squares

    # for i
    if i >= 0 and i <= 2:
        k = 0
    elif i >= 3 and i <= 5:
        k = 3
    else:
        k = 6
        
        # now for j
    if j >= 0 and j <= 2:
        l = 0
    elif j >= 3 and j <= 5:
        l = 3
    else:
        l = 6
    for x in range (k, k + 3):
        for y in range (l, l + 3):
            if not board[x][y] == 0:
                possibleArray[board[x][y]] = 1          
    
    for x in range (1, 10):
        if possibleArray[x] == 0:
            possibleArray[x] = x
        else:
            possibleArray[x] = 0
    
    return possibleArray


def printBoard(board):
    print("*********************")
    for x in range(0, 9):
        if x == 3 or x == 6:
            print("*********************")
        for y in range(0, 9):
            if y == 3 or y == 6:
                print("*", end=" ")
            print(board[x][y], end=" ")
        print()
    print("*********************")
    
  
def sudokuSolver(board):
    
    i = 0
    j = 0
    
    possiblity = {}
    global count; count += 1
    # function to check full board if in case and return board
    if BoradisFull(board):
        
        printBoard(board)
        print("Board Solved Successfully!")
        
        return
    
    else:
        # check the first blank spot
        for x in range (0, 9):
            for y in range (0, 9):
                if board[x][y] == 0:
                    # now i and j holds the value of x and y
                    i = x
                    j = y
                    
                    break
            else:
                continue
            break
        
        
        # get all the possibilities for i,j
        possiblity = possibleEntry(board, i, j)
        #print(possiblity)
        
        # go through all the possibilities and call the the function
        # again and again
        
        
        for x in range (1, 10):
            
            if not possiblity[x] == 0:
                board[i][j] = possiblity[x]
                
                #check again whole program
                sudokuSolver(board)

                
        
        
        # backtrack and it reset the particular step to 0
        board[i][j] = 0  
        
        
        
def main():
        
        start = time.time()
        grid=[[0 for x in range(9)]for y in range(9)] 
        
    # assigning values to the grid 
        #grid=[[0,0,0,0,0,9,0,0,5],
         #     [0,0,9,1,0,0,0,0,7],
          #    [8,0,0,0,0,3,0,0,4],
           #   [9,6,0,0,0,1,8,0,0],
            #  [0,0,0,0,0,0,0,0,0],
             # [0,0,2,6,0,0,0,5,1],
              #[3,0,0,9,0,0,0,0,2],
              #[1,0,0,0,0,2,3,0,0],
              #[7,0,0,4,0,0,0,0,0]]
        
        grid=[[4,0,0,0,0,5,0,0,0],
              [0,9,0,0,6,0,0,0,0],
              [6,0,0,0,2,0,4,8,0],
              [0,8,0,0,0,7,0,6,4],
              [0,5,9,0,0,0,8,3,0],
              [7,6,0,9,0,0,0,5,0],
              [0,7,5,0,4,0,0,0,8],
              [0,0,0,0,7,0,0,4,0],
              [0,0,0,1,0,0,0,0,2]]
        
        
        
        
        print("Board is yet to be filled")
        printBoard(grid)
        sudokuSolver(grid)
        print('number of iterations',count)
        end = time.time()
        print("Time to run: {}".format(end - start))
        
            
    
if __name__ == "__main__":
    
    pid=os.getpid()
   
    ps= psutil.Process(pid)
    memoryUse = ps.memory_info()
    
    print("memory", memoryUse.vms)
    main()





