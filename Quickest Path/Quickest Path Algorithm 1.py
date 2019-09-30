'''
Uses pygame to draw walls that represent one index each

- Level Creator (Reused)
    - 
- Set start and end


- Assign coord of each cell - And whether they are 1 or 0
- Assign dictionary of all adjacent from seing 1 and 0
- Djiktra's algorithm
    - Merge sort to sort into priority queue

'''
import os
import pygame
import ctypes

class Screen:
    def __init__(self,b_width,b_height,file):
        '''
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #STR file - The file name so it can be naviaged to
        '''
        
        self.file = file
        self.walls = []
        
        self.b_width = b_width
        self.b_height = b_height

        self.width = 1920
        self.height = 1080
        
        print(self.width," x ",self.height)

        contents = self.ImportData()

        ctypes.windll.user32.SetProcessDPIAware()
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.FULLSCREEN)
        self.WallDictionaryCreation()
        pygame.init()

    def ImportData(self):
        '''
        #Loads the walls from a file into a list
        '''
        file1 = open("Walls/"+self.file+".txt","r")
        contents = file1.read().split("\n")
        file1.close()
        contents.pop()
        return contents

     
    def DrawScreen(self,mouse_pos,click1):
        '''
        #Draws the screen using other class functions
        '''
        contents = self.ImportData()
        x = y = 0
        #global walls
        walls = []

        
        for Loop1 in range(0,self.b_height,1):
            for Loop2 in range(0,self.b_width,1): #
                WallID = contents[Loop1][Loop2]
                '''
                #temp will be overidden every time but it is ok as we
                handle the objects when they are appended to walls
                '''
                temp = Wall(x,y,WallID,Loop2,Loop1,self.image)
                walls = temp.Append(walls)
                
                x += 30
            y += 30
            x = 0
        for wall in walls:
            self.screen.blit(wall.image,wall.pos)
            self.HandleBlock(wall,mouse_pos,click1,contents)


    def OnlyDraw(self):
        '''
        #Draws the screen using other class functions
        '''
        contents = self.ImportData()
        x = y = 0
        #global walls
        walls = []

        
        for Loop1 in range(0,self.b_height,1):
            for Loop2 in range(0,self.b_width,1): #
                WallID = contents[Loop1][Loop2]
                '''
                #temp will be overidden every time but it is ok as we
                handle the objects when they are appended to walls
                '''
                temp = Wall(x,y,WallID,Loop2,Loop1,self.image)
                walls = temp.Append(walls)
                
                x += 30
            y += 30
            x = 0
        for wall in walls:
            self.screen.blit(wall.image,wall.pos)


    def HandleBlock(self,wall,mouse_pos,click1,contents):
        if wall.IsOver(mouse_pos) == True:
            if click1 == True: #Then alter the file
                self.DrawToFile(wall,contents)
            else: 
                pass
        else:
            pass

    def DrawToFile(self,wall,contents):
        '''
        #Re-writes a line of walls but the one wall that has changed is overwritten in the file
        so all numbers before and after the chosen wall stays the same
        '''
        x = int(wall.x_index)
        y = int(wall.y_index)
        tempStr = ""
        write_to = ""   
        for Loop1 in range(0,x,1): #32 walls, but 96 numbers storing 32 walls
            tempStr += str(contents[y][Loop1]) #Writes the blocks before

        if contents[y][x] == "0":
            tempStr += "1"
        elif contents[y][x] == "1":
            tempStr += "0"
            
        
        #tempStr += str(self.draw) #Writes the block drawn self.draw
        for Loop2 in range(x+1,self.b_width,1):
            tempStr += str(contents[y][Loop2]) #Writes the blocks after
        #contents[y][int(x*3):int((x*3)+3)] = self.draw
        contents[y] = tempStr
        for Loop3 in range(0,len(contents),1):
            write_to += contents[Loop3] #As a list cannot be written to a list, a sting can
            write_to += "\n"
        file1 = open("Walls/"+self.file+".txt","w")
        file1.write(write_to) #Re-writes whole file, but only one block has changed
        file1.close()
        

    def DrawWallButtons(self,mouse_pos,click1):
        x = 0
        y = 730 #10 pixels below drawn level
        type_wall = []
        #for Loop1 in range(0,1,1): #If more than 32 blocks, change
        for Loop1 in range(0,32,1): #Number of walls, right now it is 5
            if Loop1 < 10:
                WallID = "0" + "0" + str(Loop1)
            else:
                WallID = "0" + str(Loop1) #If Loop2 is a 2 digit number
                
            if self.draw == WallID:
                scale = 1.5 #Smaller, if the chosen WallID is this object
            else:
                scale = 1
            '''
            #temp will be overidden every time but it is ok as we
            handle the objects when they are appended to walls
            '''
            temp = TypeOfWall(x,y,scale,WallID)
            type_wall = temp.Append(type_wall)
            x += 60
        y += 60
        x = 0
        
        for Loop2 in range(32,51,1): #Number of walls, right now it is 5
            if Loop2 < 10:
                WallID = "0" + "0" + str(Loop2)
            else:
                WallID = "0" + str(Loop2) #If Loop2 is a 2 digit number
                
            if self.draw == WallID:
                scale = 1.5 #Smaller, if the chosen WallID is this object
            else:
                scale = 1
            temp = TypeOfWall(x,y,scale,WallID)
            type_wall = temp.Append(type_wall)
            x += 60
        
                

        for wall in type_wall:
            self.screen.blit(wall.image,wall.pos) #Draws the block
            self.HandleWallButtons(wall,mouse_pos,click1) #Click detector
        pygame.display.flip()
        #print(self.draw)
        

    def HandleWallButtons(self,wall,mouse_pos,click1):
        if wall.IsOver(mouse_pos) == True:
            if click1 == True:
                self.draw = wall.WallID
            else: 
                pass
        else:
            pass

    def HandleDecoButtons(self,deco,mouse_pos,click1):
        if deco.IsOver(mouse_pos) == True:
            if click1 == True:
                self.draw = deco.DecoID
            else: 
                pass
        else:
            pass


    def GetImage(self,name,scale):
        '''
        #Gets the image, scales it and returns
        '''
        image = pygame.image.load("images/blocks/"+name+".png").convert_alpha()
        dimentions = (int((60/scale)),int((60//scale)))
        image = pygame.transform.scale(image,dimentions)
        return image

    def WallDictionaryCreation(self):
        '''
        #All images of walls preloaded into a dictionary
        '''
        image = {}
        #WallID = "" 0 and 1
        image["0"] = pygame.image.load("Imgs/0.png").convert_alpha()
        image["1"] = pygame.image.load("Imgs/1.png").convert_alpha()
        self.image = image

class Wall(object):
    def __init__(self,wx,wy,WallID,x_index,y_index,img):
        #walls.append(self)
        #self.image = Display.GetImage(WallID,scale)
        self.image = img[WallID]
        self.dimentions = (30,30)
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.x_index = x_index
        self.y_index = y_index
        #self.pos = (wx,wy,(60/scale),(60/scale))
        self.pos = (wx,wy)

    def Append(self,walls):
        '''
        #Cannot return in __init__ so to avoid making walls global, i made this
        '''
        walls.append(self)
        return walls

        #image = pygame.image.load("000.png").convert_alpha()
        #screen.blit(rect, (x, y))

    def IsOver(self,mouse_pos):
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + 30: #From pixel on left to last pixel on right, as 60 width
            if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + 30:
                return True
            else:
                return False
        else:
            return False

class TypeOfWall(object):
    def __init__(self,x,y,scale,WallID):
        '''
        #INT scale - Will only be 1 or 1.5, as i want the blocks to be 60x60 unless it is clicked
        '''
        self.WallID = WallID #For later purpose
        self.image = Display.GetImage(WallID,scale) #Scale 
        #self.dimentions = (int((60/scale)),int((60//scale))) #I want them all to be 60 pixels wide and high
        self.pos = (x,y)

    def Append(self,type_wall): #The same as "Wall"
        type_wall.append(self)
        return type_wall

    def IsOver(self,mouse_pos):
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + 60: #From pixel on left to last pixel on right, as 60 width
            if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + 60:
                return True
            else:
                return False
        else:
            return False




def NewFile(b_width,b_height):
    '''
    #This creates a new blank file with all walls of '000'
    For the given width and height of the level
    '''
    #Read what count of files it is currently on
    counter = open("Walls/Counter.txt","r")
    index = counter.read()
    counter.close()
    
    #To overwrite counter file to add one
    counter = open("Walls/Counter.txt","w")
    counter.write(str(int(index)+1))
    counter.close()
    
    #Create a new file with that counter
    file = open("Walls/"+index+".txt","w")
    item = ""
    
    for Height in range(0,b_height,1):
        #For how many rows of walls
        
        for Width in range(0,b_width,1):
            item = item + "0"

        #Out of the an iteration means new row
        item = item + "\n"
    file.write(item)
    file.close()
    return str(index)


def FindFile(file):
    file1 = open("Walls/"+file+".txt","r")
    contents = file1.read().split("\n")
    contents.pop() #To get rid of " " at end

    b_width = int(len(contents[0]))
    b_height = len(contents)

    return b_width,b_height


def EventGet():
    running = True
    click1 = False
    for event in pygame.event.get(): #Sees what the user does
        if event.type == pygame.QUIT: #Quit
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click1 = True
    mouse_pos = pygame.mouse.get_pos()
    return running,mouse_pos,click1


def Main(Display,file):
    running = True
    while running:
        Display.screen.fill((0,0,0))
        running,mouse_pos,click1 = EventGet()
        Display.DrawScreen(mouse_pos,click1)
        pygame.display.flip()
        #Display.DrawWallButtons(mouse_pos,click1) #

def MainAlgorithm(Display):

    Display.screen.fill((0,0,0))
    Display.OnlyDraw()
    pygame.display.flip()

    contents = Display.ImportData()

    #print(contents)

    node_queue = []
    distances = {}
    path = {}    

    coords_dict = GetCoords(contents)
            
    
    
    #running,mouse_pos,click1 = EventGet()   
    Algorithm(Display) #Reset
    #pygame.display.flip()


def Algorithm(Display):
    pass


def GetCoords(contents):
    row_ascii = 64
    column_num = 0

    coords = {}
    
    for Row in contents:
        row_ascii += 1
        column_num = 0
        for Column in Row:
            column_num += 1
            if str(Column) == "0":
                coords[chr(row_ascii)+str(column_num)] = str(Column) # coords[A1] = 0 for example

    print(coords)


def Start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("Shortest path algorithm")

    choice = ""
    
    while choice not in ["1","2","3"]:
        choice = input("1)Create template\n2)Edit a template\n3)Shortest path\n:")
    
    if choice == "1":
        while True:
            #b_ for box, so 32 boxes width of a screen minimum
            b_width = int(input("How many boxes wide (Max 36):"))
            b_height = int(input("How many boxes high (Max 36):"))
            if b_width <= 36 and b_height <= 36:
                break

        file = NewFile(b_width,b_height)
        Display = Screen(b_width,b_height,file)
        Main(Display,file)


    elif choice == "2": #Change up
        while True:
            file = str(input("Enter the name of the file:"))
            try:
                b_width,b_height = FindFile(file)
                break
            except:
                pass
        Display = Screen(b_width,b_height,file)
        Main(Display,file)

    elif choice == "3":

        while True:
            file = str(input("Enter the name of the file:"))
            try:
                b_width,b_height = FindFile(file)
                break
            except:
                pass
        
        Display = Screen(b_width,b_height,file)
        MainAlgorithm(Display)

            

        
Start()
pygame.quit()
