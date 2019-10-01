'''
Uses pygame to draw walls that represent one index each

- Level Creator (Reused from another project)
    - 
- Set start and end with first and second click


- Assign coord of each cell - And whether they are 1 or 0
- Assign dictionary of all adjacent from seeing 1 and 0
- Djiktra's algorithm
    - Merge sort to sort into priority queue
    - Graph traversal algorithm

'''
import os
import pygame
import ctypes

class Screen:
    def __init__(self,b_width,b_height,file):
        '''
        The class that holds the screen drawing methods and attributes
        
        PARAMETERS
        INT b_width - How many boxes wide the level is
        INT b_height - How many boxes high the level is
        STR file - The file name so it can be naviaged to
        '''
        
        self.file = file
        self.walls = []
        
        self.b_width = b_width
        self.b_height = b_height

        self.node = ""

        self.width = 1920
        self.height = 1080
        
        print(self.width," x ",self.height)

        contents = self.ImportData()

        ctypes.windll.user32.SetProcessDPIAware() #This is so that resolution is not broken
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.WallDictionaryCreation()
        pygame.init()

    def ImportData(self):
        '''
        Loads the walls from a file into a list
        '''
        file1 = open("Walls/"+self.file+".txt","r")
        contents = file1.read().split("\n")
        file1.close()
        contents.pop()
        return contents

     
    def DrawScreen(self,mouse_pos,click1):
        '''
        Draws the screen using other class functions
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
        Draws the screen using other class functions and only draws the squares, no interacting with them in this method
        '''
        contents = self.ImportData()
        x = y = 0
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

    def SelectBlock(self,mouse_pos,click1):
        '''
        #Draws the screen using other class functions and allows the user to select a cell as an input
        '''
        contents = self.ImportData()
        x = y = 0
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
            self.ChoseBlock(wall,mouse_pos,click1,contents)
            

    def GetterNode(self):
        '''
        Returns the clicked on coordinate for use outside of the class
        '''
        if self.node != "":
            coord = self.node
            self.node = ""
            return coord
        else:
            return ""

    def ChoseBlock(self,wall,mouse_pos,click1,contents):
        '''
        Finds the node that you have clicked on
        '''
        if wall.IsOver(mouse_pos) == True:
            if click1 == True:
                self.ReturnNode(wall)
            else: 
                pass
        else:
            pass

    def ReturnNode(self,wall):
        '''
        W
        '''
        x = int(wall.x_index)
        y = int(wall.y_index)

        self.node = (y,x)

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
        image["2"] = pygame.image.load("Imgs/2.png").convert_alpha()
        image["3"] = pygame.image.load("Imgs/3.png").convert_alpha()
        self.image = image

    def GetterWalls(self):
        return self.image

class Wall(object):
    '''
    Is the class for a wall
    '''
    def __init__(self,wx,wy,WallID,x_index,y_index,img):
        self.image = img[WallID]
        self.dimentions = (30,30)
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.x_index = x_index
        self.y_index = y_index
        self.pos = (wx,wy)

    def Append(self,walls):
        '''
        #Cannot return in __init__ so to avoid making walls global, i made this
        '''
        walls.append(self)
        return walls

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
    This creates a new blank file with all walls of '000'
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
    '''
    Whether the user is clicking and also returns the place where mouse is
    '''
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

def MainAlgorithm(Display):
    '''
    The method that instantiates all necessary variables for the algorithm

    VARIABLES
    
    '''

    Display.screen.fill((0,0,0))
    Display.OnlyDraw()
    pygame.display.flip()

    contents = Display.ImportData()

    node_queue = GetCoords(contents)
    adjacency_list = SetAdjacencyList(node_queue)
    distances,path = SetDistancesAndPaths(node_queue)
    
    Algorithm(Display,node_queue,adjacency_list,distances,path) #Reset
    #pygame.display.flip()


def Algorithm(Display,node_queue,adjacency_list,distances,path):
    '''
    Subroutine for the Dijkstra's algorithm along with the code for inputting nodes

    #PARAMETERS
    OBJ - Display: Object that contains the methods to interact with the screen
    QUEUE - node_queue: Contains all the empty spaces on the graph (all nodes)
    DICT - adjacency_list: Dictionary of each coordinate but each coordinate contains a list of all adjacent coordinates
    DICT - distances: The dictionary of the shortest distance from the start node to each coordinate, each distance instantiated at 10000
    DICT - path: Works in tandem with distances, shows the path of the shortest route with each key having the previous node as a value

    #VARIABLES
    STR current_node: The current node the program is at
    LIST adjacent_nodes: The adjacent nodes from a node in the graph
    INT comparison: The value used to check if the new route to a node is quicker than one that has already been established
    STR coord: Used as an input, and is assigned when the user clicks the certain part of a screen where one square is
    QUEUE node_queue: A queue of all the node (so not walls), is a priority queue and is sorted (merge sort) after each iterartion of the program
    
    '''
    current_node = ""
    adjacent_nodes = []
    comparison = 0
    while True:
        coord = ""
        running,mouse_pos,click1 = EventGet()
        Display.SelectBlock(mouse_pos,click1)
        coord = Display.GetterNode()
        if coord != "":
            start_node = coord
            DrawFinalPath(Display,start_node)
            pygame.display.flip()
            break
    while True:
        coord = ""
        running,mouse_pos,click1 = EventGet()
        Display.SelectBlock(mouse_pos,click1)
        coord = Display.GetterNode()
        if coord != "":
            end_node = coord
            DrawFinalPath(Display,end_node)
            pygame.display.flip()
            break

    distances[start_node] = 0
    clock = pygame.time.Clock()
    node_queue = DepthFirstTraversal(adjacency_list,start_node,visited=[])
    
    while len(node_queue) != 0:
        current_node = node_queue.pop(0)
        if current_node == end_node:
            break
        adjacent_nodes = adjacency_list[current_node] #All adjacent nodes
        for Node in adjacent_nodes:
            comparison = distances[current_node] + 1 #+1 as all adjacent nodes are 1 distance
            DrawSearch(Display,Node)
            if comparison < distances[Node]:
                distances[Node] = comparison
                path[Node] = current_node
                #DrawSearch(Display,current_node)
                pygame.display.flip()
                clock.tick(120)
        #SORT HERE
        if len(node_queue) > 2:
            node_queue = MergeSort(distances,node_queue)
            
    print("Shortest distance is",distances[end_node],"squares to travel.")
    RecurPath(Display,start_node,end_node,path,end_node)
    pygame.display.flip()
    running = True
    while running:
        running,mouse_pos,click1 = EventGet()

def DepthFirstTraversal(adjacency_list,current_node,visited):
    '''
    Recursive subroutine that returns every single node in the graph attached to the start_node
    '''
    visited.append(current_node)
    for Node in adjacency_list[current_node]:
        if Node not in visited:
            DepthFirstTraversal(adjacency_list,Node,visited)

    return visited


def MergeSort(dictionary,merge_list):
    '''
    List is of coordinates, but when compared uses value attributed to one coorinate taken from the (distance) dictionary
    '''
    if len(merge_list) > 1:
        mid = len(merge_list) // 2
        left_half = merge_list[:mid] #Left half of list
        right_half = merge_list[mid:] #Right half of list
        #print(left_half,right_half)
        MergeSort(dictionary,left_half)  #Continually splits left half until only left with 1 item on left list
        MergeSort(dictionary,right_half) 
        i = j = k = 0
        #print(left_half,right_half)

        while i < len(left_half) and j < len(right_half): #
            if dictionary[left_half[i]] < dictionary[right_half[j]]:
                merge_list[k] = left_half[i]
                i += 1
            else:
                merge_list[k] = right_half[j]
                j += 1

            k += 1

        #Checks if left half has elements not merged (Into same value)
        while i < len(left_half):
            merge_list[k] = left_half[i]
            i += 1
            k += 1

        #Checks if right half has elements not merged
        while j < len(right_half):
            merge_list[k] = right_half[j]
            j += 1
            k += 1

        return merge_list
    

def RecurPath(Display,start_node,end_node,path,current_node):
    '''
    Used to draw the final path and recurs itself using the path dictionary
    '''
    if path[current_node] == start_node:
        DrawFinalPath(Display,current_node)
        DrawFinalPath(Display,start_node)
    else:
        DrawFinalPath(Display,current_node)
        RecurPath(Display,start_node,end_node,path,path[current_node])

def DrawSearch(Display,current_node):
    '''
    Draws a pink square to wherever the parameter node is
    '''
    images = Display.GetterWalls()
    x = y = 0

    x = (current_node[0])* 30
    y = (current_node[1]) * 30

    pos = (y,x)
    
    Display.screen.blit(images["3"],pos)

def DrawFinalPath(Display,current_node):
    '''
    Draws a red square to wherever the parameter node is
    '''
    images = Display.GetterWalls()
    x = y = 0

    x = (current_node[0]) * 30
    y = (current_node[1]) * 30

    pos = (y,x)
    
    Display.screen.blit(images["2"],pos)


def SetDistancesAndPaths(node_queue):
    '''
    Instantiates the dictionaries distances and path to default values
    '''
    distances = {}
    path = {}
    for Coordinate in node_queue:
        distances[Coordinate] = 10000
        path[Coordinate] = ""

    return distances,path

def SetAdjacencyList(node_queue):
    '''
    Takes node_queue and returns every adjacent empty space to each node in a list for that key
    '''
    adjacency_list = {}
    above = ""
    below = ""
    right = ""
    left = ""
    for Coordinate in node_queue:
        temp_list = []

        above = (Coordinate[0]-1,Coordinate[1])
        below = (Coordinate[0]+1,Coordinate[1])
    
        right = (Coordinate[0],Coordinate[1]+1)
        left = (Coordinate[0],Coordinate[1]-1)
        
        if above in node_queue:
            temp_list.append(above)
        if below in node_queue:
            temp_list.append(below)
        if right in node_queue:
            temp_list.append(right)
        if left in node_queue:
            temp_list.append(left)

        adjacency_list[Coordinate] = temp_list #All adjacent nodes of a coordinate stored in here

    return adjacency_list
        
    
def GetCoords(contents):
    '''
    Creates a list containing every single empty space (node)
    '''
    row = -1
    column = -1

    node_queue = []
    
    for Row in contents:
        row += 1
        column = -1
        for Column in Row:
            column += 1
            if str(Column) == "0":
                node_queue.append((row,column))

    return node_queue

def Start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("Shortest path algorithm")

    choice = ""
    
    while choice not in ["1","2","3"]:
        choice = input("1)Create template\n2)Edit a template\n3)Shortest path\n:")
    
    if choice == "1":
        while True:
            #b_ for box, so 32 boxes width of a screen minimum
            b_width = int(input("How many boxes wide (Max 28):"))
            b_height = int(input("How many boxes high (Max 28):"))
            if b_width <= 28 and b_height <= 28:
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
