#Not intended to have this piece of code to play the main game, this file is purely optional and is just to make and edit levels

import os
import pygame
import ctypes
import sqlite3

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
        #Resolution of screen
        #self.width = 1920
        #self.height = 1080

        self.width = 1920
        self.height = 1080
        
        print(self.width," x ",self.height)
        print(b_width," x ",b_height)

        self.d_width = 1280
        self.d_height = 720

        self.w_centre = 0
        contents = self.ImportData()
        self.h_centre = (int(len(contents)))-18
        self.scale = 1920/self.d_width
        self.draw = "000"

        ctypes.windll.user32.SetProcessDPIAware()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.WallDictionaryCreation()
        pygame.init()

    def ImportData(self):
        '''
        Loads the walls from a file into a list
        '''
        file1 = open("levels/"+self.file+".txt","r")
        contents = file1.read().split("\n")
        file1.close()
        contents.pop()
        return contents

    def ImportDecoData(self):
        '''
        Loads the deco from a file into a list
        '''
        file1 = open("levels/decoration/"+self.file+".txt","r")
        contents = file1.read().split("\n")
        contents.pop()
        for Loop1 in range(0,len(contents),1):
            contents[Loop1] = contents[Loop1].split(" ") #Splits into a 2D list
        file1.close()
        return contents

    def ImportEnemyData(self):
        '''
        #Loads the enemies from a file into a list
        '''
        file1 = open("levels/enemies/"+self.file+".txt","r")
        contents = file1.read().split("\n")
        contents.pop()
        for Loop1 in range(0,len(contents),1):
            contents[Loop1] = contents[Loop1].split(" ") #Splits into a 2D list
        file1.close()
        return contents
     
    def DrawScreen(self,left,right,up,down,mouse_pos,click1):
        '''
        #Draws the screen using other class functions
        '''
        contents = self.ImportData()
        x = y = 0
        #global walls
        walls = []
        w_centre_cap = (int(len(contents[0]))//3)-32 #0-16 for 48, does not let the number go out of those bounds
        self.w_centre = self.WidthCentre(left,right,w_centre_cap) #

        h_centre_cap = (int(len(contents)))-18 #0-9 for 27, does not let the number go out of those bounds
        self.h_centre = self.HeightCentre(up,down,h_centre_cap) #
        
        for Loop1 in range(0,18,1):
            for Loop2 in range(0,32,1): #
                WallID = contents[Loop1+self.h_centre][(Loop2+self.w_centre)*3:((Loop2+self.w_centre)*3)+3]
                '''
                #temp will be overidden every time but it is ok as we
                handle the objects when they are appended to walls
                '''
                temp = Wall(x,y,self.scale,WallID,Loop2+self.w_centre,Loop1+self.h_centre,self.image)
                walls = temp.Append(walls)
                
                x += (60/self.scale)
            y += (60/self.scale)
            x = 0
        for wall in walls:
            self.screen.blit(wall.image,wall.pos)
            self.HandleBlock(wall,mouse_pos,click1,contents)
            
    def DrawDecoBlocks(self,left,right,up,down):
        '''
        #Draws the screen using other class functions
        '''
        contents = self.ImportData()
        x = y = 0
        walls = []
        w_centre_cap = (int(len(contents[0]))//3)-32 #0-16 for 48, does not let the number go out of those bounds
        self.w_centre = self.WidthCentre(left,right,w_centre_cap) #

        h_centre_cap = (int(len(contents)))-18 #0-9 for 27, does not let the number go out of those bounds
        self.h_centre = self.HeightCentre(up,down,h_centre_cap) #
        
        #for row in contents:
        for Loop1 in range(0,18,1):
            for Loop2 in range(0,32,1): #
                WallID = contents[Loop1+self.h_centre][(Loop2+self.w_centre)*3:((Loop2+self.w_centre)*3)+3]
                '''
                #temp will be overidden every time but it is ok as we
                handle the objects when they are appended to walls
                '''
                temp = Wall(x,y,self.scale,WallID,Loop2+self.w_centre,Loop1+self.h_centre,self.image)
                walls = temp.Append(walls)
                
                x += (60/self.scale)
            y += (60/self.scale)
            x = 0
        for wall in walls:
            self.screen.blit(wall.image,wall.pos)


    def DrawDeco(self,left,right,up,down,mouse_pos,click1):
        '''
        #Draws decoration
        '''
        contents = self.ImportDecoData()
        if len(contents) >= 1:
            x = y = 0
            decos = []
            for Loop1 in range(0,len(contents),1):
                DecoID = contents[Loop1][0]
                x = int(contents[Loop1][1])/self.scale
                y = int(contents[Loop1][2])/self.scale
                center_x = x - int((self.w_centre * 60/self.scale)) ########################
                center_y = y - int((self.h_centre * 60/self.scale))
            
                if center_x < 1280 and center_y < 720: #This bound will not apply to my actual game as they would just be drawn offscreen and not visible
                    temp = Deco(center_x,center_y,DecoID,self.scale) #Object generation #############################
                    decos = temp.Append(decos)
                    
            for deco in decos:
                self.screen.blit(deco.image,deco.pos)
        self.HandleDeco(mouse_pos,click1)

    def DrawEnemy(self,left,right,up,down,mouse_pos,click1):
        '''
        #Draws enemies
        '''
        contents = self.ImportEnemyData()
        if len(contents) >= 1:
            x = y = 0
            enemies = []
            for Loop1 in range(0,len(contents),1):
                #####Get enemy name
                #EnemyID = self.GetEnemyName()[Loop1][0]

                EnemyID = contents[Loop1][0]
                
                x = int(contents[Loop1][1])/self.scale
                y = int(contents[Loop1][2])/self.scale
                center_x = x - int((self.w_centre * 60/self.scale)) #
                center_y = y - int((self.h_centre * 60/self.scale))
            
                if center_x < 1280 and center_y < 720: #This bound will not apply to my actual game as they would just be drawn offscreen and not visible
                    temp = Enemy(center_x,center_y,EnemyID,self.scale) #Object generation #############################
                    enemies = temp.Append(enemies)

            for enemy in enemies:
                self.screen.blit(enemy.image,enemy.pos)
        self.HandleEnemy(mouse_pos,click1)

    def GetEnemyName(self):
        connection = sqlite3.connect("enemiesdb.db") #:memory: for db in RAM
        c = connection.cursor()
        c.execute("SELECT EnemyName FROM tblEnemies")
        return c.fetchall()

    def HandleBlock(self,wall,mouse_pos,click1,contents):
        if wall.IsOver(mouse_pos) == True:
            if click1 == True: #Then alter the file
                self.DrawToFile(wall,contents)
            else:
                pass
        else:
            pass

    def HandleDeco(self,mouse_pos,click1):
        if click1 == True:
            if mouse_pos[0] >= 0 and mouse_pos[0] <= 1280 and mouse_pos[1] >= 0 and mouse_pos[1] <= 720:
                #d_x = mouse_pos[0]/(1/self.scale) + (self.w_centre * 60/self.scale)
                #d_y = mouse_pos[1]/(1/self.scale) + (self.h_centre * 60/self.scale)
                d_x = mouse_pos[0]/(1/self.scale) + (self.w_centre/(1/self.scale) * 60/self.scale) #####
                d_y = mouse_pos[1]/(1/self.scale) + (self.h_centre/(1/self.scale) * 60/self.scale)
                
                self.DrawDecoFile(d_x,d_y,"")

    def HandleEnemy(self,mouse_pos,click1):
        if click1 == True:
            if mouse_pos[0] >= 0 and mouse_pos[0] <= 1280 and mouse_pos[1] >= 0 and mouse_pos[1] <= 720:
                #d_x = mouse_pos[0]/(1/self.scale) + (self.w_centre * 60/self.scale)
                #d_y = mouse_pos[1]/(1/self.scale) + (self.h_centre * 60/self.scale)
                d_x = mouse_pos[0]/(1/self.scale) + (self.w_centre/(1/self.scale) * 60/self.scale) #####
                d_y = mouse_pos[1]/(1/self.scale) + (self.h_centre/(1/self.scale) * 60/self.scale)
                
                self.DrawEnemyFile(d_x,d_y,"")

    def DrawToFile(self,wall,contents):
        '''
        #Re-writes a line of walls but the one wall that has changed is overwritten in the file
        so all numbers before and after the chosen wall stays the same
        '''
        x = int(wall.x_index)
        y = int(wall.y_index)
        tempStr = ""
        write_to = ""   
        for Loop1 in range(0,x*3,1): #32 walls, but 96 numbers storing 32 walls
            tempStr += str(contents[y][Loop1]) #Writes the blocks before
        tempStr += str(self.draw) #Writes the block drawn
        for Loop2 in range((x*3)+3,self.b_width*3,1):
            tempStr += str(contents[y][Loop2]) #Writes the blocks after
        #contents[y][int(x*3):int((x*3)+3)] = self.draw
        contents[y] = tempStr
        for Loop3 in range(0,len(contents),1):
            write_to += contents[Loop3] #As a list cannot be written to a list, a sting can
            write_to += "\n"
        file1 = open("levels/"+self.file+".txt","w")
        file1.write(write_to) #Re-writes whole file, but only one block has changed
        file1.close()

    def DrawDecoFile(self,x,y,write):
        '''
        #INT x - Mouse position x
        #INT y - Mouse position y
        #STR write - Blank string "" used to write to file
        '''
        file1 = open("levels/decoration/"+self.file+".txt","a")
        write = str(self.draw) + " " + str(int(x)) + " " + str(int(y)) + "\n" #Layout of the data on file
        file1.write(write)
        file1.close()

    def DrawEnemyFile(self,x,y,write):
        '''
        #INT x - Mouse position x
        #INT y - Mouse position y
        #STR write - Blank string "" used to write to file
        '''
        file1 = open("levels/enemies/"+self.file+".txt","a")
        write = str(self.draw) + " " + str(int(x)) + " " + str(int(y)) + "\n" #Layout of the data on file
        file1.write(write)
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
        
        for Loop2 in range(32,64,1): #Number of walls, right now it is 5
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

        y += 60
        x = 0 
        
        for Loop2 in range(64,78,1): #Number of walls, right now it is 5 newblock
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
        
    def DrawDecoButtons(self,mouse_pos,click1):
        x = 0
        y = 800 #10 pixels below drawn level
        type_deco = []
        for Loop1 in range(0,1,1): #If more than 32 blocks, change
            for Loop2 in range(0,30,1): #Number of walls, right now it is 5
                if Loop2 < 10:
                    DecoID = "0" + "0" + str(Loop2)
                else:
                    DecoID = "0" + str(Loop2) #If Loop2 is a 2 digit number
                    
                if self.draw == DecoID:
                    scale = 1.5 #Smaller, if the chosen WallID is this object
                else:
                    scale = 1
                '''
                #temp will be overidden every time but it is ok as we
                handle the objects when they are appended to walls
                '''
                temp = TypeOfDeco(x,y,scale,DecoID)
                type_deco = temp.Append(type_deco)
                
                x += 60
            y += 60
            x = 0
        for deco in type_deco:
            self.screen.blit(deco.image,deco.pos) #Draws the block
            self.HandleDecoButtons(deco,mouse_pos,click1) #Click detector
        pygame.display.flip()

    def DrawEnemyButtons(self,mouse_pos,click1):
        x = 0
        y = 800 #10 pixels below drawn level
        type_enemy = []
        for Loop1 in range(0,1,1): #If more than 32 blocks, change
            for Loop2 in range(0,13,1): #Number of walls, right now it is 5
                EnemyID = self.GetEnemyName()[Loop2][0]
                '''
                if Loop2 < 10:
                    EnemyID = "0" + "0" + str(Loop2)
                else:
                    EnemyID = "0" + str(Loop2) #If Loop2 is a 2 digit number
                '''
                    
                if self.draw == EnemyID:
                    scale = 1.5 #Smaller, if the chosen WallID is this object
                else:
                    scale = 1
                '''
                #temp will be overidden every time but it is ok as we
                handle the objects when they are appended to walls
                '''
                temp = TypeOfEnemy(x,y,scale,EnemyID)
                type_enemy = temp.Append(type_enemy)
                
                x += 60
            y += 60
            x = 0
        for enemy in type_enemy:
            self.screen.blit(enemy.image,enemy.pos) #Draws the block
            self.HandleEnemyButtons(enemy,mouse_pos,click1) #Click detector
        pygame.display.flip()

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

    def HandleEnemyButtons(self,enemy,mouse_pos,click1):
        if enemy.IsOver(mouse_pos) == True:
            if click1 == True:
                self.draw = enemy.EnemyID
            else: 
                pass
        else:
            pass

    def WidthCentre(self,left,right,w_centre_cap):
        '''
        #BOOLEAN left - If the I have pressed the left arrow
        #BOOLEAN right - If the I have pressed the right arrow
        #centre_cap - Cap of how much the game can scroll
        ###Changes the centre of the drawn screen
        '''
        if left == True:
            if self.w_centre - 2 < 0:
                return 0
            else:
                return self.w_centre - 2
        elif right == True:
            if self.w_centre + 2 > w_centre_cap:
                return w_centre_cap
            else:
                return self.w_centre + 2
        else:
            return self.w_centre

    def HeightCentre(self,up,down,h_centre_cap):
        '''
        #BOOLEAN left - If the I have pressed the left arrow
        #BOOLEAN right - If the I have pressed the right arrow
        #centre_cap - Cap of how much the game can scroll
        ###Changes the centre of the drawn screen
        '''
        if up == True:
            if self.h_centre - 2 < 0:
                return 0
            else:
                return self.h_centre - 2
        elif down == True:
            if self.h_centre + 2 > h_centre_cap:
                return h_centre_cap
            else:
                return self.h_centre + 2
        else:
            return self.h_centre

    def GetImage(self,name,scale):
        '''
        #Gets the image, scales it and returns
        '''
        image = pygame.image.load("images/blocks/"+name+".png").convert_alpha()
        dimentions = (int((60/scale)),int((60//scale)))
        image = pygame.transform.scale(image,dimentions)
        return image

    def GetDecoImage(self,name):
        '''
        #Gets the image, scales it and returns
        '''
        image = pygame.image.load("images/decoration/"+name+".png").convert_alpha()
        #dimentions = (int((60/scale)),int((60//scale)))
        #image = pygame.transform.scale(image,dimentions)
        return image

    def GetEnemyImage(self,name):
        '''
        #Gets the image, scales it and returns
        '''
        image = pygame.image.load("images/enemies/"+name+"/idle/0.png").convert_alpha()
        #dimentions = (int((60/scale)),int((60//scale)))
        #image = pygame.transform.scale(image,dimentions)
        return image

    def WallDictionaryCreation(self): #newblock
        '''
        #All images of walls preloaded into a dictionary
        '''
        image = {}
        WallID = ""
        for Loop in range(0,78,1): #Second number for how many walls there are
            if Loop < 10:
                WallID = "0" + "0" + str(Loop)
            else:
                WallID = "0" + str(Loop)
            image[WallID] = pygame.image.load("images/blocks/"+WallID+".png").convert_alpha()
        self.image = image

class Wall(object):
    def __init__(self,wx,wy,scale,WallID,x_index,y_index,img):
        #walls.append(self)
        #self.image = Display.GetImage(WallID,scale)
        self.image = img[WallID]
        self.dimentions = (int((60//scale)),int((60//scale)))
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.x_index = x_index
        self.y_index = y_index
        self.scale = scale
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
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + (60/self.scale): #From pixel on left to last pixel on right, as 60 width
            if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + (60/self.scale):
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

class Deco(object):
    def __init__(self,wx,wy,DecoID,scale):
        #walls.append(self)
        self.image = Display.GetDecoImage(DecoID)
        self.width,self.height = self.image.get_size()
        #self.x_index = x_index
        #self.y_index = y_index
        #self.scale = scale
        #self.pos = (wx,wy,(60/scale),(60/scale))
        self.dimentions = (int(self.width/scale),int(self.height/scale))
        
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.pos = (wx,wy)
        #self.draw_pos = (wx,wy)
        #self.pos = (wx/scale,wy/scale)

    def Append(self,decos):
        '''
        #Cannot return in __init__ so to avoid making walls global, i made this
        '''
        decos.append(self)
        return decos

class TypeOfDeco(object):
    def __init__(self,x,y,scale,DecoID):
        '''
        #INT scale - Will only be 1 or 1.5, as i want the blocks to be 60x60 unless it is clicked
        '''
        self.DecoID = DecoID #For later purpose
        self.image = Display.GetDecoImage(DecoID) #Scale 
        self.dimentions = (int((60/scale)),int((60//scale))) #I want them all to be 60 pixels wide and high
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.pos = (x,y)

    def Append(self,type_deco): #The same as "Wall"
        type_deco.append(self)
        return type_deco

    def IsOver(self,mouse_pos):
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + 60: #From pixel on left to last pixel on right, as 60 width
            if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + 60:
                return True
            else:
                return False
        else:
            return False

class Enemy(object):
    def __init__(self,wx,wy,EnemyID,scale):
        #walls.append(self)
        self.image = Display.GetEnemyImage(EnemyID)
        self.width,self.height = self.image.get_size()
        #self.x_index = x_index
        #self.y_index = y_index
        #self.scale = scale
        #self.pos = (wx,wy,(60/scale),(60/scale))
        self.dimentions = (int(self.width/scale),int(self.height/scale))
        
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.pos = (wx,wy)
        #self.draw_pos = (wx,wy)
        #self.pos = (wx/scale,wy/scale)

    def Append(self,enemy):
        '''
        #Cannot return in __init__ so to avoid making walls global, i made this
        '''
        enemy.append(self)
        return enemy

class TypeOfEnemy(object):
    def __init__(self,x,y,scale,EnemyID):
        '''
        #INT scale - Will only be 1 or 1.5, as i want the blocks to be 60x60 unless it is clicked
        '''
        self.EnemyID = EnemyID #For later purpose
        self.image = Display.GetEnemyImage(EnemyID) #Scale 
        self.dimentions = (int((60/scale)),int((60//scale))) #I want them all to be 60 pixels wide and high
        self.image = pygame.transform.scale(self.image,self.dimentions)
        self.pos = (x,y)

    def Append(self,type_enemy): #The same as "Wall"
        type_enemy.append(self)
        return type_enemy

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
    counter = open("levels/Counter.txt","r")
    index = counter.read()
    counter.close()
    
    #To overwrite counter file to add one
    counter = open("levels/Counter.txt","w")
    counter.write(str(int(index)+1))
    counter.close()
    
    #Create a new file with that counter
    file = open("levels/"+index+".txt","w")
    item = ""
    
    for Height in range(0,b_height,1):
        #For how many rows of walls
        
        for Width in range(0,b_width,1):
            item = item + "000"

        #Out of the an iteration means new row
        item = item + "\n"
    file.write(item)
    file.close()
    file = open("levels/decoration/"+index+".txt","w") #Makes empty decoration file for level
    file.close()
    file = open("levels/enemies/"+index+".txt","w") #Makes empty enemy file for level
    file.close()
    return str(index)

def FindFile(file):
    file1 = open("levels/"+file+".txt","r")
    contents = file1.read().split("\n")
    contents.pop() #To get rid of " " at end

    b_width = int(len(contents[0]))//3
    b_height = len(contents)

    return b_width,b_height

def FindDecoFile(file):
    try:
        file1 = open("levels/decoration/"+file+".txt","r")
        #contents = file1.read().split("\n")
        #contents.pop() #To get rid of " " at end
        file1.close()
        return False
    except:
        return True
        #file1.close()
        #file1 = open("levels/decoration/"+file+".txt","w")
        #file1.close()

def FindEnemyFile(file):
    try:
        file1 = open("levels/enemies/"+file+".txt","r")
        file1.close()
        return False
    except:
        return True

def EventGet():
    running = True
    click1 = False
    left = False
    right = False
    up = False
    down = False
    for event in pygame.event.get(): #Sees what the user does
        if event.type == pygame.QUIT: #Quit
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click1 = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
                right = False
            elif event.key == pygame.K_RIGHT:
                left = False
                right = True
            elif event.key == pygame.K_UP:
                up = True
                down = False
            elif event.key == pygame.K_DOWN:
                up = False
                down = True
    mouse_pos = pygame.mouse.get_pos()
    return running,mouse_pos,click1,left,right,up,down

def Main(Display,file):
    running = True
    while running:
        Display.screen.fill((0,0,0))
        running,mouse_pos,click1,left,right,up,down = EventGet()
        Display.DrawScreen(left,right,up,down,mouse_pos,click1)
        Display.DrawWallButtons(mouse_pos,click1) #

def MainDeco(Display,file):
    running = True
    while running:
        Display.screen.fill((0,0,0))
        running,mouse_pos,click1,left,right,up,down = EventGet()
        Display.DrawDecoBlocks(left,right,up,down)
        Display.DrawDeco(left,right,up,down,mouse_pos,click1)
        Display.DrawDecoButtons(mouse_pos,click1) #

def MainEnemy(Display,file):
    running = True
    while running:
        Display.screen.fill((0,0,0))
        running,mouse_pos,click1,left,right,up,down = EventGet()
        Display.DrawDecoBlocks(left,right,up,down)
        Display.DrawEnemy(left,right,up,down,mouse_pos,click1)
        Display.DrawEnemyButtons(mouse_pos,click1) #

def Start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("Level Creator")

    choice = ""
    
    while choice not in ["New","new","Old","old"]:
        choice = input("New or old level:")
    
    if choice == "New" or choice == "new":
        while True:
            #b_ for box, so 32 boxes width of a screen minimum
            b_width = int(input("How many boxes wide (Min 32):"))
            b_height = int(input("How many boxes high (Min 18):"))
            if b_width >= 32 and b_height >= 18:
                op = "Blocks"
                break

        file = NewFile(b_width,b_height)


    elif choice == "Old" or choice == "old":
        while True:
            valid = True
            deco = str(input("Blocks: 1 or Decoration: 2 or Enemies: 3 "))
            if deco == "1":
                while True:
                    file = str(input("Enter the name of the file:"))
                    try:
                        b_width,b_height = FindFile(file)
                        op = "Blocks"
                        break
                    except:
                        pass
                break
            elif deco == "2":
                while valid:
                    file = str(input("Enter the name of the file:"))
                    valid = FindDecoFile(file)
                    b_width,b_height = FindFile(file)
                    op = "Deco"
                break
            elif deco == "3":
                while valid:
                    file = str(input("Enter the name of the file:"))
                    valid = FindEnemyFile(file)
                    b_width,b_height = FindFile(file)
                    op = "Enemies"
                break
            
    global Display
    Display = Screen(b_width,b_height,file)
    if op == "Blocks":
        Main(Display,file)
    elif op == "Deco":
        MainDeco(Display,file)
    elif op == "Enemies":
        MainEnemy(Display,file)
        
Start()
pygame.quit()
