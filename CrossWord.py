import pygame
import random

pygame.init()

#window settings
screenh = 600
screenw = 600
screen = pygame.display.set_mode((screenw, screenh))
screen.fill((240,200,200))

answers =[]#this list will contain the cell that has the first letter of the word and the cell that has the last letter
lines = []#stores the drawn lines 
cells = []#this list contains all the cells in the grid
cellSize = 40 #the size of each cell in the grid, changing it will also change the number of cells in the grid

run = True
pause = False
start = False #first mouseclick
end = False #second mouseclick

font1 = pygame.font.SysFont("comicsans", cellSize*2) #Font used in "Paused' text and "Well done" text

alphabete = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
allWords = ['onepiece', 'naruto', 'bakuman','codegeass', 'deathnote', 'nana', 'berserk'
            'monster', 'another', 'btooom', 'allout', 'gantz', 'shiki', 'working','yourname'
            'major', 'fate', 'magi', 'oneouts','toradora', 'beck','relife', 'trigun', 'overlord']
words = []

#Chooses 7 random words from the list of allWords
for i in range(7):
    x = random.choice(allWords)
    while x in words:
        x = random.choice(allWords)
    words.append(x)

#The a list inside a list, it representes the grid. The inner list that represents the cells contains random letters
grid = [[random.choice(alphabete) for y in range(screenh // cellSize)] for x in range(screenw // cellSize)]


def letters(alphabete,grid, cellSize,screenh):
    
    takenY = [] #There can only be one word in ach row. So this list contains the used rows

    #This list gose through every word in the words list         
    for word in words:
        # x and y are randomly generated and will be used as indexes
        y = random.randrange(0,screenh // cellSize)
        x = random.randrange(0,screenh // cellSize)
             
        #this loop checks if there are enough cells in the row for the letters in the row
        while x + len(word) > (screenh // cellSize):
            x = random.randrange(0,screenh // cellSize)
             
        #this loop checks if the row has been used before
        while y in takenY:
            y = random.randrange(0,screenh // cellSize)
        takenY.append(y)
             
        #this loop changes the letters in the grid to the letters of the words using indexes
        for letters in word:
            grid[y][x] = letters
            x += 1
             
        startCell = pygame.Rect((x-len(word))* cellSize, y* cellSize, cellSize,cellSize)
        endCell = pygame.Rect((x-1) * cellSize, y* cellSize, cellSize,cellSize)
        answers.append([startCell,endCell])

##        print(word, ":", "y:", y, "x:",(x-len(word))) #This prints where the answer of each word starts
        print(word)
        


def drawGrid(grid, cellSize):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            
            square = pygame.draw.rect(screen, (0,0,0), (x* cellSize, y * cellSize, cellSize, cellSize), 1)
            cells.append(square)
            
            font = pygame.font.SysFont("comicsans", cellSize)
            letter = font.render(cell, True, (0,0,0))
            screen.blit(letter, (x* cellSize + (cellSize//4),y * cellSize + (cellSize//5)))
  
def paused(pause):
    while pause:
        lower = 100
        screen.fill((240,200,200))
        font2 = pygame.font.SysFont("timesnewroman", cellSize)
        pauseText = font1.render("Paused", True, (0,0,0))
        screen.blit(pauseText, ((screenw // 3)-5, screenh // 6))
        for word in words: #Writes all the words that have to be found 
            wordsToFind = font2.render(word, True, (0,0,0))
            screen.blit(wordsToFind, ((screenw // 3)+15, (screenh // 6) + lower ))
            lower += 50
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    screen.fill((240,200,200))
                    drawGrid(grid, cellSize)
                    start = False
                    end = False
                    for linecoord in lines:
                        pygame.draw.line(screen, (255,255,255), linecoord[0], linecoord[1], 4)

        pygame.display.update()


def gameLoop(run, start,end):
    while run:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the exit button is clicked the gameloop will be exited
                run = False
                
            if event.type == pygame.KEYDOWN: #To pause the game
                if event.key == pygame.K_p:
                    pause = True
                    paused(pause)
                    
            if event.type == pygame.MOUSEBUTTONDOWN: #if the mouse is clicked
                mx,my = pygame.mouse.get_pos()
                pos = pygame.Rect(mx, my, 1,1)#stores the coordinate of the mouseclick as a rect to use it in checking for collisions later
                for oneCell in cells:
                    if oneCell.colliderect(pos):
                        if start == False:
                            y = pos[1]
                            startPos = pygame.Rect(pos[0], y,1,1) #stores the coordinates of the first click as a rect 
                            start = True
                        elif end == False:
                            endPos = pygame.Rect(pos[0], y,1,1)##stores the coordinates of the second click as a rect  
                            end = True
                            
                        if start == True and end == True:
                            for answer in answers:#Goes through every answer in the list and checks for collision between it and the position of the first mouseclick and second mouseclick
                                if (answer[0].colliderect(startPos) and answer[1].colliderect(endPos)) or (answer[1].colliderect(startPos) and answer[0].colliderect(endPos)):
                                    
                                    line = pygame.draw.line(screen,(255,255,255),(startPos[0],startPos[1]),(endPos[0],endPos[1]),4)
                                    linecoord = ((startPos[0],startPos[1]),(endPos[0],endPos[1]))
                                    lines.append(linecoord)
                                    answers.remove(answer) #removes a word from the list once it's found
                                    break
                                
                            start = False
                            end = False
                           
        if answers == []: #Checks if all the words have been found
            screen.fill((200,240,200))
            wonText = font1.render("Well done!", True, (0,0,0))
            screen.blit(wonText, ((screenw // 3)-30, screenh // 3))
            




letters(alphabete,grid, cellSize,screenh)
drawGrid(grid, cellSize)
gameLoop(run, start,end)
pygame.quit()
                                         
