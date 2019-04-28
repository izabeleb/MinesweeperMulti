from random import choices

def generateBombs(numRows, numCols, numBombs):
    
    bombs = 0
    boxList = []
    
    # optimal ratio for bomb generation
    emptyRatio = ((numRows * numCols) - numBombs) / 100
    bombRatio = 1 - emptyRatio
    
    for r in range(numRows):
    
        rowList = []  
    
        for c in range(numCols):
            
            item = choices(['.', '@'], [emptyRatio, bombRatio], k=1)[0]
            rowList.append(item)
            
            if item == '@':
                
                bombs += 1         
            
        boxList.append(rowList)
       
    print("Num Bombs Generated: " + str(bombs))
    
    if bombs == numBombs:
        
        return boxList
    
    else: 
        
        return generateBombs(numRows, numCols, numBombs)


def addNums(boxList, numRows, numCols):
    
    for row in range(numRows):
        
        for col in range(numCols):
            
            if boxList[row][col] != '@':
            
                string = ''
            
                if row == 0:
                    
                    string += countCols(numCols, boxList, row, col) + countCols(numCols, boxList, row + 1, col)
                
                elif row == numRows - 1:
                
                    string += countCols(numCols, boxList, row - 1, col) + countCols(numCols, boxList, row, col)
            
                else:
                    
                    string += countCols(numCols, boxList, row - 1, col) + countCols(numCols, boxList, row, col) + countCols(numCols, boxList, row + 1, col)
                    
                boxList[row][col] = str(string.count('@'))
    
def countCols(numCols, boxList, r, c):
        
    string = '' 
        
    if c == 0:
        
        string += boxList[r][c] + boxList[r][c + 1]
        
    elif c == numCols - 1:
        
        string += boxList[r][c - 1] + boxList[r][c]
        
    else:
        
        string += boxList[r][c - 1] + boxList[r][c] + boxList[r][c + 1]

    return string
    
def main():
    
    boxList = generateBombs(10, 10, 10)
    
    print("Printing box list:")
    for r in range(10):
        
        for c in range(10):
            
            print(boxList[r][c], end='    ')
            
        print("\n")
    
    addNums(boxList, 10, 10)

    print("Printing box list:")
    for r in range(10):
        
        for c in range(10):
            
            print(boxList[r][c], end='    ')
            
        print("\n")

if __name__ == "__main__":
    
    main()