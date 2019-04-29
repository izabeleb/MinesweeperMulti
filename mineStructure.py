from random import randint

BOMB = '#'
SPACE = ' '

def generateBombs(numRows, numCols, numBombs):
    
    boxList = []
    bombsInGrid = 0
    
    for r in range(numRows):
            
        boxList.append([SPACE] * numCols)
        
    while bombsInGrid < numBombs:
        
        randRow = randint(0, numRows - 1)
        randCol = randint(0, numCols - 1)
        
        if not boxList[randRow][randCol] == BOMB:
            
            boxList[randRow][randCol] = BOMB
            bombsInGrid += 1
    
    return boxList

def addNums(boxList, numRows, numCols):
    
    for row in range(numRows):
        
        for col in range(numCols):
            
            # if current box not a bomb, counts all surrounding bomb instances
            if boxList[row][col] != BOMB:
            
                icons = ''
            
                # top row
                if row == 0:
                    
                    icons += countCols(numCols, boxList, row, col) + countCols(numCols, boxList, row + 1, col)
                
                # bottom row
                elif row == numRows - 1:
                
                    icons += countCols(numCols, boxList, row - 1, col) + countCols(numCols, boxList, row, col)
            
                # middle rows
                else:
                    
                    icons += countCols(numCols, boxList, row - 1, col) + countCols(numCols, boxList, row, col) + countCols(numCols, boxList, row + 1, col)
                    
                boxList[row][col] = str(icons.count(BOMB))
    
def countCols(numCols, boxList, r, c):
        
    icons = '' 
        
    # top col 
    if c == 0:
        
        icons += boxList[r][c] + boxList[r][c + 1]
     
    # bottom col
    elif c == numCols - 1:
        
        icons += boxList[r][c - 1] + boxList[r][c]
      
    # middle cols
    else:
        
        icons += boxList[r][c - 1] + boxList[r][c] + boxList[r][c + 1]

    return icons

def printGrid(boxList, numRows, numCols):
    
    print("Printing box list:")
    for r in range(numRows):
        
        for c in range(numCols):
            
            print(boxList[r][c], end='    ')
            
        print("\n")
     
def main():
    
    numRows = 10
    numCols = 10
    numBombs = 10
    
    boxList = generateBombs(numRows, numCols, numBombs)
    printGrid(boxList, numRows, numCols)
    
    addNums(boxList, numRows, numCols)
    printGrid(boxList, numRows, numCols)

if __name__ == "__main__":
    
    main()