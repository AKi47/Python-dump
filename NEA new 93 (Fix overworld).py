import os
import pygame
import ctypes
import sqlite3
import time
import random
import math

#                   R    G    B     Colour pallete
white           = (255, 255, 255)
black           = (  0,   0,   0)
red             = (255,   0,   0)
grass_green     = (133, 242, 133)
dark_green      = (  0, 155,   0)
dark_grey       = ( 40,  40,  40)
sky_blue        = (138, 237, 252)
old_yellow      = (242, 235, 135)
light_grey      = (237, 237, 237)
off_yellow      = (253, 255, 196)

class Screen:
    def __init__(self,width,height): #All these commented lines of code in the constructor were me playing around with how this imported module works in fixing my problem
        ctypes.windll.user32.SetProcessDPIAware()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.FULLSCREEN,pygame.RESIZABLE)
        pygame.init()
        self.game_state = "Main Menu"
        self.screen_state = "Main Menu"

        self.font_scale = 1
        
        self.GameDB = DBTable('settings.db','tblGame',['option','state'],'tblGame_Default')           
        self.ControlsDB = DBTable('settings.db','tblControls',['control','key','alternate'],'tblControls_Default')
        self.VideoDB = DBTable('settings.db','tblVideo',['option','state'],'tblVideo_Default')
        self.AudioDB = DBTable('settings.db','tblAudio',['option','value'],'tblAudio_Default')

        clickdown = False
        
        #Checks DB whether to start fullscreen or not
        if self.VideoDB.QueryTable()[0][1] == 'Fullscreen':
            self.fullscreen = 0
            self.mode = pygame.RESIZABLE
        else:
            self.fullscreen = 1
            self.mode = pygame.FULLSCREEN
        self.attribute_change = "Full Change"
        self.SettingsChange(clickdown)
        self.res = int(self.VideoDB.QueryTable()[1][1])-1 #Had to add -1 so the resolution stays the same
        if self.res == 0: #Incase the res is out of range, set it back to 3
            self.res = 3

        self.attribute_change = "Res Change"
        self.SettingsChange(clickdown)
        #self.res = resol
        self.attribute_change = ""
        #Controls menu scroller
        self.cscroll = 1
        self.csypos = (self.height/18)*5.7
        self.scrollbar1 = AttributeButton("","Move Scroll Bar",((self.width/32)*30.25 +1,(self.height/18)*5.7),(self.width/32)*0.7,(self.height/18)*4,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.movescroll = False
        #Audio menu scrollers
        volumes = self.AudioDB.QueryTable()

        self.as1xpos = ((self.width/32)*10.25)+((volumes[0][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
        self.as2xpos = ((self.width/32)*10.25)+((volumes[1][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
        self.as3xpos = ((self.width/32)*10.25)+((volumes[2][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))

        self.difficulty = self.GameDB.QueryTable()[0][1]

        self.main_menu_image = pygame.image.load("images/backgrounds/MainDraft4.png").convert_alpha()

        self.htp_page = 1 #jumpto101
        self.htp_max = 10

        self.change_HTP = None
    

    def InstantiateButtons(self):
        
        #_txt_ is for text boxes
        #_font_ is for font size of text 
        menu_txt_x = int(400/self.font_scale)
        menu_txt_y = int(90/self.font_scale)
        menu_font_size = int(60/self.font_scale)
        x_txt_size = int(50/self.font_scale)
        x_font_size = int(60/self.font_scale)
        op_txt_x = int(424/self.font_scale)
        op_txt_y = int(106/self.font_scale)
        op_font_size = int(50/self.font_scale)
        op_att_size = int(60/self.font_scale)
        
        #Main menu buttons  PARAMETERES:text,navigate_to,position(?,?),width,height,colour,font,font_size,state
        self.New_game = MenuButton("New game", "New game", ((self.width/2),(self.height/18)*6),menu_txt_x,menu_txt_y, black, "georgia",menu_font_size, "Main Menu")
        self.Load_game = MenuButton("Load game","Load game",((self.width/2),(self.height/18)*7.5),menu_txt_x,menu_txt_y,black,"georgia",menu_font_size,"Main Menu")
        self.Options = MenuButton("Options","Options",((self.width/2),(self.height/18)*9),menu_txt_x,menu_txt_y,black,"georgia",menu_font_size,"Main Menu")
        self.Credits = MenuButton("Credits","Credits",((self.width/2),(self.height/18)*10.5),menu_txt_x,menu_txt_y,black,"georgia",menu_font_size,"Main Menu")
        self.How_to_play = MenuButton("How to play","How to play",((self.width/2),(self.height/18)*12),menu_txt_x,menu_txt_y,black,"georgia",menu_font_size,"Main Menu")
        self.Close_game = MenuButton("Close game","Close game",((self.width/2),(self.height/18)*13.5),menu_txt_x,menu_txt_y,black,"georgia",menu_font_size,"Main Menu")

        #New game buttons
        self.NG_P1 = MenuButton("New Profile","NG Profile 1",((self.width/32)*(31-2.25) -4,(self.height/18)*((4+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.NG_P2 = MenuButton("New Profile","NG Profile 2",((self.width/32)*(31-2.25) -4,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.NG_P3 = MenuButton("New Profile","NG Profile 3",((self.width/32)*(31-2.25) -4,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")

        self.NG_back = MenuButton("X","Main Menu",((self.width/32)*30.5,(self.height/18)*1.5),x_txt_size,x_txt_size,red,"georgia",x_font_size,"Main Menu")

        #New profile buttons
        self.NP_continue = MenuButton("Proceed","New Profile",((self.width/32)*16,(self.height/18)*14),(self.width/32)*4,(self.height/18)*1.5,red,"georgia",x_font_size,"Main Menu")
        self.NP_back = MenuButton("X","New game",((self.width/32)*26.4,(self.height/18)*3.6),x_txt_size,x_txt_size,red,"georgia",x_font_size,"Main Menu")

        
        #Load game buttons
        self.LG_P1 = MenuButton("Load Profile","LG Profile 1",((self.width/32)*(31-2.25) -4,(self.height/18)*((4+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.LG_P2 = MenuButton("Load Profile","LG Profile 2",((self.width/32)*(31-2.25) -4,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.LG_P3 = MenuButton("Load Profile","LG Profile 3",((self.width/32)*(31-2.25) -4,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")

        self.DG_P1 = MenuButton("Delete Profile","LG Deletee 1",((self.width/32)*(31-7.25) -4,(self.height/18)*((4+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.DG_P2 = MenuButton("Delete Profile","LG Deletee 2",((self.width/32)*(31-7.25) -4,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.DG_P3 = MenuButton("Delete Profile","LG Deletee 3",((self.width/32)*(31-7.25) -4,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-0.75) -4),(self.width/32)*4.5-2,(self.height/18)*1.5 -2,black,"georgia",int(40/self.font_scale),"Main Menu")

        self.LG_back = MenuButton("X","Main Menu",((self.width/32)*30.5,(self.height/18)*1.5),x_txt_size,x_txt_size,red,"georgia",x_font_size,"Main Menu")

        #Delete profile buttons
        self.Delete_back = MenuButton("Back","Load game",(760/self.font_scale,640/self.font_scale),int(250/self.font_scale),menu_txt_y, black, "georgia",menu_font_size,"Main Menu")
        self.Delete_profile = MenuButton("Delete","Delete Profile",(1140/self.font_scale,640/self.font_scale),int(250/self.font_scale),menu_txt_y, red, "georgia",menu_font_size,"Main Menu")

        #Options buttons
        #Sub menu buttons           PARAMETERES:text,menu_change,position(?,?),width,height,colour,font,font_size,state
        self.Op_game = SubMenuButton("Game Options","Game Menu",(((self.width/32)*4.9),((self.height/18)*4.5)),op_txt_x,op_txt_y,black,"georgia",op_font_size,"Main Menu")
        self.Op_video = SubMenuButton("Video Settings","Video Menu",(((self.width/32)*12.3),((self.height/18)*4.5)),op_txt_x,op_txt_y,black,"georgia",op_font_size,"Main Menu")
        self.Op_controls = SubMenuButton("Controls","Controls Menu",(((self.width/32)*19.7),((self.height/18)*4.5)),op_txt_x,op_txt_y,black,"georgia",op_font_size,"Main Menu")
        self.Op_audio = SubMenuButton("Audio Settings","Audio Menu",(((self.width/32)*27.1),((self.height/18)*4.5)),op_txt_x,op_txt_y,black,"georgia",op_font_size,"Main Menu")
        #Attribute buttons  PARAMETERES:text,attribute_change,position(?,?),width,height,colour,font,state
        self.difficulty = self.GameDB.QueryTable()[0][1]
        self.Op_game_difficulty = AttributeButton("Difficulty:","Difficulty Change",((self.width/32)*5,(self.height/18)*8),int(300/self.font_scale),op_txt_y,black,"georgia",op_att_size,"Main Menu")
        self.Op_game_text1 = AttributeButton(str(self.difficulty),None,((self.width/32)*10,(self.height/18)*8),int(300/self.font_scale),op_txt_y,black,"georgia",op_att_size,"Main Menu")


        self.Op_video_full = AttributeButton("Fullscreen:","Full Change",((self.width/32)*5,(self.height/18)*8),int(300/self.font_scale),op_txt_y,black,"georgia",op_att_size,"Main Menu")
        self.Op_video_res = AttributeButton("Resolution:","Res Change",((self.width/32)*5,(self.height/18)*10),int(300/self.font_scale),op_txt_y,black,"georgia",op_att_size,"Main Menu")

        self.Op_game_reset = AttributeButton("Reset to defaults","Game Options Reset",((self.width/32)*27.1,(self.height/18)*16.35),(self.width/32)*7+4,(self.height/18)*0.9+4,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.Op_video_reset = AttributeButton("Reset to defaults","Video Settings Reset",((self.width/32)*27.1,(self.height/18)*16.35),(self.width/32)*7+4,(self.height/18)*0.9+4,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.Op_controls_reset = AttributeButton("Reset to defaults","aControls Reset",((self.width/32)*27.1,(self.height/18)*16.35),(self.width/32)*7+4,(self.height/18)*0.9+4,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.Op_audio_reset = AttributeButton("Reset to defaults","Audio Settings Reset",((self.width/32)*27.1,(self.height/18)*16.35),(self.width/32)*7+4,(self.height/18)*0.9+4,black,"georgia",int(40/self.font_scale),"Main Menu")

        self.Op_back = MenuButton("X","Main Menu",((self.width/32)*30.5,(self.height/18)*1.5),x_txt_size,x_txt_size,red,"georgia",x_font_size,"Main Menu")


        #Credits buttons
        self.Cr_back = MenuButton("X","Main Menu",((self.width/32)*30.5,(self.height/18)*1.5),x_txt_size,x_txt_size,red,"georgia",x_font_size,"Main Menu")


        #How to play buttons jumpto102
        rarrow_x = 1060#/self.font_scale
        rarrow_y = 940#/self.font_scale

        larrow_x = 860#/self.font_scale
        larrow_y = 940#/self.font_scale
        
        self.HTP_back = MenuButton("X","Main Menu",((self.width/32)*30.5,(self.height/18)*1.5),x_txt_size,x_txt_size,red,"georgia",x_font_size,"Main Menu")
        self.HTPright = AttributeButton("","HTP right",((rarrow_x+(20))/self.font_scale,(rarrow_y+(20))/self.font_scale),int(40/self.font_scale),int(40/self.font_scale),black,"georgia",int(60/self.font_scale),"Game")
        self.HTPleft = AttributeButton("","HTP left",((larrow_x-(20))/self.font_scale,(larrow_y+(20))/self.font_scale),int(40/self.font_scale),int(40/self.font_scale),black,"georgia",int(60/self.font_scale),"Game")



        #Close game buttons
        self.CG_back = MenuButton("Back","Main Menu",(self.width/2+int(100/self.font_scale),self.height/1.85),int(150/self.font_scale),int(60/self.font_scale),black,"georgia",int(60/self.font_scale),"Main Menu")
        self.CG_close = MenuButton("Yes","Quit",(self.width/2-int(100/self.font_scale),self.height/1.85),int(150/self.font_scale),int(60/self.font_scale),red,"georgia",int(60/self.font_scale),"Main Menu")

    def InstantiateControls(self,mouse_pos,clickdown): #More of an update or a "re-instantiating" method
        keys = self.ControlsDB.QueryTable()
        self.control_change = 0 #Indentifies which control to change
        #                    PARAMETERES:text,menu_change,position(?,?),width,height,colour,font,font_size,state
        self.Op_control = AttributeButton("Control",None,((self.width/32)*6.15,(self.height/18)*6.2),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.Op_ckey = AttributeButton("Key",None,((self.width/32)*15.65,(self.height/18)*6.2),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.Op_cakey = AttributeButton("Alternate",None,((self.width/32)*25.15,(self.height/18)*6.2),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
        
        self.Op_control1 = AttributeButton(keys[0][0],None,((self.width/32)*6.15,(self.height/18)*(8.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey1 = AttributeButton(keys[0][1],"Control01",((self.width/32)*15.65,(self.height/18)*(8.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey1 = AttributeButton(keys[0][2],"Control02",((self.width/32)*25.15,(self.height/18)*(8.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control2 = AttributeButton(keys[1][0],None,((self.width/32)*6.15,(self.height/18)*(9.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey2 = AttributeButton(keys[1][1],"Control11",((self.width/32)*15.65,(self.height/18)*(9.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey2 = AttributeButton(keys[1][2],"Control12",((self.width/32)*25.15,(self.height/18)*(9.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control3 = AttributeButton(keys[2][0],None,((self.width/32)*6.15,(self.height/18)*(10.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey3 = AttributeButton(keys[2][1],"Control21",((self.width/32)*15.65,(self.height/18)*(10.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey3 = AttributeButton(keys[2][2],"Control22",((self.width/32)*25.15,(self.height/18)*(10.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control4 = AttributeButton(keys[3][0],None,((self.width/32)*6.15,(self.height/18)*(11.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey4 = AttributeButton(keys[3][1],"Control31",((self.width/32)*15.65,(self.height/18)*(11.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey4 = AttributeButton(keys[3][2],"Control32",((self.width/32)*25.15,(self.height/18)*(11.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control5 = AttributeButton(keys[4][0],None,((self.width/32)*6.15,(self.height/18)*(12.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey5 = AttributeButton(keys[4][1],"Control41",((self.width/32)*15.65,(self.height/18)*(12.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey5 = AttributeButton(keys[4][2],"Control42",((self.width/32)*25.15,(self.height/18)*(12.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control6 = AttributeButton(keys[5][0],None,((self.width/32)*6.15,(self.height/18)*(13.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey6 = AttributeButton(keys[5][1],"Control51",((self.width/32)*15.65,(self.height/18)*(13.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey6 = AttributeButton(keys[5][2],"Control52",((self.width/32)*25.15,(self.height/18)*(13.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control7 = AttributeButton(keys[6][0],None,((self.width/32)*6.15,(self.height/18)*(14.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey7 = AttributeButton(keys[6][1],"Control61",((self.width/32)*15.65,(self.height/18)*(14.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey7 = AttributeButton(keys[6][2],"Control62",((self.width/32)*25.15,(self.height/18)*(14.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control8 = AttributeButton(keys[7][0],None,((self.width/32)*6.15,(self.height/18)*(15.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey8 = AttributeButton(keys[7][1],"Control71",((self.width/32)*15.65,(self.height/18)*(15.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey8 = AttributeButton(keys[7][2],"Control72",((self.width/32)*25.15,(self.height/18)*(15.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control9 = AttributeButton(keys[8][0],None,((self.width/32)*6.15,(self.height/18)*(16.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey9 = AttributeButton(keys[8][1],"Control81",((self.width/32)*15.65,(self.height/18)*(16.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey9 = AttributeButton(keys[8][2],"Control82",((self.width/32)*25.15,(self.height/18)*(16.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control10 = AttributeButton(keys[9][0],None,((self.width/32)*6.15,(self.height/18)*(17.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey10 = AttributeButton(keys[9][1],"Control91",((self.width/32)*15.65,(self.height/18)*(17.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey10 = AttributeButton(keys[9][2],"Control92",((self.width/32)*25.15,(self.height/18)*(17.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        self.Op_control11 = AttributeButton(keys[10][0],None,((self.width/32)*6.15,(self.height/18)*(18.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey11 = AttributeButton(keys[10][1],"Control101",((self.width/32)*15.65,(self.height/18)*(18.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey11 = AttributeButton(keys[10][2],"Control102",((self.width/32)*25.15,(self.height/18)*(18.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")

        '''
        self.Op_control12 = AttributeButton(keys[11][0],None,((self.width/32)*6.15,(self.height/18)*(19.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_ckey12 = AttributeButton(keys[11][1],"Control111",((self.width/32)*15.65,(self.height/18)*(19.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        self.Op_cakey12 = AttributeButton(keys[11][2],"Control112",((self.width/32)*25.15,(self.height/18)*(19.2-self.cscroll)),(self.width/32)*9.5 +2,(self.height/18)*1,black,"georgia",int(30/self.font_scale),"Main Menu")
        '''
        
        #Scroll bar click detection and position updating       
        if self.movescroll == True:
            if clickdown == False: #To make sure
                self.movescroll = False
            if self.movescroll == True:
                self.csypos = mouse_pos[1] - (self.height/18)*0.5 #So the bar moves to the centre of the mouse
                if mouse_pos[1] <= (self.height/18)*6.2: #6.2 as that is the centre of where the user is clicking the rectangle
                    self.csypos = (self.height/18)*5.7
                if mouse_pos[1] >= (self.height/18)*15.2:
                    self.csypos = (self.height/18)*14.7
                #self.csypos is the position of the black rectangle at the top left

        scrollpossibility = self.ControlsDB.Count() - 8
        
        if self.movescroll == True:
            if scrollpossibility > 1: #If there are 9 records, there is no scrolling so none of this
                space_scroll = ((self.height/18)*15.2)-((self.height/18)*6.2) #The area on screen where the bar can go
                for Loop in range(1,scrollpossibility+1,1): #For the amount of times the table can scroll (11 records means 2 hidden so can scroll twice as can only fit 9 in table at one time)
                    if self.csypos-((self.height/18)*6.2) <= ((space_scroll/scrollpossibility)*Loop): #If the scroll bar is past an increment of scrolling, update the button possition                    
                        self.cscroll = Loop
                        break
            else:
                self.cscroll = 1
            
    def UpdateAudioMenu(self,mouse_pos,clickdown): #Non static parts of Audio Menu
        volume = self.AudioDB.QueryTable()

        font4 = pygame.font.SysFont("georgia", int(60/self.font_scale))
        text_master = font4.render(str(volume[0][1]), True, black)
        text_master_box = text_master.get_rect()
        text_master_box.center = ((self.width/32)*29),((self.height/18)*8)
        self.screen.blit(text_master,text_master_box)

        text_music = font4.render(str(volume[1][1]), True, black)
        text_music_box = text_music.get_rect()
        text_music_box.center = ((self.width/32)*29),((self.height/18)*10.5)
        self.screen.blit(text_music,text_music_box)

        text_sound = font4.render(str(volume[2][1]), True, black)
        text_sound_box = text_sound.get_rect()
        text_sound_box.center = ((self.width/32)*29),((self.height/18)*13)
        self.screen.blit(text_sound,text_sound_box)
        
        if self.moveslide1 == True:
            if clickdown == False: #To make sure
                self.moveslide1 = False
            if self.moveslide1 == True:
                self.as1xpos = mouse_pos[0] - (self.width/32)*0.25 #So the bar moves to the centre of the mouse
                if mouse_pos[0] <= (self.width/32)*10.5: #Left cap
                    self.as1xpos = (self.width/32)*10.25 
                if mouse_pos[0] >= (self.width/32)*27: #Right cap
                    self.as1xpos = (self.width/32)*26.75

        if self.moveslide2 == True:
            if clickdown == False: #To make sure
                self.moveslide2 = False
            if self.moveslide2 == True:
                self.as2xpos = mouse_pos[0] - (self.width/32)*0.25 #So the bar moves to the centre of the mouse
                if mouse_pos[0] <= (self.width/32)*10.25:
                    self.as2xpos = (self.width/32)*10.25 
                if mouse_pos[0] >= (self.width/32)*27:
                    self.as2xpos = (self.width/32)*26.75

        if self.moveslide3 == True:
            if clickdown == False: #To make sure
                self.moveslide3 = False
            if self.moveslide3 == True:
                self.as3xpos = mouse_pos[0] - (self.width/32)*0.25 #So the bar moves to the centre of the mouse
                if mouse_pos[0] <= (self.width/32)*10.25:
                    self.as3xpos = (self.width/32)*10.25 
                if mouse_pos[0] >= (self.width/32)*27:
                    self.as3xpos = (self.width/32)*26.75

        scrollpossibility = 100
        space_scroll = ((self.width/32)*26.75)-((self.width/32)*10.25) #The area on screen where the bar can go

        Volume = 100
        
        if self.moveslide1 == True:           
            for Loop in range(0,scrollpossibility,1):
                if self.as1xpos-(self.width/32)*10.25 <= (space_scroll/scrollpossibility)*Loop: #If the scroll bar is past an increment of scrolling, update the volume                    
                    Volume = Loop
                    break
                
            self.AudioDB.UpdateRecord2("Master Volume",Volume)

        if self.moveslide2 == True:           
            for Loop in range(0,scrollpossibility,1):
                if self.as2xpos-(self.width/32)*10.25 <= (space_scroll/scrollpossibility)*Loop:                   
                    Volume = Loop
                    break
            self.AudioDB.UpdateRecord2("Music Volume",Volume)

        if self.moveslide3 == True:           
            for Loop in range(0,scrollpossibility,1):
                if self.as3xpos-(self.width/32)*10.25 <= (space_scroll/scrollpossibility)*Loop:                  
                    Volume = Loop
                    break
            self.AudioDB.UpdateRecord2("Sound Effects",Volume)
        
        self.slidebar1 = AttributeButton("","Move Master",(self.as1xpos+(self.width/32)*0.25,(self.height/18)*8),(self.width/32)*0.7,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.slidebar2 = AttributeButton("","Move Music",(self.as2xpos+(self.width/32)*0.25,(self.height/18)*10.5),(self.width/32)*0.7,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
        self.slidebar3 = AttributeButton("","Move Sound",(self.as3xpos+(self.width/32)*0.25,(self.height/18)*13),(self.width/32)*0.7,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
        
        
    def StateSetter(self,mouse_pos,click1,clickdown,running):
        '''
        #Calls the object for the correct screen depending on the state the program has set for the screen
        '''
        if self.game_state == "Main Menu":
            if self.screen_state == "Main Menu":
                self.DrawMainMenu(mouse_pos,click1)
            elif self.screen_state == "New game":
                self.DrawNewGame(mouse_pos,click1)
            elif self.screen_state[:10] == "NG Profile":
                profile = int(self.screen_state[11])
                self.DrawNGProfile(mouse_pos,click1,profile) #Either 1, 2 or 3
            elif self.screen_state[:10] == "LG Profile":
                profile = int(self.screen_state[11])
                self.chosen_profile = profile
                self.screen_state = "Load Profile"
            elif self.screen_state[:10] == "LG Deletee":
                delete_profile = int(self.screen_state[11])
                self.DrawDeleteConfirmation(mouse_pos,click1,delete_profile)
                if self.screen_state == "Delete Profile":
                    self.DeleteProfile(delete_profile)
                    self.screen_state = "Load game"
            elif self.screen_state == "Load game":
                self.DrawLoadGame(mouse_pos,click1)
            elif self.screen_state == "Options":
                self.DrawOptions(mouse_pos,click1,clickdown)
            elif self.screen_state == "Credits":
                self.DrawCredits(mouse_pos,click1)
            elif self.screen_state == "How to play":
                self.DrawHowToPlay(mouse_pos,click1)
            elif self.screen_state == "Close game":
                self.DrawCloseGame(mouse_pos,click1)
            elif self.screen_state == "Quit":
                return False #Returned value is what is set to running, which would end the main loop and close the game.
            elif self.screen_state == "New Profile":
                self.game_state = "Game"
            elif self.screen_state == "Load Profile":
                self.game_state = "Game"
        elif self.game_state == "Game":
            if self.screen_state == "New Profile":
                #print(self.chosen_profile)
                self.screen.fill(black)
                pygame.display.flip()
                time.sleep(1)
                Game = GameClass(self.chosen_profile,True,self.prof_name,self.font_scale,self.ControlsDB)
                running = Game.GameState(self,0)
                self.screen_state = "Main Menu"
                self.game_state = "Main Menu"
            elif self.screen_state == "Load Profile":
                #print(self.chosen_profile)
                self.screen.fill(black)
                pygame.display.flip()
                time.sleep(1)
                Game = GameClass(self.chosen_profile,False,None,self.font_scale,self.ControlsDB)
                running = Game.GameState(self,None)
                self.screen_state = "Main Menu"
                self.game_state = "Main Menu"
        return running
                

    def DrawMainMenu(self,mouse_pos,click1): #Draws the main menu        
        font1 = pygame.font.SysFont("georgia", int(100/self.font_scale))
        font2 = pygame.font.SysFont("georgia", int(90/self.font_scale))
        
       #Game title text & background colour
        main_menutext1 = font1.render("Trek for Atonement", True, white)
        main_menutext1outline = font1.render("Trek for Atonement", True, black)
        main_menutextbox1 = main_menutext1.get_rect()
        main_menutextbox1outline = main_menutext1outline.get_rect()
        main_menutextbox1.center = (self.width/2, self.height/5.7)
        main_menutextbox1outline.center = ((self.width/2)+2, (self.height/5.7)+2)

        
        self.MainMenuImageDraw()
        #self.screen.fill(grass_green) #Draws over everything #
        self.screen.blit(main_menutext1outline,main_menutextbox1outline)
        self.screen.blit(main_menutext1,main_menutextbox1)
        
        #Last arguement is if there is outline for text so is a boolean
                        #mouse_pos,click,draw_outline
                                        #PARAMETERES:mouse_pos,leftclick,screen_state
        self.New_game.Draw(mouse_pos,click1,True,self)
        self.screen_state = self.New_game.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.Load_game.Draw(mouse_pos,click1,True,self)
        self.screen_state = self.Load_game.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.Options.Draw(mouse_pos,click1,True,self)
        self.screen_state = self.Options.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.Credits.Draw(mouse_pos,click1,True,self)
        self.screen_state = self.Credits.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.How_to_play.Draw(mouse_pos,click1,True,self)
        self.screen_state = self.How_to_play.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.Close_game.Draw(mouse_pos,click1,True,self)
        self.screen_state = self.Close_game.IsOver(mouse_pos,click1,self.screen_state,self)

    def MainMenuImageDraw(self):
        image = self.main_menu_image
        dimentions = (int(1920/self.font_scale),int(1080/self.font_scale))
        image = pygame.transform.scale(image,dimentions)
        self.screen.blit(image,(0,0))
    

    def DrawNewGame(self,mouse_pos,click1): #Draws the new game menu
        self.prof_name = []
        font1 = pygame.font.SysFont("georgia", int(80/self.font_scale))
        
        new_menutext1 = font1.render("New game", True, black)
        new_menutextbox1 = new_menutext1.get_rect()
        new_menutextbox1.center = (self.width/2, self.height/7.5)
        
        #self.screen.fill(grass_green) #Draws over everything
        pygame.draw.rect(self.screen, black, pygame.Rect(self.width/32 -2, self.height/18 -2, (self.width/32)*30 +4, (self.height/18)*16 +4)) #Black 2 pixel outline
        pygame.draw.rect(self.screen, old_yellow, pygame.Rect(self.width/32, self.height/18, (self.width/32)*30, (self.height/18)*16)) #Yellow inside
        self.screen.blit(new_menutext1,new_menutextbox1)
        
        #Profile 1,2 and 3 outline
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*4,(self.width/32)*30 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+(13/3)),(self.width/32)*30 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+((13/3)*2)),(self.width/32)*30 -8,(self.height/18)*(13-((13/3)*2)) -4))

        #Profile 1,2 and 3
        pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32) +6,(self.height/18)*4 +2,(self.width/32)*30 -12,(self.height/18)*(13-((13/3)*2)) -8))
        pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32) +6,(self.height/18)*(4+(13/3)) +2,(self.width/32)*30 -12,(self.height/18)*(13-((13/3)*2)) -8))
        pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32) +6,(self.height/18)*(4+((13/3)*2)) +2,(self.width/32)*30 -12,(self.height/18)*(13-((13/3)*2)) -8))

        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*(31-4.5) -4,(self.height/18)*((4+(13-((13/3)*2)))-1.5) -4,(self.width/32)*4.5,(self.height/18)*1.5))
        pygame.draw.rect(self.screen, light_grey, pygame.Rect((self.width/32)*(31-4.5) -2,(self.height/18)*((4+(13-((13/3)*2)))-1.5) -2,(self.width/32)*4.5 -4,(self.height/18)*1.5 -4))

        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*(31-4.5) -4,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-1.5) -5,(self.width/32)*4.5,(self.height/18)*1.5))
        pygame.draw.rect(self.screen, light_grey, pygame.Rect((self.width/32)*(31-4.5) -2,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-1.5) -3,(self.width/32)*4.5 -4,(self.height/18)*1.5 -4))

        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*(31-4.5) -4,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-1.5) -4,(self.width/32)*4.5,(self.height/18)*1.5))
        pygame.draw.rect(self.screen, light_grey, pygame.Rect((self.width/32)*(31-4.5) -2,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-1.5) -2,(self.width/32)*4.5 -4,(self.height/18)*1.5 -4))
        

        font5 = pygame.font.SysFont("georgia", int(50/self.font_scale))
        file = open("profiles\Profile1.txt","r")
        profile1 = file.read()
        file.close()
        name_list = []
        name = ""
        if profile1 != "": #If not empty, it will do stuff here
            ###########NAME
            profile1 = profile1.split("\n")
            name_list = profile1[1].split("  ")
            for letter in name_list:
                name = name + str(letter)
            t_prof1 = font5.render(name, True, black)
            t_prof1_box = t_prof1.get_rect()
            width,height = t_prof1.get_size()
            t_prof1_box.center = (((self.width/32)*4)+width/2),((320/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_prof1,t_prof1_box)

            #Time in format 00:00
            #seconds = (int(float(profile1[0])))
            
            total_minutes = (int(float( (int(float(profile1[0]))) / 60)))
            if total_minutes >= 60:
                hours = int(float(total_minutes / 60))
                minutes = int(((total_minutes % 60)/60)*60)
                if hours < 10:
                    if minutes < 10:
                        time_text = "0"+str(hours)+":0"+str(minutes)
                    else:
                        time_text = "0"+str(hours)+":"+str(minutes)
                elif hours >= 99:
                    if minutes < 10:
                        time_text = "99:0"+str(minutes)
                    else:
                        time_text = "99:"+str(minutes)
                else:
                    if minutes < 10:
                        time_text = str(hours)+":0"+str(minutes)
                    else:
                        time_text = str(hours)+":"+str(minutes)
            else:
                hours = 0
                minutes = int(((total_minutes % 60)/60)*60)
                if minutes < 10:
                    time_text = "00:0"+str(minutes)
                else:
                    time_text = "00:"+str(minutes)

            t_time1 = font5.render("Game Time: "+time_text, True, black)
            t_time1_box = t_time1.get_rect()
            t_time1_box.center = (1570/self.font_scale),((320/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_time1,t_time1_box)
            #Level [7]
            t_lvl1 = font5.render("Level: "+str(profile1[7]), True, black)
            t_lvl1_box = t_lvl1.get_rect()
            t_lvl1_box.center = (1170/self.font_scale),((320/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_lvl1,t_lvl1_box)

            items = profile1[13].split(" ")
            items.pop()
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Sword_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(240/self.font_scale,400/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Torch_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(299/self.font_scale,400/self.font_scale))
            if items[5] == "True":
                main_menu_image = pygame.image.load("images/menu/Bomb_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(358/self.font_scale,400/self.font_scale))
            if items[7] == "True":
                main_menu_image = pygame.image.load("images/menu/Hookshot_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(417/self.font_scale,400/self.font_scale))
            if items[9] == "True":
                main_menu_image = pygame.image.load("images/menu/Bow_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(476/self.font_scale,400/self.font_scale))
            
            items = profile1[16].split(" ")
            items.pop()
            
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss1.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(560/self.font_scale,398/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss2.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(623/self.font_scale,398/self.font_scale))

        else:
            text_prof1 = font5.render("[ Empty Profile ]", True, black)
            text_prof1_box = text_prof1.get_rect()
            text_prof1_box.center = ((self.width/32)*16),((self.height/18)*(4+((13-((13/3)*2))/2))) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(text_prof1,text_prof1_box)

        file = open("profiles\Profile2.txt","r")
        profile2 = file.read()
        file.close()
        name_list = []
        name = ""
        if profile2 != "":
            profile2 = profile2.split("\n")
            name_list = profile2[1].split("  ")
            for letter in name_list:
                name = name + str(letter)
            t_prof2 = font5.render(name, True, black)
            t_prof2_box = t_prof2.get_rect()
            width,height = t_prof2.get_size()
            t_prof2_box.center = (((self.width/32)*4)+width/2),((580/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_prof2,t_prof2_box)
            #Game time
            total_minutes = (int(float( (int(float(profile2[0]))) / 60)))
            if total_minutes >= 60:
                hours = int(float(total_minutes / 60))
                minutes = int(((total_minutes % 60)/60)*60)
                if hours < 10:
                    if minutes < 10:
                        time_text = "0"+str(hours)+":0"+str(minutes)
                    else:
                        time_text = "0"+str(hours)+":"+str(minutes)
                elif hours >= 99:
                    if minutes < 10:
                        time_text = "99:0"+str(minutes)
                    else:
                        time_text = "99:"+str(minutes)
                else:
                    if minutes < 10:
                        time_text = str(hours)+":0"+str(minutes)
                    else:
                        time_text = str(hours)+":"+str(minutes)
            else:
                hours = 0
                minutes = int(((total_minutes % 60)/60)*60)
                if minutes < 10:
                    time_text = "00:0"+str(minutes)
                else:
                    time_text = "00:"+str(minutes)

            t_time2 = font5.render("Game Time: "+time_text, True, black)
            t_time2_box = t_time2.get_rect()
            t_time2_box.center = (1570/self.font_scale),((580/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_time2,t_time2_box)
            #Level [7]
            t_lvl2 = font5.render("Level: "+str(profile2[7]), True, black)
            t_lvl2_box = t_lvl2.get_rect()
            t_lvl2_box.center = (1170/self.font_scale),((580/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_lvl2,t_lvl2_box)

            items = profile2[13].split(" ")
            items.pop()
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Sword_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(240/self.font_scale,660/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Torch_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(299/self.font_scale,660/self.font_scale))
            if items[5] == "True":
                main_menu_image = pygame.image.load("images/menu/Bomb_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(358/self.font_scale,660/self.font_scale))
            if items[7] == "True":
                main_menu_image = pygame.image.load("images/menu/Hookshot_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(417/self.font_scale,660/self.font_scale))
            if items[9] == "True":
                main_menu_image = pygame.image.load("images/menu/Bow_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(476/self.font_scale,660/self.font_scale))
            
            items = profile2[16].split(" ")
            items.pop()
            
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss1.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(560/self.font_scale,658/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss2.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(623/self.font_scale,658/self.font_scale))
            
        else:
            text_prof2 = font5.render("[ Empty Profile ]", True, black)
            text_prof2_box = text_prof2.get_rect()
            text_prof2_box.center = ((self.width/32)*16),((self.height/18)*((4+(13/3))+((13-((13/3)*2))/2)))
            self.screen.blit(text_prof2,text_prof2_box)

        file = open("profiles\Profile3.txt","r")
        profile3 = file.read()
        file.close()
        name_list = []
        name = ""
        if profile3 != "":
            profile3 = profile3.split("\n")
            name_list = profile3[1].split("  ")
            for letter in name_list:
                name = name + str(letter)
            t_prof3 = font5.render(name, True, black)
            t_prof3_box = t_prof3.get_rect()
            width,height = t_prof3.get_size()
            t_prof3_box.center = (((self.width/32)*4)+width/2),((840/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_prof3,t_prof3_box)
            #Game time
            total_minutes = (int(float( (int(float(profile3[0]))) / 60)))
            if total_minutes >= 60:
                hours = int(float(total_minutes / 60))
                minutes = int(((total_minutes % 60)/60)*60)
                if hours < 10:
                    if minutes < 10:
                        time_text = "0"+str(hours)+":0"+str(minutes)
                    else:
                        time_text = "0"+str(hours)+":"+str(minutes)
                elif hours >= 99:
                    if minutes < 10:
                        time_text = "99:0"+str(minutes)
                    else:
                        time_text = "99:"+str(minutes)
                else:
                    if minutes < 10:
                        time_text = str(hours)+":0"+str(minutes)
                    else:
                        time_text = str(hours)+":"+str(minutes)
            else:
                hours = 0
                minutes = int(((total_minutes % 60)/60)*60)
                if minutes < 10:
                    time_text = "00:0"+str(minutes)
                else:
                    time_text = "00:"+str(minutes)

            t_time3 = font5.render("Game Time: "+time_text, True, black)
            t_time3_box = t_time3.get_rect()
            t_time3_box.center = (1570/self.font_scale),((840/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_time3,t_time3_box)
            #Level [7]
            t_lvl3 = font5.render("Level: "+str(profile3[7]), True, black)
            t_lvl3_box = t_lvl3.get_rect()
            t_lvl3_box.center = (1170/self.font_scale),((840/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_lvl3,t_lvl3_box)

            items = profile3[13].split(" ")
            items.pop()
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Sword_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(240/self.font_scale,920/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Torch_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(299/self.font_scale,920/self.font_scale))
            if items[5] == "True":
                main_menu_image = pygame.image.load("images/menu/Bomb_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(358/self.font_scale,920/self.font_scale))
            if items[7] == "True":
                main_menu_image = pygame.image.load("images/menu/Hookshot_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(417/self.font_scale,920/self.font_scale))
            if items[9] == "True":
                main_menu_image = pygame.image.load("images/menu/Bow_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(476/self.font_scale,920/self.font_scale))
            
            items = profile3[16].split(" ")
            items.pop()
            
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss1.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(560/self.font_scale,918/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss2.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(623/self.font_scale,918/self.font_scale))
            
            
        else:
            text_prof3 = font5.render("[ Empty Profile ]", True, black)
            text_prof3_box = text_prof3.get_rect()
            text_prof3_box.center = ((self.width/32)*16),((self.height/18)*((4+((13/3)*2))+((13-((13/3)*2))/2)))
            self.screen.blit(text_prof3,text_prof3_box)

        #Backing for number of profile
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*4,(self.width/32)*2 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+(13/3)),(self.width/32)*2 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+((13/3)*2)),(self.width/32)*2 -8,(self.height/18)*(13-((13/3)*2)) -4))

        font2 = pygame.font.SysFont("georgia", int(60/self.font_scale))

        new_menutext2 = font2.render("1", True, white)
        new_menutextbox2 = new_menutext2.get_rect()
        new_menutextbox2.center = ((self.width/32)*2,(self.height/18)*6)

        new_menutext3 = font2.render("2", True, white)
        new_menutextbox3 = new_menutext3.get_rect()
        new_menutextbox3.center = ((self.width/32)*2,(self.height/18)*10.25)

        new_menutext4 = font2.render("3", True, white)
        new_menutextbox4 = new_menutext4.get_rect()
        new_menutextbox4.center = ((self.width/32)*2,(self.height/18)*14.5)

        self.screen.blit(new_menutext2,new_menutextbox2)
        self.screen.blit(new_menutext3,new_menutextbox3)
        self.screen.blit(new_menutext4,new_menutextbox4)

        self.NG_P1.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.NG_P1.IsOver(mouse_pos,click1,self.screen_state,self)

        self.NG_P2.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.NG_P2.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.NG_P3.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.NG_P3.IsOver(mouse_pos,click1,self.screen_state,self)

        self.NG_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.NG_back.IsOver(mouse_pos,click1,self.screen_state,self)

    def DrawNGProfile(self,mouse_pos,click1,profile): #Draws the menu for creating a name (Profile)
        while True:
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*5,(self.height/18)*3,(self.width/32)*22,(self.height/18)*12))
            pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*5 +3,(self.height/18)*3 +3,(self.width/32)*22 -6,(self.height/18)*12 -6))
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*8,(self.height/18)*8,(self.width/32)*16,(self.height/18)*2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*8 +2,(self.height/18)*8 +2,(self.width/32)*16 -4,(self.height/18)*2 -4))
            font2 = pygame.font.SysFont("georgia", int(65/self.font_scale))
            NP_text1 = font2.render("Enter your hero's name (16 letter limit):", True, black)
            NP_textbox1 = NP_text1.get_rect()
            NP_textbox1.center = ((self.width/32)*16,(self.height/18)*6)
            self.screen.blit(NP_text1,NP_textbox1)
            click1 = False
            letter = ""
            backspace = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: #So only registers when pressed down once
                    if 97 <= event.key <= 123 or event.key == 32: #a-z or space
                        if event.mod == 8192: #If letter is a capital
                            letter = chr(event.key).upper()
                        else:
                            letter = chr(event.key)
                    elif event.key == 8:#8 - Backspace
                        backspace = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    click1 = True
            if letter != "": #Appends to end of list
                if len(self.prof_name) < 16:
                    self.prof_name.append(letter)
                    
                self.prof_name[0] = self.prof_name[0].upper() #So the name starts capitalised
            if backspace == True: #Pops last in list
                if len(self.prof_name) != 0:
                    self.prof_name.pop()

            self.DrawNPName()
            
            mouse_pos = pygame.mouse.get_pos()

            self.NP_continue.Draw(mouse_pos,click1,False,self)
            if len(self.prof_name) >= 1:
                self.screen_state = self.NP_continue.IsOver(mouse_pos,click1,self.screen_state,self)
                if self.screen_state == "New Profile":
                    self.chosen_profile = profile
          
            self.NP_back.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.NP_back.IsOver(mouse_pos,click1,self.screen_state,self)
            if self.screen_state[:10] != "NG Profile":
                break
            else:
                pygame.display.flip()

    def DrawNPName(self): #Draws what name the user has typed (Or is in the process of typing)
        string = ""
        for Letter in self.prof_name:
            string += Letter
        font2 = pygame.font.SysFont("georgia", int(60/self.font_scale))
        NP_text2 = font2.render(string, True, black)
        NP_textbox2 = NP_text2.get_rect()
        NP_textbox2.center = ((self.width/32)*16,(self.height/18)*9)
        self.screen.blit(NP_text2,NP_textbox2)


    def DrawLoadGame(self,mouse_pos,click1): #Draws the load game menu
        font1 = pygame.font.SysFont("georgia", int(80/self.font_scale))
        
        main_menutext1 = font1.render("Load game", True, black)
        main_menutextbox1 = main_menutext1.get_rect()
        main_menutextbox1.center = (self.width/2, self.height/7.5)
        
        pygame.draw.rect(self.screen, black, pygame.Rect(self.width/32 -2, self.height/18 -2, (self.width/32)*30 +4, (self.height/18)*16 +4)) #Black 2 pixel outline (This is the menu box)
        pygame.draw.rect(self.screen, old_yellow, pygame.Rect(self.width/32, self.height/18, (self.width/32)*30, (self.height/18)*16)) #Yellow inside

        self.screen.blit(main_menutext1,main_menutextbox1)
        
        
        #Profile 1,2 and 3 outline
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*4,(self.width/32)*30 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+(13/3)),(self.width/32)*30 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+((13/3)*2)),(self.width/32)*30 -8,(self.height/18)*(13-((13/3)*2)) -4))

        #Profile 1,2 and 3
        pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32) +6,(self.height/18)*4 +2,(self.width/32)*30 -12,(self.height/18)*(13-((13/3)*2)) -8))
        pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32) +6,(self.height/18)*(4+(13/3)) +2,(self.width/32)*30 -12,(self.height/18)*(13-((13/3)*2)) -8))
        pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32) +6,(self.height/18)*(4+((13/3)*2)) +2,(self.width/32)*30 -12,(self.height/18)*(13-((13/3)*2)) -8))

        font5 = pygame.font.SysFont("georgia", int(50/self.font_scale))
        file = open("profiles\Profile1.txt","r")
        profile1 = file.read()
        file.close()
        name_list = []
        name = ""
        if profile1 != "": #If not empty, it will do stuff here
            profile1 = profile1.split("\n")
            name_list = profile1[1].split("  ")
            for letter in name_list:
                name = name + str(letter)
            t_prof1 = font5.render(name, True, black)
            t_prof1_box = t_prof1.get_rect()
            width,height = t_prof1.get_size()
            t_prof1_box.center = (((self.width/32)*4)+width/2),((320/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_prof1,t_prof1_box)
            
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*(31-4.5) -4,(self.height/18)*((4+(13-((13/3)*2)))-1.5) -4,(self.width/32)*4.5,(self.height/18)*1.5))
            pygame.draw.rect(self.screen, light_grey, pygame.Rect((self.width/32)*(31-4.5) -2,(self.height/18)*((4+(13-((13/3)*2)))-1.5) -2,(self.width/32)*4.5 -4,(self.height/18)*1.5 -4))

            self.LG_P1.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.LG_P1.IsOver(mouse_pos,click1,self.screen_state,self)

            self.DG_P1.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.DG_P1.IsOver(mouse_pos,click1,self.screen_state,self)

            #Time in format 00:00
            #seconds = (int(float(profile1[0])))
            
            total_minutes = (int(float( (int(float(profile1[0]))) / 60)))
            if total_minutes >= 60:
                hours = int(float(total_minutes / 60))
                minutes = int(((total_minutes % 60)/60)*60)
                if hours < 10:
                    if minutes < 10:
                        time_text = "0"+str(hours)+":0"+str(minutes)
                    else:
                        time_text = "0"+str(hours)+":"+str(minutes)
                elif hours >= 99:
                    if minutes < 10:
                        time_text = "99:0"+str(minutes)
                    else:
                        time_text = "99:"+str(minutes)
                else:
                    if minutes < 10:
                        time_text = str(hours)+":0"+str(minutes)
                    else:
                        time_text = str(hours)+":"+str(minutes)
            else:
                hours = 0
                minutes = int(((total_minutes % 60)/60)*60)
                if minutes < 10:
                    time_text = "00:0"+str(minutes)
                else:
                    time_text = "00:"+str(minutes)

            t_time1 = font5.render("Game Time: "+time_text, True, black)
            t_time1_box = t_time1.get_rect()
            t_time1_box.center = (1570/self.font_scale),((320/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_time1,t_time1_box)
            #Level [7]
            t_lvl1 = font5.render("Level: "+str(profile1[7]), True, black)
            t_lvl1_box = t_lvl1.get_rect()
            t_lvl1_box.center = (1170/self.font_scale),((320/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_lvl1,t_lvl1_box)

            items = profile1[13].split(" ")
            items.pop()
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Sword_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(240/self.font_scale,400/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Torch_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(299/self.font_scale,400/self.font_scale))
            if items[5] == "True":
                main_menu_image = pygame.image.load("images/menu/Bomb_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(358/self.font_scale,400/self.font_scale))
            if items[7] == "True":
                main_menu_image = pygame.image.load("images/menu/Hookshot_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(417/self.font_scale,400/self.font_scale))
            if items[9] == "True":
                main_menu_image = pygame.image.load("images/menu/Bow_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(476/self.font_scale,400/self.font_scale))
            
            items = profile1[16].split(" ")
            items.pop()
            
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss1.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(560/self.font_scale,398/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss2.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(623/self.font_scale,398/self.font_scale))
            
        else:
            text_prof1 = font5.render("[ Empty Profile ]", True, black)
            text_prof1_box = text_prof1.get_rect()
            text_prof1_box.center = ((self.width/32)*16),((self.height/18)*(4+((13-((13/3)*2))/2))) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(text_prof1,text_prof1_box)

        file = open("profiles\Profile2.txt","r")
        profile2 = file.read()
        file.close()
        name_list = []
        name = ""
        if profile2 != "":
            profile2 = profile2.split("\n")
            name_list = profile2[1].split("  ")
            for letter in name_list:
                name = name + str(letter)
            t_prof2 = font5.render(name, True, black)
            t_prof2_box = t_prof2.get_rect()
            width,height = t_prof2.get_size()
            t_prof2_box.center = (((self.width/32)*4)+width/2),((580/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_prof2,t_prof2_box)

            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*(31-4.5) -4,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-1.5) -5,(self.width/32)*4.5,(self.height/18)*1.5))
            pygame.draw.rect(self.screen, light_grey, pygame.Rect((self.width/32)*(31-4.5) -2,(self.height/18)*(((4+(13/3))+(13-((13/3)*2)))-1.5) -3,(self.width/32)*4.5 -4,(self.height/18)*1.5 -4))

            self.LG_P2.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.LG_P2.IsOver(mouse_pos,click1,self.screen_state,self)

            self.DG_P2.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.DG_P2.IsOver(mouse_pos,click1,self.screen_state,self)

            #Game time
            total_minutes = (int(float( (int(float(profile2[0]))) / 60)))
            if total_minutes >= 60:
                hours = int(float(total_minutes / 60))
                minutes = int(((total_minutes % 60)/60)*60)
                if hours < 10:
                    if minutes < 10:
                        time_text = "0"+str(hours)+":0"+str(minutes)
                    else:
                        time_text = "0"+str(hours)+":"+str(minutes)
                elif hours >= 99:
                    if minutes < 10:
                        time_text = "99:0"+str(minutes)
                    else:
                        time_text = "99:"+str(minutes)
                else:
                    if minutes < 10:
                        time_text = str(hours)+":0"+str(minutes)
                    else:
                        time_text = str(hours)+":"+str(minutes)
            else:
                hours = 0
                minutes = int(((total_minutes % 60)/60)*60)
                if minutes < 10:
                    time_text = "00:0"+str(minutes)
                else:
                    time_text = "00:"+str(minutes)

            t_time2 = font5.render("Game Time: "+time_text, True, black)
            t_time2_box = t_time2.get_rect()
            t_time2_box.center = (1570/self.font_scale),((580/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_time2,t_time2_box)
            #Level [7]
            t_lvl2 = font5.render("Level: "+str(profile2[7]), True, black)
            t_lvl2_box = t_lvl2.get_rect()
            t_lvl2_box.center = (1170/self.font_scale),((580/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_lvl2,t_lvl2_box)

            items = profile2[13].split(" ")
            items.pop()
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Sword_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(240/self.font_scale,660/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Torch_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(299/self.font_scale,660/self.font_scale))
            if items[5] == "True":
                main_menu_image = pygame.image.load("images/menu/Bomb_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(358/self.font_scale,660/self.font_scale))
            if items[7] == "True":
                main_menu_image = pygame.image.load("images/menu/Hookshot_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(417/self.font_scale,660/self.font_scale))
            if items[9] == "True":
                main_menu_image = pygame.image.load("images/menu/Bow_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(476/self.font_scale,660/self.font_scale))
            
            items = profile2[16].split(" ")
            items.pop()
            
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss1.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(560/self.font_scale,658/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss2.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(623/self.font_scale,658/self.font_scale))
            
        else:
            text_prof2 = font5.render("[ Empty Profile ]", True, black)
            text_prof2_box = text_prof2.get_rect()
            text_prof2_box.center = ((self.width/32)*16),((self.height/18)*((4+(13/3))+((13-((13/3)*2))/2)))
            self.screen.blit(text_prof2,text_prof2_box)

        file = open("profiles\Profile3.txt","r")
        profile3 = file.read()
        file.close()
        name_list = []
        name = ""
        if profile3 != "":
            profile3 = profile3.split("\n")
            name_list = profile3[1].split("  ")
            for letter in name_list:
                name = name + str(letter)
            t_prof3 = font5.render(name, True, black)
            t_prof3_box = t_prof3.get_rect()
            width,height = t_prof3.get_size()
            t_prof3_box.center = (((self.width/32)*4)+width/2),((840/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_prof3,t_prof3_box)
            
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*(31-4.5) -4,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-1.5) -4,(self.width/32)*4.5,(self.height/18)*1.5))
            pygame.draw.rect(self.screen, light_grey, pygame.Rect((self.width/32)*(31-4.5) -2,(self.height/18)*(((4+((13/3)*2))+(13-((13/3)*2)))-1.5) -2,(self.width/32)*4.5 -4,(self.height/18)*1.5 -4))

            self.LG_P3.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.LG_P3.IsOver(mouse_pos,click1,self.screen_state,self)

            self.DG_P3.Draw(mouse_pos,click1,False,self)
            self.screen_state = self.DG_P3.IsOver(mouse_pos,click1,self.screen_state,self)

            #Game time
            total_minutes = (int(float( (int(float(profile3[0]))) / 60)))
            if total_minutes >= 60:
                hours = int(float(total_minutes / 60))
                minutes = int(((total_minutes % 60)/60)*60)
                if hours < 10:
                    if minutes < 10:
                        time_text = "0"+str(hours)+":0"+str(minutes)
                    else:
                        time_text = "0"+str(hours)+":"+str(minutes)
                elif hours >= 99:
                    if minutes < 10:
                        time_text = "99:0"+str(minutes)
                    else:
                        time_text = "99:"+str(minutes)
                else:
                    if minutes < 10:
                        time_text = str(hours)+":0"+str(minutes)
                    else:
                        time_text = str(hours)+":"+str(minutes)
            else:
                hours = 0
                minutes = int(((total_minutes % 60)/60)*60)
                if minutes < 10:
                    time_text = "00:0"+str(minutes)
                else:
                    time_text = "00:"+str(minutes)

            t_time3 = font5.render("Game Time: "+time_text, True, black)
            t_time3_box = t_time3.get_rect()
            t_time3_box.center = (1570/self.font_scale),((840/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_time3,t_time3_box)
            #Level [7]
            t_lvl3 = font5.render("Level: "+str(profile3[7]), True, black)
            t_lvl3_box = t_lvl3.get_rect()
            t_lvl3_box.center = (1170/self.font_scale),((840/self.font_scale)) #Numbers just so it is centered in the middle of the profile
            self.screen.blit(t_lvl3,t_lvl3_box)

            items = profile3[13].split(" ")
            items.pop()
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Sword_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(240/self.font_scale,920/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Torch_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(299/self.font_scale,920/self.font_scale))
            if items[5] == "True":
                main_menu_image = pygame.image.load("images/menu/Bomb_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(358/self.font_scale,920/self.font_scale))
            if items[7] == "True":
                main_menu_image = pygame.image.load("images/menu/Hookshot_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(417/self.font_scale,920/self.font_scale))
            if items[9] == "True":
                main_menu_image = pygame.image.load("images/menu/Bow_Icon.png").convert_alpha()
                main_menu_image = pygame.transform.scale(main_menu_image,(int(60/self.font_scale),int(60/self.font_scale)))
                self.screen.blit(main_menu_image,(476/self.font_scale,920/self.font_scale))
            
            items = profile3[16].split(" ")
            items.pop()
            
            if items[1] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss1.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(560/self.font_scale,918/self.font_scale))
            if items[3] == "True":
                main_menu_image = pygame.image.load("images/menu/Boss2.png").convert_alpha()
                boss_img = pygame.transform.scale(main_menu_image,(int(64/self.font_scale),int(64/self.font_scale)))
                self.screen.blit(boss_img,(623/self.font_scale,918/self.font_scale))
            
        else:
            text_prof3 = font5.render("[ Empty Profile ]", True, black)
            text_prof3_box = text_prof3.get_rect()
            text_prof3_box.center = ((self.width/32)*16),((self.height/18)*((4+((13/3)*2))+((13-((13/3)*2))/2)))
            self.screen.blit(text_prof3,text_prof3_box)

        #Backing for number of profile
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*4,(self.width/32)*2 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+(13/3)),(self.width/32)*2 -8,(self.height/18)*(13-((13/3)*2)) -4))
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32) +4,(self.height/18)*(4+((13/3)*2)),(self.width/32)*2 -8,(self.height/18)*(13-((13/3)*2)) -4))

        font2 = pygame.font.SysFont("georgia", int(60/self.font_scale))

        new_menutext2 = font2.render("1", True, white)
        new_menutextbox2 = new_menutext2.get_rect()
        new_menutextbox2.center = ((self.width/32)*2,(self.height/18)*6)

        new_menutext3 = font2.render("2", True, white)
        new_menutextbox3 = new_menutext3.get_rect()
        new_menutextbox3.center = ((self.width/32)*2,(self.height/18)*10.25)

        new_menutext4 = font2.render("3", True, white)
        new_menutextbox4 = new_menutext4.get_rect()
        new_menutextbox4.center = ((self.width/32)*2,(self.height/18)*14.5)

        self.screen.blit(new_menutext2,new_menutextbox2)
        self.screen.blit(new_menutext3,new_menutextbox3)
        self.screen.blit(new_menutext4,new_menutextbox4)

        self.NG_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.NG_back.IsOver(mouse_pos,click1,self.screen_state,self)
        
        self.LG_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.LG_back.IsOver(mouse_pos,click1,self.screen_state,self)

    def DrawDeleteConfirmation(self,mouse_pos,click1,delete_profile):

        font1 = pygame.font.SysFont("georgia", int(30/self.font_scale))
        font2 = pygame.font.SysFont("georgia", int(70/self.font_scale))
        
        pygame.draw.rect(self.screen, black, pygame.Rect(560/self.font_scale -2,340/self.font_scale -2,800/self.font_scale +4,400/self.font_scale +4))
        pygame.draw.rect(self.screen, off_yellow, pygame.Rect(560/self.font_scale,340/self.font_scale,800/self.font_scale,400/self.font_scale))
        
        menu_txt_x = int(300/self.font_scale) #960, 
        menu_txt_y = int(90/self.font_scale)
        menu_font_size = int(60/self.font_scale)

        deletetext1 = font2.render("Are you sure?", True, black)
        deletetextbox1 = deletetext1.get_rect()
        deletetextbox1.center = (960/self.font_scale,460/self.font_scale)

        deletetext2 = font1.render("(Deletion cannot be undone)", True, black)
        deletetextbox2 = deletetext2.get_rect()
        deletetextbox2.center = (960/self.font_scale,530/self.font_scale)

        self.Delete_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.Delete_back.IsOver(mouse_pos,click1,self.screen_state,self)

        self.Delete_profile.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.Delete_profile.IsOver(mouse_pos,click1,self.screen_state,self)

        self.screen.blit(deletetext1,deletetextbox1)
        self.screen.blit(deletetext2,deletetextbox2)

    def DeleteProfile(self,delete_profile):
        file = open("profiles\Profile"+str(delete_profile)+".txt","w")
        file.close()

    def DrawOptions(self,mouse_pos,click1,clickdown): #Draws the options menu, and all the contents of the sub-menus
        self.attribute_change = None
        font1 = pygame.font.SysFont("georgia", int(80/self.font_scale))

        #self.screen.fill(grass_green)
        self.MainMenuImageDraw()
        
        main_menutext1 = font1.render("Options", True, black)
        main_menutextbox1 = main_menutext1.get_rect()
        main_menutextbox1.center = (self.width/2, self.height/7.5)

        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)-2, self.height/18 -2, (self.width/32)*30 +4, (self.height/18)*16 +4)) #Black 2 pixel outline
        pygame.draw.rect(self.screen, old_yellow, pygame.Rect((self.width/32), self.height/18, (self.width/32)*30, (self.height/18)*16)) #White inside
        
        self.screen.blit(main_menutext1,main_menutextbox1)


        #Sub menu changing buttons
        try:
            self.subscreen_state
        except: #If the state variable has not been instanitated and the state is the options menu
            self.subscreen_state = "Game Menu" #Then change subscreen state to Game menu

        #Draws the box behind which sub-menu it is
                            #PARAMETERES:Screen,Colour,xpos,ypos,width,height
        #Behind "Game Options", first line outline then second line is hollow yellow fill
        pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*1.4 -2 , ((self.height/18)*4.5)-int(50/self.font_scale) -2 , (self.width/32)*7 +4 , int(100/self.font_scale)+4))
        pygame.draw.rect(self.screen, off_yellow, pygame.Rect(((self.width/32)*1.4),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
        #Behind "Video Settings"
        pygame.draw.rect(self.screen, black, pygame.Rect(((self.width/32)*8.8)-2,((self.height/18)*4.5)-int(50/self.font_scale)-2,(self.width/32)*7+4,int(100/self.font_scale)+4))
        pygame.draw.rect(self.screen, off_yellow, pygame.Rect(((self.width/32)*8.8),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
        #Behind "Controls"
        pygame.draw.rect(self.screen, black, pygame.Rect(((self.width/32)*16.2)-2,((self.height/18)*4.5)-int(50/self.font_scale)-2,(self.width/32)*7+4,int(100/self.font_scale)+4))
        pygame.draw.rect(self.screen, off_yellow, pygame.Rect(((self.width/32)*16.2),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
        #Behind "Audio Settings"
        pygame.draw.rect(self.screen, black, pygame.Rect(((self.width/32)*23.6)-2,((self.height/18)*4.5)-int(50/self.font_scale)-2,(self.width/32)*7+4,int(100/self.font_scale)+4))
        pygame.draw.rect(self.screen, off_yellow, pygame.Rect(((self.width/32)*23.6),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))

        if self.subscreen_state == "Game Menu": #Before the same selection statement later as so this is drawn behind the text
            pygame.draw.rect(self.screen, light_grey, pygame.Rect(((self.width/32)*1.4),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
        elif self.subscreen_state == "Video Menu":
            pygame.draw.rect(self.screen, light_grey, pygame.Rect(((self.width/32)*8.8),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
        elif self.subscreen_state == "Controls Menu":
            pygame.draw.rect(self.screen, light_grey, pygame.Rect(((self.width/32)*16.2),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
        elif self.subscreen_state == "Audio Menu":
            pygame.draw.rect(self.screen, light_grey, pygame.Rect(((self.width/32)*23.6),((self.height/18)*4.5)-int(50/self.font_scale),(self.width/32)*7,int(100/self.font_scale)))
            
        #Draws the buttons and the method used for it to function
        #"Game Options"
        self.Op_game.Draw(mouse_pos,click1,False,self)
        self.subscreen_state = self.Op_game.IsOver(mouse_pos,click1,self.subscreen_state,self)
        #"Video Settings"
        self.Op_video.Draw(mouse_pos,click1,False,self)
        self.subscreen_state = self.Op_video.IsOver(mouse_pos,click1,self.subscreen_state,self)
        #"Controls"
        self.Op_controls.Draw(mouse_pos,click1,False,self)
        self.subscreen_state = self.Op_controls.IsOver(mouse_pos,click1,self.subscreen_state,self)
        #"Audio Settings"
        self.Op_audio.Draw(mouse_pos,click1,False,self)
        self.subscreen_state = self.Op_audio.IsOver(mouse_pos,click1,self.subscreen_state,self)

        if self.subscreen_state == "Game Menu": #The buttons in each sub-menu here
            
            self.Op_game_difficulty.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_game_difficulty.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_game_text1.Draw(mouse_pos,click1,False,self)

            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*23.6-2,(self.height/18)*15.9 -2,(self.width/32)*7+4,(self.height/18)*0.9+4)) #Reset to default button backing
            pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*23.6,(self.height/18)*15.9,(self.width/32)*7,(self.height/18)*0.9))

            self.Op_game_reset.Draw(mouse_pos,click1,False,self) #Reset to default button text
            self.attribute_change = self.Op_game_reset.IsOver(mouse_pos,click1,self.attribute_change,self)

        elif self.subscreen_state == "Video Menu":

            font3 = pygame.font.SysFont("georgia", int(60/self.font_scale))
            
            #Fullscreen
            self.Op_video_full.Draw(mouse_pos,click1,False,self) #False means no outline lol
            self.attribute_change = self.Op_video_full.IsOver(mouse_pos,click1,self.attribute_change,self) #Changes the actual thing to "Full Change"
            if self.fullscreen == 1: #Text for whether fullscreen or not
                text_full = font3.render("Fullscreen", True, black)
                text_full_box = text_full.get_rect()
                text_full_box.center = ((self.width/32)*10)+10,((self.height/18)*8)+3
                self.screen.blit(text_full,text_full_box)

            elif self.fullscreen == 0:
                text_full = font3.render("Windowed", True, black)
                text_full_box = text_full.get_rect()
                text_full_box.center = ((self.width/32)*10)+10,((self.height/18)*8)+3
                self.screen.blit(text_full,text_full_box)
                
            #Resolution
            self.Op_video_res.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_video_res.IsOver(mouse_pos,click1,self.attribute_change,self)
            if self.res == 1:
                text_full = font3.render("1920×1080", True, black)
                text_full_box = text_full.get_rect()
                text_full_box.center = ((self.width/32)*10)+15,((self.height/18)*10)+1
                self.screen.blit(text_full,text_full_box)
            elif self.res == 2:
                text_full = font3.render("1280×720", True, black)
                text_full_box = text_full.get_rect()
                text_full_box.center = ((self.width/32)*10)+15,((self.height/18)*10)+1
                self.screen.blit(text_full,text_full_box)
            elif self.res == 3:
                text_full = font3.render("1024×576", True, black)
                text_full_box = text_full.get_rect()
                text_full_box.center = ((self.width/32)*10)+15,((self.height/18)*10)+1
                self.screen.blit(text_full,text_full_box)

            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*23.6-2,(self.height/18)*15.9 -2,(self.width/32)*7+4,(self.height/18)*0.9+4)) #Reset to default button backing
            pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*23.6,(self.height/18)*15.9,(self.width/32)*7,(self.height/18)*0.9))

            self.Op_video_reset.Draw(mouse_pos,click1,False,self) #Reset to default button text
            self.attribute_change = self.Op_video_reset.IsOver(mouse_pos,click1,self.attribute_change,self)


        elif self.subscreen_state == "Controls Menu":
                                            #Colour,xpos,ypos,width,height
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*1.4 -2, (self.height/18)*5.7 -2, (self.width/32)*29.2 +4,(self.height/18)*10 +4)) #Table outline
            pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*1.4, (self.height/18)*5.7, (self.width/32)*29.2, (self.height/18)*10))

            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*1.4, (self.height/18)*5.7, (self.width/32)*28.5 +2, (self.height/18)*10))
            
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*5.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*6.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*7.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*8.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*9.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*10.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*11.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*12.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*13.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*14.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))

            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*5.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*6.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*7.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*8.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*9.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*10.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*11.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*12.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*13.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*10.9 +1, (self.height/18)*14.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))

            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*5.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*6.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*7.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*8.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*9.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*10.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*11.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*12.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*13.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))
            pygame.draw.rect(self.screen, white, pygame.Rect((self.width/32)*20.4 +1, (self.height/18)*14.7 +1, (self.width/32)*9.5 -2, (self.height/18)*1 -2))

            
            self.InstantiateControls(mouse_pos,clickdown)
            self.DrawControls(mouse_pos,click1,clickdown)
            self.scrollbar1 = AttributeButton("","Move Scroll Bar",((self.width/32)*30.25 +1,self.csypos+(self.height/18)*0.5),(self.width/32)*0.7,(self.height/18)*1,black,"georgia",int(40/self.font_scale),"Main Menu")
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*29.9,self.csypos,(self.width/32)*0.7,(self.height/18)*1)) #Actual black rectangle of the scroll bar


            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*23.6-2,(self.height/18)*15.9 -2,(self.width/32)*7+4,(self.height/18)*0.9+4)) #Reset to default button backing
            pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*23.6,(self.height/18)*15.9,(self.width/32)*7,(self.height/18)*0.9))

            self.scrollbar1.Draw(mouse_pos,clickdown,False,self)
            self.attribute_change = self.scrollbar1.IsOver(mouse_pos,clickdown,self.attribute_change,self)
            
            self.Op_controls_reset.Draw(mouse_pos,click1,False,self) #Reset to default button and text
            self.attribute_change = self.Op_controls_reset.IsOver(mouse_pos,click1,self.attribute_change,self)

        elif self.subscreen_state == "Audio Menu":
            font4 = pygame.font.SysFont("georgia", int(60/self.font_scale))

            text_full = font4.render("Master Volume:", True, black)
            text_full_box = text_full.get_rect()
            text_full_box.center = ((self.width/32)*5.7),((self.height/18)*8)
            self.screen.blit(text_full,text_full_box)

            text_full = font4.render("Music Volume:", True, black)
            text_full_box = text_full.get_rect()
            text_full_box.center = ((self.width/32)*5.7),((self.height/18)*10.5)
            self.screen.blit(text_full,text_full_box)

            text_full = font4.render("Sound Effects:", True, black)
            text_full_box = text_full.get_rect()
            text_full_box.center = ((self.width/32)*5.7),((self.height/18)*13)
            self.screen.blit(text_full,text_full_box)

            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*10.25,(self.height/18)*8,(self.width/32)*17,(self.height/18)*0.1)) #Line for volume
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*10.25,(self.height/18)*10.5,(self.width/32)*17,(self.height/18)*0.1))
            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*10.25,(self.height/18)*13,(self.width/32)*17,(self.height/18)*0.1))


            self.UpdateAudioMenu(mouse_pos,clickdown)

            self.slidebar1.Draw(mouse_pos,clickdown,False,self) #Reset to default button and text
            self.attribute_change = self.slidebar1.IsOver(mouse_pos,clickdown,self.attribute_change,self)

            self.slidebar2.Draw(mouse_pos,clickdown,False,self) #Reset to default button and text
            self.attribute_change = self.slidebar2.IsOver(mouse_pos,clickdown,self.attribute_change,self)

            self.slidebar3.Draw(mouse_pos,clickdown,False,self) #Reset to default button and text
            self.attribute_change = self.slidebar3.IsOver(mouse_pos,clickdown,self.attribute_change,self)
            
            pygame.draw.rect(self.screen, black, pygame.Rect(self.as1xpos,(self.height/18)*7.5,(self.width/32)*0.5,(self.height/18)*1)) #Reset to default button backing
            pygame.draw.rect(self.screen, black, pygame.Rect(self.as2xpos,(self.height/18)*10,(self.width/32)*0.5,(self.height/18)*1)) #Reset to default button backing
            pygame.draw.rect(self.screen, black, pygame.Rect(self.as3xpos,(self.height/18)*12.5,(self.width/32)*0.5,(self.height/18)*1)) #Reset to default button backing


            pygame.draw.rect(self.screen, black, pygame.Rect((self.width/32)*23.6-2,(self.height/18)*15.9 -2,(self.width/32)*7+4,(self.height/18)*0.9+4)) #Reset to default button backing
            pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*23.6,(self.height/18)*15.9,(self.width/32)*7,(self.height/18)*0.9))

            self.Op_audio_reset.Draw(mouse_pos,click1,False,self) #Reset to default button text
            self.attribute_change = self.Op_audio_reset.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.attribute_change != None:

            self.SettingsChange(clickdown)
        
        self.Op_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.Op_back.IsOver(mouse_pos,click1,self.screen_state,self)#

        self.InstantiateControls(mouse_pos,clickdown)

    def DrawControls(self,mouse_pos,click1,clickdown):
        self.attribute_change = None
        self.Op_control.Draw(mouse_pos,click1,False,self)
        self.Op_ckey.Draw(mouse_pos,click1,False,self)
        self.Op_cakey.Draw(mouse_pos,click1,False,self)

        self.InstantiateControls(mouse_pos,clickdown)

        if self.cscroll <= 1: #Will not be drawn if scrolled down by 1
            self.Op_control1.Draw(mouse_pos,click1,False,self) #First column of first row of controls (One line as no click detection)
            self.Op_ckey1.Draw(mouse_pos,click1,False,self) #Second column of first row of controls
            self.attribute_change = self.Op_ckey1.IsOver(mouse_pos,click1,self.attribute_change,self) #Click detection for that button drawn above
            self.Op_cakey1.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey1.IsOver(mouse_pos,click1,self.attribute_change,self)
            
        if self.cscroll <= 2:
            self.Op_control2.Draw(mouse_pos,click1,False,self)
            self.Op_ckey2.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey2.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey2.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey2.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.cscroll <= 3:
            self.Op_control3.Draw(mouse_pos,click1,False,self)
            self.Op_ckey3.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey3.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey3.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey3.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.cscroll <= 4:
            self.Op_control4.Draw(mouse_pos,click1,False,self)
            self.Op_ckey4.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey4.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey4.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey4.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.cscroll <= 5:
            self.Op_control5.Draw(mouse_pos,click1,False,self)
            self.Op_ckey5.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey5.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey5.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey5.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.cscroll <= 6:
            self.Op_control6.Draw(mouse_pos,click1,False,self)
            self.Op_ckey6.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey6.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey6.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey6.IsOver(mouse_pos,click1,self.attribute_change,self)
            
        if self.cscroll <= 7:
            self.Op_control7.Draw(mouse_pos,click1,False,self)
            self.Op_ckey7.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey7.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey7.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey7.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.cscroll <= 8:
            self.Op_control8.Draw(mouse_pos,click1,False,self)
            self.Op_ckey8.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey8.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey8.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey8.IsOver(mouse_pos,click1,self.attribute_change,self)

        if self.cscroll <= 9:
            self.Op_control9.Draw(mouse_pos,click1,False,self)
            self.Op_ckey9.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey9.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey9.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey9.IsOver(mouse_pos,click1,self.attribute_change,self)
            
        if self.cscroll <= 10 and self.cscroll >= 2:
            self.Op_control10.Draw(mouse_pos,click1,False,self)
            self.Op_ckey10.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey10.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey10.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey10.IsOver(mouse_pos,click1,self.attribute_change,self)
            
        if self.cscroll <= 11 and self.cscroll >= 3:
            self.Op_control11.Draw(mouse_pos,click1,False,self)
            self.Op_ckey11.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey11.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey11.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey11.IsOver(mouse_pos,click1,self.attribute_change,self)

        '''

        if self.cscroll <= 12 and self.cscroll >= 4:
            self.Op_control12.Draw(mouse_pos,click1,False,self)
            self.Op_ckey12.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_ckey12.IsOver(mouse_pos,click1,self.attribute_change,self)
            self.Op_cakey12.Draw(mouse_pos,click1,False,self)
            self.attribute_change = self.Op_cakey12.IsOver(mouse_pos,click1,self.attribute_change,self)

        '''

    def DrawCredits(self,mouse_pos,click1): #Draws the credits menu
        font1 = pygame.font.SysFont("georgia", int(80/self.font_scale))
        font2 = pygame.font.SysFont("georgia", int(40/self.font_scale))
        font3 = pygame.font.SysFont("georgia", int(60/self.font_scale))
        
        main_menutext1 = font1.render("Credits", True, black)
        main_menutextbox1 = main_menutext1.get_rect()
        main_menutextbox1.center = (self.width/2, self.height/7.5)

        pygame.draw.rect(self.screen, black, pygame.Rect(self.width/32 -2, self.height/18 -2, (self.width/32)*30 +4, (self.height/18)*16 +4)) #Black 2 pixel outline
        pygame.draw.rect(self.screen, old_yellow, pygame.Rect(self.width/32, self.height/18, (self.width/32)*30, (self.height/18)*16)) #White inside
        

        creditstext1 = font2.render("All programming, design and the majority of the art is made by Akibul Hoque.", True, black)
        creditstextbox1 = creditstext1.get_rect()
        creditstextbox1.center = (960/self.font_scale,480/self.font_scale)

        creditstext2 = font2.render("Credits to all other assets used in this game is containted in the credits text file alongside this game.", True, black)
        creditstextbox2 = creditstext2.get_rect()
        creditstextbox2.center = (960/self.font_scale,550/self.font_scale)

        creditstext3 = font2.render("Any assets I have created is also free for anyone to use.", True, black)
        creditstextbox3 = creditstext3.get_rect()
        creditstextbox3.center = (960/self.font_scale,620/self.font_scale)

        creditstext4 = font3.render("My Github: AKi47", True, black)
        creditstextbox4 = creditstext4.get_rect()
        creditstextbox4.center = (960/self.font_scale,880/self.font_scale)

        self.screen.blit(main_menutext1,main_menutextbox1)
        self.screen.blit(creditstext1,creditstextbox1)
        self.screen.blit(creditstext2,creditstextbox2)
        self.screen.blit(creditstext3,creditstextbox3)
        self.screen.blit(creditstext4,creditstextbox4)
        
        self.Cr_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.Cr_back.IsOver(mouse_pos,click1,self.screen_state,self)

    def DrawHowToPlay(self,mouse_pos,click1): #Draws the how to play menu jumpto101
        font1 = pygame.font.SysFont("georgia", int(80/self.font_scale))
        font2 = pygame.font.SysFont("georgia", int(32/self.font_scale))
        font3 = pygame.font.SysFont("georgia", int(40/self.font_scale))
        font4 = pygame.font.SysFont("georgia", int(46/self.font_scale))
        font5 = pygame.font.SysFont("georgia", int(42/self.font_scale))

        main_menutext1 = font1.render("How to play", True, black)
        main_menutextbox1 = main_menutext1.get_rect()
        main_menutextbox1.center = (self.width/2, self.height/7.5)

        pygame.draw.rect(self.screen, black, pygame.Rect(self.width/32 -2, self.height/18 -2, (self.width/32)*30 +4, (self.height/18)*16 +4)) #Black 2 pixel outline
        pygame.draw.rect(self.screen, old_yellow, pygame.Rect(self.width/32, self.height/18, (self.width/32)*30, (self.height/18)*16)) #White inside
        
        self.screen.blit(main_menutext1,main_menutextbox1)

        #PG and
        pagetext1 = font2.render(str(self.htp_page)+" of "+str(self.htp_max), True, black)
        pagetextbox1 = pagetext1.get_rect()
        pagetextbox1.center = (960/self.font_scale,960/self.font_scale)

        self.screen.blit(pagetext1,pagetextbox1)

        rarrow_x = 1060/self.font_scale
        rarrow_y = 940/self.font_scale

        larrow_x = 820/self.font_scale
        larrow_y = 940/self.font_scale

        arrow_dim = (int((39//self.font_scale)),int((40//self.font_scale)))
        

        if self.htp_page == 1:
            #self.Bombs = AttributeButton("","Bombs",(510/self.scale,460/self.self.font_scale),int(120/self.self.font_scale),int(120/self.self.font_scale),black,"georgia",int(60/self.font_scale),"Game")
            larrowinv_img = pygame.image.load("images/menu/leftarrowmax.png").convert_alpha()
            larrowinv_img = pygame.transform.scale(larrowinv_img,arrow_dim)
            larrowinv_pos = (larrow_x,larrow_y)
            self.screen.blit(larrowinv_img,larrowinv_pos)

        elif self.htp_page < 1:
            self.htp_page = 1
        else:
            larrowval_img = pygame.image.load("images/menu/leftarrow.png").convert_alpha()
            larrowval_img = pygame.transform.scale(larrowval_img,arrow_dim)
            larrowval_pos = (larrow_x,larrow_y)
            self.screen.blit(larrowval_img,larrowval_pos)
            
            self.HTPleft.Draw(mouse_pos,click1,False,self)
            self.change_HTP = self.HTPleft.IsOver(mouse_pos,click1,self.change_HTP,self)

        if self.htp_page == self.htp_max:
            rarrowinv_img = pygame.image.load("images/menu/rightarrowmax.png").convert_alpha()
            rarrowinv_img = pygame.transform.scale(rarrowinv_img,arrow_dim)
            rarrowinv_pos = (rarrow_x,rarrow_y)
            self.screen.blit(rarrowinv_img,rarrowinv_pos)
            
        elif self.htp_page > self.htp_max:
            self.htp_page = self.htp_max
        else:
            rarrowval_img = pygame.image.load("images/menu/rightarrow.png").convert_alpha()
            rarrowval_img = pygame.transform.scale(rarrowval_img,arrow_dim)
            rarrowval_pos = (rarrow_x,rarrow_y)
            self.screen.blit(rarrowval_img,rarrowval_pos)
            
            self.HTPright.Draw(mouse_pos,click1,False,self)
            self.change_HTP = self.HTPright.IsOver(mouse_pos,click1,self.change_HTP,self)

        if self.change_HTP == "HTP right":
            self.htp_page += 1
            self.change_HTP = None
        elif self.change_HTP == "HTP left":
            self.htp_page -= 1
            self.change_HTP = None

        if self.htp_page == 1: #Before you play
            #1 text boxes + heading box

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Before you start", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)
            
            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("Change your control binds in the", True, black)
            htptext2 = font2.render("controls menu in the options menu.", True, black)
            htptext3 = font2.render("Another important thing is to save", True, black)
            htptext4 = font2.render("your game often, when ingame press", True, black)
            htptext5 = font2.render("your bind for the menu (Default to", True, black)
            htptext6 = font2.render("ESC) and click save game and", True, black)
            htptext7 = font2.render("click confirm.", True, black)
            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()

            
            htptextbox1.center = (960/self.font_scale, 390/self.font_scale)
            htptextbox2.center = (960/self.font_scale, 430/self.font_scale)
            
            htptextbox3.center = (960/self.font_scale, 490/self.font_scale)
            htptextbox4.center = (960/self.font_scale, 530/self.font_scale)
            htptextbox5.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox6.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox7.center = (960/self.font_scale, 650/self.font_scale)

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            #1680 whole space (tot - 240)
            #560 - 3 sections
            #20 10 10 20 - shaved off
            #120 > 660 size 540
            #690 > 1230 size 540
            #1260 > 1800 size 540
        
        elif self.htp_page == 2: #Movement
            #1 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Movement", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("You move your character with the", True, black)
            htptext2 = font2.render("default buttons WASD or the arrow", True, black)
            htptext3 = font2.render("keys. You can jump with W and duck", True, black)
            htptext4 = font2.render("using S to avoid projectiles.", True, black)
            
            htptext5 = font2.render("If you lose your momentum mid-air", True, black)
            htptext6 = font2.render("(by hitting a ceiling or wall) you", True, black)
            htptext7 = font2.render("need to press the direction key", True, black)
            htptext8 = font2.render("again to move in that direction but", True, black)
            htptext9 = font2.render("slower, or else you wont go", True, black)
            htptext10 = font2.render("anywhere.", True, black)
            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()

            
            htptextbox1.center = (960/self.font_scale, 390/self.font_scale)
            htptextbox2.center = (960/self.font_scale, 430/self.font_scale)
            htptextbox3.center = (960/self.font_scale, 470/self.font_scale)
            htptextbox4.center = (960/self.font_scale, 510/self.font_scale)

            htptextbox5.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox6.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox7.center = (960/self.font_scale, 650/self.font_scale)
            htptextbox8.center = (960/self.font_scale, 690/self.font_scale)
            htptextbox9.center = (960/self.font_scale, 730/self.font_scale)
            htptextbox10.center = (960/self.font_scale, 770/self.font_scale)

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            
        elif self.htp_page == 3: #Attacking
            #3 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((120/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((120/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((1260/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((1260/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Attacking", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font5.render("Normal Attacks", True, black)
            htptext2 = font2.render("Once you have a sword, using the", True, black)
            htptext3 = font2.render("attack button (left click by", True, black)
            htptext4 = font2.render("default) will let your player swing", True, black)
            htptext5 = font2.render("their sword that upon hitting an", True, black)
            htptext6 = font2.render("enemy, knocks them back (depending", True, black)
            htptext7 = font2.render("on the enemy) and damages them.", True, black)
            
            htptext8 = font2.render("However enemies (as well as you)", True, black)
            htptext9 = font2.render("have attack immunity briefly after", True, black)
            htptext10 = font2.render("being hit.", True, black)


            htptext11 = font5.render("Low Attacks", True, black)
            htptext12 = font2.render("If you are crouched and you press", True, black)
            htptext13 = font2.render("the attack button, your character", True, black)
            htptext14 = font2.render("will perform a low attack.", True, black)
            htptext15 = font2.render("This is so that you can attack", True, black)
            htptext16 = font2.render("enemies on a ledge below you,", True, black)
            htptext17 = font2.render("however you cannot move while", True, black)
            htptext18 = font2.render("performing a low attack.", True, black)


            htptext19 = font5.render("Bow attacks", True, black)
            htptext20 = font2.render("Once you have acquired the bow and", True, black)
            htptext21 = font2.render("arrow, you can shoot enemies as", True, black)
            htptext22 = font2.render("long as you have arrows. Note you", True, black)
            htptext23 = font2.render("can't move when charging your bow.", True, black)
            
            htptext24 = font2.render("You can also shoot multiple enemies", True, black)
            htptext25 = font2.render("with one arrow and also remember", True, black)
            htptext26 = font2.render("that some levels are much easier", True, black)
            htptext27 = font2.render("by using the bow to kill enemies.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()
            htptextbox11 = htptext11.get_rect()
            htptextbox12 = htptext12.get_rect()
            htptextbox13 = htptext13.get_rect()
            htptextbox14 = htptext14.get_rect()
            htptextbox15 = htptext15.get_rect()
            htptextbox16 = htptext16.get_rect()
            htptextbox17 = htptext17.get_rect()
            htptextbox18 = htptext18.get_rect()
            htptextbox19 = htptext19.get_rect()
            htptextbox20 = htptext20.get_rect()
            htptextbox21 = htptext21.get_rect()
            htptextbox22 = htptext22.get_rect()
            htptextbox23 = htptext23.get_rect()
            htptextbox24 = htptext24.get_rect()
            htptextbox25 = htptext25.get_rect()
            htptextbox26 = htptext26.get_rect()
            htptextbox27 = htptext27.get_rect()


            
            htptextbox1.center = (390/self.font_scale, 360/self.font_scale)
            htptextbox2.center = (390/self.font_scale, 430/self.font_scale)
            htptextbox3.center = (390/self.font_scale, 470/self.font_scale)
            htptextbox4.center = (390/self.font_scale, 510/self.font_scale)
            htptextbox5.center = (390/self.font_scale, 550/self.font_scale)
            htptextbox6.center = (390/self.font_scale, 590/self.font_scale)
            htptextbox7.center = (390/self.font_scale, 630/self.font_scale)
            
            htptextbox8.center = (390/self.font_scale, 690/self.font_scale)
            htptextbox9.center = (390/self.font_scale, 730/self.font_scale)
            htptextbox10.center = (390/self.font_scale, 770/self.font_scale)


            htptextbox11.center = (960/self.font_scale, 390/self.font_scale)
            htptextbox12.center = (960/self.font_scale, 460/self.font_scale)
            htptextbox13.center = (960/self.font_scale, 500/self.font_scale)
            htptextbox14.center = (960/self.font_scale, 540/self.font_scale)
            htptextbox15.center = (960/self.font_scale, 580/self.font_scale)
            htptextbox16.center = (960/self.font_scale, 620/self.font_scale)
            htptextbox17.center = (960/self.font_scale, 660/self.font_scale)
            htptextbox18.center = (960/self.font_scale, 700/self.font_scale)


            htptextbox19.center = (1530/self.font_scale, 360/self.font_scale)
            htptextbox20.center = (1530/self.font_scale, 430/self.font_scale)
            htptextbox21.center = (1530/self.font_scale, 470/self.font_scale)
            htptextbox22.center = (1530/self.font_scale, 510/self.font_scale)
            htptextbox23.center = (1530/self.font_scale, 550/self.font_scale)
            
            htptextbox24.center = (1530/self.font_scale, 610/self.font_scale)
            htptextbox25.center = (1530/self.font_scale, 650/self.font_scale)
            htptextbox26.center = (1530/self.font_scale, 690/self.font_scale)
            htptextbox27.center = (1530/self.font_scale, 730/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            self.screen.blit(htptext11,htptextbox11)
            self.screen.blit(htptext12,htptextbox12)
            self.screen.blit(htptext13,htptextbox13)
            self.screen.blit(htptext14,htptextbox14)
            self.screen.blit(htptext15,htptextbox15)
            self.screen.blit(htptext16,htptextbox16)
            self.screen.blit(htptext17,htptextbox17)
            self.screen.blit(htptext18,htptextbox18)
            self.screen.blit(htptext19,htptextbox19)
            self.screen.blit(htptext20,htptextbox20)
            self.screen.blit(htptext21,htptextbox21)
            self.screen.blit(htptext22,htptextbox22)
            self.screen.blit(htptext23,htptextbox23)
            self.screen.blit(htptext24,htptextbox24)
            self.screen.blit(htptext25,htptextbox25)
            self.screen.blit(htptext26,htptextbox26)
            self.screen.blit(htptext27,htptextbox27)

        elif self.htp_page == 4: #Levelling
            #3 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((120/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((120/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((1260/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((1260/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Levelling", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font5.render("EXP", True, black)
            htptext2 = font2.render("When you kill enemies, you gain exp", True, black)
            htptext3 = font2.render("points. Press the inventory button", True, black)
            htptext4 = font2.render("(ENTER by default) to view levels", True, black)
            htptext5 = font2.render("and EXP. When you gain enough exp", True, black)
            htptext6 = font2.render("to level up, you will gain a skill", True, black)
            htptext7 = font2.render("point to level up a stat:", True, black)
            
            htptext8 = font5.render("Strength", True, black)
            htptext9 = font2.render("The strength stat refers to how", True, black)
            htptext10 = font2.render("much damage your sword will deal.", True, black)
            htptext11 = font2.render("Note that this is only your sword's", True, black)

            htptext12 = font2.render("damage and not your bow damage.", True, black)
            
            htptext13 = font5.render("Resilience", True, black)
            htptext14 = font2.render("Your resilience level refers to", True, black)
            htptext15 = font2.render("how much health you have, so the", True, black)
            htptext16 = font2.render("higher your level, the more hits", True, black)
            htptext17 = font2.render("you can take from enemies and not", True, black)
            htptext18 = font2.render("die. One level adds 5 hit points", True, black)
            htptext19 = font2.render("to your max health pool as well", True, black)
            htptext20 = font2.render("as heals you fully upon levelling", True, black)
            htptext21 = font2.render("up the skill.", True, black)
            
            htptext22 = font5.render("Speed", True, black)
            htptext23 = font2.render("The speed stat refers to how fast", True, black)
            htptext24 = font2.render("your character moves left and", True, black)
            
            htptext25 = font2.render("right. This can help making some", True, black)
            htptext26 = font2.render("jumps much easier to clear.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()
            htptextbox11 = htptext11.get_rect()
            htptextbox12 = htptext12.get_rect()
            htptextbox13 = htptext13.get_rect()
            htptextbox14 = htptext14.get_rect()
            htptextbox15 = htptext15.get_rect()
            htptextbox16 = htptext16.get_rect()
            htptextbox17 = htptext17.get_rect()
            htptextbox18 = htptext18.get_rect()
            htptextbox19 = htptext19.get_rect()
            htptextbox20 = htptext20.get_rect()
            htptextbox21 = htptext21.get_rect()
            htptextbox22 = htptext22.get_rect()
            htptextbox23 = htptext23.get_rect()
            htptextbox24 = htptext24.get_rect()
            htptextbox25 = htptext25.get_rect()
            htptextbox26 = htptext26.get_rect()


            
            htptextbox1.center = (390/self.font_scale, 360/self.font_scale)
            htptextbox2.center = (390/self.font_scale, 420/self.font_scale)
            htptextbox3.center = (390/self.font_scale, 460/self.font_scale)
            htptextbox4.center = (390/self.font_scale, 500/self.font_scale)
            htptextbox5.center = (390/self.font_scale, 540/self.font_scale)
            htptextbox6.center = (390/self.font_scale, 580/self.font_scale)
            htptextbox7.center = (390/self.font_scale, 620/self.font_scale)

            htptextbox8.center = (390/self.font_scale, 680/self.font_scale)
            htptextbox9.center = (390/self.font_scale, 740/self.font_scale)
            htptextbox10.center = (390/self.font_scale, 780/self.font_scale)
            htptextbox11.center = (390/self.font_scale, 820/self.font_scale)

            
            htptextbox12.center = (960/self.font_scale, 390/self.font_scale)  
            htptextbox13.center = (960/self.font_scale, 450/self.font_scale)
            htptextbox14.center = (960/self.font_scale, 510/self.font_scale)
            htptextbox15.center = (960/self.font_scale, 550/self.font_scale)
            htptextbox16.center = (960/self.font_scale, 590/self.font_scale)
            htptextbox17.center = (960/self.font_scale, 630/self.font_scale)
            htptextbox18.center = (960/self.font_scale, 670/self.font_scale)
            htptextbox19.center = (960/self.font_scale, 710/self.font_scale)
            htptextbox20.center = (960/self.font_scale, 750/self.font_scale)
            htptextbox21.center = (960/self.font_scale, 790/self.font_scale)

            
            htptextbox22.center = (1530/self.font_scale, 360/self.font_scale)
            htptextbox23.center = (1530/self.font_scale, 420/self.font_scale) 
            htptextbox24.center = (1530/self.font_scale, 460/self.font_scale)
            htptextbox25.center = (1530/self.font_scale, 500/self.font_scale)
            htptextbox26.center = (1530/self.font_scale, 540/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            self.screen.blit(htptext11,htptextbox11)
            self.screen.blit(htptext12,htptextbox12)
            self.screen.blit(htptext13,htptextbox13)
            self.screen.blit(htptext14,htptextbox14)
            self.screen.blit(htptext15,htptextbox15)
            self.screen.blit(htptext16,htptextbox16)
            self.screen.blit(htptext17,htptextbox17)
            self.screen.blit(htptext18,htptextbox18)
            self.screen.blit(htptext19,htptextbox19)
            self.screen.blit(htptext20,htptextbox20)
            self.screen.blit(htptext21,htptextbox21)
            self.screen.blit(htptext22,htptextbox22)
            self.screen.blit(htptext23,htptextbox23)
            self.screen.blit(htptext24,htptextbox24)
            self.screen.blit(htptext25,htptextbox25)
            self.screen.blit(htptext26,htptextbox26)
            
        elif self.htp_page == 5: #Interactables
            #3 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((120/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((120/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((1260/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((1260/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Interactables", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("You can interact with an object", True, black)
            htptext2 = font2.render("when a question mark appears above", True, black)
            htptext3 = font2.render("your character's head. The button", True, black)
            htptext4 = font2.render("to interact is 'E' by default.", True, black)
            htptext5 = font5.render("People", True, black)
            htptext6 = font2.render("You can talk to people. Some people", True, black)
            htptext7 = font2.render("have no significance except for", True, black)
            htptext8 = font2.render("subtle hints while other characters", True, black)
            htptext9 = font2.render("are crucial for story progression.", True, black)
            htptext10 = font2.render("Also some NPCs can heal you by", True, black)
            htptext11 = font2.render("talking to them.", True, black)

            htptext12 = font5.render("Level Doors", True, black)
            htptext13 = font2.render("These doors appear as black", True, black)
            htptext14 = font2.render("entrances and serve as direct", True, black)
            htptext15 = font2.render("connectors between levels. So", True, black)
            htptext16 = font2.render("interacting with this kind of door", True, black)
            htptext17 = font2.render("sends you to and from certain", True, black)
            htptext18 = font2.render("levels or positions in the same", True, black)
            htptext19 = font2.render("level.", True, black)
            htptext20 = font5.render("Key Doors", True, black)
            htptext21 = font2.render("Key doors require you to have", True, black)

            
            htptext22 = font2.render("picked up a key to progress through", True, black)
            htptext23 = font2.render("the level. You can get a key for", True, black)
            htptext24 = font2.render("every door, some keys you need", True, black)
            
            htptext25 = font2.render("to look harder for than others. You", True, black)
            htptext26 = font2.render("can view how many keys you have in", True, black)
            htptext27 = font2.render("your inventory.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()
            htptextbox11 = htptext11.get_rect()
            htptextbox12 = htptext12.get_rect()
            htptextbox13 = htptext13.get_rect()
            htptextbox14 = htptext14.get_rect()
            htptextbox15 = htptext15.get_rect()
            htptextbox16 = htptext16.get_rect()
            htptextbox17 = htptext17.get_rect()
            htptextbox18 = htptext18.get_rect()
            htptextbox19 = htptext19.get_rect()
            htptextbox20 = htptext20.get_rect()
            htptextbox21 = htptext21.get_rect()
            htptextbox22 = htptext22.get_rect()
            htptextbox23 = htptext23.get_rect()
            htptextbox24 = htptext24.get_rect()
            htptextbox25 = htptext25.get_rect()
            htptextbox26 = htptext26.get_rect()
            htptextbox27 = htptext27.get_rect()


            
            htptextbox1.center = (390/self.font_scale, 360/self.font_scale)
            htptextbox2.center = (390/self.font_scale, 400/self.font_scale)
            htptextbox3.center = (390/self.font_scale, 440/self.font_scale)
            htptextbox4.center = (390/self.font_scale, 480/self.font_scale)
            htptextbox5.center = (390/self.font_scale, 540/self.font_scale)
            htptextbox6.center = (390/self.font_scale, 600/self.font_scale)
            htptextbox7.center = (390/self.font_scale, 640/self.font_scale)
            htptextbox8.center = (390/self.font_scale, 680/self.font_scale)
            htptextbox9.center = (390/self.font_scale, 720/self.font_scale)
            htptextbox10.center = (390/self.font_scale, 760/self.font_scale)
            htptextbox11.center = (390/self.font_scale, 800/self.font_scale)

            
            htptextbox12.center = (960/self.font_scale, 390/self.font_scale)  #
            htptextbox13.center = (960/self.font_scale, 450/self.font_scale)
            htptextbox14.center = (960/self.font_scale, 490/self.font_scale)
            htptextbox15.center = (960/self.font_scale, 530/self.font_scale)
            htptextbox16.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox17.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox18.center = (960/self.font_scale, 650/self.font_scale)
            htptextbox19.center = (960/self.font_scale, 690/self.font_scale)
            htptextbox20.center = (960/self.font_scale, 750/self.font_scale) #
            htptextbox21.center = (960/self.font_scale, 810/self.font_scale)

            
            htptextbox22.center = (1530/self.font_scale, 360/self.font_scale)
            htptextbox23.center = (1530/self.font_scale, 400/self.font_scale) 
            htptextbox24.center = (1530/self.font_scale, 440/self.font_scale)
            htptextbox25.center = (1530/self.font_scale, 480/self.font_scale)
            htptextbox26.center = (1530/self.font_scale, 520/self.font_scale)
            htptextbox27.center = (1530/self.font_scale, 560/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            self.screen.blit(htptext11,htptextbox11)
            self.screen.blit(htptext12,htptextbox12)
            self.screen.blit(htptext13,htptextbox13)
            self.screen.blit(htptext14,htptextbox14)
            self.screen.blit(htptext15,htptextbox15)
            self.screen.blit(htptext16,htptextbox16)
            self.screen.blit(htptext17,htptextbox17)
            self.screen.blit(htptext18,htptextbox18)
            self.screen.blit(htptext19,htptextbox19)
            self.screen.blit(htptext20,htptextbox20)
            self.screen.blit(htptext21,htptextbox21)
            self.screen.blit(htptext22,htptextbox22)
            self.screen.blit(htptext23,htptextbox23)
            self.screen.blit(htptext24,htptextbox24)
            self.screen.blit(htptext25,htptextbox25)
            self.screen.blit(htptext26,htptextbox26)
            self.screen.blit(htptext27,htptextbox27)
            
        elif self.htp_page == 6: #Usable Items
            #3 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((120/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((120/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((1260/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((1260/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Usable Items", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("Once you pick up a usable item you", True, black)
            htptext2 = font2.render("can equip it by clicking it in your", True, black)
            htptext3 = font2.render("inventory and then use it in game", True, black)
            htptext4 = font2.render("by pressing right click by default.", True, black)
            htptext5 = font5.render("Bombs", True, black)
            htptext6 = font2.render("When you are on the ground, you can", True, black)
            htptext7 = font2.render("place a bomb on your feet that", True, black)
            htptext8 = font2.render("explodes once the fuse runs out.", True, black)
            htptext9 = font2.render("If the explosion touches any", True, black)
            htptext10 = font2.render("breakable walls, they disappear and", True, black)
            htptext11 = font2.render("it also damages enemies.", True, black)

            htptext12 = font5.render("Hookshot", True, black)
            htptext13 = font2.render("The hookshot requires you to aim", True, black)
            htptext14 = font2.render("at a target and then shoot. If the", True, black)
            htptext15 = font2.render("hook connects then the player is", True, black)
            htptext16 = font2.render("reeled in to the target position", True, black)
            htptext17 = font2.render("unless they hit a wall and fall.", True, black)
            htptext18 = font2.render("Aiming if a bit off so you need", True, black)
            htptext19 = font2.render("to compensate at times.", True, black)
            htptext20 = font5.render("Bow and Arrow", True, black)
            htptext21 = font2.render("The bow requires you to aim as well", True, black)

            
            htptext22 = font2.render("and has the same compensation as", True, black)
            htptext23 = font2.render("the hookshot. You can shoot enemies", True, black)
            htptext24 = font2.render("through one block gaps to kill them", True, black)
            htptext25 = font2.render("from a distance and to make", True, black)
            htptext26 = font2.render("progressing through some levels", True, black)
            htptext27 = font2.render("easier. An arrow does 5 damage", True, black)
            htptext28 = font2.render("and that does not change.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()
            htptextbox11 = htptext11.get_rect()
            htptextbox12 = htptext12.get_rect()
            htptextbox13 = htptext13.get_rect()
            htptextbox14 = htptext14.get_rect()
            htptextbox15 = htptext15.get_rect()
            htptextbox16 = htptext16.get_rect()
            htptextbox17 = htptext17.get_rect()
            htptextbox18 = htptext18.get_rect()
            htptextbox19 = htptext19.get_rect()
            htptextbox20 = htptext20.get_rect()
            htptextbox21 = htptext21.get_rect()
            htptextbox22 = htptext22.get_rect()
            htptextbox23 = htptext23.get_rect()
            htptextbox24 = htptext24.get_rect()
            htptextbox25 = htptext25.get_rect()
            htptextbox26 = htptext26.get_rect()
            htptextbox27 = htptext27.get_rect()
            htptextbox28 = htptext28.get_rect()


            
            htptextbox1.center = (390/self.font_scale, 360/self.font_scale)
            htptextbox2.center = (390/self.font_scale, 400/self.font_scale)
            htptextbox3.center = (390/self.font_scale, 440/self.font_scale)
            htptextbox4.center = (390/self.font_scale, 480/self.font_scale)
            htptextbox5.center = (390/self.font_scale, 540/self.font_scale)
            htptextbox6.center = (390/self.font_scale, 600/self.font_scale)
            htptextbox7.center = (390/self.font_scale, 640/self.font_scale)
            htptextbox8.center = (390/self.font_scale, 680/self.font_scale)
            htptextbox9.center = (390/self.font_scale, 720/self.font_scale)
            htptextbox10.center = (390/self.font_scale, 760/self.font_scale)
            htptextbox11.center = (390/self.font_scale, 800/self.font_scale)

            
            htptextbox12.center = (960/self.font_scale, 390/self.font_scale)  #
            htptextbox13.center = (960/self.font_scale, 450/self.font_scale)
            htptextbox14.center = (960/self.font_scale, 490/self.font_scale)
            htptextbox15.center = (960/self.font_scale, 530/self.font_scale)
            htptextbox16.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox17.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox18.center = (960/self.font_scale, 650/self.font_scale)
            htptextbox19.center = (960/self.font_scale, 690/self.font_scale)
            htptextbox20.center = (960/self.font_scale, 750/self.font_scale) #
            htptextbox21.center = (960/self.font_scale, 810/self.font_scale)

            
            htptextbox22.center = (1530/self.font_scale, 360/self.font_scale)   
            htptextbox23.center = (1530/self.font_scale, 400/self.font_scale) 
            htptextbox24.center = (1530/self.font_scale, 440/self.font_scale)
            htptextbox25.center = (1530/self.font_scale, 480/self.font_scale)
            htptextbox26.center = (1530/self.font_scale, 520/self.font_scale)
            htptextbox27.center = (1530/self.font_scale, 560/self.font_scale)
            htptextbox28.center = (1530/self.font_scale, 600/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            self.screen.blit(htptext11,htptextbox11)
            self.screen.blit(htptext12,htptextbox12)
            self.screen.blit(htptext13,htptextbox13)
            self.screen.blit(htptext14,htptextbox14)
            self.screen.blit(htptext15,htptextbox15)
            self.screen.blit(htptext16,htptextbox16)
            self.screen.blit(htptext17,htptextbox17)
            self.screen.blit(htptext18,htptextbox18)
            self.screen.blit(htptext19,htptextbox19)
            self.screen.blit(htptext20,htptextbox20)
            self.screen.blit(htptext21,htptextbox21)
            self.screen.blit(htptext22,htptextbox22)
            self.screen.blit(htptext23,htptextbox23)
            self.screen.blit(htptext24,htptextbox24)
            self.screen.blit(htptext25,htptextbox25)
            self.screen.blit(htptext26,htptextbox26)
            self.screen.blit(htptext27,htptextbox27)
            self.screen.blit(htptext28,htptextbox28)
            
        elif self.htp_page == 7: #Key Items
            #1 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Key Items", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font5.render("Torch", True, black)
            htptext2 = font2.render("You need to obtain a torch to be", True, black)
            htptext3 = font2.render("able to go into dark caves which is", True, black)
            htptext4 = font2.render("required to progress on the story.", True, black)
            htptext5 = font5.render("Keys", True, black)
            htptext6 = font2.render("Keys can be found in dungeons and", True, black)
            htptext7 = font2.render("you walk over them to pick them up", True, black)
            htptext8 = font2.render("and you are able to open key doors", True, black)
            htptext9 = font2.render("with a key.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()



            
            htptextbox1.center = (960/self.font_scale, 390/self.font_scale)
            htptextbox2.center = (960/self.font_scale, 450/self.font_scale)
            htptextbox3.center = (960/self.font_scale, 490/self.font_scale)
            htptextbox4.center = (960/self.font_scale, 550/self.font_scale)
            htptextbox5.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox6.center = (960/self.font_scale, 670/self.font_scale)
            htptextbox7.center = (960/self.font_scale, 710/self.font_scale)
            htptextbox8.center = (960/self.font_scale, 750/self.font_scale)
            htptextbox9.center = (960/self.font_scale, 790/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            
        elif self.htp_page == 8: #Level enemies
            #3 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((120/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((120/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((1260/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((1260/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Level Enemies", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("Enemies respawn when you enter a", True, black)
            htptext2 = font2.render("dungeon/area from the overworld", True, black)
            htptext3 = font2.render("and don't respawn when switching", True, black)
            htptext4 = font2.render("screens. There are 4 types:", True, black)
            htptext5 = font5.render("Stationary", True, black)
            htptext6 = font2.render("Stationary enemies don't move and", True, black)
            htptext7 = font2.render("just stare at you... That's it.", True, black)
            htptext8 = font5.render("Random", True, black)
            htptext9 = font2.render("These kinds of enemies move", True, black)
            htptext10 = font2.render("randomly and for a random distance", True, black)
            htptext11 = font2.render("not affected by player position.", True, black)

            htptext12 = font5.render("Chase", True, black)
            htptext13 = font2.render("These enemies chase you and move", True, black)
            htptext14 = font2.render("either left or right depending on", True, black)
            htptext15 = font2.render("where you are. Ideally you want to", True, black)
            htptext16 = font2.render("knock these guys back continually", True, black)
            htptext17 = font2.render("to defeat them (that is if they", True, black)
            htptext18 = font2.render("have knockback).", True, black)
            htptext19 = font5.render("Projectiles", True, black)
            htptext20 = font2.render("These enemies are stationary but", True, black)
            htptext21 = font2.render("shoot projectiles in the direction", True, black)

            
            htptext22 = font2.render("of the player horizontally. You", True, black)
            htptext23 = font2.render("cannot block these projectiles so", True, black)
            htptext24 = font2.render("to deal with them you either kill", True, black)
            htptext25 = font2.render("the enemy to prevent further", True, black)
            htptext26 = font2.render("projectiles or dodge them.", True, black)
            
            htptext27 = font2.render("Note: Enemies have invulnerability", True, black)
            htptext28 = font2.render("after being hit (cannot be bit) for", True, black)
            htptext29 = font2.render("about half a second, so do you as a", True, black)
            htptext30 = font2.render("player.", True, black)

            

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()
            htptextbox11 = htptext11.get_rect()
            htptextbox12 = htptext12.get_rect()
            htptextbox13 = htptext13.get_rect()
            htptextbox14 = htptext14.get_rect()
            htptextbox15 = htptext15.get_rect()
            htptextbox16 = htptext16.get_rect()
            htptextbox17 = htptext17.get_rect()
            htptextbox18 = htptext18.get_rect()
            htptextbox19 = htptext19.get_rect()
            htptextbox20 = htptext20.get_rect()
            htptextbox21 = htptext21.get_rect()
            htptextbox22 = htptext22.get_rect()
            htptextbox23 = htptext23.get_rect()
            htptextbox24 = htptext24.get_rect()
            htptextbox25 = htptext25.get_rect()
            htptextbox26 = htptext26.get_rect()
            htptextbox27 = htptext27.get_rect()
            htptextbox28 = htptext28.get_rect()
            htptextbox29 = htptext29.get_rect()
            htptextbox30 = htptext30.get_rect()


            
            htptextbox1.center = (390/self.font_scale, 360/self.font_scale)
            htptextbox2.center = (390/self.font_scale, 400/self.font_scale)
            htptextbox3.center = (390/self.font_scale, 440/self.font_scale)
            htptextbox4.center = (390/self.font_scale, 480/self.font_scale)
            htptextbox5.center = (390/self.font_scale, 540/self.font_scale)
            htptextbox6.center = (390/self.font_scale, 600/self.font_scale)
            htptextbox7.center = (390/self.font_scale, 640/self.font_scale)
            htptextbox8.center = (390/self.font_scale, 700/self.font_scale)
            htptextbox9.center = (390/self.font_scale, 760/self.font_scale)
            htptextbox10.center = (390/self.font_scale, 800/self.font_scale)
            htptextbox11.center = (390/self.font_scale, 840/self.font_scale)

            
            htptextbox12.center = (960/self.font_scale, 390/self.font_scale)  #
            htptextbox13.center = (960/self.font_scale, 450/self.font_scale)
            htptextbox14.center = (960/self.font_scale, 490/self.font_scale)
            htptextbox15.center = (960/self.font_scale, 530/self.font_scale)
            htptextbox16.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox17.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox18.center = (960/self.font_scale, 650/self.font_scale)
            htptextbox19.center = (960/self.font_scale, 710/self.font_scale)
            htptextbox20.center = (960/self.font_scale, 770/self.font_scale) #
            htptextbox21.center = (960/self.font_scale, 810/self.font_scale)

            
            htptextbox22.center = (1530/self.font_scale, 360/self.font_scale)   
            htptextbox23.center = (1530/self.font_scale, 400/self.font_scale) 
            htptextbox24.center = (1530/self.font_scale, 440/self.font_scale)
            htptextbox25.center = (1530/self.font_scale, 480/self.font_scale)
            htptextbox26.center = (1530/self.font_scale, 520/self.font_scale)
            htptextbox27.center = (1530/self.font_scale, 580/self.font_scale)
            htptextbox28.center = (1530/self.font_scale, 620/self.font_scale)
            htptextbox29.center = (1530/self.font_scale, 660/self.font_scale)
            htptextbox30.center = (1530/self.font_scale, 700/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            self.screen.blit(htptext11,htptextbox11)
            self.screen.blit(htptext12,htptextbox12)
            self.screen.blit(htptext13,htptextbox13)
            self.screen.blit(htptext14,htptextbox14)
            self.screen.blit(htptext15,htptextbox15)
            self.screen.blit(htptext16,htptextbox16)
            self.screen.blit(htptext17,htptextbox17)
            self.screen.blit(htptext18,htptextbox18)
            self.screen.blit(htptext19,htptextbox19)
            self.screen.blit(htptext20,htptextbox20)
            self.screen.blit(htptext21,htptextbox21)
            self.screen.blit(htptext22,htptextbox22)
            self.screen.blit(htptext23,htptextbox23)
            self.screen.blit(htptext24,htptextbox24)
            self.screen.blit(htptext25,htptextbox25)
            self.screen.blit(htptext26,htptextbox26)
            self.screen.blit(htptext27,htptextbox27)
            self.screen.blit(htptext28,htptextbox28)
            self.screen.blit(htptext29,htptextbox29)
            self.screen.blit(htptext30,htptextbox30)
            
        elif self.htp_page == 9: #Overworld enemies
            #3 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((120/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((120/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((1260/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((1260/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Overworld Enemies", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("Overworld enemies spawn on the", True, black)
            htptext2 = font2.render("overworld map once you have a", True, black)
            htptext3 = font2.render("sword and chases you until either", True, black)
            htptext4 = font2.render("they expire or you get caught which", True, black)
            htptext5 = font2.render("then is followed by an enemy", True, black)
            htptext6 = font2.render("encounter where you are put in a", True, black)
            htptext7 = font2.render("level with enemies. To complete an", True, black)
            htptext8 = font2.render("encounter you must either leave from", True, black)
            htptext9 = font2.render("the left or the right of the screen.", True, black)
            htptext10 = font5.render("Tiles", True, black)
            htptext11 = font2.render("The enemy encounter when you are", True, black)

            htptext12 = font2.render("caught depends on two factors:", True, black)
            htptext13 = font2.render("Your player level and the tile you", True, black)
            htptext14 = font2.render("are caught on such as dirt or sand.", True, black)
            htptext15 = font2.render("Some tiles are harder than others.", True, black)
            htptext16 = font2.render("Path tile: Easiest tile where", True, black)
            htptext17 = font2.render("where no enemies ever spawn.", True, black)
            htptext18 = font2.render("Bridge tile: Doesn't really scale", True, black)
            htptext19 = font2.render("with player level and only one on", True, black)
            htptext20 = font2.render("the map for this encounter possible.", True, black)
            htptext21 = font2.render("Beach tile: Sand tile, doesn't", True, black)

            
            htptext22 = font2.render("really scale either compared to", True, black)
            htptext23 = font2.render("bridge tile and relatively easy.", True, black)
            htptext24 = font2.render("Plains tile: The most common tile,", True, black)
            htptext25 = font2.render("scales normally and is generally", True, black)
            htptext26 = font2.render("difficult.", True, black)
            htptext27 = font2.render("Forest tile: Hardest tile, enemy", True, black)
            htptext28 = font2.render("count is increased so try to stay", True, black)
            htptext29 = font2.render("out of these tiles.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()
            htptextbox10 = htptext10.get_rect()
            htptextbox11 = htptext11.get_rect()
            htptextbox12 = htptext12.get_rect()
            htptextbox13 = htptext13.get_rect()
            htptextbox14 = htptext14.get_rect()
            htptextbox15 = htptext15.get_rect()
            htptextbox16 = htptext16.get_rect()
            htptextbox17 = htptext17.get_rect()
            htptextbox18 = htptext18.get_rect()
            htptextbox19 = htptext19.get_rect()
            htptextbox20 = htptext20.get_rect()
            htptextbox21 = htptext21.get_rect()
            htptextbox22 = htptext22.get_rect()
            htptextbox23 = htptext23.get_rect()
            htptextbox24 = htptext24.get_rect()
            htptextbox25 = htptext25.get_rect()
            htptextbox26 = htptext26.get_rect()
            htptextbox27 = htptext27.get_rect()
            htptextbox28 = htptext28.get_rect()
            htptextbox29 = htptext29.get_rect()


            
            htptextbox1.center = (390/self.font_scale, 360/self.font_scale)
            htptextbox2.center = (390/self.font_scale, 400/self.font_scale)
            htptextbox3.center = (390/self.font_scale, 440/self.font_scale)
            htptextbox4.center = (390/self.font_scale, 480/self.font_scale)
            htptextbox5.center = (390/self.font_scale, 520/self.font_scale)
            htptextbox6.center = (390/self.font_scale, 560/self.font_scale)
            htptextbox7.center = (390/self.font_scale, 600/self.font_scale)
            htptextbox8.center = (390/self.font_scale, 640/self.font_scale)
            htptextbox9.center = (390/self.font_scale, 680/self.font_scale)
            htptextbox10.center = (390/self.font_scale, 740/self.font_scale)
            htptextbox11.center = (390/self.font_scale, 800/self.font_scale)

            
            htptextbox12.center = (960/self.font_scale, 390/self.font_scale)  #
            htptextbox13.center = (960/self.font_scale, 430/self.font_scale)
            htptextbox14.center = (960/self.font_scale, 470/self.font_scale)
            htptextbox15.center = (960/self.font_scale, 510/self.font_scale)
            htptextbox16.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox17.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox18.center = (960/self.font_scale, 670/self.font_scale)
            htptextbox19.center = (960/self.font_scale, 710/self.font_scale)
            htptextbox20.center = (960/self.font_scale, 750/self.font_scale) #
            htptextbox21.center = (960/self.font_scale, 810/self.font_scale)

            
            htptextbox22.center = (1530/self.font_scale, 360/self.font_scale)   
            htptextbox23.center = (1530/self.font_scale, 400/self.font_scale) 
            htptextbox24.center = (1530/self.font_scale, 460/self.font_scale)
            htptextbox25.center = (1530/self.font_scale, 500/self.font_scale)
            htptextbox26.center = (1530/self.font_scale, 540/self.font_scale)
            htptextbox27.center = (1530/self.font_scale, 600/self.font_scale)
            htptextbox28.center = (1530/self.font_scale, 640/self.font_scale)
            htptextbox29.center = (1530/self.font_scale, 680/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
            self.screen.blit(htptext10,htptextbox10)
            self.screen.blit(htptext11,htptextbox11)
            self.screen.blit(htptext12,htptextbox12)
            self.screen.blit(htptext13,htptextbox13)
            self.screen.blit(htptext14,htptextbox14)
            self.screen.blit(htptext15,htptextbox15)
            self.screen.blit(htptext16,htptextbox16)
            self.screen.blit(htptext17,htptextbox17)
            self.screen.blit(htptext18,htptextbox18)
            self.screen.blit(htptext19,htptextbox19)
            self.screen.blit(htptext20,htptextbox20)
            self.screen.blit(htptext21,htptextbox21)
            self.screen.blit(htptext22,htptextbox22)
            self.screen.blit(htptext23,htptextbox23)
            self.screen.blit(htptext24,htptextbox24)
            self.screen.blit(htptext25,htptextbox25)
            self.screen.blit(htptext26,htptextbox26)
            self.screen.blit(htptext27,htptextbox27)
            self.screen.blit(htptext28,htptextbox28)
            self.screen.blit(htptext29,htptextbox29)
            
        elif self.htp_page == 10: #Bosses
            #1 text boxes + heading box
            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (640/self.font_scale) +4)) 
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (640/self.font_scale)))

            pygame.draw.rect(self.screen, black, pygame.Rect((690/self.font_scale) -2, (240/self.font_scale) -2, (540/self.font_scale) +4, (100/self.font_scale) +4))
            pygame.draw.rect(self.screen, white, pygame.Rect((690/self.font_scale), (240/self.font_scale), (540/self.font_scale), (100/self.font_scale)))

            #Title text
            htptext = font4.render("Bosses", True, black) #Overworld encounters #Before you start
            htptextbox = htptext.get_rect()
            htptextbox.center = (960/self.font_scale, 290/self.font_scale)

            #All text info
            htptextp = font2.render("Before you start the game right her", True, black)
            htptext1 = font2.render("Every boss is different has has a", True, black)
            htptext2 = font2.render("unique approach required to beat", True, black)
            htptext3 = font2.render("them.", True, black)
            htptext4 = font2.render("The boss health bar will be", True, black)
            htptext5 = font2.render("displayed on the top right of your", True, black)
            htptext6 = font2.render("screen.", True, black)
            htptext7 = font2.render("Upon beating a boss, all doors that", True, black)
            htptext8 = font2.render("have been blocked off upon entering", True, black)
            htptext9 = font2.render("will be opened up.", True, black)

            
            
            htptextbox1 = htptext1.get_rect()
            htptextbox2 = htptext2.get_rect()
            htptextbox3 = htptext3.get_rect()
            htptextbox4 = htptext4.get_rect()
            htptextbox5 = htptext5.get_rect()
            htptextbox6 = htptext6.get_rect()
            htptextbox7 = htptext7.get_rect()
            htptextbox8 = htptext8.get_rect()
            htptextbox9 = htptext9.get_rect()



            
            htptextbox1.center = (960/self.font_scale, 390/self.font_scale)
            htptextbox2.center = (960/self.font_scale, 430/self.font_scale)
            htptextbox3.center = (960/self.font_scale, 470/self.font_scale)
            htptextbox4.center = (960/self.font_scale, 530/self.font_scale)
            htptextbox5.center = (960/self.font_scale, 570/self.font_scale)
            htptextbox6.center = (960/self.font_scale, 610/self.font_scale)
            htptextbox7.center = (960/self.font_scale, 670/self.font_scale)
            htptextbox8.center = (960/self.font_scale, 710/self.font_scale)
            htptextbox9.center = (960/self.font_scale, 750/self.font_scale)
            
            

            self.screen.blit(htptext,htptextbox)
            self.screen.blit(htptext1,htptextbox1)
            self.screen.blit(htptext2,htptextbox2)
            self.screen.blit(htptext3,htptextbox3)
            self.screen.blit(htptext4,htptextbox4)
            self.screen.blit(htptext5,htptextbox5)
            self.screen.blit(htptext6,htptextbox6)
            self.screen.blit(htptext7,htptextbox7)
            self.screen.blit(htptext8,htptextbox8)
            self.screen.blit(htptext9,htptextbox9)
        
        self.HTP_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.HTP_back.IsOver(mouse_pos,click1,self.screen_state,self)

    def DrawCloseGame(self,mouse_pos,click1): #Draws the close game confirmation
        font1 = pygame.font.SysFont("georgia", int(60/self.font_scale))

        box_width = int(600/self.font_scale)
        box_height = int(375/self.font_scale)
        
        close_gametext1 = font1.render("Are you sure?", True, black)
        close_gametextbox1 = close_gametext1.get_rect()
        close_gametextbox1.center = (self.width/2, self.height/2.3)

        CG_box = pygame.Rect(self.width/2 - box_width/2, self.height/2 - box_height/2, box_width, box_height)
        CG_outline = pygame.Rect((self.width/2 - box_width/2)-2, (self.height/2 - box_height/2)-2, box_width + 4, box_height + 4)
        pygame.draw.rect(self.screen,black,CG_outline)
        pygame.draw.rect(self.screen,old_yellow,CG_box)
        
        self.screen.blit(close_gametext1,close_gametextbox1)

        self.CG_back.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.CG_back.IsOver(mouse_pos,click1,self.screen_state,self)
        self.CG_close.Draw(mouse_pos,click1,False,self)
        self.screen_state = self.CG_close.IsOver(mouse_pos,click1,self.screen_state,self)

    def SettingsChange(self,clickdown): #"Full Change", "Res Change"
        
        if self.attribute_change == "Res Change":
            
            '''
            if self.res == 0: #0-4 for the 4 different resolutions
                self.width = 1366
                self.height = 768
                self.res = 1
                self.font_scale = 1920/self.width
                self.VideoDB.UpdateRecord2("Resolution","1")
            '''
            if self.res == 1:
                self.width = 1280
                self.height = 720
                self.res = 2
                self.font_scale = 1920/self.width
                self.VideoDB.UpdateRecord2("Resolution","2")
            elif self.res == 2:
                self.width = 1024
                self.height = 576
                self.res = 3
                self.font_scale = 1920/self.width
                self.VideoDB.UpdateRecord2("Resolution","3")
            elif self.res == 3:
                self.width = 1920
                self.height = 1080
                self.res = 1
                self.font_scale = 1
                self.VideoDB.UpdateRecord2("Resolution","1")
            self.csypos = (self.height/18)*5.7
            volumes = self.AudioDB.QueryTable()
            self.as1xpos = ((self.width/32)*10.25) + ((volumes[0][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
            self.as2xpos = ((self.width/32)*10.25)+((volumes[1][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
            self.as3xpos = ((self.width/32)*10.25)+((volumes[2][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
                
        if self.attribute_change == "Full Change":
            if self.fullscreen == 1:
                pygame.display.quit()
                pygame.display.init()
                self.fullscreen = 0
                self.mode = pygame.RESIZABLE
                self.VideoDB.UpdateRecord2("Fullscreen","Windowed")
            elif self.fullscreen == 0:
                pygame.display.quit()
                pygame.display.init()
                self.fullscreen = 1
                self.mode = pygame.FULLSCREEN
                self.VideoDB.UpdateRecord2("Fullscreen","Fullscreen")
                
        if self.attribute_change == "Game Options Reset": #####################Add game options database
            self.GameDB.GetDefaults()
        if self.attribute_change == "Video Settings Reset":
            self.VideoDB.GetDefaults() #Resets the database file, changing all records to the records in the default table
            if self.fullscreen == 0:
                self.attribute_change = "Full Change"
                self.SettingsChange(clickdown)
            self.res = int(self.VideoDB.QueryTable()[1][1])-1 #Had to add -1 so the resolution stays the same
            if self.res == 0: #Incase the res is out of range, set it back to 3
                self.res = 3 #If do program like this again, have a set define to reset screen with all attributes instead of having to do this
            self.attribute_change = "Res Change"
            self.SettingsChange(clickdown)
        elif self.attribute_change == "aControls Reset":
            self.ControlsDB.GetDefaults()
        elif self.attribute_change == "Audio Settings Reset":
            self.AudioDB.GetDefaults()
            volumes = self.AudioDB.QueryTable()
            self.as1xpos = ((self.width/32)*10.25) + ((volumes[0][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
            self.as2xpos = ((self.width/32)*10.25)+((volumes[1][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))
            self.as3xpos = ((self.width/32)*10.25)+((volumes[2][1]/100)*(((self.width/32)*26.75)-((self.width/32)*10.25)))

        if self.attribute_change == "Difficulty Change":
            if self.difficulty == "Easy":
                self.GameDB.UpdateRecord2("Difficulty","Medium")
            elif self.difficulty == "Medium":
                self.GameDB.UpdateRecord2("Difficulty","Hard")
            elif self.difficulty == "Hard":
                self.GameDB.UpdateRecord2("Difficulty","Impossible")
            elif self.difficulty == "Impossible":
                self.GameDB.UpdateRecord2("Difficulty","Easy")
          
            
        #pygame.draw.rect(self.screen, off_yellow, pygame.Rect((self.width/32)*1.4 +1, (self.height/18)*5.7 +1, (self.width/32)*9.5 -2, (self.height/18)*10 -2))

        if self.attribute_change[:7] == "Control": #String manipulation ##########

            box_width = int(600/self.font_scale)
            box_height = int(375/self.font_scale)

            text_box = pygame.Rect(self.width/2 - box_width/2, self.height/2 - box_height/2, box_width, box_height)
            text_box_outline = pygame.Rect((self.width/2 - box_width/2)-2, (self.height/2 - box_height/2)-2, box_width + 4, box_height + 4)
            pygame.draw.rect(self.screen,black,text_box_outline) #For the box around text
            pygame.draw.rect(self.screen,off_yellow,text_box) #Only drawn once so outside is of Until Loop, so does not get drawn over any text

            if len(self.attribute_change) == 9: #Index of which control has been clicked
                index1 = int(self.attribute_change[7])
                index2 = int(self.attribute_change[8])

            elif len(self.attribute_change) == 10: #Incase first index is a 2 digit number
                index1 = int(self.attribute_change[7]+self.attribute_change[8])
                index2 = int(self.attribute_change[9])


            while True:
                font1 = pygame.font.SysFont("georgia", int(60/self.font_scale))
                
                controls_menutext1 = font1.render("Enter a key", True, black)
                controls_menutextbox1 = controls_menutext1.get_rect()
                controls_menutextbox1.center = (self.width/2, self.height/2.3)

                self.screen.blit(controls_menutext1,controls_menutextbox1)

                pygame.display.flip()

                event = pygame.event.wait()
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                        #print(event)
                        # gets the key name
                        key_name = pygame.key.name(event.key)

                        # converts to uppercase the key name
                        key_name = key_name.upper()
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        key_name = "Mouse 1"
                    elif event.button == 2:
                        key_name = "Mouse 3" #As middle mouse for me is mouse 3
                    elif event.button == 3:
                        key_name = "Mouse 2"
                    elif event.button == 4:
                        key_name = "Scroll Up"
                    elif event.button == 5:
                        key_name = "Scroll Down"
                    elif event.button == 6:
                        key_name = "Mouse 4"
                    elif event.button == 7:
                        key_name = "Mouse 5"


                else:
                    key_name = None
                    

                if key_name != None:

                    keys = self.ControlsDB.QueryTable()
                    invalid = False
                    for Loop in keys: 
                        for Loop2 in Loop:
                            if Loop2 == key_name:
                                #print(keys[index1][index2])
                                if keys[index1][index2] != key_name:
                                    invalid = True

                    if invalid == False:
                        if index2 == 1: #Which column
                            self.ControlsDB.UpdateRecord3(keys[index1][0],key_name,keys[index1][2]) #For if it is the first column (key)
                        elif index2 == 2:
                            self.ControlsDB.UpdateRecord3(keys[index1][0],keys[index1][1],key_name) #For if it is the second column (alternate)
                        break
                    else:
                        controls_menutext2 = font1.render("Invalid Key", True, black)
                        controls_menutextbox2 = controls_menutext2.get_rect()
                        controls_menutextbox2.center = (self.width/2, self.height/1.9)
                        self.screen.blit(controls_menutext2,controls_menutextbox2)
            
        if clickdown == True: #This is here just so it is not set to False for as long as the mouse is held down
            if self.attribute_change == "Move Scroll Bar":
                self.movescroll = True
            elif self.attribute_change == "Move Master":
                self.moveslide1 = True
            elif self.attribute_change == "Move Music":
                self.moveslide2 = True
            elif self.attribute_change == "Move Sound":
                self.moveslide3 = True
        else:
            self.screen = pygame.display.set_mode((self.width,self.height),self.mode)
            self.movescroll = False
            self.moveslide1 = False
            self.moveslide2 = False
            self.moveslide3 = False

        self.InstantiateButtons()


    def ReturnScreen(self):
        return self.screen

    def ReturnFontScale(self):
        return self.font_scale


class Button: #The mother class for the different kinds of buttons, the attributes that all the buttons have and the draw subroutine is in here
    def __init__(self,text,position,width,height,colour,font,font_size,state):
        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.colour = colour
        self.og_colour = colour
        self.state = state

    def Draw(self,mouse_pos,click1,draw_outline,Display): #Draws the button according to the attributes that were set during insantiation
        text = self.font.render(self.text, True, self.colour)
        textbox = text.get_rect()      
        textbox.center = (self.position)
        Display.ReturnScreen().blit(text,textbox) #Draws the button to the screen
        if draw_outline == True:
            self.DrawOutlineText(Display)
            
    def DrawOutlineText(self,Display): #If the text has an outline, this will draw that outline
        text = self.font.render(self.text, True, white)
        textbox = text.get_rect()
        textbox.center = (self.position[0]-1,self.position[1]-1)
        Display.ReturnScreen().blit(text,textbox)


class MenuButton(Button):#This will be options like New Game, Load Game, etc
    def __init__(self,text,navigate_to,position,width,height,colour,font,font_size,state):
        self.navigate_to = navigate_to
        Button.__init__(self,text,position,width,height,colour,font,font_size,state)

    def IsOver(self,mouse_pos,click1,screen_state,Display): #
        is_over = False
        if mouse_pos[0] > self.position[0] - self.width/2 and mouse_pos[0] < self.position[0] + self.width/2: #Checks if x pos of mouse is within the shape of the text box 
            if mouse_pos[1] > self.position[1] - self.height/2 and mouse_pos[1] < self.position[1] + self.height/2: #Checks if y pos of mouse is within the shape of the text box 
                self.colour = white
                is_over = True
            else:
                self.colour = self.og_colour #So if not hoveing over button, change text colour back to original state
        else:
            self.colour = self.og_colour

        if click1 == True and is_over == True: #Checks if player clicks while over the button
            text = self.font.render(self.text, True, self.colour) #Two lines return text to original colour when clicked so they dont stay white
            textbox = text.get_rect()
            textbox.center = (self.position)
            Display.ReturnScreen().blit(text,textbox)
            return self.navigate_to #Returns the new screen
        else:
            #return None
            return screen_state #Returns the same screen, so nothing is changed
    

class SubMenuButton(Button): #This will be options such as the different sub-headings in the options menu or changing the inventory screens or the pause menu
    def __init__(self,text,menu_change,position,width,height,colour,font,font_size,state):
        self.menu_change = menu_change
        Button.__init__(self,text,position,width,height,colour,font,font_size,state)

    def IsOver(self,mouse_pos,click1,subscreen_state,Display): #
        is_over = False
        if mouse_pos[0] > self.position[0] - self.width/2 and mouse_pos[0] < self.position[0] + self.width/2: #Checks if x pos of mouse is within the shape of the text box 
            if mouse_pos[1] > self.position[1] - self.height/2 and mouse_pos[1] < self.position[1] + self.height/2: #Checks if y pos of mouse is within the shape of the text box 
                self.colour = white
                is_over = True
            else:
                self.colour = self.og_colour #So if not hoveing over button, change text colour back to original state
        else:
            self.colour = self.og_colour

        if click1 == True and is_over == True: #Checks if player clicks while over the button
            text = self.font.render(self.text, True, self.colour) #Two lines return text to original colour when clicked so they dont stay white
            textbox = text.get_rect()
            textbox.center = (self.position)
            Display.ReturnScreen().blit(text,textbox)
            return self.menu_change #Returns the new sub screen
        else:
            return subscreen_state #Returns the same screen, so nothing is changed

class AttributeButton(Button): #This will change attributes of the game such as volume, res, etc.
    def __init__(self,text,attribute_change,position,width,height,colour,font,font_scale,state):
        self.attribute_change = attribute_change
        Button.__init__(self,text,position,width,height,colour,font,font_scale,state)

    def IsOver(self,mouse_pos,click1,attribute_change,Display):
        is_over = False
        if mouse_pos[0] > self.position[0] - self.width/2 and mouse_pos[0] < self.position[0] + self.width/2: #Checks if x pos of mouse is within the shape of the text box 
            if mouse_pos[1] > self.position[1] - self.height/2 and mouse_pos[1] < self.position[1] + self.height/2: #Checks if y pos of mouse is within the shape of the text box 
                self.colour = white
                is_over = True
            else:
                self.colour = self.og_colour #So if not hoveing over button, change text colour back to original state
        else:
            self.colour = self.og_colour

        if click1 == True and is_over == True: #Checks if player clicks while over the button
            text = self.font.render(self.text, True, self.colour) #Two lines return text to original colour when clicked so they dont stay white
            textbox = text.get_rect()
            textbox.center = (self.position)
            Display.ReturnScreen().blit(text,textbox)
            return self.attribute_change #Returns what the button is meant to do
        else:
            return attribute_change #Returns a blank variable


class GameClass: #Main game class
    def __init__(self,profile,new_file,name,scale,ControlsDB):
        '''
        #INT profile - Which profile was chosen - (1,2,3)
        #BOOLEAN new_file - Whether it is a new game or a load game - (True, False)
        '''
        if new_file == True:
            #Will set all these attributes to starter, default values, also will save default values to
            time,char_name,location,pos_x,pos_y,health,max_health,level,exp,skill_points,strength,resilience,speed,items,items_dict,events,bosses,last_location,last_move,last_overworld_x,last_overworld_y = self.LoadNewProfile(name)
            self.start_spawn = False
        elif new_file == False:
            #This function will use the text file to get all these attributes
            time,char_name,location,pos_x,pos_y,health,max_health,level,exp,skill_points,strength,resilience,speed,items,items_dict,events,bosses,last_location,last_move,last_overworld_x,last_overworld_y = self.LoadOldProfile(profile)
            self.start_spawn = True

        self.profile = profile
        self.item_equipt = None
        #Imported attributes
        self.prof_time = time
        self.char_name = char_name
        self.location = location
        self.pos_x = pos_x
        self.pos_y = pos_y #5
        self.health = health
        self.max_health = max_health
        self.level = level
        self.exp = exp
        self.skill_points = skill_points #10
        self.strength = strength
        self.resilience = resilience
        self.speed = speed
        self.items = items #15
        self.items_dict = items_dict
        self.events = events
        self.bosses = bosses
        
        self.temp_skill = self.skill_points
        self.temp_str = self.strength
        self.temp_res = self.resilience
        self.temp_spe = self.speed

        self.ControlsDB = ControlsDB

        self.scale = scale

        #self.last_move = "W"
        
        self.last_location = last_location
        self.last_move = last_move

        self.last_overworld_x = last_overworld_x
        self.last_overworld_y = last_overworld_y
        
        self.die = False
        self.over_stopped = False
        self.encounter = False
        self.over_encounter = ""
        
        self.enemies = []
        self.text_list = []
        self.current_interactables = []
        self.current_cutscenes = []

        self.switch_event = True
        self.event_delay = 10

        self.overworld_enemies_random = 240 #SETTO
        self.overworld_spawn = False
        self.overworld_enemies = []
        self.enemy_live = 300

        self.wait_item = 0
        self.hook_travel = False
        self.hookshot = None
        self.hook_x = self.hook_y = 0
        self.bow_released = False
        self.hold_mouse_pos = 0
        self.hold_bow_pull = 0

        self.cutscene_1_image = ""
        self.cutscene_1_x = 0
        self.cutscene_1_y = 0
        self.cutscene_1_width = 0
        self.cutscene_1_height = 0

        self.final_exp_tick = 0
        self.final_exp_x = 0
        self.final_exp_y = 0


        self.harb_master = 0

        #Static Dictonaries
        '''
        #The numbers from these dictionary will be used when file handling to find the location of where these levels are stored
        '''
        self.exp_cap = {}
        for Level in range(1,17,1): #Level 1 to level 16
            self.exp_cap[Level] = Level*10 #10 exp for lvl 1, 20 exp for lvl 2, etc

        self.location_dict = {"Overworld":0,
                              "Beach":1, #More to come
                              "Castaway Village 1":2,
                              "Castaway Village 2":3,
                              "Castaway Village Armoury":4,
                              "Mountain Pass 1":5,
                              "Mountain Pass 2":6,
                              "Bridge Pass 1":7,
                              "Harbrew Town 1":8,
                              "Harbrew Town 2":9,
                              "Mt Komodo Level 1":10,
                              "Mt Komodo Level 2":11,
                              "Mt Komodo Level 3":12,
                              "Mt Komodo Level 4":13, #Exit room
                              "Mt Komodo Mineshaft":14, #Bomb room
                              
                              "Lakeview Harbour":15,
                              "Lakeview Harbour Docks":16,
                              
                              "Bridge Pass 2 One":17, 
                              "Bridge Pass 2 Two":18, #

                              "Mountain Camp Level 1":19,
                              "Mountain Camp Level 2":20,
                              "Mountain Camp Level 3":21, #####Currently done
                              "Mountain Camp Level 4":22, #
                              "Mountain Camp Level 5":23, 
                              "Mountain Camp Level 6":24, #
                              "Mountain Camp Level 7":25,
                              "Mountain Camp Boss":26,

                              "Research Lab Front":27,
                              "Research Lab Back":28,
                              "Research Lab Level 1":29,
                              "Research Lab Level 2":30,
                              "Research Lab Level 3":31,
                              "Research Lab Level 4":32,
                              "Research Lab Level 5":33,
                              "Research Lab Level 6":34,
                              "Research Lab Level 7":35,
                              "Research Lab Level 8":36,
                              
                              

                              "Path Random Level 1":37,

                              "Plains Random Level 1":38,
                              "Plains Random Level 2":39,
                              "Plains Random Level 3":40,
                              "Plains Random Level 4":41,

                              "Bridge Random Level 1":42,

                              "Beach Random Level 1":43,

                              "Forest Random Level 1":44, #
                              "Forest Random Level 2":45, #
                              "Forest Random Level 3":46, #
                              "Forest Random Level 4":47, #

                              "Harbrew Town 1 Heal Hut":48,
                              "Harbrew Town 1 Quiet House":49,
                              "Harbrew Town 2 Hint Guy":50,
                              "Harbrew Town 2 Hint Guy Attic":51,

                              "Cave near start 1":52,
                              "Cave near start 2":53,

                              "Bridge Pass 2 Guards":54, #With guards

                              "Lakeview Harbour House 1":55,
                              "Lakeview Harbour Healer":56,
                              
                              "Research Lab Boss":57,
                              "Research Lab Level 9":58,

                              "Behind Castle":59,
                              "Castle Level 1":60,
                              "Castle Level 2":61,
                              "Castle Level 3":62,
                              "Castle Level 4":63,
                              "Castle Level 5":64,
                              "Castle Level 6":65,
                              "Castle Level 7":66,
                              "Castle Level 8":67,
                              "Castle Level 9":68,
                              "Castle Level 10":69,
                              "Castle Level 11":70,
                              "Castle Throne Room":71

                              

                              }
        x = y = 0
                                                                #(x,y) = pos_x and pos_y
        self.level_exits = {"Beach":             {"Left":    ["Overworld",(2070.0,6150.0)] #2070.0 6150.0, 1830.0 6210.0 , 1710.0,6390.0
                                                 },
                   
                            "Castaway Village 1":{"Left":    ["Overworld",(2370.0,5970.0)],
                                                 "Right":   ["Castaway Village 2",(90.0,730.0)]
                                                 },

                            "Castaway Village 2":{"Left":    ["Castaway Village 1",(3750,730.0)],
                                                 "3 Door 1":["Castaway Village Armoury",(120.0,730.0)],
                                                 "Right":   ["Overworld",(2370.0,5970.0)]
                                                 },
                            
                            "Castaway Village Armoury":{"Left":["Castaway Village 2",(1650.0,730.0)]
                                                 },

                            "Mountain Pass 1"   :{"Left":    ["Overworld",(1770.0,5910.0)],
                                                 "Right":   ["Mountain Pass 2",(90.0,1140.0)]
                                                 },

                            "Mountain Pass 2"   :{"Left":    ["Mountain Pass 1",(2790.0,900.0)],
                                                 "Right":   ["Overworld",(1770.0,5610.0)]
                                                 },

                            "Bridge Pass 1"     :{"Left":    ["Overworld",(1230.0,4710.0)],
                                                 "Right":   ["Overworld",(1230.0,4350.0)]
                                                 },
                            
                            "Harbrew Town 1"    :{"Left":    ["Overworld",(2790.0,3570.0)],
                                                 "8 Door 1":["Harbrew Town 1 Heal Hut",(120.0,670.0)],
                                                 "8 Door 2":["Harbrew Town 1 Quiet House",(120.0,900.0)],
                                                 "Right":   ["Harbrew Town 2",(120.0,1310.0)] #8
                                                 },
                            
                            "Harbrew Town 2"    :{"Left":    ["Harbrew Town 1",(3720.0,770.0)],
                                                 "9 Door 1":["Harbrew Town 2 Hint Guy",(120.0,790.0)],
                                                 "9 Door 2":["Harbrew Town 2 Hint Guy Attic",(120.0,300.0)]
                                                 },

                            "Harbrew Town 1 Heal Hut":{"Left":["Harbrew Town 1",(630.0,790.0)]
                                                 },

                            "Harbrew Town 1 Quiet House":{"Left":["Harbrew Town 1",(3270.0,790.0)]
                                                 },

                            "Harbrew Town 2 Hint Guy":{"Left":["Harbrew Town 2",(1410.0,1330.0)]
                                                 },

                            "Harbrew Town 2 Hint Guy Attic":{"Left":["Harbrew Town 2",(1410.0,790.0)]
                                                 },
                            
                            "Mt Komodo Level 1" :{"Left":    ["Overworld",(3090.0,3450.0)],                                   
                                                 "Right":   ["Mt Komodo Level 2",(120.0,410.0)]
                                                 },
                            
                            "Mt Komodo Level 2" :{"Left":    ["Mt Komodo Level 1",(2760.0,660.0)],                                   
                                                 "Right":   ["Mt Komodo Level 3",(120.0,1920.0)]
                                                 },
                            
                            "Mt Komodo Level 3" :{"Left":    ["Mt Komodo Level 2",(3720.0,1260.0)],
                                                 "12 Door 1":["Mt Komodo Mineshaft",(120.0,840.0)],
                                                 "Right":   ["Mt Komodo Level 4",(120.0,830.0)]
                                                 },
                            
                            "Mt Komodo Level 4" :{"Left":    ["Mt Komodo Level 3",(2760.0,1920.0)],                                   
                                                 "Right":   ["Overworld",(3630.0,3150.0)]
                                                 },

                            "Mt Komodo Mineshaft":{"Left":["Mt Komodo Level 3",(2520.0,430.0)]
                                                 },

                            "Lakeview Harbour" :{"Left":    ["Overworld",(3870.0,3930.0)],
                                                 "15 Door 1":["Lakeview Harbour House 1",(120.0,660.0)],
                                                 "15 Door 2":["Lakeview Harbour Healer",(120.0,660.0)],
                                                 "Right":   ["Lakeview Harbour Docks",(120.0,790.0)]
                                                 },

                            "Lakeview Harbour House 1":{"Left":    ["Lakeview Harbour",(2010.0,790.0)]
                                                 },

                            "Lakeview Harbour Healer":{"Left":  ["Lakeview Harbour",(870.0,790.0)]
                                                 },

                            "Lakeview Harbour Docks":{"Left":   ["Lakeview Harbour",(3720.0,790.0)]   
                                                 },

                            "Bridge Pass 2 Guards" :{"Left":    ["Overworld",(4470.0,4290.0)],                                   
                                                 "Right":   ["Bridge Pass 2 One",(120.0,1400.0)]
                                                 },
                            
                            "Bridge Pass 2 One" :{"Left":    ["Bridge Pass 2 Guards",(2790.0,1400.0)],                                   
                                                 "Right":   ["Bridge Pass 2 Two",(120.0,660.0)]
                                                 },
                            
                            "Bridge Pass 2 Two" :{"Left":    ["Bridge Pass 2 One",(2790.0,660.0)],                                   
                                                 "Right":   ["Overworld",(4470.0,5250.0)]
                                                 },
                            
                            "Mountain Camp Level 1" :{"Left":    ["Overworld",(4470.0,2250.0)],                                   
                                                 "Right":   ["Mountain Camp Level 2",(120.0,600.0)]
                                                 },
                            
                            "Mountain Camp Level 2" :{"Left":    ["Mountain Camp Level 1",(2790.0,290.0)],                                   
                                                 "Right":   ["Mountain Camp Level 3",(120.0,2400.0)]
                                                 },
                            
                            "Mountain Camp Level 3" :{"Left":    ["Mountain Camp Level 2",(3720.0,660.0)],                                   
                                                 "Right":   ["Mountain Camp Level 4",(120.0,2940.0)]
                                                 },

                            "Mountain Camp Level 4" :{"Left":    ["Mountain Camp Level 3",(3720.0,480.0)],                                   
                                                 "Right":   ["Mountain Camp Level 5",(120.0,2380.0)]
                                                 },

                            "Mountain Camp Level 5" :{"Left":    ["Mountain Camp Level 4",(3720.0,550.0)],                                   
                                                 "Right":   ["Mountain Camp Level 6",(120.0,900.0)]
                                                 },

                            "Mountain Camp Level 6" :{"Left":    ["Mountain Camp Level 5",(5640.0,480.0)],                                   
                                                 "Right":   ["Mountain Camp Level 7",(120.0,1500.0)]
                                                 },

                            "Mountain Camp Level 7" :{"Left":    ["Mountain Camp Level 6",(3720.0,730.0)],
                                                 "Right":   ["Mountain Camp Boss",(240.0,820.0)]
                                                 },

                            "Mountain Camp Boss" :{"Left":    ["Mountain Camp Level 7",(2760.0,850.0)],
                                                 "Right":   ["Overworld",(4470.0,2250.0)]
                                                 },

                            "Research Lab Front" :{"Left":    ["Overworld",(5610.0,6450.0)],                                   
                                                 "Right":   ["Research Lab Back",(120.0,730.0)]
                                                 },

                            "Research Lab Back" :{"Left":    ["Research Lab Front",(3720.0,730.0)],                                   
                                                 "Right":   ["Research Lab Level 1",(120.0,790.0)]
                                                 },

                            "Research Lab Level 1" :{"Left":    ["Research Lab Back",(2520.0,730.0)],                                   
                                                 "Right":   ["Research Lab Level 2",(120.0,1570.0)]
                                                 },
                            
                            "Research Lab Level 2" :{"Left":    ["Research Lab Level 1",(2760.0,1570.0)],                                   
                                                 "Right":   ["Research Lab Level 3",(120.0,550.0)]
                                                 },

                            "Research Lab Level 3" :{"Left":    ["Research Lab Level 2",(3720.0,550.0)],
                                                 "31 Door 1":["Research Lab Level 4",(3480.0,425.0)],
                                                 "Right":   ["Research Lab Level 5",(120.0,610.0)]
                                                 },
                            
                            "Research Lab Level 4" :{"32 Door 1":    ["Research Lab Level 3",(3420.0,1390.0)]                              
                                                 },

                            "Research Lab Level 5" :{"Left":    ["Research Lab Level 3",(3720.0,550.0)],
                                                 "Right":   ["Research Lab Level 6",(120.0,1380.0)]
                                                 },
                            
                            "Research Lab Level 6" :{"Left":    ["Research Lab Level 5",(2760.0,1330.0)],
                                                 "34 Door 1":["Research Lab Level 7",(300.0,849.0)],
                                                 "Right":   ["Research Lab Level 8",(120.0,790.0)]
                                                 },

                            "Research Lab Level 7" :{"35 Door 1":    ["Research Lab Level 6",(280.0,489.0)]
                                                 },

                            "Research Lab Level 8" :{"Left":    ["Research Lab Level 6",(2760.0,670.0)],
                                                 "Right":   ["Research Lab Boss",(240.0,850.0)]
                                                 },

                            "Research Lab Boss" :{"Left":    ["Research Lab Level 8",(2760.0,790.0)],
                                                 "57 Door 1":   ["Research Lab Level 9",(300.0,785.0)]
                                                 },

                            "Research Lab Level 9" :{"58 Door 1":    ["Research Lab Boss",(2580.0,850.0)],
                                                 "Right":   ["Overworld",(5610.0,6450.0)]
                                                 },

                            "Behind Castle" :{"Left":    ["Overworld",(6030.0,3690.0)],                                   
                                                 "Right":   ["Castle Level 1",(120.0,845.0)]
                                                 },

                            "Castle Level 1":{"Left":    ["Behind Castle",(3720.0,1270.0)],                                   
                                                 "Right":   ["Castle Level 2",(120.0,845.0)]
                                                 },

                            "Castle Level 2":{"Left":    ["Castle Level 1",(1800.0,845.0)],                                   
                                                 "Right":   ["Castle Level 3",(120.0,1870.0)]
                                                 },

                            "Castle Level 3":{"Left":    ["Castle Level 2",(1800.0,845.0)],
                                              "62 Door 1":   ["Castle Level 4",(240.0,310.0)],
                                              "62 Door 2":   ["Castle Level 10",(480.0,849.0)],
                                                 "Right":   ["Castle Level 6",(120.0,1269.0)]
                                                 },

                            "Castle Level 4":{"Left":    ["Castle Level 5",(2760.0,670.0)],
                                              "63 Door 1":   ["Castle Level 3",(1840.0,1810.0)]
                                                 },

                            "Castle Level 5":{"Right":   ["Castle Level 4",(120.0,1210.0)]
                                                 },

                            "Castle Level 6":{"Left":    ["Castle Level 3",(3720.0,1870.0)],
                                              "65 Door 1":   ["Castle Level 9",(2590.0,369.0)],
                                                 "Right":   ["Castle Level 7",(120.0,849.0)]
                                                 },

                            "Castle Level 7":{"Left":    ["Castle Level 8",(1800.0,849.0)],                                   
                                                 "Right":   ["Castle Level 7",(120.0,849.0)]
                                                 },

                            "Castle Level 8":{"Left":    ["Castle Level 6",(2760.0,430.0)],                                   
                                                 "Right":   ["Castle Level 7",(120.0,849.0)]
                                                 },

                            "Castle Level 9":{"68 Door 1":   ["Castle Level 6",(2580.0,1270.0)]
                                                 },

                            "Castle Level 10":{"69 Door 1":    ["Castle Level 3",(2040.0,910.0)],                                   
                                                 "Right":   ["Castle Level 11",(120.0,845.0)]
                                                 },

                            "Castle Level 11":{"Left":    ["Castle Level 10",(2760.0,850.0)],                                   
                                                 "Right":   ["Castle Throne Room",(120.0,850.0)]
                                                 },

                            "Castle Throne Room":{"Left":    ["Castle Level 11",(1800.0,850.0)]
                                                 },

                            


                            "Path Random Level 1" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)], #Random encounters in the overworld map                                  
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Plains Random Level 1" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Plains Random Level 2" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Plains Random Level 3" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Plains Random Level 4" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Bridge Random Level 1" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Forest Random Level 1" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Forest Random Level 2" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Forest Random Level 3" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },
                            "Forest Random Level 4" :{"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 },

                            "Cave near start 1" :{"Left":    ["Cave near start 2",(3720.0,480.0)],                                   
                                                 "Right":   ["Overworld",(1050.0,6390.0)]
                                                  },

                            "Cave near start 2" :{"Right":    ["Cave near start 1",(120.0,480.0)]
                                                  }
                    
                            
                           } #Jumptolevels
        
        self.overworld_exits = {(2430.0,5970.0):    ["Castaway Village 1",(90.0,730.0)],
                                (1770.0,5850.0):    ["Mountain Pass 1"   ,(90.0,590.0)],
                                (1770.0,5670.0):    ["Mountain Pass 2"   ,(2790.0,840.0)],
                                (1230.0,4650.0):    ["Bridge Pass 1"     ,(120.0,650.0)], #Below
                                (1230.0,4410.0):    ["Bridge Pass 1"     ,(3710.0,650.0)],
                                (2790.0,3630.0):    ["Harbrew Town 1"    ,(120.0,770.0)],

                                (3150.0,3450.0):    ["Mt Komodo Level 1" ,(120.0,650.0)],
                                (3570.0,3150.0):    ["Mt Komodo Level 4" ,(1800.0,830.0)],

                                (3810.0,3930.0):    ["Lakeview Harbour"  ,(120.0,650.0)],
                                (4470.0,4350.0):    ["Bridge Pass 2 Guards"  ,(120.0,1500.0)],
                                #(4470.0,4350.0):    ["Bridge Pass 2 One"  ,(120.0,1500.0)],
                                (4470.0,5190.0):    ["Bridge Pass 2 Two"  ,(2790.0,1480.0)],

                                (4470.0,2190.0):    ["Mountain Camp Level 1"  ,(90.0,1920.0)],

                                (5670.0,6450.0):    ["Research Lab Front",(120.0,650.0)],

                                (6030.0,3750.0):    ["Behind Castle",(120.0,1270.0)],

                                (990.0,6390.0):    ["Cave near start 1",(3720.0,650.0)]
                                
                                }
        
        self.overworld_encounters_dict = {"Path Random Level 1":(960.0,790.0),
                                    "Plains Random Level 1":(1920.0,790.0),
                                    "Plains Random Level 2":(1920.0,790.0),
                                "Plains Random Level 3":(1920.0,790.0),
                                "Plains Random Level 4":(1920.0,730.0),
                                "Bridge Random Level 1":(1920.0,650.0),
                                "Beach Random Level 1":(1920.0,650.0),
                                "Forest Random Level 1":(1920.0,730.0),
                                "Forest Random Level 2":(1920.0,730.0),
                                "Forest Random Level 3":(1920.0,730.0),
                                "Forest Random Level 4":(1920.0,730.0)
                                }
        
        
        self.overworld_walls = {"000":True,"001":False,"002":False,"003":False,"004":False,"005":True,"006":False,"007":False,"008":False,"009":False,
                                "010":False,"011":True,"012":False,"013":False,"014":False,"015":False,"016":False,"017":False,"018":False,"019":False,
                                "020":False,"021":False,"022":False,"023":True,"024":False,"025":False,"026":False,"027":False,"028":False,"029":False,
                                "030":False, "031":False, "032":False, "033":False, "034":False, "035":False, "036":False, "037":False, "038":False, "039":False,
                                "040":False, "041":False, "042":False, "043":False, "044":False, "045":False, "046":False, "047":False, "048":False, "049":False,
                                "050":False, "051":False, "052":False, "053":False, "054":False, "055":False, "056":False, "057":False, "058":False, "059":False,
                                "060":True, "061":True, "062":True, "063":True, "064":False, "065":False, "066":False, "067":True, "068":False, "069":True,
                                "070":True, "071":True, "072":False, "073":True, "074":True, "075":True, "076":True, "077":True
                                }

        self.level_walls =  {"000":False,"001":True,"002":True,"003":True,"004":False,"005":True,"006":False,"007":False,"008":False,"009":False,
                             "010":False, "011":False,"012":False,"013":False,"014":False,"015":False,"016":False,"017":False,"018":False,"019":False,
                             "020":False, "021":False,"022":False,"023":False,"024":False,"025":False,"026":False,"027":False,"028":False,"029":False,
                             "030":False, "031":True, "032":False, "033":True, "034":False, "035":True, "036":False, "037":False, "038":True, "039":False,
                             "040":False, "041":False, "042":False, "043":False, "044":False, "045":False, "046":False, "047":False, "048":False, "049":True,
                             "050":False, "051":True, "052":True, "053":False, "054":True, "055":True, "056":False, "057":False, "058":False, "059":True,
                             "060":True, "061":True, "062":False, "063":True, "064":False, "065":True, "066":False, "067":False, "068":True, "069":True,
                             "070":True, "071":True, "072":False, "073":True, "074":False, "075":True, "076":False, "077":False
                             }
        
        self.event_dict = {   "Wake up beach":0, #jumptoevents
                              "Sign castaway 1":1, #More to come
                              "Cutscene armoury":2, 
                              "Enter castaway armoury":3,
                              "Enter harbrew heal hut":4,
                              "Enter harbrew quiet hut":5,
                              "Enter harbrew hint hut":6,
                              "Enter harbrew attic":7,
                              "Enter Mt Komodo mineshaft":8,
                              "Obtain bombs":9,
                              "Talk to harbrew old man":10,
                              "Talk to healer":11, #Repeated in multiple places
                              "Talk to harbrew quiet 1":12,
                              "Talk to harbrew quiet 2":13,
                              "Talk to harbrew hint guy":14,
                              "Candle for Mt Komodo":15,
                              "Candle for start cave":16,
                              "Obtain hookshot":17,
                              "Key Door 1":18,
                              "Key Pickup 1":19, #Mt komodo
                              "Read sign Mountain Camp Level 7":20,
                              "Enter research lab level 4":21,
                              "Enter research lab level 3":22,
                              "Key Pickup 2":23, #Research lab level 4
                              "Key Door 2":24, #Research lab level 3
                              "RLL5 Door down":25, #Research lab level 5
                              "RLL5 Door up":26, #Research lab level 5
                              "RLL6 Door to 7":27, #Research lab level 6
                              "RLL7 Door to 6":28, #Research lab level 7
                              "Obtain bow":29,
                              "Key Pickup 3":30,
                              "Key Door 3":31,
                              "Sign harbrew 1":32,
                              "Sign lakeview 1":33,
                              "Enter lakeview harbour house 1":34,
                              "Talk to lakeview fighter":35,
                              "Talk to harbour master":36,
                              "Enter lakeview harbour healer":37,
                              "Check guard bribe":38,
                              "See scientist":39,
                              "Talk to scientist":40,
                              "RLLB Door to 9":41,
                              "RLL9 Door to boss":42,
                              "CL3 to 4":43,
                              "CL4 to 3":44,
                              "Key Pickup 4":45,
                              "Key Pickup 5":46,
                              "CL6 to 9":47,
                              "CL9 to 6":48,
                              "CL9 door 1":49,
                              "CL9 door 2":50,
                              "CL9 door 3":51,
                              "CL9 door 4":52,
                              "CL9 door 5":53,
                              "CL9 door 6":54,
                              "CL9 door 7":55,
                              "CL9 door 8":56,
                              "CL9 door 9":57,
                              "CL9 door 10":58,
                              "Key Pickup 6":59,
                              "CL3 to 10":60,
                              "CL10 to 3":61,
                              "Key Door 4":62,
                              "Key Door 5":63,
                              "Key Door 6":64,
                              "Final Cutscene":65
                              }

        self.boss_loc = {"Mountain Camp Boss":0, #First boss in this place
                         "Research Lab Boss":1
                         }

        
        #Static Lists
        self.interactables = [
            [750.0,730.0,100,100,"Castaway Village 1","Sign castaway 1"],
            [1650.0,730.0,100,100,"Castaway Village 2","Enter castaway armoury"],
            [630.0,790.0,100,100,"Harbrew Town 1","Enter harbrew heal hut"],
            [3270.0,790.0,100,100,"Harbrew Town 1","Enter harbrew quiet hut"],
            [1410.0,1330.0,100,100,"Harbrew Town 2","Enter harbrew hint hut"],
            [1410.0,790.0,100,100,"Harbrew Town 2","Enter harbrew attic"],
            [2520.0,430.0,200,200,"Mt Komodo Level 3","Enter Mt Komodo mineshaft"],
            [1576.0,369.0,200,100,"Harbrew Town 2 Hint Guy Attic","Talk to harbrew old man"],
            [966.0,669.0,200,100,"Harbrew Town 1 Heal Hut","Talk to healer"],
            [1179.0,910.0,200,100,"Harbrew Town 1 Quiet House","Talk to harbrew quiet 1"],
            [500.0,490.0,200,100,"Harbrew Town 1 Quiet House","Talk to harbrew quiet 2"],
            [968.0,790.0,200,100,"Harbrew Town 2 Hint Guy","Talk to harbrew hint guy"],
            [3600.0,2940.0,100,100,"Mountain Camp Level 5","Key Door 1"],
            [2256.0,852.0,60,120,"Mountain Camp Level 7","Read sign Mountain Camp Level 7"],
            [3540.0,1510.0,100,100,"Research Lab Level 3","Enter research lab level 4"],
            [3660.0,310.0,100,100,"Research Lab Level 4","Enter research lab level 3"],
            [3710.0,540.0,100,100,"Research Lab Level 3","Key Door 2"],
            [2580.0,610.0,100,100,"Research Lab Level 5","RLL5 Door down"],
            [300.0,1330.0,100,100,"Research Lab Level 5","RLL5 Door up"],
            [180.0,489.0,100,100,"Research Lab Level 6","RLL6 Door to 7"],
            [180.0,849.0,100,100,"Research Lab Level 7","RLL7 Door to 6"],
            [2740.0,660.0,100,100,"Research Lab Level 6","Key Door 3"],
            [330.0,790.0,100,100,"Harbrew Town 1","Sign harbrew 1"],
            [330.0,790.0,100,100,"Lakeview Harbour","Sign lakeview 1"],
            [2010.0,790.0,100,100,"Lakeview Harbour","Enter lakeview harbour house 1"],
            [1100.0,660.0,200,100,"Lakeview Harbour House 1","Talk to lakeview fighter"],
            [2480.0,790.0,100,100,"Lakeview Harbour Docks","Talk to harbour master"],
            [870.0,790.0,100,100,"Lakeview Harbour","Enter lakeview harbour healer"],
            [1040.0,669.0,200,100,"Lakeview Harbour Healer","Talk to healer"],
            [2700.0,850.0,100,100,"Research Lab Boss","RLLB Door to 9"],
            [180.0,790.0,100,100,"Research Lab Level 9","RLL9 Door to boss"],
            [1920.0,1990.0,100,100,"Castle Level 3","CL3 to 4"],
            [120.0,310.0,100,100,"Castle Level 4","CL4 to 3"],
            [2700.0,1270.0,100,100,"Castle Level 6","CL6 to 9"],
            [2700.0,370.0,100,100,"Castle Level 9","CL9 to 6"],
            [2150.0,370.0,100,100,"Castle Level 9","CL9 door 1"],
            [480.0,370.0,100,100,"Castle Level 9","CL9 door 2"],
            [720.0,370.0,100,100,"Castle Level 9","CL9 door 3"],
            [240.0,370.0,100,100,"Castle Level 9","CL9 door 4"],
            [900.0,850.0,100,100,"Castle Level 9","CL9 door 5"],
            [1020.0,310.0,100,100,"Castle Level 9","CL9 door 6"],
            [2400.0,1160.0,100,200,"Castle Level 9","CL9 door 7"],
            [2400.0,1510.0,100,100,"Castle Level 9","CL9 door 8"],
            [600.0,1210.0,100,100,"Castle Level 9","CL9 door 9"],
            [1740.0,1510.0,100,100,"Castle Level 9","CL9 door 10"],
            [1920.0,910.0,100,100,"Castle Level 3","CL3 to 10"],
            [360.0,850.0,100,100,"Castle Level 10","CL10 to 3"],
            [2240.0,850.0,100,100,"Castle Level 10","Key Door 4"],
            [2480.0,850.0,100,100,"Castle Level 10","Key Door 5"],
            [2720.0,850.0,100,100,"Castle Level 10","Key Door 6"]
            
            ]
        
        #Only happens once
        self.cutscenes = [
            [930,730,100,100,"Beach","Wake up beach"],
            [550,730,400,900,"Castaway Village 2","Cutscene armoury"],
            [2720,880,86//self.scale,106//self.scale,"Mt Komodo Mineshaft","Obtain bombs"],
            [120.0,650.0,1000,1000,"Mt Komodo Level 1","Candle for Mt Komodo"], #cannot enter mt komodo
            [3720.0,480.0,1000,1000,"Cave near start 1","Candle for start cave"], #cannot enter mt komodo
            [4912.0,2980.0,136//self.scale,96//self.scale,"Mountain Camp Level 5","Obtain hookshot"],
            [1190.0,1090.0,24//self.scale,54//self.scale,"Mountain Camp Level 4","Key Pickup 1"],
            [350.0,1330.0,24//self.scale,54//self.scale,"Research Lab Level 4","Key Pickup 2"],
            [2280.0,850.0,54//self.scale,112//self.scale,"Research Lab Level 7","Obtain bow"],
            [2580.0,850.0,24//self.scale,54//self.scale,"Research Lab Level 7","Key Pickup 3"],
            [1670.0,1512.0,10//self.scale,3000//self.scale,"Bridge Pass 2 Guards","Check guard bribe"],
            [900.0,790.0,10//self.scale,3000//self.scale,"Research Lab Level 8","See scientist"],
            [480.0,790.0,10//self.scale,3000//self.scale,"Research Lab Level 9","Talk to scientist"],
            [450.0,1330.0,23//self.scale,54//self.scale,"Castle Level 5","Key Pickup 4"],
            [960.0,850.0,23//self.scale,54//self.scale,"Castle Level 8","Key Pickup 5"],
            [1400.0,1510.0,23//self.scale,54//self.scale,"Castle Level 9","Key Pickup 6"],
            [2340.0,0.0,10//self.scale,3000//self.scale,"Castle Throne Room","Final Cutscene"]


            ]

        self.key_doors = [["Mountain Camp Level 5",3600.0,2880.0],
                          ["Research Lab Level 3",3720.0,480.0],
                          ["Research Lab Level 6",2760.0,600.0],
                          ["Castle Level 10",2280.0,780.0],
                          ["Castle Level 10",2520.0,780.0],
                          ["Castle Level 10",2760.0,780.0]
                          
                          ]

        self.obj_door = []

        self.interact_obj = []

        for Item in self.interactables: #Loads all interactables into a list
            try: #If a one time interactable
                if self.events[self.event_dict[Item[5]]] == False: #If that interactable has not been activated
                    temp = Interactable(Item[0],Item[1],Item[2],Item[3],Item[4],Item[5])
                    self.interact_obj = temp.Append(self.interact_obj)
            except: #If it can be activated as many times
                temp = Interactable(Item[0],Item[1],Item[2],Item[3],Item[4],Item[5])
                self.interact_obj = temp.Append(self.interact_obj) 

        self.cutscenetrigger = []

        for Item2 in self.cutscenes: #
            if self.events[self.event_dict[Item2[5]]] == False:
                temp = CutsceneTrigger(Item2[0],Item2[1],Item2[2],Item2[3],Item2[4],Item2[5])
                self.cutscenetrigger = temp.Append(self.cutscenetrigger)


        self.TempWallsDB = DBTable('destroyedwalls.db','tblProfile'+str(profile),['Level','X','Y','Block','Destroyed'],"")
        
        if new_file == True:
            redo_db = self.TempWallsDB.QueryTable()
            for Data in redo_db:
                self.TempWallsDB.UpdateDestroyed(Data[0],Data[1],Data[2],"False") #(one,two,three,four) Levels,x,y,dest
            #profile

        self.temp_data = []
        self.temp_walls = []
        self.temp_drops = []

        self.ReinstantiateTempWalls()
        
        self.projectiles = []

        self.MakeHeight()
                              
        #Inventory Buttons
        self.Inventory_back = MenuButton("X",None,(1830/self.scale,90/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        #Skill points
        self.Confirm_SP = AttributeButton("Confirm Allocation","Confirm SP",(1440/self.scale,850/self.scale),int(500/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        self.Str_add = AttributeButton("+","+str",(1540/self.scale,550/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        self.Str_deduct = AttributeButton("-","-str",(1740/self.scale,550/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        self.Res_add = AttributeButton("+","+res",(1540/self.scale,650/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        self.Res_deduct = AttributeButton("-","-res",(1740/self.scale,650/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        self.Spe_add = AttributeButton("+","+spe",(1540/self.scale,750/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        self.Spe_deduct = AttributeButton("-","-spe",(1740/self.scale,750/self.scale),int(50/self.scale),int(50/self.scale),red,"georgia",int(60/self.scale),"Game")
        #Items jumpto 102
        self.Bombs = AttributeButton("","Bombs",(510/self.scale,460/self.scale),int(120/self.scale),int(120/self.scale),black,"georgia",int(60/self.scale),"Game")
        self.Hookshot = AttributeButton("","Hookshot",(510/self.scale,640/self.scale),int(120/self.scale),int(120/self.scale),black,"georgia",int(60/self.scale),"Game")
        self.Bow = AttributeButton("","Bow",(510/self.scale,820/self.scale),int(120/self.scale),int(120/self.scale),black,"georgia",int(60/self.scale),"Game")

        controls = self.ControlsDB.QueryTable()
        for Record in controls:
            if Record[0] == "Attack":
                self.sword_button = str(Record[1])
            elif Record[0] == "Use Item":
                self.item_button = str(Record[1])
            elif Record[0] == "Duck":
                self.shield_button = str(Record[1])
    
        
        #Menu Buttons
        #menu_txt_x = int(400/self.scale)
        #menu_txt_y = int(90/self.scale)
        #menu_font_size = int(60/self.scale)
        self.Resume_menu = MenuButton("Resume", None,(960/self.scale,450/self.scale),int(400/self.scale),int(90/self.scale), black, "georgia",int(60/self.scale), "Game")
        self.Save_game = MenuButton("Save Game","Save Game Confirmation",(960/self.scale,600/self.scale),int(400/self.scale),int(90/self.scale), black, "georgia",int(60/self.scale), "Game")
        self.Back_main = MenuButton("Main Menu", "Back Confirmation",(960/self.scale,750/self.scale),int(400/self.scale),int(90/self.scale), black, "georgia",int(60/self.scale),"Game")

        #Confirm main menu buttons
        #menu_txt_x = int(300/self.scale) #960, 
        #menu_txt_y = int(90/self.scale)
        #menu_font_size = int(60/self.scale)
        self.Back_menu = MenuButton("Back","Menu",(760/self.scale,640/self.scale),int(300/self.scale),int(90/self.scale), black, "georgia",int(60/self.scale),"Game")
        self.Main_confirm = MenuButton("Main Menu","Back To Menu",(1140/self.scale,640/self.scale),int(300/self.scale),int(90/self.scale), red, "georgia",int(60/self.scale),"Game")

        #Confirm close game buttons
        #menu_txt_x = int(330/self.scale) #960, 
        #menu_txt_y = int(90/self.scale)
        #menu_font_size = int(60/self.scale)
        self.Resume_game = MenuButton("Resume", None,(760/self.scale,640/self.scale),int(330/self.scale),int(90/self.scale), black, "georgia",int(60/self.scale),"Game")
        self.Close_game = MenuButton("Close Game", "Close",(1140/self.scale,640/self.scale),int(330/self.scale),int(90/self.scale), red, "georgia",int(60/self.scale),"Game")
        
        #Confirm save buttons
        #menu_txt_x = int(330/self.scale)
        #menu_txt_y = int(90/self.scale)
        #menu_font_size = int(60/self.scale)
        self.Back_save_game = MenuButton("Back","Menu",(760/self.scale,640/self.scale),int(330/self.scale),int(90/self.scale), black, "georgia",int(60/self.scale),"Game")
        self.Saved_game = MenuButton("Save","Save Game",(1160/self.scale,640/self.scale),int(330/self.scale),int(90/self.scale), red, "georgia",int(60/self.scale),"Game")

        #time,char_name,location,x,y,level,strength,resilience,speed,items,items_dict,events,bosses
        
    def MakeHeight(self): #ChangeLevel
        self.height_dict = {}
        self.width_dict = {}
        for Loop in range(0,72,1):
            file = open("levels/"+str(Loop)+".txt","r")
            contents = file.read().split("\n")
            file.close()
            contents.pop()
            b_height = len(contents)
            b_width = int(len(contents[0])//3)
            self.height_dict[Loop] = b_height
            self.width_dict[Loop] = b_width

            
        
    def LoadNewProfile(self,name):
        '''
        #STR name - Character name the user has chosen as a new profile
        '''
        time = 0.0 #Float
        char_name = name #Str
        #location = ["Overworld","Beach","Castaway Village 2"]
        #location = ["Overworld","Beach","Castaway Village 1"] #Stack
        location = ["Overworld","Beach"]
        #location = ["Overworld"]
        #pos_x = 1710.0 #28 > +30 #OVERWORLD START
        #pos_y = 6390.0 #106 v + 30
        pos_x = 930
        #pos_x = 1590
        pos_y = 730
        health = 10
        max_health = 10
        level = 1 #Int
        exp = 0
        skill_points = 0
        strength = 0 #Int
        resilience = 0 #Int
        speed = 0 #Int
        items = {"Sword":False,"Torch":False,"Bombs":False,"Hookshot":False,"Bow":False,"Gold":False} #If the user has obtained these items
        items_dict = {"Bombs":0,"Arrows":0,"Keys":0} #How many bombs and arrows for the bow the user has (And dunegon keys)
        events = {} #None triggered
        temp = [0,2,9,10,15,16,17,18,19,23,24,29,30,31,36,38,39,40,45,46,59,65] #One time, non recurant events
        #Only events that matter
        for Loop1 in temp: #Loop till how many events in game
            events[int(Loop1)] = False
            
        bosses = {} #None triggered
        for Loop1 in range(0,2,1): #Loop till how many bosses in game
            bosses[Loop1] = False
        last_location = ["Overworld","Beach"]
        last_move = None
        last_overworld_x = 0
        last_overworld_y = 0

        return time,char_name,location,pos_x,pos_y,health,max_health,level,exp,skill_points,strength,resilience,speed,items,items_dict,events,bosses,last_location,last_move,last_overworld_x,last_overworld_y

    def LoadOldProfile(self,profile): #######################When i have a save to file option, then i can implement loading
        '''
        #STR name - Character name the user has chosen as a new profile
        '''
        file = open("profiles/Profile"+str(profile)+".txt","r")
        contents = file.read()
        contents = contents.split("\n")
        contents.pop()

        time = float(contents[0])

        name_list = contents[1].split("  ")
        name_list.pop()
        char_name = name_list #Str

        location_list = contents[2].split("  ")
        location_list.pop()
        location = location_list #Stack
        
        pos_x = float(contents[3]) #Measured in blocks left and right of centers
        pos_y = float(contents[4]) #Measured in height from a certain point of height
        health = int(contents[5])
        max_health = int(contents[6])
        level = int(contents[7]) #Int
        exp = int(contents[8])
        skill_points = int(contents[9])
        strength = int(contents[10]) #Int
        resilience = int(contents[11]) #Int
        speed = int(contents[12]) #Int

        def BoolConverter(string):
            if string == "True":
                return True
            elif string == "False":
                return False

        items_list = contents[13].split(" ")
        items_list.pop()
        items = {}
        items[str(items_list[0])] = BoolConverter(items_list[1])
        items[str(items_list[2])] = BoolConverter(items_list[3])
        items[str(items_list[4])] = BoolConverter(items_list[5])
        items[str(items_list[6])] = BoolConverter(items_list[7])
        items[str(items_list[8])] = BoolConverter(items_list[9])
        items[str(items_list[10])] = BoolConverter(items_list[11]) #If the user has obtained these items

        items_d_list = contents[14].split(" ") #Dictonary
        items_d_list.pop()
        items_dict = {}
        items_dict[str(items_d_list[0])] = int(items_d_list[1]) #As these are integers
        items_dict[str(items_d_list[2])] = int(items_d_list[3])
        items_dict[str(items_d_list[4])] = int(items_d_list[5])

        events_list = contents[15].split(" ") #Dictonary
        events_list.pop()
        events = {}
        '''
        events[int(events_list[0])] = BoolConverter(events_list[1])
        events[int(events_list[2])] = BoolConverter(events_list[3])
        events[int(events_list[4])] = BoolConverter(events_list[5])
        events[int(events_list[6])] = BoolConverter(events_list[7])
        events[int(events_list[8])] = BoolConverter(events_list[9])
        events[int(events_list[10])] = BoolConverter(events_list[11])
        events[int(events_list[12])] = BoolConverter(events_list[13])
        '''

        for Loop in range(0,int(len(events_list)//2),1):
            events[int(events_list[Loop*2])] = BoolConverter(events_list[(Loop*2)+1])

        bosses_list = contents[16].split(" ") #Dictonary
        bosses_list.pop()
        bosses = {}
        bosses[int(bosses_list[0])] = BoolConverter(bosses_list[1])
        bosses[int(bosses_list[2])] = BoolConverter(bosses_list[3])

        last_location_list = contents[17].split("  ")
        last_location_list.pop()
        last_location = last_location_list

        last_move = str(contents[18])

        last_overworld_x = float(contents[19])
        last_overworld_y = float(contents[20])

        return time,char_name,location,pos_x,pos_y,health,max_health,level,exp,skill_points,strength,resilience,speed,items,items_dict,events,bosses,last_location,last_move,last_overworld_x,last_overworld_y

    def GameState(self,Display,event):
        '''
        #OBJECT Display - The class that draws to the screen
        #INT event - Will be None if no event is happening,
        '''
        self.event = event
        if self.event == 0:
            self.buffer_event = 0
            self.event_delay = 0
            self.event_index = 0
        button = None
        button_down = False
        mouse = None
        mouse_down = False
        clickdown = False
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()/1000
        self.level_change = True
        self.contents = ""
        self.walls = []
        Player = PlayerClass(self.pos_x,self.pos_y,self.scale)
        Player.SetStats(self.strength,self.speed)
        self.WallDictionaryCreation()
        self.DecoDictionaryCreation()
        self.InputDictionaryCreation()

        self.small_font1 = pygame.font.SysFont("georgia", int(30/self.scale))
        self.big_font1 = pygame.font.SysFont("georgia", int(70/self.scale))
        self.big_font2 = pygame.font.SysFont("georgia", int(60/self.scale))
        
        while True: #jumptomainmain
            #print(self.location)
            #print(self.event)
            if self.start_spawn == True:
                if 37 <= self.location_dict[self.location[len(self.location)-1]] <= 47:
                    self.WallsMethod(Display,Player)
                    self.LoadEncounterEnemies(self.location_dict[self.location[len(self.location)-1]],Display)
                    self.start_spawn = False
                elif self.location[len(self.location)-1] == "Overworld":
                    self.start_spawn = False
                else:
                    self.WallsMethod(Display,Player)
                    self.LoadEnemiesFromLoad(Display)
                    self.start_spawn = False
            
            if self.event == None: #Game
                self.buffer_event = 0
                self.event_index = 0
                if self.event_delay != 0:
                    self.event_delay -= 1

                self.switch_event = True #So events load once
                
                self.temp_skill = self.skill_points
                self.temp_str = self.strength
                self.temp_res = self.resilience
                self.temp_spe = self.speed
                
                button,button_down,mouse,mouse_down = self.InputGetter(button,button_down,mouse,mouse_down)
                b_input,m_input = self.InputInterpreter(button,button_down,mouse,mouse_down)
                
                if b_input == "Menu" or m_input == "Menu":
                    if self.location[len(self.location)-1] == "Overworld":
                        if Player.over_walk_tic == 16: #Idle
                            self.event = "Menu"
                            b_input = m_input = button = None
                            button_down = False
                        
                    else:
                        self.event = "Menu"
                        b_input = m_input = button = None
                        button_down = False
                        
                if b_input == "Inventory" or m_input == "Inventory":
                    if self.location[len(self.location)-1] == "Overworld":
                        if Player.over_walk_tic == 16:
                            self.event = "Inventory"
                            b_input = m_input = button = None
                            button_down = False

                    else:
                        self.event = "Inventory"
                        b_input = m_input = button = None
                        button_down = False
                    
                #print(button,mouse,button_down)
                #print(button)
                if self.location[len(self.location)-1] == "Overworld":
                    self.last_location = ["Overworld"]
                    
                    self.OverworldWallsMethods(Display)

                    Player.PlayerOverworldMove(self.walls,self.overworld_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)

                    Player.PlayerOverworldMethod(Display,self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)

                    self.over_stopped = Player.GetOverworldStopped()

                    if self.items["Sword"] == True:
                        #pass
                        #print("KFS")
                        self.EnemyEncounters(Display)

                    #self.FindBehindTile()
                    

                    self.OverworldChangeDetector(Display,Player)
                    
                else:                               #####In a level jumptomain

                    runnning,mouse_pos,click1,clickdown = EventGet(clickdown)
                    
                    self.LevelUpMethod()
                    
                    self.WallsMethod(Display,Player)

                    
                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)

                    Player.PlayerMethod(Display,self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale,self)

                    self.DrawHealth(Display)
                    self.DrawItemIcon(Display)
                    self.CheckHP(Display,Player)

                    self.HandleUseItem(b_input,m_input,mouse_pos,Player,Display,clickdown) #jumpback
                    self.HandleProjectiles(Player,Display)

                    if len(self.temp_walls) != 0:
                        if len(self.projectiles) != 0:
                            self.CheckDestruction()
                        if self.location[len(self.location)-1] == "Mountain Camp Boss": #jumpback8
                            self.CheckBossDoor(0)
                        elif self.location[len(self.location)-1] == "Research Lab Boss": #jumpback8
                            self.CheckBossDoor(1)

                    if self.location[len(self.location)-1] == "Mountain Camp Boss":
                        if self.bosses[0] == False:
                            self.DrawBossHealthBar(Display,"BossOrc")
                            
                    if self.location[len(self.location)-1] == "Research Lab Boss":
                        if self.bosses[1] == False:
                            self.DrawBossHealthBar(Display,"BossDemonOrc")

                    if len(self.temp_drops) != 0:
                        self.DrawDrops(Display,Player)

                    #if len(self.obj_door) != 0:
                        #self.UpdateKeyDoor(Display,Player)
                    
                    if len(self.current_interactables) != 0:
                        self.HandleInteractables(button,button_down,b_input,m_input,Player,Display)
                    if len(self.current_cutscenes) != 0:
                        self.HandleCutscenes(Player,Display)

                    self.LevelChangeDetector(Display,Player)
                
                pygame.display.flip()
                #self.event = 1
                #print(self.pos_x,self.pos_y) #printpos

                
                self.time = pygame.time.get_ticks()/1000 - start_time #+profile loaded time
                #print(self.time)
                #print(int(time)) #Integer time
                #print(clock.get_fps())
                clock.tick(60)
            else:
                
                if self.event_delay == 0:
                    if self.buffer_event != 0:
                        self.buffer_event -= 1
                    
                    runnning,mouse_pos,click1,clickdown = EventGet(clickdown)
                    
                    if self.event == "Inventory": #
                        self.DrawIngameInventory(Display,mouse_pos,click1)

                    elif self.event == "Confirm SP":
                        before_res = ""
                        before_res = self.resilience
                        self.skill_points = self.temp_skill
                        self.strength = self.temp_str
                        self.resilience = self.temp_res
                        self.speed = self.temp_spe
                        self.event = "Inventory"
                        Player.SetStats(self.strength,self.speed)
                        self.max_health = (self.resilience+2)*5
                        if self.resilience != before_res:
                            self.health = self.max_health
                        
                    elif self.event == "+str":
                        self.temp_str += 1
                        self.temp_skill -= 1
                        self.event = "Inventory"
                    elif self.event == "-str":
                        self.temp_str -= 1
                        self.temp_skill += 1
                        self.event = "Inventory"
                    elif self.event == "+res":
                        self.temp_res += 1
                        self.temp_skill -= 1
                        self.event = "Inventory"
                    elif self.event == "-res":
                        self.temp_res -= 1
                        self.temp_skill += 1
                        self.event = "Inventory"
                    elif self.event == "+spe":
                        self.temp_skill -= 1
                        self.temp_spe += 1
                        self.event = "Inventory"
                    elif self.event == "-spe":
                        self.temp_spe -= 1
                        self.temp_skill += 1
                        self.event = "Inventory"
                        
                    elif self.event == "Menu":
                        self.DrawIngameMenu(Display,mouse_pos,click1)

                    elif self.event == "Save Game Confirmation":
                        self.DrawSavedConfirmation(Display,mouse_pos,click1)

                    elif self.event == "Save Game":
                        self.DrawSaved(Display)
                        
                    elif self.event == "Back Confirmation":
                        self.DrawBackConfirmation(Display,mouse_pos,click1)
                        
                    elif self.event == "Back To Menu":
                        self.event = None
                        self.event_delay = 10
                        running = True
                        break

                    elif self.event == "Confirm Close":
                        self.DrawCloseConfirmation(Display,mouse_pos,click1)
                        
                    elif self.event == "Close":
                        self.event = None
                        self.event_delay = 10
                        running = False
                        break
                    ########################################0-4
                    elif self.event == 0: #Waking up on beach #.txt [0]
                        if self.event_index == 0: #Set delay
                            self.RedrawBehindOnly(Display,Player)
                            
                            sleeping = pygame.image.load("images/player/Sleeping1.png").convert_alpha()
                            sleeping_dimentions = (int(110//self.scale),int(55//self.scale))
                            sleeping = pygame.transform.scale(sleeping,sleeping_dimentions)
                            Display.screen.blit(sleeping,(int(830//self.scale),int(740//self.scale)))
                            
                            self.buffer_event = 180
                            self.event_index += 1
                                
                        elif self.event_index == 1: #Lying on the floor
                            if self.buffer_event != 0:
                                pass
                            else:
                                self.buffer_event = 0
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1
                                
                        elif self.event_index == 2: #Stand up
                            if self.buffer_event != 0:
                                #self.RedrawBehind(Display,Player)
                                pass
                            else:
                                self.buffer_event = 60
                                self.event_index += 1

                                Player.SetDirection("Left")
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 3: #Look left (Confused)
                            if self.buffer_event != 0:
                                #Player.SetDirection("Left")
                                #self.RedrawBehind(Display,Player)
                                pass
                            else:
                                #self.buffer_event = 250
                                self.event_index += 1
      
                        elif self.event_index == 4: #Talk to self
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,3,1):
                                    temp = Dialogue("0",Lines,self.scale,Display)
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    
                            if len(self.text_list) == 0:
                                self.event = None
                                self.event_delay = 10
                                b_input = m_input = button = None
                                button_down = False
                                self.events[0] = True
                                for Cutscene in self.cutscenetrigger:
                                    if self.event_dict[Cutscene.ReturnEvent()] == 0:
                                        self.cutscenetrigger.remove(Cutscene)
                                        self.current_cutscenes.remove(Cutscene)

                        #self.buffer_event = 150
                        #self.event_index = 1
                        #self.event = None
                        #self.event_delay = 10
                    ########################################Castaway village sign
                    elif self.event == 1: ##.txt [1]
                        if self.switch_event == True:#
                            self.switch_event = False
                            self.RedrawBehind(Display,Player)
                            for Lines in range(0,1,1):
                                temp = Dialogue("1",Lines,self.scale,Display)
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            self.RedrawBehind(Display,Player)
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                
                        if len(self.text_list) == 0:
                            self.event = None
                            self.event_delay = 10
                            b_input = m_input = button = None
                            button_down = False
                    ########################################Castaway village armoury cutscene
                    elif self.event == 2: #.txt [2,3,4,5,6,7]
                        
                        if self.event_index == 0: #"What happened here".txt 2
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("2",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1 #Alteration
                                self.buffer_event = 9999
                                Player.SetDirection("Right")
                                        
                        elif self.event_index == 1: #Walk along until see monsters
                            if self.buffer_event != 0:
                                if self.pos_x < 1920:
                                    self.RedrawBehind(Display,Player)
                                    #Player.ChangeVel(5,0)
                                    b_input = "Move Right"
                                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                else:
                                    self.buffer_event = 0
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 2: #"Arrrgh" + "Woah".txt 3
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("3",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 9999
                                Player.SetDirection("Left")

                        elif self.event_index == 3: #Run to armoury and enter
                            if self.buffer_event != 0:
                                if self.pos_x > 1655:
                                    self.RedrawBehind(Display,Player)
                                    b_input = "Move Left"
                                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                else:
                                    self.buffer_event = 0
                            else:
                                self.buffer_event = 90
                                self.LevelCutsceneChange("3 Door 1") #Change level
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration
                                Player.SetToIdle()

                                Player.SetDirection("Left")

                        elif self.event_index == 4: #Look left and "lock door"
                            if self.buffer_event != 0:
                                self.RedrawBehind(Display,Player)
                            else:
                                self.buffer_event = 9999
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration
                                Player.SetDirection("Right")

                        elif self.event_index == 5: #Run to center
                            if self.buffer_event != 0:
                                if self.pos_x < 960:
                                    self.RedrawBehind(Display,Player)
                                    b_input = "Move Right"
                                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                else:
                                    self.buffer_event = 0
                            else:
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration

                        elif self.event_index == 6: #"What happened here".txt 4
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("4",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1 #Alteration
                                self.buffer_event = 120
                                
                                Player.SetDirection("Left")
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 7: #Look left
                            if self.buffer_event != 0:
                                pass
                            else:
                                self.buffer_event = 60
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration

                                Player.SetDirection("Right")
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 8: #Look right
                            if self.buffer_event != 0:
                                pass
                            else:
                                self.buffer_event = 60
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration

                        elif self.event_index == 9: #"On second thoughts, what do we have here".txt 5
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("5",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1 #Alteration
                                self.buffer_event = 9999

                        elif self.event_index == 10: #Walk to right end
                            if self.buffer_event != 0:
                                if self.pos_x < 1740:
                                    self.RedrawBehind(Display,Player)
                                    b_input = "Move Right"
                                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)

                                else:
                                    self.buffer_event = 0
                            else:
                                self.buffer_event = 120
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration

                        elif self.event_index == 11: #Search
                            if self.buffer_event != 0:
                                pass
                            else:
                                self.buffer_event = 0
                                self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration

                                Player.SetDirection("Right")
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 12: #"Woah a sword".txt 6
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("6",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1 #Alteration
                                self.buffer_event = 30

                        elif self.event_index == 13: #Image of sword obtained
                            if self.buffer_event != 0:
                                pass
                            else:
                                self.buffer_event = 30
                                #self.RedrawBehind(Display,Player)
                                self.event_index += 1 #Alteration
                                #self.RedrawBehindOnly(Display,Player)

                        elif self.event_index == 14: #"You have acquired a sword!".txt 7
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehindOnly(Display,Player)

                                sword_get = pygame.image.load("images/player/SwordGet1.png").convert_alpha()
                                sword_get_dimentions = (int(69//self.scale),int(175//self.scale))

                                x,y,width,height = Player.ReturnDraw()

                                dif_width = (sword_get_dimentions[0] - width)/2
                                x -= width/2
                                x -= dif_width

                                dif_height = sword_get_dimentions[1] - height
                                y -= height/2
                                y -= dif_height
                                
                                sword_get = pygame.transform.scale(sword_get,sword_get_dimentions)
                                Display.screen.blit(sword_get,(x,y))
                                
                                for Lines in range(0,4,1): #Alteration
                                    temp = Dialogue("7",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                self.events[2] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event = None
                                for Cutscene in self.cutscenetrigger:
                                    if self.event_dict[Cutscene.ReturnEvent()] == 2: #Alteration
                                        self.cutscenetrigger.remove(Cutscene)
                                        #self.current_cutscenes.remove(Cutscene)
                                self.items["Sword"] = True
                    ########################################Castaway armoury entry
                    elif self.event == 3:
                        pos = self.level_exits[self.location[len(self.location)-1]]["3 Door 1"][1]
                        #self.location.append(self.level_exits[self.location[len(self.location)-1]]["Left"][0]) #Add to stack
                        self.location.append("Castaway Village Armoury")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Harbrew Town 1 Heal Hut entry
                    elif self.event == 4:
                        pos = self.level_exits[self.location[len(self.location)-1]]["8 Door 1"][1]
                        self.location.append("Harbrew Town 1 Heal Hut")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Harbrew Town 1 Quiet House entry
                    elif self.event == 5:
                        pos = self.level_exits[self.location[len(self.location)-1]]["8 Door 2"][1]
                        self.location.append("Harbrew Town 1 Quiet House")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Harbrew Town 2 Hint Guy entry
                    elif self.event == 6:
                        pos = self.level_exits[self.location[len(self.location)-1]]["9 Door 1"][1]
                        self.location.append("Harbrew Town 2 Hint Guy")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Harbrew Town 2 Hint Guy Attic entry
                    elif self.event == 7:
                        pos = self.level_exits[self.location[len(self.location)-1]]["9 Door 2"][1]
                        self.location.append("Harbrew Town 2 Hint Guy Attic")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Mt Komodo Mineshaft entry
                    elif self.event == 8:
                        pos = self.level_exits[self.location[len(self.location)-1]]["12 Door 1"][1]
                        self.location.append("Mt Komodo Mineshaft")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Mt Komodo bombs get
                    elif self.event == 9: #.txt [8]
                        #if self.event_index == 0: #"Bomb get".txt 5
                        if self.switch_event == True:
                            self.events[9] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            bomb_get = pygame.image.load("images/player/BombGet1.png").convert_alpha()
                            bomb_get_dimentions = (int(81//self.scale),int(159//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (bomb_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = bomb_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            bomb_get = pygame.transform.scale(bomb_get,bomb_get_dimentions)
                            Display.screen.blit(bomb_get,(x,y))
                            
                            for Lines in range(0,4,1): #Alteration
                                temp = Dialogue("8",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 9: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items["Bombs"] = True
                            self.items_dict["Bombs"] = 20
                    ########################################Talk to old man        
                    elif self.event == 10: #.txt [9,10,11 or 16]
                        if self.items["Torch"] == False:
                            if self.event_index == 0: #"They lacked taxes".txt 9
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,13,1): #Alteration
                                        temp = Dialogue("9",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.event_index += 1 #Alteration
                                    self.buffer_event = 60
                                    
                                    #Player.SetDirection("Left")
                                    self.RedrawBehind(Display,Player)

                            elif self.event_index == 1:
                                if self.buffer_event != 0:
                                    pass
                                else:
                                    self.buffer_event = 30
                                    self.event_index += 1

                            elif self.event_index == 2: #"You got a torch!".txt 4
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehindOnly(Display,Player)
                                    torch_get = pygame.image.load("images/player/TorchGet1.png").convert_alpha()
                                    torch_get_dimentions = (int(71//self.scale),int(146//self.scale))

                                    x,y,width,height = Player.ReturnDraw()

                                    dif_width = (torch_get_dimentions[0] - width)/2
                                    x -= width/2
                                    x -= dif_width

                                    dif_height = torch_get_dimentions[1] - height
                                    y -= height/2
                                    y -= dif_height
                                    
                                    torch_get = pygame.transform.scale(torch_get,torch_get_dimentions)
                                    Display.screen.blit(torch_get,(x,y))
                                    for Lines in range(0,2,1): #Alteration
                                        temp = Dialogue("10",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.event_index += 1
                                    self.buffer_event = 60
                                    
                                    #Player.SetDirection("Left")
                                    self.RedrawBehind(Display,Player)
                                    
                            elif self.event_index == 3:
                                if self.buffer_event != 0:
                                    Player.SetDirection("Left")
                                else:
                                    self.buffer_event = 30
                                    Player.SetDirection("Right")
                                    self.event_index += 1
                            
                            elif self.event_index == 4: #Good luck.txt 4
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,2,1): #Alteration
                                        temp = Dialogue("11",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    self.events[10] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.event = None
                                    self.buffer_event = 60
                                    self.items["Torch"] = True
                                    
                                    #Player.SetDirection("Left")
                                    self.RedrawBehind(Display,Player)
                            
                        else: #If already been through conversation
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("16",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                                
                                #Player.SetDirection("Left")
                                self.RedrawBehind(Display,Player)

                    ########################################Talk to a healer        
                    elif self.event == 11: #.txt [12]
                        if self.event_index == 0: #"Let me heal you".txt 12
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("12",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.health = self.max_health
                                self.event = None
                    ########################################Talk to quiet 1       
                    elif self.event == 12: #.txt [13]
                        if self.event_index == 0: #"Casta-what?".txt 12
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,5,1): #Alteration
                                    temp = Dialogue("13",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Talk to quiet 2       
                    elif self.event == 13: #.txt [14]
                        if self.event_index == 0: #"Get out of my house".txt 14
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,7,1): #Alteration
                                    temp = Dialogue("14",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Talk to hint guy        
                    elif self.event == 14: #.txt [15]
                        if self.event_index == 0: #"Monsters in my attic".txt 14
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,4,1): #Alteration
                                    temp = Dialogue("15",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Leave mt komodo if no torch       
                    elif self.event == 15: #.txt [17]
                        if self.items["Torch"] == False:
                            if self.event_index == 0: #"Too dark to enter mt komodo".txt 14
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #Alteration
                                        temp = Dialogue("17",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.event_index += 1
                                    self.LevelCutsceneChange("Left") #Change level
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None

                        else:
                            self.events[15] = True
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 15: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                    ########################################Leave start cave if no torch       
                    elif self.event == 16: #.txt [17]
                        if self.items["Torch"] == False:
                            if self.event_index == 0: #"Too dark to enter start cave".txt 14
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #Alteration
                                        temp = Dialogue("17",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.event_index += 1
                                    self.LevelCutsceneChange("Right") #Change level
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None

                        else:
                            self.events[16] = True
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 16: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                    ########################################Hookshot acquired 
                    elif self.event == 17: #.txt [18]
                        #if self.event_index == 0: #"Hookshot get".txt 1
                        if self.switch_event == True:
                            self.events[17] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            hook_get = pygame.image.load("images/player/HookGet1.png").convert_alpha()
                            hook_get_dimentions = (int(107//self.scale),int(177//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (hook_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = hook_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            hook_get = pygame.transform.scale(hook_get,hook_get_dimentions)
                            Display.screen.blit(hook_get,(x,y))
                            
                            for Lines in range(0,4,1): #Alteration
                                temp = Dialogue("18",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 17: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items["Hookshot"] = True

                        #if self.ground
                    ########################################Open key door
                    elif self.event == 18: #.txt [19]
                        if self.items_dict["Keys"] >= 1:
                            self.events[18] = True
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.items_dict["Keys"] -= 1

                            #'''
                            
                            for Door in self.temp_walls:
                                if Door.ReturnBlock() == "Door": #ReturnDBData
                                    if Door.ReturnDBData()[0] == "Mountain Camp Level 5" and Door.ReturnDBData()[1] == 3600 and Door.ReturnDBData()[2] == 2880:
                                        Door.SetOpened()
                                        
                                        #self.temp_walls.remove(Door)
                            #print(self.interact_obj)
                            for Interactable in self.interact_obj: #self.interact_obj self.iteractables
                                if self.event_dict[Interactable.ReturnEvent()] == 18: #Alteration
                                    self.current_interactables.remove(Interactable)
                                    self.interact_obj.remove(Interactable)
                            #'''
                        else:
                            
                            if self.event_index == 0:
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #Alteration
                                        temp = Dialogue("19",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None
                                    
                    ########################################Get key 1 in mt komodo
                    elif self.event == 19: #.txt [20]
                        #if self.event_index == 0: #"Hookshot get".txt 1
                        if self.switch_event == True:
                            self.events[19] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            key_get = pygame.image.load("images/player/KeyGet1.png").convert_alpha()
                            key_get_dimentions = (int(81//self.scale),int(148//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (key_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = key_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            key_get = pygame.transform.scale(key_get,key_get_dimentions)
                            Display.screen.blit(key_get,(x,y))
                            
                            for Lines in range(0,2,1): #Alteration
                                temp = Dialogue("20",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 19: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items_dict["Keys"] += 1

                    ########################################Talk to hint guy        
                    elif self.event == 20: #.txt [21]
                        if self.event_index == 0: #"Monsters in my attic".txt 14
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("21",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Research lab level 4 entry
                    elif self.event == 21:
                        pos = self.level_exits[self.location[len(self.location)-1]]["31 Door 1"][1]
                        self.location.append("Research Lab Level 4")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Research lab level 3 entry
                    elif self.event == 22:
                        pos = self.level_exits[self.location[len(self.location)-1]]["32 Door 1"][1]
                        self.location.pop()
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Get key 2 in research lab 4
                    elif self.event == 23: #.txt [20]
                        #if self.event_index == 0: #"Key get".txt 1
                        if self.switch_event == True:
                            self.events[23] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            key_get = pygame.image.load("images/player/KeyGet1.png").convert_alpha()
                            key_get_dimentions = (int(81//self.scale),int(148//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (key_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = key_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            key_get = pygame.transform.scale(key_get,key_get_dimentions)
                            Display.screen.blit(key_get,(x,y))
                            
                            for Lines in range(0,2,1): #Alteration
                                temp = Dialogue("20",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 23: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items_dict["Keys"] += 1
                    ########################################Open key door 2
                    elif self.event == 24: #.txt [19]
                        if self.items_dict["Keys"] >= 1:
                            self.events[24] = True #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.items_dict["Keys"] -= 1

                            #'''
                            
                            for Door in self.temp_walls:
                                if Door.ReturnBlock() == "Door": #ReturnDBData
                                    if Door.ReturnDBData()[0] == "Research Lab Level 3" and Door.ReturnDBData()[1] == 3720 and Door.ReturnDBData()[2] == 480:
                                        Door.SetOpened()
                                        
                                        #self.temp_walls.remove(Door)
                            #print(self.interact_obj)
                            for Interactable in self.interact_obj: #self.interact_obj self.iteractables
                                if self.event_dict[Interactable.ReturnEvent()] == 24: #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                    self.current_interactables.remove(Interactable)
                                    self.interact_obj.remove(Interactable)
                            #'''
                        else:
                            
                            if self.event_index == 0:
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        temp = Dialogue("19",Lines,self.scale,Display) #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None
                    ########################################RLL5 Door down
                    elif self.event == 25:
                        self.pos_x = 450
                        self.pos_y = 1330
                        self.event = None
                    ########################################RLL5 Door up
                    elif self.event == 26:
                        self.pos_x = 2460
                        self.pos_y = 610
                        self.event = None
                    ########################################RLL6 Door to 7
                    elif self.event == 27:
                        pos = self.level_exits[self.location[len(self.location)-1]]["34 Door 1"][1]
                        self.location.append("Research Lab Level 7")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################RLL6 Door to 7
                    elif self.event == 28:
                        pos = self.level_exits[self.location[len(self.location)-1]]["35 Door 1"][1]
                        self.location.pop()
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Bow acquired 
                    elif self.event == 29: #.txt [2]
                        #if self.event_index == 0: #"Bow get".txt 1
                        if self.switch_event == True:
                            self.events[29] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            hook_get = pygame.image.load("images/player/BowGet1.png").convert_alpha()
                            hook_get_dimentions = (int(107//self.scale),int(177//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (hook_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = hook_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            hook_get = pygame.transform.scale(hook_get,hook_get_dimentions)
                            Display.screen.blit(hook_get,(x,y))
                            
                            for Lines in range(0,4,1): #Alteration
                                temp = Dialogue("22",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 29: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items["Bow"] = True
                            self.items_dict["Arrows"] = 30
                    ########################################Get key 3 in research lab 7
                    elif self.event == 30: #.txt [20]
                        #if self.event_index == 0: #"Key get".txt 1
                        if self.switch_event == True:
                            self.events[23] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            key_get = pygame.image.load("images/player/KeyGet1.png").convert_alpha()
                            key_get_dimentions = (int(81//self.scale),int(148//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (key_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = key_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            key_get = pygame.transform.scale(key_get,key_get_dimentions)
                            Display.screen.blit(key_get,(x,y))
                            
                            for Lines in range(0,2,1): #Alteration
                                temp = Dialogue("20",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 30: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items_dict["Keys"] += 1
                    ########################################Open key door 3
                    elif self.event == 31: #.txt [19]
                        if self.items_dict["Keys"] >= 1:
                            self.events[31] = True #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.items_dict["Keys"] -= 1

                            #'''
                            
                            for Door in self.temp_walls:
                                if Door.ReturnBlock() == "Door": #ReturnDBData
                                    if Door.ReturnDBData()[0] == "Research Lab Level 6" and Door.ReturnDBData()[1] == 2760 and Door.ReturnDBData()[2] == 600:
                                        Door.SetOpened()
                                        
                                        #self.temp_walls.remove(Door)
                            #print(self.interact_obj)
                            for Interactable in self.interact_obj: #self.interact_obj self.iteractables
                                if self.event_dict[Interactable.ReturnEvent()] == 31: #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                    self.current_interactables.remove(Interactable)
                                    self.interact_obj.remove(Interactable)
                            #'''
                        else:
                            
                            if self.event_index == 0:
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        temp = Dialogue("19",Lines,self.scale,Display) #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None
                    ########################################Welcome to harbrew town      
                    elif self.event == 32: #.txt [23]
                        if self.event_index == 0:
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("23",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Welcome to lakeview harbour      
                    elif self.event == 33: #.txt [24]
                        if self.event_index == 0:
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("24",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Lakeview harbour house 1
                    elif self.event == 34:
                        pos = self.level_exits[self.location[len(self.location)-1]]["15 Door 1"][1]
                        self.location.append("Lakeview Harbour House 1")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Talk to lakeview fighter     
                    elif self.event == 35: #.txt [25]
                        if self.event_index == 0:
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,5,1): #Alteration
                                    temp = Dialogue("25",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                    ########################################Talk to lakeview harbour master    
                    elif self.event == 36: #.txt [26, 27, 28, 29, 30]
                        if self.bosses[0] == False:
                            if self.harb_master == 0: #First time talk to guy
                                if self.event_index == 0:
                                    if self.switch_event == True:
                                        self.switch_event = False
                                        self.RedrawBehind(Display,Player)
                                        for Lines in range(0,9,1): #Alteration
                                            temp = Dialogue("26",Lines,self.scale,Display) #Alteration
                                            self.text_list = temp.Append(self.text_list)
                                            self.switch_event = False

                                    self.text_list[0].Draw(self.char_name,Display)
                                        
                                    if click1 == True:
                                        self.RedrawBehind(Display,Player)
                                        if self.text_list[0].ReturnLenQueue() == 0:
                                            self.text_list.pop(0)
                                            
                                        else:
                                            self.text_list[0].EmptyAssembled()
                                            self.text_list[0].SetDraw()
                                            
                                    if len(self.text_list) == 0:
                                        #self.events[0] = True
                                        self.harb_master = 1
                                        self.switch_event = True
                                        b_input = m_input = button = None
                                        button_down = False
                                        self.buffer_event = 120
                                        self.event = None
                            else: #Recurring talking to him
                                if self.event_index == 0:
                                    if self.switch_event == True:
                                        self.switch_event = False
                                        self.RedrawBehind(Display,Player)
                                        for Lines in range(0,3,1): #Alteration
                                            temp = Dialogue("27",Lines,self.scale,Display) #Alteration
                                            self.text_list = temp.Append(self.text_list)
                                            self.switch_event = False

                                    self.text_list[0].Draw(self.char_name,Display)
                                        
                                    if click1 == True:
                                        self.RedrawBehind(Display,Player)
                                        if self.text_list[0].ReturnLenQueue() == 0:
                                            self.text_list.pop(0)
                                            
                                        else:
                                            self.text_list[0].EmptyAssembled()
                                            self.text_list[0].SetDraw()
                                            
                                    if len(self.text_list) == 0:
                                        #self.events[0] = True
                                        self.harb_master = 1
                                        self.switch_event = True
                                        b_input = m_input = button = None
                                        button_down = False
                                        self.buffer_event = 120
                                        self.event = None
                                
                        else: #If boss beaten
                            if self.items["Gold"] == False:
                                if self.event_index == 0:
                                    if self.switch_event == True:
                                        self.switch_event = False
                                        self.RedrawBehind(Display,Player)
                                        for Lines in range(0,3,1): #Alteration
                                            temp = Dialogue("28",Lines,self.scale,Display) #Alteration
                                            self.text_list = temp.Append(self.text_list)
                                            self.switch_event = False

                                    self.text_list[0].Draw(self.char_name,Display)
                                        
                                    if click1 == True:
                                        self.RedrawBehind(Display,Player)
                                        if self.text_list[0].ReturnLenQueue() == 0:
                                            self.text_list.pop(0)
                                            
                                        else:
                                            self.text_list[0].EmptyAssembled()
                                            self.text_list[0].SetDraw()
                                            
                                    if len(self.text_list) == 0:
                                        self.switch_event = True
                                        b_input = m_input = button = None
                                        button_down = False
                                        self.event_index += 1 #Alteration
                                        self.buffer_event = 60
                                        
                                        #Player.SetDirection("Left")
                                        self.RedrawBehind(Display,Player)
                                        
                                        
                                elif self.event_index == 1:
                                    if self.buffer_event != 0:
                                        pass
                                    else:
                                        self.buffer_event = 30
                                        self.event_index += 1

                                elif self.event_index == 2: #"You got a gold!".txt 4
                                    if self.switch_event == True:
                                        self.switch_event = False
                                        self.RedrawBehindOnly(Display,Player)
                                        torch_get = pygame.image.load("images/player/GoldGet1.png").convert_alpha()
                                        torch_get_dimentions = (int(120//self.scale),int(191//self.scale))

                                        x,y,width,height = Player.ReturnDraw()

                                        dif_width = (torch_get_dimentions[0] - width)/2
                                        x -= width/2
                                        x -= dif_width

                                        dif_height = torch_get_dimentions[1] - height
                                        y -= height/2
                                        y -= dif_height
                                        
                                        torch_get = pygame.transform.scale(torch_get,torch_get_dimentions)
                                        Display.screen.blit(torch_get,(x,y))
                                        for Lines in range(0,2,1): #Alteration
                                            temp = Dialogue("30",Lines,self.scale,Display) #Alteration
                                            self.text_list = temp.Append(self.text_list)
                                            self.switch_event = False

                                    self.text_list[0].Draw(self.char_name,Display)
                                        
                                    if click1 == True:
                                        if self.text_list[0].ReturnLenQueue() == 0:
                                            self.text_list.pop(0)
                                            
                                        else:
                                            self.text_list[0].EmptyAssembled()
                                            
                                    if len(self.text_list) == 0:
                                        self.items["Gold"] = True
                                        self.switch_event = True
                                        b_input = m_input = button = None
                                        button_down = False
                                        self.buffer_event = 120
                                        self.event = None
                                        
                            else: #"Venture on"
                                if self.event_index == 0:
                                    if self.switch_event == True:
                                        self.switch_event = False
                                        self.RedrawBehind(Display,Player)
                                        for Lines in range(0,2,1): #Alteration
                                            temp = Dialogue("29",Lines,self.scale,Display) #Alteration
                                            self.text_list = temp.Append(self.text_list)
                                            self.switch_event = False

                                    self.text_list[0].Draw(self.char_name,Display)
                                        
                                    if click1 == True:
                                        self.RedrawBehind(Display,Player)
                                        if self.text_list[0].ReturnLenQueue() == 0:
                                            self.text_list.pop(0)
                                            
                                        else:
                                            self.text_list[0].EmptyAssembled()
                                            self.text_list[0].SetDraw()
                                            
                                    if len(self.text_list) == 0:
                                        #self.events[0] = True
                                        self.switch_event = True
                                        b_input = m_input = button = None
                                        button_down = False
                                        self.buffer_event = 120
                                        self.event = None
                    ########################################Lakeview harbour healer house
                    elif self.event == 37:
                        pos = self.level_exits[self.location[len(self.location)-1]]["15 Door 2"][1]
                        self.location.append("Lakeview Harbour Healer")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Talk to guards 
                    elif self.event == 38: #.txt [31, 32]
                        if self.items["Gold"] == False:
                            if self.event_index == 0:
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,5,1): #Alteration
                                        temp = Dialogue("31",Lines,self.scale,Display) #Alteration
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.event_index += 1
                                    self.buffer_event = 9999
                                    Player.SetDirection("Left")

                            elif self.event_index == 1:
                                if self.buffer_event != 0:
                                    if self.pos_x > 1300:
                                        self.RedrawBehind(Display,Player)
                                        b_input = "Move Left"
                                        Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                    else:
                                        self.buffer_event = 0
                                else:
                                    self.buffer_event = 90
                                    self.RedrawBehind(Display,Player)
                                    self.event_index += 1 #Alteration
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.event = None
                                    Player.SetToIdle()

                                    Player.SetDirection("Left")


                                
                        else:
                            if self.switch_event == True:
                                self.switch_event = False
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("32",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                                for Cutscene in self.cutscenetrigger:
                                    if self.event_dict[Cutscene.ReturnEvent()] == 38: #Alteration
                                        self.cutscenetrigger.remove(Cutscene)
                                        self.current_cutscenes.remove(Cutscene)
                    ########################################See the scientist for him to run  jumpback11
                    elif self.event == 39: #.txt [33, 34, 3]
                        if self.event_index == 0: #"Hey!".txt 2
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.events[39] = True
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("33",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False
                                self.cutscene_1_image = pygame.image.load("images/decoration/022.png").convert_alpha()
                                self.cutscene_1_x = 1820.0//self.scale
                                self.cutscene_1_y = 779.0//self.scale
                                self.cutscene_1_width = int(55//self.scale)
                                self.cutscene_1_height = int(125//self.scale)

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)
                                
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1 #Alteration
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.transform.flip(self.cutscene_1_image,True,False) #Flips horizontally - to left
                                

                        elif self.event_index == 1: #Looks at player
                            if self.buffer_event != 0:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 30
                                self.event_index += 1
                                self.cutscene_1_image = pygame.transform.flip(self.cutscene_1_image,True,False) #Flips horizontally - to right

                        elif self.event_index == 2: #He runs
                            if self.buffer_event != 0:
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_x += 5

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)

                                
                                

                                Display.screen.blit(self.cutscene_1_image,pos)
                            else:
                                self.buffer_event = 30
                                self.event_index += 1

                        elif self.event_index == 3: #"I just want to talk".txt 3
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("34",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 9999
                                Player.SetDirection("Left")
                                        
                        elif self.event_index == 4: #Walk along until see monsters
                            if self.buffer_event != 0:
                                if self.pos_x < 1920:
                                    self.RedrawBehind(Display,Player)
                                    #Player.ChangeVel(5,0)
                                    b_input = "Move Right"
                                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                else:
                                    self.buffer_event = 0
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 5: #"Arrrgh" + "Woah".txt 3
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("3",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.event = None
                                for Cutscene in self.cutscenetrigger:
                                    if self.event_dict[Cutscene.ReturnEvent()] == 39: #Alteration
                                        self.cutscenetrigger.remove(Cutscene)
                                        self.current_cutscenes.remove(Cutscene)
                    ########################################Talk to scientist
                    elif self.event == 40: #.txt [35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
                        if self.event_index == 0: #"Phew".txt 35
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("35",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False
                            
                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1 #Alteration
                                self.buffer_event = 9999
                                Player.SetDirection("Right")                          

                        elif self.event_index == 1: #Walk infront of scientist
                            if self.buffer_event != 0:
                                if self.pos_x < 980:
                                    self.RedrawBehind(Display,Player)
                                    #Player.ChangeVel(5,0)
                                    b_input = "Move Right"
                                    Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                else:
                                    self.buffer_event = 0
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.SetDirection("Left")  
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 2: #"Who are you!".txt 36
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,11,1): #Alteration
                                    temp = Dialogue("36",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()
                                self.cutscene_1_x = 960.0//self.scale
                                self.cutscene_1_y = 540.0//self.scale
                                self.cutscene_1_width = int(1920//self.scale)
                                self.cutscene_1_height = int(1080//self.scale)

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 3: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/901.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                        
                        elif self.event_index == 4: #Image 901 + "The famed adventurer".txt 37
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,4,1): #Alteration
                                    temp = Dialogue("37",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False
                                
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 5: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/902.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 6: #Image 902 + "You found it.".txt 38
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("38",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)
                                
                        elif self.event_index == 7: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/903.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 8: #Image 903 + "You brought it back".txt 39
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("39",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 9: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/904.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 10: #Image 904 + "..sneek in".txt 40
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,2,1): #Alteration
                                    temp = Dialogue("40",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 11: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/905.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 12: #Image 905 + "executed".txt 41
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,4,1): #Alteration
                                    temp = Dialogue("41",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 13: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/906.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 14: #Image 906 + "beaten up".txt 42
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("42",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/907.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 15: #Image 907 + "on raft".txt 43
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("43",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Left")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 16: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)

                        elif self.event_index == 17: #all about stone.txt 44
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,20,1): #Alteration
                                    temp = Dialogue("44",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False


                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 60
                                Player.SetDirection("Left")

                        elif self.event_index == 18: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 60
                                
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.buffer_event = 120
                                self.events[40] = True
                                self.event = None
                                for Cutscene in self.cutscenetrigger:
                                    if self.event_dict[Cutscene.ReturnEvent()] == 40: #Alteration
                                        self.cutscenetrigger.remove(Cutscene)
                                        self.current_cutscenes.remove(Cutscene)

                    ########################################Lakeview harbour healer house
                    elif self.event == 41:
                        pos = self.level_exits[self.location[len(self.location)-1]]["57 Door 1"][1]
                        self.location.append("Research Lab Level 9")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Lakeview harbour healer house
                    elif self.event == 42:
                        pos = self.level_exits[self.location[len(self.location)-1]]["58 Door 1"][1]
                        self.location.pop()
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Lakeview harbour healer house
                    elif self.event == 43:
                        pos = self.level_exits[self.location[len(self.location)-1]]["62 Door 1"][1]
                        self.location.append("Castle Level 4")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Lakeview harbour healer house
                    elif self.event == 44:
                        pos = self.level_exits[self.location[len(self.location)-1]]["63 Door 1"][1]
                        self.location.pop()
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Get key 4 in castle 5
                    elif self.event == 45: #.txt [20]
                        #if self.event_index == 0: #"Key get".txt 1
                        if self.switch_event == True:
                            self.events[45] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            key_get = pygame.image.load("images/player/KeyGet1.png").convert_alpha()
                            key_get_dimentions = (int(81//self.scale),int(148//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (key_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = key_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            key_get = pygame.transform.scale(key_get,key_get_dimentions)
                            Display.screen.blit(key_get,(x,y))
                            
                            for Lines in range(0,2,1): #Alteration
                                temp = Dialogue("20",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 45: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items_dict["Keys"] += 1
                    ########################################Get key 4 in castle 5
                    elif self.event == 46: #.txt [20]
                        #if self.event_index == 0: #"Key get".txt 1
                        if self.switch_event == True:
                            self.events[46] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            key_get = pygame.image.load("images/player/KeyGet1.png").convert_alpha()
                            key_get_dimentions = (int(81//self.scale),int(148//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (key_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = key_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            key_get = pygame.transform.scale(key_get,key_get_dimentions)
                            Display.screen.blit(key_get,(x,y))
                            
                            for Lines in range(0,2,1): #Alteration
                                temp = Dialogue("20",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 46: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items_dict["Keys"] += 1
                    ########################################Lakeview harbour healer house
                    elif self.event == 47:
                        pos = self.level_exits[self.location[len(self.location)-1]]["65 Door 1"][1]
                        self.location.append("Castle Level 9")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Lakeview harbour healer house
                    elif self.event == 48:
                        pos = self.level_exits[self.location[len(self.location)-1]]["68 Door 1"][1]
                        self.location.pop()
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################CL door 1
                    elif self.event == 49:
                        self.pos_x = 360
                        self.pos_y = 370
                        self.event = None
                    ########################################CL door 2
                    elif self.event == 50:
                        self.pos_x = 2280
                        self.pos_y = 370
                        self.event = None
                    ########################################CL door 3
                    elif self.event == 51:
                        self.pos_x = 360
                        self.pos_y = 850
                        self.event = None
                    ########################################CL door 4
                    elif self.event == 52:
                        self.pos_x = 2280
                        self.pos_y = 1510
                        self.event = None
                    ########################################CL door 5
                    elif self.event == 53:
                        self.pos_x = 2280
                        self.pos_y = 1510
                        self.event = None
                    ########################################CL door 6
                    elif self.event == 54:
                        self.pos_x = 2400
                        self.pos_y = 810
                        self.event = None
                    ########################################CL door 7
                    elif self.event == 55:
                        self.pos_x = 240
                        self.pos_y = 1209
                        self.event = None
                    ########################################CL door 8
                    elif self.event == 56:
                        self.pos_x = 360
                        self.pos_y = 370
                        self.event = None
                    ########################################CL door 9
                    elif self.event == 57:
                        self.pos_x = 1140
                        self.pos_y = 1509
                        self.event = None
                    ########################################CL door 10
                    elif self.event == 58:
                        self.pos_x = 2280
                        self.pos_y = 370
                        self.event = None
                    ########################################Get key 4 in castle 5
                    elif self.event == 59: #.txt [20]
                        #if self.event_index == 0: #"Key get".txt 1
                        if self.switch_event == True:
                            self.events[59] = True
                            self.switch_event = False
                            self.RedrawBehindOnly(Display,Player)

                            key_get = pygame.image.load("images/player/KeyGet1.png").convert_alpha()
                            key_get_dimentions = (int(81//self.scale),int(148//self.scale))

                            x,y,width,height = Player.ReturnDraw()

                            dif_width = (key_get_dimentions[0] - width)/2
                            x -= width/2
                            x -= dif_width

                            dif_height = key_get_dimentions[1] - height
                            y -= height/2
                            y -= dif_height
                            
                            key_get = pygame.transform.scale(key_get,key_get_dimentions)
                            Display.screen.blit(key_get,(x,y))
                            
                            for Lines in range(0,2,1): #Alteration
                                temp = Dialogue("20",Lines,self.scale,Display) #Alteration
                                self.text_list = temp.Append(self.text_list)
                                self.switch_event = False

                        self.text_list[0].Draw(self.char_name,Display)
                            
                        if click1 == True:
                            if self.text_list[0].ReturnLenQueue() == 0:
                                self.text_list.pop(0)
                                
                            else:
                                self.text_list[0].EmptyAssembled()
                                self.text_list[0].SetDraw()
                                
                        if len(self.text_list) == 0:
                            #self.events[9] = True
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.event = None
                            for Cutscene in self.cutscenetrigger:
                                if self.event_dict[Cutscene.ReturnEvent()] == 59: #Alteration
                                    self.cutscenetrigger.remove(Cutscene)
                                    self.current_cutscenes.remove(Cutscene)
                            self.items_dict["Keys"] += 1
                    ########################################Lakeview harbour healer house
                    elif self.event == 60:
                        pos = self.level_exits[self.location[len(self.location)-1]]["62 Door 2"][1]
                        self.location.append("Castle Level 10")
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Lakeview harbour healer house
                    elif self.event == 61:
                        pos = self.level_exits[self.location[len(self.location)-1]]["69 Door 1"][1]
                        self.location.pop()
                        self.pos_x = pos[0]
                        self.pos_y = pos[1]
                        self.level_change = True
                        self.event = None
                    ########################################Open key door 4
                    elif self.event == 62: #.txt [19]
                        if self.items_dict["Keys"] >= 1:
                            self.events[62] = True #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.items_dict["Keys"] -= 1

                            #'''
                            
                            for Door in self.temp_walls:
                                if Door.ReturnBlock() == "Door": #ReturnDBData
                                    if Door.ReturnDBData()[0] == "Castle Level 10" and Door.ReturnDBData()[1] == 2280 and Door.ReturnDBData()[2] == 780:
                                        Door.SetOpened()
                                        
                                        #self.temp_walls.remove(Door)
                            #print(self.interact_obj)
                            for Interactable in self.interact_obj: #self.interact_obj self.iteractables
                                if self.event_dict[Interactable.ReturnEvent()] == 62: #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                    self.current_interactables.remove(Interactable)
                                    self.interact_obj.remove(Interactable)
                            #'''
                        else:
                            
                            if self.event_index == 0:
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        temp = Dialogue("19",Lines,self.scale,Display) #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None
                    ########################################Open key door 5
                    elif self.event == 63: #.txt [19]
                        if self.items_dict["Keys"] >= 1:
                            self.events[63] = True #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.items_dict["Keys"] -= 1

                            #'''
                            
                            for Door in self.temp_walls:
                                if Door.ReturnBlock() == "Door": #ReturnDBData
                                    if Door.ReturnDBData()[0] == "Castle Level 10" and Door.ReturnDBData()[1] == 2520 and Door.ReturnDBData()[2] == 780:
                                        Door.SetOpened()
                                        
                                        #self.temp_walls.remove(Door)
                            #print(self.interact_obj)
                            for Interactable in self.interact_obj: #self.interact_obj self.iteractables
                                if self.event_dict[Interactable.ReturnEvent()] == 63: #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                    self.current_interactables.remove(Interactable)
                                    self.interact_obj.remove(Interactable)
                            #'''
                        else:
                            
                            if self.event_index == 0:
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        temp = Dialogue("19",Lines,self.scale,Display) #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None
                    ########################################Open key door 6
                    elif self.event == 64: #.txt [19]
                        if self.items_dict["Keys"] >= 1:
                            self.events[64] = True #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                            self.event = None
                            self.switch_event = True
                            b_input = m_input = button = None
                            button_down = False
                            self.items_dict["Keys"] -= 1

                            #'''
                            
                            for Door in self.temp_walls:
                                if Door.ReturnBlock() == "Door": #ReturnDBData
                                    if Door.ReturnDBData()[0] == "Castle Level 10" and Door.ReturnDBData()[1] == 2760 and Door.ReturnDBData()[2] == 780:
                                        Door.SetOpened()
                                        
                                        #self.temp_walls.remove(Door)
                            #print(self.interact_obj)
                            for Interactable in self.interact_obj: #self.interact_obj self.iteractables
                                if self.event_dict[Interactable.ReturnEvent()] == 64: #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                    self.current_interactables.remove(Interactable)
                                    self.interact_obj.remove(Interactable)
                            #'''
                        else:
                            
                            if self.event_index == 0:
                                Player.SetGround()
                                if self.switch_event == True:
                                    self.switch_event = False
                                    self.RedrawBehind(Display,Player)
                                    for Lines in range(0,1,1): #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        temp = Dialogue("19",Lines,self.scale,Display) #-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        self.text_list = temp.Append(self.text_list)
                                        self.switch_event = False

                                self.text_list[0].Draw(self.char_name,Display)
                                    
                                if click1 == True:
                                    self.RedrawBehind(Display,Player)
                                    if self.text_list[0].ReturnLenQueue() == 0:
                                        self.text_list.pop(0)
                                        
                                    else:
                                        self.text_list[0].EmptyAssembled()
                                        self.text_list[0].SetDraw()
                                        
                                if len(self.text_list) == 0:
                                    #self.events[0] = True
                                    self.switch_event = True
                                    b_input = m_input = button = None
                                    button_down = False
                                    self.buffer_event = 120
                                    self.current_cutscenes = []
                                    #self.RedrawBehind(Display,Player)
                                    self.event = None
                    ########################################Open key door 6
                    elif self.event == 65: #.txt [19]
                        if self.event_index == 0: #all about stone.txt 44
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,10,1): #Alteration
                                    temp = Dialogue("45",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False


                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 30
                                Player.SetDirection("Left")
                                self.cutscene_1_image = pygame.image.load("images/decoration/BlackScreen.png").convert_alpha()
                                self.cutscene_1_x = 960.0//self.scale
                                self.cutscene_1_y = 540.0//self.scale
                                self.cutscene_1_width = int(1920//self.scale)
                                self.cutscene_1_height = int(1080//self.scale)

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                        elif self.event_index == 1: #Black screen transition
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/908.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 2: #Image 908 + "..sneek in".txt 40
                            if self.switch_event == True:
                                self.switch_event = False
                                Player.SetToIdle()
                                self.RedrawBehind(Display,Player)
                                for Lines in range(0,1,1): #Alteration
                                    temp = Dialogue("46",Lines,self.scale,Display) #Alteration
                                    self.text_list = temp.Append(self.text_list)
                                    self.switch_event = False

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                            self.text_list[0].Draw(self.char_name,Display)
                                
                            if click1 == True:
                                self.RedrawBehind(Display,Player)
                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                if self.text_list[0].ReturnLenQueue() == 0:
                                    self.text_list.pop(0)
                                    
                                else:
                                    self.text_list[0].EmptyAssembled()
                                    self.text_list[0].SetDraw()
                                    
                            if len(self.text_list) == 0:
                                #self.events[0] = True
                                self.switch_event = True
                                b_input = m_input = button = None
                                button_down = False
                                self.event_index += 1
                                self.buffer_event = 120
                                Player.SetDirection("Right")
                                self.cutscene_1_image = pygame.image.load("images/decoration/909.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                                self.final_exp_x = 1500//self.scale
                                self.final_exp_y = 600//self.scale
                                self.final_exp_tick = 0

                        elif self.event_index == 3: #Get exp jumpback15
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                                if self.final_exp_tick < 60:
                                    self.final_exp_tick += 1

                                    font = pygame.font.SysFont("georgia", int((40-(self.final_exp_tick*0.3))/self.scale))
                                    
                                    text = font.render("+99999999 exp", True, black)
                                    text_box = text.get_rect()
                                    self.final_exp_y -= 0.5
                                    text_box.center = (self.final_exp_x,self.final_exp_y-50)
                             
                                    Display.screen.blit(text,text_box)
                            
                            else:
                                self.buffer_event = 180
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/910.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 4: #Get exp jumpback15
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                                if self.final_exp_tick < 60:
                                    self.final_exp_tick += 1

                                    font = pygame.font.SysFont("georgia", int((40-(self.final_exp_tick*0.3))/self.scale))
                                    
                                    text = font.render("+99999999 exp", True, black)
                                    text_box = text.get_rect()
                                    self.final_exp_y -= 0.5
                                    text_box.center = (self.final_exp_x,self.final_exp_y-50)
                             
                                    Display.screen.blit(text,text_box)
                            
                            else:
                                self.buffer_event = 180
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.RedrawBehind(Display,Player)
                                self.cutscene_1_image = pygame.image.load("images/decoration/911.png").convert_alpha()

                                dimentions = (self.cutscene_1_width,self.cutscene_1_height)
                                self.cutscene_1_image = pygame.transform.scale(self.cutscene_1_image,dimentions)

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)

                        elif self.event_index == 5: #Get exp jumpback15
                            if self.buffer_event != 0:

                                pos = (self.cutscene_1_x-self.cutscene_1_width/2,self.cutscene_1_y-self.cutscene_1_height/2)
                                Display.screen.blit(self.cutscene_1_image,pos)
                            
                            else:
                                self.buffer_event = 9999
                                
                                self.event_index += 1
                                b_input = m_input = button = None
                                button_down = False
                                Player.PlayerLevelMove(self.walls,self.level_walls,self.pos_x,self.pos_y,b_input,m_input,self.temp_walls,self)
                                self.events[65] = True
                                self.event = None
                                self.event_delay = 10
                                running = True
                                break



                    #10
                        
                    pygame.display.flip()
                    clock.tick(60)
                    
                else:
                    self.event = None #jumptoevent

        return running
        

    def ReinstantiateTempWalls(self):
        if len(self.temp_data) == 0:
            self.temp_data = self.TempWallsDB.QueryTable()

        else:
            for Data in self.temp_data:
                self.TempWallsDB.UpdateDestroyed(Data[0],Data[1],Data[2],Data[4]) #(one,two,three,four) Levels,x,y,dest

    def InstantiateTempWalls(self,level,x,y,wall):
        if wall == "Door":
            temp = KeyDoor(level,x,y,self.scale)
            self.temp_walls = temp.Append(self.temp_walls)
        else: #Anything else is different graphics for a blow-up-able wall
            temp = TemporaryWalls(level,x,y,self.scale,wall,self.image,self.b_width,self.b_height)
            self.temp_walls = temp.Append(self.temp_walls)
        

    def ReinstantiateEncounters(self):
        '''
        Purpose is so that the variables for self.last_overworld are updated right as an overworld encounter takes place
        '''
        self.level_exits["Path Random Level 1"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)], #Random encounters in the overworld map                                  
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Plains Random Level 1"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Plains Random Level 2"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Plains Random Level 3"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Plains Random Level 4"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Bridge Random Level 1"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Beach Random Level 1"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Forest Random Level 1"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Forest Random Level 2"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Forest Random Level 3"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }
        self.level_exits["Forest Random Level 4"] = {"Left":    ["Overworld",(self.last_overworld_x,self.last_overworld_y)],                                   
                                                 "Right":   ["Overworld",(self.last_overworld_x,self.last_overworld_y)]
                                                 }

        

    def HandleUseItem(self,b_input,m_input,mouse_pos,Player,Display,clickdown):
        #print(b_input,m_input)
        if self.wait_item != 0:
            self.wait_item -= 1
        if self.wait_item == 0:
            if Player.ReturnGrounded() == True:
                if b_input == "Use Item" or m_input == "Use Item":
                    if self.item_equipt == "Bombs":
                        if self.items_dict["Bombs"] != 0: #(self.pos_x,self.pos_y,velocity,type_projectile) jumpback7
                            #- (287 + 55) #- (532/(self.scale*2)) + self.scale*36
                            #temp = PlayerBombs(self.pos_x - (216),self.pos_y - ((243 + 55/(self.scale))+self.scale*43),0,"Player Bombs",self.scale,self.b_height)
                            temp = PlayerBombs(self.pos_x - (216),self.pos_y - ((243 + 55/(self.scale))+self.scale*43),0,"Player Bombs",self.scale,self.b_height,self.b_width)
                            self.projectiles = temp.Append(self.projectiles)
                            self.items_dict["Bombs"] -= 1
                            self.wait_item = 120

                    elif self.item_equipt == "Hookshot":
                        Player.SetUsingItem(True)

                    elif self.item_equipt == "Bow":
                        if self.items_dict["Arrows"] != 0:
                            Player.SetUsingItem(True)
                            
                if Player.ReturnUsingItem() == True:
                    #Player.DrawUseItem(Display) #jumpback
                    if self.item_equipt == "Hookshot":
                        if self.hook_travel == False:
                            if (b_input == "Use Item" or m_input == "Use Item") and self.hook_travel == False:
                                Player.DrawHookshot(Display,mouse_pos)
                                Player.SetToIdle()
                            else:
                                x,y = Player.ReturnPlayerPos()
                                self.hookshot = PlayerHookshot(x,y,18,"Hookshot",mouse_pos,self.scale,self.b_height,self.b_width)
                                self.hook_travel = True
                                self.hook_x,self.hook_y = self.hookshot.ReturnVel()
                                
                                #Player.SetUsingItem(False)
                                #self.wait_item = 120

                        else:
                            Player.DrawHookshotLess(Display)
                            if self.hookshot.ReturnDead() == False:
                                if self.hookshot.ReturnReel() == False:
                                    if self.hookshot.ReturnReset() == False:
                                        self.hookshot.ProjMain(Player,Display,self.walls,self.level_walls)
                                        self.hookshot.Draw(Display,self.pos_x,self.pos_y)
                                        #self.hookshot.CalculateProjPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                                        self.hookshot.CalculateCenter(self.pos_x,self.pos_y,self.b_width,self.b_height)

                                        self.hookshot.CheckPos(Player)

                                    else: #Reverse till at player then check for if to kill projectile
                                        self.hookshot.SetNegativeVel()

                                else:
                                    #self.hookshot.ProjMain(Player,Display,self.walls,self.level_walls) #jumpback3
                                    #self.hookshot.Draw(Display,self.pos_x,self.pos_y)
                                    #self.hookshot.CalculateCenter(self.pos_x,self.pos_y,self.b_width,self.b_height)
                                    done = Player.PulledByHookshot(self.hook_x,self.hook_y,self.walls,self.level_walls,self.pos_x,self.pos_y,self.temp_walls,self,Display)
                                    
                                    if done == True:
                                        Player.DDraw(Display,self)
                                        self.hookshot.SetDead()
                                     
                            #else:
                            if self.hookshot.ReturnDead() == True:
                                #print("Falling")
                                #Player.DDraw(Display,self)
                                self.hookshot = None
                                self.hook_travel = False
                                b_input = m_input = None
                                Player.SetUsingItem(False)
                                self.wait_item = 30
                                #Player.DDraw(Display,self)
                                
                    elif self.item_equipt == "Bow": #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-jumpback9
                        if self.bow_released == False:
                            if (b_input == "Use Item" or m_input == "Use Item"):
                                Player.DrawBowPull(Display,mouse_pos)
                                Player.SetBowShooting(True)
                                Player.CalculateBowFrame()
                                Player.SetToIdle()
                            else:
                                if Player.ReturnBowShooting() == False and (b_input != "Use Item" or m_input != "Use Item"): #So keep pulling bow even if let go of mouse
                                    Player.SetBowRelease(True)
                                    Player.CalculateBowFrame()
                                    x,y = Player.ReturnPlayerPos() #append
                                    
                                    temp = PlayerArrows(self.pos_x,self.pos_y,18,"Player Arrow",mouse_pos,self.scale,self.b_height,self.b_width,x,y)
                                    self.projectiles = temp.Append(self.projectiles)
                                    #self.hook_x,self.hook_y = self.hookshot.ReturnVel()
                                    #self.hookshot = PlayerArrow(x,y,18,"Hookshot",mouse_pos,self.scale,self.b_height,self.b_width)
                                    self.bow_released = True
                                    self.hold_bow_pull = 30
                                    self.hold_mouse_pos = mouse_pos
                                    self.items_dict["Arrows"] -= 1
                                    Player.SetBowVariables()
                                    Player.DrawBowLess(Display,self.hold_mouse_pos)
                                    Player.SetToIdle()
                                else:
                                    Player.DrawBowPull(Display,mouse_pos)
                                    Player.CalculateBowFrame()
                                    Player.SetToIdle()
                                
                                
                                #Player.SetUsingItem(False)
                                #self.wait_item = 120
                        else:
        
                            if self.hold_bow_pull == 0:
                                b_input = m_input = None
                                Player.SetUsingItem(False)
                                self.bow_released = False
                                self.wait_item = 30
                            else:
                                Player.DrawBowLess(Display,self.hold_mouse_pos)
                                Player.SetToIdle()
                                self.hold_bow_pull -= 1
                        '''

                        else:
                            Player.DrawBowLess(Display)
                            if self.hookshot.ReturnDead() == False:
                                if self.hookshot.ReturnReel() == False:
                                    if self.hookshot.ReturnReset() == False:
                                        self.hookshot.ProjMain(Player,Display,self.walls,self.level_walls)
                                        self.hookshot.Draw(Display,self.pos_x,self.pos_y)
                                        #self.hookshot.CalculateProjPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                                        self.hookshot.CalculateCenter(self.pos_x,self.pos_y,self.b_width,self.b_height)

                                        self.hookshot.CheckPos(Player)

                                    else: #Reverse till at player then check for if to kill projectile
                                        self.hookshot.SetNegativeVel()

                                else:
                                    #self.hookshot.ProjMain(Player,Display,self.walls,self.level_walls) #jumpback3
                                    #self.hookshot.Draw(Display,self.pos_x,self.pos_y)
                                    #self.hookshot.CalculateCenter(self.pos_x,self.pos_y,self.b_width,self.b_height)
                                    done = Player.PulledByHookshot(self.hook_x,self.hook_y,self.walls,self.level_walls,self.pos_x,self.pos_y,self.temp_walls,self,Display)
                                    
                                    if done == True:
                                        Player.DDraw(Display,self)
                                        self.hookshot.SetDead()
                                     
                            #else:
                            if self.hookshot.ReturnDead() == True:
                                #print("Falling")
                                #Player.DDraw(Display,self)
                                self.hookshot = None
                                self.hook_travel = False
                                b_input = m_input = None
                                Player.SetUsingItem(False)
                                self.wait_item = 30
                                #Player.DDraw(Display,self)
                        '''

    def HandleProjectiles(self,Player,Display): #jumpback1
        for Projectile in self.projectiles:
            if Projectile.ReturnDead() == True:
                self.projectiles.remove(Projectile)
            else:
                #x,y,width,height = Player.ReturnPos()

                #height -= 12
                #y += 12

                #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(x-width/2,y-height/2,width,height))
                Projectile.ProjMain(Player,Display,self.walls,self.level_walls) 
                Projectile.Draw(Display,self.pos_x,self.pos_y)
                if Projectile.ReturnType() != "Player Arrow":
                    Projectile.PlayerCollide(Player,self)
                Projectile.CalculateProjPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                #Projectile.CalculateCenter(self.pos_x,self.pos_y,self.b_width,self.b_height)


    def CheckBossDoor(self,boss):
        if self.bosses[boss] == True:
            # if db of walls is false, set to true
            for Temp_Walls in self.temp_walls:
                if Temp_Walls.ReturnDestroyed() == False:
                    if self.boss_loc[Temp_Walls.ReturnDBData()[0]] == boss:
                        Temp_Walls.SetDestroyed(True)

    def CheckDestruction(self):
        for Projectile in self.projectiles:
            if Projectile.ReturnType() == "Player Bombs":
                if Projectile.ReturnExploded() == True:
                    pos = width = height = 0
                    for Temp_Walls in self.temp_walls:
                        if Temp_Walls.ReturnBlock() in ["043","063"]:
                            pos,width,height = Projectile.ReturnPoses()
                            #return self.pos,self.width,self.height
                            
                            if Temp_Walls.CollideBomb(pos,width,height):
                                Temp_Walls.SetDestroyed(True)

    def EnemyRandomTick(self):
        '''
        Calculates how long it will take for an enemy on the overworld map to respawn randomly
        '''
        if self.overworld_enemies_random == 0:
            if self.over_stopped == True: #Only spawns when the player is stopped or has finished moving (As you stop for 1 frame)
                self.overworld_spawn = True
                self.overworld_enemies_random = random.randint(240,300)
        else:
            self.overworld_enemies_random -= 1

    def OverworldEnemyLive(self): #Even if i have multiple enemies at once, they will all have the same life duration
        '''
        Method that ticks down the lifespan of an enemy on the overworld map
        '''
        if self.enemy_live != 0:
            self.enemy_live -= 1
        else:
            self.overworld_enemies = [] #Gets rid of enemy

        for Overworld in self.overworld_enemies:
            if Overworld.ReturnRemoved() == True:
                self.overworld_enemies = []

    def EnemyEncounters(self,Display): #jumpto2
        '''
        Handles overworld enemy spawns and all related
        '''
        if len(self.overworld_enemies) != 0: #Main for the overworld enemy
            self.OverworldEnemyLive() #Ticks for the life of the enemy
            
            for Enemy in self.overworld_enemies:
                Enemy.ChangePlayerPos(self.pos_x,self.pos_y)
                Enemy.Main()
                Enemy.Draw(Display)
                if Enemy.ReturnCollided() == True:
                    self.encounter = True
                    #self.LoadEnemies(Display)
                    if self.over_stopped == True:
                        self.RandomEncounter(Display)
                        
                        #self.LoadEnemies(Display)

        else:
            self.overworld_spawn = False
            self.EnemyRandomTick()
            if self.overworld_spawn == True: #self.over_stopped
                self.enemy_live = 300
                temp = OverworldEnemy(self.pos_x,self.pos_y,self.overworld_walls,self.scale) #Make one enemy
                self.overworld_enemies.append(temp) #Incase i want multiple possible encounters
                #pass

    def RandomEncounter(self,Display):
        self.last_overworld_x = self.pos_x
        self.last_overworld_y = self.pos_y #jumptoissue
        self.last_location = ["Overworld"]
        tile = self.FindBehindTile()
        if tile == "010": #Path
            self.over_encounter = "Path Random Level 1"
        elif tile == "002" or tile == "001": #Plains
            if self.level < 5: #Level 1
                self.over_encounter = "Plains Random Level 1"
            elif self.level < 10: #Level 2
                self.over_encounter = "Plains Random Level 2"
            elif self.level < 15: #Level 3
                self.over_encounter = "Plains Random Level 3"
            elif self.level == 15 or self.level == 16: #Level 4
                self.over_encounter = "Plains Random Level 4"
        elif tile == "006": #Bridge
            self.over_encounter = "Bridge Random Level 1"
        elif tile == "003": #Beach
            self.over_encounter = "Beach Random Level 1"
        elif tile == "008": #Forest
            if self.level < 5: #Level 1
                self.over_encounter = "Forest Random Level 1"
            elif self.level < 10: #Level 2
                self.over_encounter = "Forest Random Level 2"
            elif self.level < 15: #Level 3
                self.over_encounter = "Forest Random Level 3"
            elif self.level == 15 or self.level == 16: #Level 4
                self.over_encounter = "Forest Random Level 4"

        if self.die == False:
            self.last_location = ["Overworld"]
        else:
            self.die = False
        #self.location.append(self.overworld_exits[(self.pos_x,self.pos_y)][0]) #Add to stack
        self.ReinstantiateEncounters()
        self.location.append(self.over_encounter)
        pos = self.overworld_encounters_dict[self.over_encounter] #self.over_encounter
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.level_change = True
        self.LoadEncounterEnemies(self.location_dict[self.over_encounter],Display)
        #self.location_dict[self.over_encounter]

    def FindBehindTile(self):
        x_index = int((self.pos_x-30)//60)
        y_index = int((self.pos_y-30)//60)
        file = open("levels/0.txt","r")
        contents = file.read().split("\n")
        file.close()
        contents.pop()
        
        tile = contents[y_index][x_index*3:(x_index*3)+3]

        return tile

    def DrawDeathScreen(self,Display):
        Display.screen.fill(black)
        font1 = pygame.font.SysFont("georgia", int(80/self.scale))
        font2 = pygame.font.SysFont("georgia", int(70/self.scale))
        
        death_text1 = font1.render("You have died!", True, white)
        death_textbox1 = death_text1.get_rect()
        death_textbox1.center = (960/self.scale, 490/self.scale)

        death_text2 = font2.render("You will lose all current character level progress.", True, white)
        death_textbox2 = death_text2.get_rect()
        death_textbox2.center = (960/self.scale, 590/self.scale)

        Display.screen.blit(death_text1,death_textbox1)
        Display.screen.blit(death_text2,death_textbox2)

        pygame.display.flip()
        time.sleep(3)
        self.exp = 0

    def DrawCutsceneDependant(self,Display): #Added
        for Scene in self.current_cutscenes:
            if Scene.ReturnEvent() == "Obtain bombs":
                if self.events[9] == False:
                    center_x,center_y = self.GetCenter()
                    x = 2720//self.scale
                    y = 880//self.scale
                    width = int(43//self.scale)
                    height = int(53//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Bomb_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -400 <= pos[0] <= 2321/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Candle for Mt Komodo": #Draw darkness
                if self.events[15] == False:
                    pygame.draw.rect(Display.screen, black, pygame.Rect(0,0,1920,1080))
                    #image = pygame.image.load("okay.jpg").convert_alpha()
                    #pos = (500,500)
                    #Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Candle for start cave": #Draw darkness
                if self.events[16] == False:
                    pygame.draw.rect(Display.screen, black, pygame.Rect(0,0,1920,1080))

            if Scene.ReturnEvent() == "Obtain hookshot":
                if self.events[17] == False:
                    center_x,center_y = self.GetCenter()
                    x = 4912.0//self.scale
                    y = 2980.0//self.scale
                    width = int(68//self.scale)
                    height = int(48//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Hookshot_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -400 <= pos[0] <= 2321/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Key Pickup 1":
                #1190.0 1092.0
                if self.events[19] == False:
                    center_x,center_y = self.GetCenter()
                    x = 1180.0//self.scale
                    y = 1125.0//self.scale
                    width = int(12//self.scale)
                    height = int(27//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Key_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Key Pickup 2":
                if self.events[23] == False:
                    center_x,center_y = self.GetCenter()
                    x = 330.0//self.scale
                    y = 1330.0//self.scale
                    width = int(12//self.scale)
                    height = int(27//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Key_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Obtain bow":
                if self.events[29] == False:
                    center_x,center_y = self.GetCenter()
                    x = 2310.0//self.scale
                    y = 850.0//self.scale
                    width = int(54//self.scale)
                    height = int(112//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Bow_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Key Pickup 3":
                if self.events[30] == False:
                    center_x,center_y = self.GetCenter()
                    x = 2590.0//self.scale
                    y = 850.0//self.scale
                    width = int(12//self.scale)
                    height = int(27//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Key_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "See scientist": #jumpback11
                if self.events[39] == False:
                    center_x,center_y = self.GetCenter()
                    x = 1820.0//self.scale
                    y = 779.0//self.scale
                    width = int(55//self.scale)
                    height = int(125//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/decoration/022.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Talk to scientist": #jumpback11
                if self.events[40] == False:
                    center_x,center_y = self.GetCenter()
                    x = 920.0//self.scale
                    y = 779.0//self.scale
                    width = int(55//self.scale)
                    height = int(125//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/decoration/022.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Key Pickup 4":
                if self.events[45] == False:
                    center_x,center_y = self.GetCenter()
                    x = 450.0//self.scale
                    y = 1330.0//self.scale
                    width = int(12//self.scale)
                    height = int(27//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Key_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Key Pickup 5":
                if self.events[46] == False:
                    center_x,center_y = self.GetCenter()
                    x = 950.0//self.scale
                    y = 850.0//self.scale
                    width = int(12//self.scale)
                    height = int(27//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Key_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

            if Scene.ReturnEvent() == "Key Pickup 6":
                if self.events[59] == False:
                    center_x,center_y = self.GetCenter()
                    x = 1400.0//self.scale
                    y = 1510.0//self.scale
                    width = int(12//self.scale)
                    height = int(27//self.scale)

                    pos = ((x + center_x)-width/2,(y + center_y)-height/2)

                    image = pygame.image.load("images/items/Key_pickup.png").convert_alpha()
                    
                    dimentions = (width,height)
                    image = pygame.transform.scale(image,dimentions)
                    
                    if -100 <= pos[0] <= 2021/self.scale:
                        if -60 <= pos[1] <= 1081/self.scale:
                            Display.screen.blit(image,pos)

    def GetCenter(self):

        center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Minus so camera moves right when pos_x moves up 
        center_y = -((self.pos_y/self.scale) - ((1080/2)/self.scale))
        if center_x > 0:
            center_x = 0
        elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
            center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        if center_y > 0:
            center_y = 0
        elif center_y < -(((self.b_height*60)/self.scale)-(1080/self.scale)):
            center_y = -(((self.b_height*60)/self.scale)-(1080/self.scale))

        return center_x,center_y


    def LevelCutsceneChange(self,move):
        '''
        Parameters
        STR move - Command to change level
        '''
        self.last_move = move

        if self.level_exits[self.location[len(self.location)-1]][move][0] in self.location: #If currently not in the stack, if it is then pop, if isnt then add
            
            place = self.level_exits[self.location[len(self.location)-1]][move][0] #[Key][key][index]
            pos = self.level_exits[self.location[len(self.location)-1]][move][1]
            while True: #Until last item is new location
                
                if place != self.location[len(self.location)-1]: #If new location is not last in stack
                    
                    something = self.location[len(self.location)-1]
                    
                    self.location.pop()

                else: #If new location is last in stack, keep stack and break look
                    break

                
        else: #If place is not in stack, it is new location so add to stack
            
            pos = self.level_exits[self.location[len(self.location)-1]][move][1]
            self.location.append(self.level_exits[self.location[len(self.location)-1]][move][0]) #Add to stack

        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.level_change = True
        self.UpdateBoxAttribute()

    def RedrawBehind(self,Display,Player):
        self.WallsMethod(Display,Player)
        Player.PlayerMethod(Display,self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale,self)

    def RedrawBehindOnly(self,Display,Player):
        self.WallsMethod(Display,Player)

    def DrawBossHealthBar(self,Display,boss_name): #jumpback8
        for Enemy in self.enemies:
            if Enemy.ReturnName() == boss_name:
                hp,max_hp = Enemy.ReturnHPs()

                # 1820 center, starts 200
                bar_x = 1815//self.scale
                bar_y = 220//self.scale
                bar_width = 10//self.scale
                bar_height = 400//self.scale

                pygame.draw.rect(Display.screen, black, pygame.Rect(bar_x -4,bar_y -4,bar_width +8,bar_height +8)) #Black 4 pixel outline
                pygame.draw.rect(Display.screen, white, pygame.Rect(bar_x,bar_y,bar_width,bar_height)) #White behind missing health

                red_width_multiplier = hp / max_hp

                pygame.draw.rect(Display.screen, red, pygame.Rect(bar_x,bar_y,bar_width,bar_height*red_width_multiplier))

                tick_divider = int((max_hp/10)) #10 leaves a divider of 2, so 1 tick 1/2 way
                for Loop in range(1,tick_divider,1):
                    #print(Loop)
                    tick = bar_y +((bar_height/tick_divider)*Loop) #If 15, divider of 3 and 2 ticks so loops 1 and 2 with tick 1/3 and 2/3 the way
                    pygame.draw.rect(Display.screen, black, pygame.Rect(bar_x,tick,bar_width,2/self.scale))

                break

    def DrawItemIcon(self,Display):
        item_x = 1760/self.scale
        item_y = 80/self.scale
        item_pos = (item_x,item_y)
        item_dimentions = (int((120//self.scale)),int((120//self.scale)))
        
        pygame.draw.rect(Display.screen, black, pygame.Rect(item_x -2,item_y -2, 120/self.scale +4, 120/self.scale +4))
        pygame.draw.rect(Display.screen, white, pygame.Rect(item_x,item_y, 120/self.scale, 120/self.scale))

        if self.item_equipt == "Bombs":
            
            bomb_img = pygame.image.load("images/items/Bomb_Icon.png").convert_alpha()
            bomb_img = pygame.transform.scale(bomb_img,item_dimentions)
            Display.screen.blit(bomb_img,item_pos)

            bomb_text1 = self.small_font1.render("x"+str(self.items_dict["Bombs"]), True, black)
            bomb_textbox1 = bomb_text1.get_rect()
            bomb_textbox1.center = (1850/self.scale, 180/self.scale)

            Display.screen.blit(bomb_text1,bomb_textbox1)

        elif self.item_equipt == "Hookshot":

            hookshot_img = pygame.image.load("images/items/Hookshot_Icon.png").convert_alpha()
            hookshot_img = pygame.transform.scale(hookshot_img,item_dimentions)
            Display.screen.blit(hookshot_img,item_pos)

        elif self.item_equipt == "Bow":

            bow_img = pygame.image.load("images/items/Bow_Icon.png").convert_alpha()
            bow_img = pygame.transform.scale(bow_img,item_dimentions)
            Display.screen.blit(bow_img,item_pos)

            bow_text1 = self.small_font1.render("x"+str(self.items_dict["Arrows"]), True, black)
            bow_textbox1 = bow_text1.get_rect()
            bow_textbox1.center = (1850/self.scale, 180/self.scale)

            Display.screen.blit(bow_text1,bow_textbox1)

    def DrawIngameMenu(self,Display,mouse_pos,click1):

        pygame.draw.rect(Display.screen, black, pygame.Rect(560/self.scale -2,240/self.scale -2,800/self.scale +4,600/self.scale +4))
        pygame.draw.rect(Display.screen, light_grey, pygame.Rect(560/self.scale,240/self.scale,800/self.scale,600/self.scale))

        game_menutext1 = self.big_font1.render("Menu", True, black)
        game_menutextbox1 = game_menutext1.get_rect()
        game_menutextbox1.center = (960/self.scale,320/self.scale)

        Display.screen.blit(game_menutext1,game_menutextbox1)
        
        #self.Resume_menu = MenuButton("Resume", None,(960/self.scale,450/self.scale),menu_txt_x,menu_txt_y, black, "georgia",menu_font_size, "Game")
        #self.Save_game = MenuButton("Save Game","Save Game Confirmation",(960/self.scale,600/self.scale),menu_txt_x,menu_txt_y, black, "georgia",menu_font_size, "Game")
        #self.Back_menu = MenuButton("Main Menu", "Back Confirmation",(960/self.scale,750/self.scale),menu_txt_x,menu_txt_y, black, "georgia",menu_font_size,"Game")
        
        self.Resume_menu.Draw(mouse_pos,click1,False,Display)
        self.event = self.Resume_menu.IsOver(mouse_pos,click1,self.event,Display)

        self.Save_game.Draw(mouse_pos,click1,False,Display)
        self.event = self.Save_game.IsOver(mouse_pos,click1,self.event,Display)

        self.Back_main.Draw(mouse_pos,click1,False,Display)
        self.event = self.Back_main.IsOver(mouse_pos,click1,self.event,Display)
        
        #self.event = None #Back to game
        #self.event = "Back Confirmation" #Confirm if user wants to go back to main menu

    def DrawBackConfirmation(self,Display,mouse_pos,click1):

        pygame.draw.rect(Display.screen, black, pygame.Rect(560/self.scale -2,340/self.scale -2,800/self.scale +4,400/self.scale +4))
        pygame.draw.rect(Display.screen, off_yellow, pygame.Rect(560/self.scale,340/self.scale,800/self.scale,400/self.scale))

        backtext1 = self.big_font1.render("Are you sure?", True, black)
        backtextbox1 = backtext1.get_rect()
        backtextbox1.center = (960/self.scale,460/self.scale)

        backtext2 = self.small_font1.render("(Any unsaved data will be lost)", True, black)
        backtextbox2 = backtext2.get_rect()
        backtextbox2.center = (960/self.scale,530/self.scale)

        self.Back_menu.Draw(mouse_pos,click1,False,Display)
        self.event = self.Back_menu.IsOver(mouse_pos,click1,self.event,Display)

        self.Main_confirm.Draw(mouse_pos,click1,False,Display)
        self.event = self.Main_confirm.IsOver(mouse_pos,click1,self.event,Display)

        Display.screen.blit(backtext1,backtextbox1)
        Display.screen.blit(backtext2,backtextbox2)
    


    def DrawIngameInventory(self,Display,mouse_pos,click1):


        inventory_text1 = self.big_font1.render("Inventory", True, black)
        inventory_textbox1 = inventory_text1.get_rect()
        inventory_textbox1.center = (960/self.scale, 144/self.scale)

        pygame.draw.rect(Display.screen, black, pygame.Rect(60/self.scale -2, 60/self.scale -2, 1800/self.scale +4, 960/self.scale +4)) #Black 2 pixel outline
        pygame.draw.rect(Display.screen, old_yellow, pygame.Rect(60/self.scale, 60/self.scale, 1800/self.scale, 960/self.scale)) #Inside of big box
        

        '''Levels and EXP section'''


        inventory_text2 = self.big_font1.render("Level "+str(self.level), True, black) #Level display
        inventory_textbox2 = inventory_text2.get_rect()
        inventory_textbox2.center = (1440/self.scale, 240/self.scale)

        

        bar_width = 400/self.scale #Whole bar width
        bar_height = 30/self.scale
        bar_x = (1440/self.scale) - (bar_width/2) #1440 is centre in line with "Level #" text, so we minus half width so it stays centered no matter what width is
        bar_y = 290/self.scale
        
        inventory_text3 = self.small_font1.render(str(self.exp)+" exp", True, black) #Current exp display
        inventory_textbox3 = inventory_text3.get_rect()
        inventory_textbox3.center = (1440/self.scale - bar_width/2, 350/self.scale)

        exp_left = self.exp_cap[self.level] - self.exp #From dictioanary, determine how far away i am from level up
        exp_percent = (self.exp_cap[self.level] - exp_left) / self.exp_cap[self.level] #How much percent is that to next level

        inventory_text4 = self.small_font1.render(str(exp_left)+" exp left", True, black) #Exp needed display
        inventory_textbox4 = inventory_text4.get_rect()
        inventory_textbox4.center = (1440/self.scale + bar_width/2, 350/self.scale)


        pygame.draw.rect(Display.screen, black, pygame.Rect(bar_x -2,bar_y -2,bar_width +4,bar_height +4)) #Exp bar
        pygame.draw.rect(Display.screen, white, pygame.Rect(bar_x,bar_y,bar_width,bar_height)) #Plain width and height i determined before

        pygame.draw.rect(Display.screen, black, pygame.Rect(bar_x -2,bar_y -2,bar_width*exp_percent +4,bar_height +4)) #How much of exp bar is filled dependant on exp and max exp
        pygame.draw.rect(Display.screen, light_grey, pygame.Rect(bar_x,bar_y,bar_width*exp_percent,bar_height)) #Width * percentage (Decimal so smaller than width)



        inventory_text5 = self.small_font1.render("Skill points: "+str(self.temp_skill), True, black) #Skill points
        inventory_textbox5 = inventory_text5.get_rect()
        inventory_textbox5.center = (1440/self.scale, 420/self.scale)

        

        inventory_text6 = self.big_font1.render(":", True, black) #Skill points
        inventory_textbox6 = inventory_text6.get_rect()
        inventory_textbox6.center = (1440/self.scale, 550/self.scale)

        inventory_text7 = self.big_font1.render(":", True, black) #Skill points
        inventory_textbox7 = inventory_text7.get_rect()
        inventory_textbox7.center = (1440/self.scale, 650/self.scale)
        
        inventory_text8 = self.big_font1.render(":", True, black) #Skill points
        inventory_textbox8 = inventory_text8.get_rect()
        inventory_textbox8.center = (1440/self.scale, 750/self.scale)



        inventory_text9 = self.big_font1.render("Strength", True, black) #Skill points
        inventory_textbox9 = inventory_text9.get_rect()
        inventory_textbox9.center = (1060/self.scale + inventory_text9.get_size()[0]/2, 550/self.scale)
        #inventory_textbox9.center = (1440/self.scale, 550/self.scale)

        inventory_text10 = self.big_font1.render("Resilience", True, black) #Skill points
        inventory_textbox10 = inventory_text10.get_rect()
        inventory_textbox10.center = (1060/self.scale + inventory_text10.get_size()[0]/2, 650/self.scale)

        inventory_text11 = self.big_font1.render("Speed", True, black) #Skill points
        inventory_textbox11 = inventory_text11.get_rect()
        inventory_textbox11.center = (1060/self.scale + inventory_text11.get_size()[0]/2, 750/self.scale)

        inventory_text12 = self.big_font1.render(str(self.temp_str), True, black) #Skill points
        inventory_textbox12 = inventory_text12.get_rect()
        inventory_textbox12.center = (1640/self.scale, 550/self.scale)

        inventory_text13 = self.big_font1.render(str(self.temp_res), True, black) #Skill points
        inventory_textbox13 = inventory_text13.get_rect()
        inventory_textbox13.center = (1640/self.scale, 650/self.scale)
        
        inventory_text14 = self.big_font1.render(str(self.temp_spe), True, black) #Skill points
        inventory_textbox14 = inventory_text14.get_rect()
        inventory_textbox14.center = (1640/self.scale, 750/self.scale)


        
        Display.screen.blit(inventory_text1,inventory_textbox1) #"Inventory"
        Display.screen.blit(inventory_text2,inventory_textbox2) #"Level #"
        Display.screen.blit(inventory_text3,inventory_textbox3) #"# exp"
        Display.screen.blit(inventory_text4,inventory_textbox4) #"# exp left"
        Display.screen.blit(inventory_text5,inventory_textbox5) #"Skill points #"
        Display.screen.blit(inventory_text6,inventory_textbox6) #":"
        Display.screen.blit(inventory_text7,inventory_textbox7) #":"
        Display.screen.blit(inventory_text8,inventory_textbox8) #":"
        Display.screen.blit(inventory_text9,inventory_textbox9) #"Strength"
        Display.screen.blit(inventory_text10,inventory_textbox10) #"Resilience"
        Display.screen.blit(inventory_text11,inventory_textbox11) #"Speed"
        Display.screen.blit(inventory_text12,inventory_textbox12) #"#" Strength value
        Display.screen.blit(inventory_text13,inventory_textbox13) #"#" Resilience value
        Display.screen.blit(inventory_text14,inventory_textbox14) #"#" Speed value



        if self.temp_skill > 0: #If the user has skill points
            if self.temp_str < 5: #Level 5 skills for now
                self.Str_add.Draw(mouse_pos,click1,False,Display) #"+" for strength
                self.event = self.Str_add.IsOver(mouse_pos,click1,self.event,Display)

            if self.temp_res < 5:
                self.Res_add.Draw(mouse_pos,click1,False,Display) #"+" for resilience
                self.event = self.Res_add.IsOver(mouse_pos,click1,self.event,Display)

            if self.temp_spe < 5:
                self.Spe_add.Draw(mouse_pos,click1,False,Display) #"+" for speed
                self.event = self.Spe_add.IsOver(mouse_pos,click1,self.event,Display)

        if self.temp_str > self.strength: #"-" for strength #Does not let you go below confirmed level
            self.Str_deduct.Draw(mouse_pos,click1,False,Display)
            self.event = self.Str_deduct.IsOver(mouse_pos,click1,self.event,Display)

        if self.temp_res > self.resilience: #"-" for resilience
            self.Res_deduct.Draw(mouse_pos,click1,False,Display)
            self.event = self.Res_deduct.IsOver(mouse_pos,click1,self.event,Display)

        if self.temp_spe > self.speed: #"-" for speed
            self.Spe_deduct.Draw(mouse_pos,click1,False,Display)
            self.event = self.Spe_deduct.IsOver(mouse_pos,click1,self.event,Display)


        if self.temp_skill != self.skill_points:
            self.Confirm_SP.Draw(mouse_pos,click1,False,Display)
            self.event = self.Confirm_SP.IsOver(mouse_pos,click1,self.event,Display)


        '''Items section'''


        pygame.draw.rect(Display.screen, black, pygame.Rect(120/self.scale -2, 220/self.scale -2, 780/self.scale +4, 740/self.scale +4)) #Black 2 pixel outline
        pygame.draw.rect(Display.screen, white, pygame.Rect(120/self.scale, 220/self.scale, 780/self.scale, 740/self.scale))

        item_text1 = self.big_font2.render("Items", True, black) #Level display
        item_textbox1 = item_text1.get_rect()
        item_textbox1.center = (250/self.scale, 280/self.scale)

        item_text2 = self.small_font1.render("Key Items:", True, black) #Level display
        item_textbox2 = item_text2.get_rect()
        item_textbox2.center = (600/self.scale, 280/self.scale)


        #items = {"Sword":False,"Shield":False,"Torch":False,"Bombs":False,"Hookshot":False,"Bow":False} #If the user has obtained these items
        #items_dict = {"Bombs":False,"Bow":False,"Keys":False}
        item_dimentions = (int((120//self.scale)),int((120//self.scale)))
        

        sword_x = 210/self.scale
        sword_y = 400/self.scale

        pygame.draw.rect(Display.screen, black, pygame.Rect(sword_x -2, sword_y -2, 120/self.scale +4, 120/self.scale +4))   
        
        if self.items["Sword"] == True:

            sword_text1 = self.small_font1.render(self.sword_button, True, black) #Skill points
            sword_textbox1 = sword_text1.get_rect()
            sword_textbox1.center = (270/self.scale, 370/self.scale)

            sword_text2 = self.small_font1.render("Sword", True, black) #Skill points
            sword_textbox2 = sword_text2.get_rect()
            sword_textbox2.center = (270/self.scale,550/self.scale)
            
            pygame.draw.rect(Display.screen, old_yellow, pygame.Rect(sword_x, sword_y, 120/self.scale, 120/self.scale))
            sword_img = pygame.image.load("images/items/Sword_Icon.png").convert_alpha()
            #self.dimentions = (int((60//scale)),int((60//scale)))
            sword_img = pygame.transform.scale(sword_img,item_dimentions)
            #width,height = sword_img.get_size()
            sword_pos = (sword_x,sword_y)
            Display.screen.blit(sword_img,sword_pos)

            Display.screen.blit(sword_text1,sword_textbox1)
            Display.screen.blit(sword_text2,sword_textbox2)
            
        else:
            pygame.draw.rect(Display.screen, light_grey, pygame.Rect(sword_x, sword_y, 120/self.scale, 120/self.scale))

        bomb_x = 450/self.scale
        bomb_y = 400/self.scale

        pygame.draw.rect(Display.screen, black, pygame.Rect(bomb_x -2, bomb_y -2, 120/self.scale +4, 120/self.scale +4))

        if self.items["Bombs"] == True:

            bomb_text1 = self.small_font1.render(self.item_button, True, black)
            bomb_textbox1 = bomb_text1.get_rect()
            bomb_textbox1.center = (510/self.scale, 370/self.scale)
            
            bomb_text2 = self.small_font1.render("Bombs", True, black)
            bomb_textbox2 = bomb_text2.get_rect()
            bomb_textbox2.center = (510/self.scale, 550/self.scale)
            
            bomb_text3 = self.small_font1.render("x"+str(self.items_dict["Bombs"]), True, black)
            bomb_textbox3 = bomb_text3.get_rect()
            bomb_textbox3.center = (540/self.scale, 500/self.scale)
            
            if self.item_equipt == "Bombs":
                pygame.draw.rect(Display.screen, old_yellow, pygame.Rect(bomb_x, bomb_y, 120/self.scale, 120/self.scale))
            else:
                pygame.draw.rect(Display.screen, white, pygame.Rect(bomb_x, bomb_y, 120/self.scale, 120/self.scale))
            bomb_img = pygame.image.load("images/items/Bomb_Icon.png").convert_alpha()
            bomb_img = pygame.transform.scale(bomb_img,item_dimentions)
            bomb_pos = (bomb_x,bomb_y)
            Display.screen.blit(bomb_img,bomb_pos)
            
            Display.screen.blit(bomb_text1,bomb_textbox1)
            Display.screen.blit(bomb_text2,bomb_textbox2)
            Display.screen.blit(bomb_text3,bomb_textbox3)

            self.Bombs.Draw(mouse_pos,click1,False,Display)
            self.item_equipt = self.Bombs.IsOver(mouse_pos,click1,self.item_equipt,Display)
            
        else:
            pygame.draw.rect(Display.screen, light_grey, pygame.Rect(bomb_x,bomb_y, 120/self.scale, 120/self.scale))
            

        hookshot_x = 450/self.scale
        hookshot_y = 580/self.scale

        pygame.draw.rect(Display.screen, black, pygame.Rect(hookshot_x -2,hookshot_y -2, 120/self.scale +4, 120/self.scale +4))

        if self.items["Hookshot"] == True:
            
            hookshot_text1 = self.small_font1.render("Hookshot", True, black)
            hookshot_textbox1 = hookshot_text1.get_rect()
            hookshot_textbox1.center = (510/self.scale, 730/self.scale)
            
            if self.item_equipt == "Hookshot":
                pygame.draw.rect(Display.screen, old_yellow, pygame.Rect(hookshot_x,hookshot_y, 120/self.scale, 120/self.scale))
            else:
                pygame.draw.rect(Display.screen, white, pygame.Rect(hookshot_x,hookshot_y, 120/self.scale, 120/self.scale))
            hookshot_img = pygame.image.load("images/items/Hookshot_Icon.png").convert_alpha()
            hookshot_img = pygame.transform.scale(hookshot_img,item_dimentions)
            hookshot_pos = (hookshot_x,hookshot_y)
            Display.screen.blit(hookshot_img,hookshot_pos)

            Display.screen.blit(hookshot_text1,hookshot_textbox1)

            self.Hookshot.Draw(mouse_pos,click1,False,Display)
            self.item_equipt = self.Hookshot.IsOver(mouse_pos,click1,self.item_equipt,Display)
            
        else:
            pygame.draw.rect(Display.screen, light_grey, pygame.Rect(hookshot_x,hookshot_y, 120/self.scale, 120/self.scale))

        bow_x = 450/self.scale
        bow_y = 760/self.scale

        pygame.draw.rect(Display.screen, black, pygame.Rect(bow_x -2,bow_y -2, 120/self.scale +4, 120/self.scale +4))
        
        if self.items["Bow"] == True:

            bow_text1 = self.small_font1.render("x"+str(self.items_dict["Arrows"]), True, black)
            bow_textbox1 = bow_text1.get_rect()
            bow_textbox1.center = (540/self.scale, 860/self.scale)

            bow_text2 = self.small_font1.render("Bow", True, black)
            bow_textbox2 = bow_text2.get_rect()
            bow_textbox2.center = (510/self.scale, 910/self.scale)
            
            if self.item_equipt == "Bow":
                pygame.draw.rect(Display.screen, old_yellow, pygame.Rect(bow_x,bow_y, 120/self.scale, 120/self.scale))
            else:
                pygame.draw.rect(Display.screen, white, pygame.Rect(bow_x,bow_y, 120/self.scale, 120/self.scale))
            bow_img = pygame.image.load("images/items/Bow_Icon.png").convert_alpha()
            bow_img = pygame.transform.scale(bow_img,item_dimentions)
            bow_pos = (bow_x,bow_y)
            Display.screen.blit(bow_img,bow_pos)

            Display.screen.blit(bow_text1,bow_textbox1)
            Display.screen.blit(bow_text2,bow_textbox2)

            self.Bow.Draw(mouse_pos,click1,False,Display)
            self.item_equipt = self.Bow.IsOver(mouse_pos,click1,self.item_equipt,Display)
            
        else:
            pygame.draw.rect(Display.screen, light_grey, pygame.Rect(bow_x,bow_y, 120/self.scale, 120/self.scale))

        key_item_dimentions = (int(24//self.scale),int(54//self.scale))
        
        torch_x = 690/self.scale
        torch_y = 280/self.scale
        
        if self.items["Torch"] == True:
            torch_img = pygame.image.load("images/items/Torch_Icon.png").convert_alpha()
            torch_img = pygame.transform.scale(torch_img,key_item_dimentions)
            
            torch_x = 720/self.scale
            torch_y = 280/self.scale - (torch_img.get_size()[1]/2)
            
            torch_pos = (torch_x,torch_y)
            Display.screen.blit(torch_img,torch_pos)
        

        key_img = pygame.image.load("images/items/Key_Icon.png").convert_alpha()
        key_img = pygame.transform.scale(key_img,key_item_dimentions)
        
        key_x = 790/self.scale
        key_y = 280/self.scale - (key_img.get_size()[1]/2)
        
        key_pos = (key_x,key_y)
        Display.screen.blit(key_img,key_pos)

        key_text1 = self.small_font1.render("x"+str(self.items_dict["Keys"]), True, black)
        key_textbox1 = key_text1.get_rect()
        key_textbox1.center = (830/self.scale, 290/self.scale)

        Display.screen.blit(key_text1,key_textbox1)



        Display.screen.blit(item_text1,item_textbox1)
        Display.screen.blit(item_text2,item_textbox2)
        
        self.Inventory_back.Draw(mouse_pos,click1,False,Display)
        self.event = self.Inventory_back.IsOver(mouse_pos,click1,self.event,Display)

    def DrawCloseConfirmation(self,Display,mouse_pos,click1):

        pygame.draw.rect(Display.screen, black, pygame.Rect(560/self.scale -2,340/self.scale -2,800/self.scale +4,400/self.scale +4))
        pygame.draw.rect(Display.screen, off_yellow, pygame.Rect(560/self.scale,340/self.scale,800/self.scale,400/self.scale))

        closetext1 = self.big_font1.render("Are you sure?", True, black)
        closetextbox1 = closetext1.get_rect()
        closetextbox1.center = (960/self.scale,460/self.scale)

        closetext2 = self.small_font1.render("(Any unsaved data will be lost)", True, black)
        closetextbox2 = closetext2.get_rect()
        closetextbox2.center = (960/self.scale,530/self.scale)

        self.Resume_game.Draw(mouse_pos,click1,False,Display)
        self.event = self.Resume_game.IsOver(mouse_pos,click1,self.event,Display)

        self.Close_game.Draw(mouse_pos,click1,False,Display)
        self.event = self.Close_game.IsOver(mouse_pos,click1,self.event,Display)

        Display.screen.blit(closetext1,closetextbox1)
        Display.screen.blit(closetext2,closetextbox2)

    def DrawSavedConfirmation(self,Display,mouse_pos,click1):

        pygame.draw.rect(Display.screen, black, pygame.Rect(560/self.scale -2,340/self.scale -2,800/self.scale +4,400/self.scale +4))
        pygame.draw.rect(Display.screen, off_yellow, pygame.Rect(560/self.scale,340/self.scale,800/self.scale,400/self.scale))

        savetext1 = self.big_font1.render("Are you sure?", True, black)
        savetextbox1 = savetext1.get_rect()
        savetextbox1.center = (960/self.scale,460/self.scale)

        savetext2 = self.small_font1.render("(Data will be overwritten)", True, black)
        savetextbox2 = savetext2.get_rect()
        savetextbox2.center = (960/self.scale,530/self.scale)

        self.Back_save_game.Draw(mouse_pos,click1,False,Display)
        self.event = self.Back_save_game.IsOver(mouse_pos,click1,self.event,Display)

        self.Saved_game.Draw(mouse_pos,click1,False,Display)
        self.event = self.Saved_game.IsOver(mouse_pos,click1,self.event,Display)

        Display.screen.blit(savetext1,savetextbox1)
        Display.screen.blit(savetext2,savetextbox2)

    def DrawSaved(self,Display):
        
        pygame.draw.rect(Display.screen, black, pygame.Rect(760/self.scale -2,440/self.scale -2,400/self.scale +4,200/self.scale +4))
        pygame.draw.rect(Display.screen, off_yellow, pygame.Rect(760/self.scale,440/self.scale,400/self.scale,200/self.scale))

        savetext3 = self.big_font1.render("Saved!", True, black)
        savetextbox3 = savetext3.get_rect()
        savetextbox3.center = (960/self.scale,540/self.scale)

        Display.screen.blit(savetext3,savetextbox3)

        self.SaveGame()
        
        self.event = "Menu"
        pygame.display.flip()
        time.sleep(1)

    def SaveGame(self):

        self.ReinstantiateTempWalls() #Saves broken walls to database
        
        file_pointer = "Profile"+str(self.profile)
        file = open("profiles/"+str(file_pointer)+".txt","w")

        items = [self.prof_time+self.time,self.char_name,self.location,self.pos_x,self.pos_y,self.health,self.max_health,self.level,self.exp,
                 self.skill_points,self.strength,self.resilience,self.speed,self.items,self.items_dict,self.events,self.bosses,
                 self.last_location,self.last_move,self.last_overworld_x,self.last_overworld_y]
        
        for Item in items:
            write_item = ""
            if str(Item)[0] == "[":
                for Loop in Item: #List is stored as items with spaces
                    write_item = str(write_item) + str(Loop) + "  "
                    
            elif str(Item)[0] == "{":
                for Key in Item: #Dict is stored as keys and values with spaces
                    write_item = str(write_item)+ str(Key) + " " + str(Item[Key]) + " " 
            else:
                write_item = Item
            file.write(str(write_item))
            file.write("\n")

        file.close()
        
    def DrawHealth(self,Display):
        
        healthtext1 = self.small_font1.render("Health:", True, black)
        healthtextbox1 = healthtext1.get_rect()
        healthtextbox1.center = (1500/self.scale,40/self.scale)

        bar_x = 1580/self.scale
        bar_y = 25/self.scale
        bar_width = 300/self.scale
        bar_height = 30/self.scale

        pygame.draw.rect(Display.screen, black, pygame.Rect(bar_x -4,bar_y -4,bar_width +8,bar_height +8)) #Black 4 pixel outline
        pygame.draw.rect(Display.screen, white, pygame.Rect(bar_x,bar_y,bar_width,bar_height)) #White behind missing health

        red_width_multiplier = self.health / self.max_health
        
        pygame.draw.rect(Display.screen, red, pygame.Rect(bar_x,bar_y,bar_width*red_width_multiplier,bar_height)) #Actual health

        tick_divider = int((self.max_health/5)) #10 leaves a divider of 2, so 1 tick 1/2 way
        for Loop in range(1,tick_divider,1):
            #print(Loop)
            tick = bar_x +((bar_width/tick_divider)*Loop) #If 15, divider of 3 and 2 ticks so loops 1 and 2 with tick 1/3 and 2/3 the way
            pygame.draw.rect(Display.screen, black, pygame.Rect(tick,bar_y,2/self.scale,bar_height)) #Draws the tic
        
        Display.screen.blit(healthtext1,healthtextbox1)

    def LevelUpMethod(self):
        if self.exp >= self.exp_cap[self.level]: #If above cap or equal to
            if self.level < 16: #Level 16 is cap
                self.exp = self.exp - self.exp_cap[self.level] #Minuses the required level up exp 
                self.level += 1 #Adds a level
                self.skill_points += 1
                
            else:
                self.exp = self.exp_cap[self.level] #Cannot gain more exp after maxing level 16

    def UpdateBoxAttribute(self):
        file = self.ChooseWalls()
        file1 = open("levels/"+str(file)+".txt","r")
        contents = file1.read().split("\n")
        file1.close()
        contents.pop()
        self.b_width = int(len(contents[0])//3)
        self.b_height = len(contents)
        
                
    def LevelChangeDetector(self,Display,Player): #Left and right of screens right now
        '''
        Checks if player is on either end of a level and changes the level dependant on the current level and where it leads
        '''
        if self.pos_x < 0: #Detector for left side exit
            self.last_move = "Left"

            if self.die == False:
                self.GetLoc()
            else:
                self.die = False

            if self.level_exits[self.location[len(self.location)-1]]["Left"][0] in self.location: #If currently not in the stack, if it is then pop, if isnt then add
                
                place = self.level_exits[self.location[len(self.location)-1]]["Left"][0] #[Key][key][index]
                pos = self.level_exits[self.location[len(self.location)-1]]["Left"][1]
                while True: #Until last item is new location
                    
                    if place != self.location[len(self.location)-1]: #If new location is not last in stack
                        
                        something = self.location[len(self.location)-1]
                        
                        self.location.pop()

                    else: #If new location is last in stack, keep stack and break look
                        break
                    
            else: #If place is not in stack, it is new location so add to stack
                
                pos = self.level_exits[self.location[len(self.location)-1]]["Left"][1]
                self.location.append(self.level_exits[self.location[len(self.location)-1]]["Left"][0]) #Add to stack

            self.pos_x = pos[0]
            self.pos_y = pos[1]
            self.level_change = True
            self.UpdateBoxAttribute()
        elif self.pos_x > self.b_width*60: #Detector for right side exit
            self.last_move = "Right"
            
            if self.die == False:
                self.GetLoc()
            else:
                self.die = False

            if self.level_exits[self.location[len(self.location)-1]]["Right"][0] in self.location:

                place = self.level_exits[self.location[len(self.location)-1]]["Right"][0]
                pos = self.level_exits[self.location[len(self.location)-1]]["Right"][1]
                while True:
                    if place != self.location[len(self.location)-1]:
                        self.location.pop()
                    else:
                        break
            else:

                pos = self.level_exits[self.location[len(self.location)-1]]["Right"][1]
                self.location.append(self.level_exits[self.location[len(self.location)-1]]["Right"][0]) #Add to stack
            self.pos_x = pos[0]
            self.pos_y = pos[1]
            self.level_change = True
            self.UpdateBoxAttribute()

        if self.pos_y > self.b_height*60:
            if self.location[len(self.location)-1] != "Overworld":
                #pass
                self.DeathPlace(Display,Player)

    def GetLoc(self):
        self.last_location = []
        for List in range(0,len(self.location),1):
            self.last_location.append(self.location[List])

    def CheckHP(self,Display,Player):
        if self.health <= 0:
            self.DeathPlace(Display,Player)

    def DeathPlace(self,Display,Player):
        self.die = False
        self.health = self.max_health
        self.DrawDeathScreen(Display)
        if self.last_location == ['Overworld']:
            for Location in self.overworld_exits:
                if self.overworld_exits[Location][0] == self.location[len(self.location)-1]:
                    place = self.overworld_exits[Location][0]
                    pos = self.overworld_exits[Location][1]
                    self.location = self.last_location
                    self.location.append(place)
                    break
                else:
                    place = "Overworld"
                    pos = (self.last_overworld_x,self.last_overworld_y)
            if place == "Overworld":
                self.location = ["Overworld"]
            self.last_location = ["Overworld"]
            self.pos_x = pos[0]
            self.pos_y = pos[1]
            self.level_change = True
            Player.ChangeVel(0,0)
            print(self.location, self.last_location)
            
        else:
            if self.last_move == "Left": #If their last move was going left a level
                temp = []
                for item in self.last_location:
                    temp.append(item)
                self.location = self.last_location #Set new location stack to last location stack
                #This acts as entering the level again from the last location
                if self.level_exits[self.location[len(self.location)-1]]["Left"][0] in self.location: #Same level change code
                    place = self.level_exits[self.location[len(self.location)-1]]["Left"][0]
                    pos = self.level_exits[self.location[len(self.location)-1]]["Left"][1]
                    while True:
                        if place != self.location[len(self.location)-1]: #If new location is not last in stack
                            self.location.pop() #Remove from stack
                        else: #If new location is last in stack, keep stack and break look
                            break
                else: #If place is not in stack, it is new location so add to stack
                    pos = self.level_exits[self.location[len(self.location)-1]]["Left"][1]
                    self.location.append(self.level_exits[self.location[len(self.location)-1]]["Left"][0]) #Add to stack
                self.last_location = temp
                #print(self.last_location)
                self.pos_x = pos[0]
                self.pos_y = pos[1]
                self.level_change = True
                Player.ChangeVel(0,0)
                
            elif self.last_move == "Right":
                #temp = self.last_location
                temp = []
                for item in self.last_location:
                    temp.append(item)
                self.location = self.last_location
                if self.level_exits[self.location[len(self.location)-1]]["Right"][0] in self.location:
                    place = self.level_exits[self.location[len(self.location)-1]]["Right"][0]
                    pos = self.level_exits[self.location[len(self.location)-1]]["Right"][1]
                    while True:
                        if place != self.location[len(self.location)-1]:
                            self.location.pop()
                        else:
                            break
                else:
                    pos = self.level_exits[self.location[len(self.location)-1]]["Right"][1]
                    self.location.append(self.level_exits[self.location[len(self.location)-1]]["Right"][0]) #Add to stack
                self.last_location = temp
                #print("e",temp)
                #print(self.last_location)
                self.pos_x = pos[0]
                self.pos_y = pos[1]
                self.level_change = True
                Player.ChangeVel(0,0)

    def OverworldChangeDetector(self,Display,Player):
        if (self.pos_x,self.pos_y) in self.overworld_exits:
            self.level_change = True
            #self.WallsMethod(Display,Player)
            self.LoadEnemies(Display)
            if self.die == False:
                self.GetLoc()
            else:
                self.die = False
            self.location.append(self.overworld_exits[(self.pos_x,self.pos_y)][0]) #Add to stack
            pos = self.overworld_exits[(self.pos_x,self.pos_y)][1]
            self.pos_x = pos[0]
            self.pos_y = pos[1]
            #self.level_change = True

    def InputGetter(self,button,button_down,mouse,mouse_down):
        scroll = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #So only registers when pressed down once
                button_down = True
                button = pygame.key.name(event.key).upper() #Gets keyboard key and capitalises the words as that is how it is stored in the SQL file
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse inputs
                if event.button == 1:
                    mouse = "Mouse 1"
                elif event.button == 2:
                    mouse = "Mouse 3" #As middle mouse for me is mouse 3
                elif event.button == 3:
                    mouse = "Mouse 2"
                elif event.button == 4:
                    mouse = "Scroll Up"
                    scroll = True
                elif event.button == 5:
                    mouse = "Scroll Down"
                    scroll = True
                elif event.button == 6:
                    mouse = "Mouse 4"
                elif event.button == 7:
                    mouse = "Mouse 5"
                mouse_down = True
            if event.type == pygame.KEYUP:
                button_down = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            if event.type == pygame.QUIT:
                #running = False #Should be a "Are you sure" screen
                self.event = "Confirm Close"
        if button_down == False:
            button = None
        if mouse_down == False and scroll == False:
            mouse = None
        return button,button_down,mouse,mouse_down

    def InputInterpreter(self,button,button_down,mouse,mouse_down):
        command1 = None
        command2 = None
        if button in self.input_dict:
            command1 = self.input_dict[button]
        if mouse in self.input_dict:
            command2 = self.input_dict[mouse]
        return command1,command2

    def WallsMethod(self,Display,Player): #Jumptowallsmethod
        file = self.ChooseWalls()
        
        if self.level_change == True: #So file only read once per level
            self.overworld_enemies = []
            self.projectiles = []
            
            self.contents = self.ImportWalls(file)
            self.deco_contents = self.ImportDecoData(file)
            
            self.current_interactables = []
            self.current_cutscenes = []

            for interactable in self.interact_obj: #Loads interactables such as doors and signs
                if interactable.CompareLevel(self.location[len(self.location)-1]) == True:
                    self.current_interactables.append(interactable)

            for cutscene in self.cutscenetrigger: #Loads interactables such as doors and signs
                if cutscene.CompareLevel(self.location[len(self.location)-1]) == True:
                    #if cutscene.ReturnEventSen(self.events[1]) == True:
                    if self.events[self.event_dict[cutscene.ReturnEvent()]] == False:
                        if len(self.current_cutscenes) != 0:
                            for compare_cutscene in self.current_cutscenes:
                                if compare_cutscene.ReturnEvent() == cutscene.ReturnEvent():
                                    pass
                                else:
                                    self.current_cutscenes.append(cutscene)
                        else:
                            self.current_cutscenes.append(cutscene)

            #self.ReinstantiateTempWalls()
            
            self.temp_walls = []
            for Data in self.temp_data:
                if Data[0] == self.location[len(self.location)-1]: #Location of wall
                    if Data[4] == 'False': #If wall is broken, if not then create it
                        self.InstantiateTempWalls(Data[0],Data[1],Data[2],Data[3])

            for door in self.key_doors:
                if door[0] == self.location[len(self.location)-1]:
                    self.DrawKeyDoor(door)

        self.DrawWalls(self.contents,Display)
        self.DrawDeco(self.deco_contents,Display)
        self.UpdateEnemies(Display,Player)
        if len(self.temp_walls) != 0:
            self.DrawBreakables(Display,Player)
        if len(self.current_cutscenes) != 0:
            self.DrawCutsceneDependant(Display)

    def DrawKeyDoor(self,door): #(self,level,wx,wy,scale)
        temp = KeyDoor(door[0],door[1],door[2],self.scale)
        self.obj_door = temp.Append(self.obj_door)

    def UpdateKeyDoor(self,Display,Player):
        for Door in self.obj_door:
            if Door.ReturnFinished() == True:
                
                self.obj_door.remove(Door)

            else:
                Door.Draw(Display)
                Door.CalculateDoorPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                '''
                if -60 <= enemy.pos[0] <= 1981/self.scale:
                    if -60 <= enemy.pos[1] <= 1141/self.scale:
                        self.EnemiesMethod(enemy,Display,Player)
                    else:
                        enemy.CentralEnemy(self.pos_x,self.pos_y,self.b_width,self.b_height)
                        enemy.Draw(Display,self.pos_x,self.pos_y)
                else:
                    enemy.CentralEnemy(self.pos_x,self.pos_y,self.b_width,self.b_height)
                    enemy.Draw(Display,self.pos_x,self.pos_y)
                '''
        
            
    def LoadEnemies(self,Display):
        enemy_index = []
        #Below loads enemies using graph traversals
        #if self.last_location[len(self.last_location)-1] == "Overworld" or self.start_spawn == True:
        if self.last_location[len(self.last_location)-1] == "Overworld" or self.start_spawn == True:
            self.start_spawn = False
            
            current_node = self.overworld_exits[(self.pos_x,self.pos_y)][0]
            #current_node = self.location[len(self.location)-1]
            adjacency_list = SetAdjacencyList(self.level_exits)
            Nodes = DepthFirstTraversal(adjacency_list,current_node,visited=[])

            self.enemy_contents = [] #Empties
            for files in Nodes: #Nodes is list of all the levels in the graph,
                if len(self.enemy_contents) == 0:

                    self.enemy_contents = self.ImportEnemyData(self.location_dict[files])
                    for Enemy in self.ImportEnemyData(self.location_dict[files]):
                        enemy_index.append(self.location_dict[files])
                else:
                    data = self.ImportEnemyData(self.location_dict[files]) #D
                    #for Enemy in self.ImportEnemyData(self.location_dict[files]):
                    for Enemy in data:
                        enemy_index.append(self.location_dict[files])

                    if len(data) != 0:
                        #print("wjejqhkwj",data[0])
                        for Enemy in data:
                            self.enemy_contents.append(Enemy)
                        #enemy_index.append(self.location_dict[files])
            if len(self.enemy_contents) != 0:
                self.DrawEnemies(self.enemy_contents,Display,enemy_index) #Instantiates enemies

    def LoadEncounterEnemies(self,encounter_level,Display):
        contents = []
        enemy_index = []
        contents = self.ImportEnemyData(encounter_level)
        for Level in range(0,len(contents),1):
            enemy_index.append(encounter_level)
        self.DrawEnemies(contents,Display,enemy_index)

    def LoadEnemiesFromLoad(self,Display):
        enemy_index = []
        self.start_spawn = False
            
        #current_node = self.overworld_exits[(self.pos_x,self.pos_y)][0]
        current_node = self.location[len(self.location)-1]
        adjacency_list = SetAdjacencyList(self.level_exits)
        Nodes = DepthFirstTraversal(adjacency_list,current_node,visited=[])

        self.enemy_contents = [] #Empties
        for files in Nodes: #Nodes is list of all the levels in the graph,
            if len(self.enemy_contents) == 0:

                self.enemy_contents = self.ImportEnemyData(self.location_dict[files])
                for Enemy in self.ImportEnemyData(self.location_dict[files]):
                    enemy_index.append(self.location_dict[files])
            else:
                data = self.ImportEnemyData(self.location_dict[files]) #D
                #for Enemy in self.ImportEnemyData(self.location_dict[files]):
                for Enemy in data:
                    enemy_index.append(self.location_dict[files])

                if len(data) != 0:
                    #print("wjejqhkwj",data[0])
                    for Enemy in data:
                        self.enemy_contents.append(Enemy)
                    #enemy_index.append(self.location_dict[files])
        if len(self.enemy_contents) != 0:
            self.DrawEnemies(self.enemy_contents,Display,enemy_index) #Instantiates enemies
        

    def HandleInteractables(self,button,button_down,b_input,m_input,Player,Display):
        for interactable in self.current_interactables:
            if interactable.CheckCollision(self.pos_x,self.pos_y) == True:
                draw_x,draw_y = Player.ReturnPlayerPos()
                interactable.DrawInteract(draw_x,draw_y,self.scale,Display)
                if b_input == "Interact" or m_input == "Interact":
                    self.event = self.event_dict[interactable.ReturnEvent()]

    def HandleCutscenes(self,Player,Display):
        for cutscenes in self.current_cutscenes:
            if cutscenes.CheckCollision(self.pos_x,self.pos_y) == True:
                self.event = self.event_dict[cutscenes.ReturnEvent()]
                
    def OverworldWallsMethods(self,Display):
        file = self.ChooseWalls()
        self.enemies = []
        if self.level_change == True: #So file only read once per level
            self.contents = self.ImportWalls(file)
        self.DrawOverworld(self.contents,Display)

    def ChooseWalls(self):
        place = self.location[len(self.location)-1]
        file = self.location_dict[place]
        return file

    def ReturnFile(self,file_name):
        file = self.location_dict[file_name]
        return file_name

    def ImportWalls(self,file):
        '''
        #Loads the walls from a file into a list
        '''
        file1 = open("levels/"+str(file)+".txt","r")
        contents = file1.read().split("\n")
        file1.close()
        contents.pop()
        self.b_width = int(len(contents[0])//3)
        self.b_height = len(contents)
        return contents

    def ImportDecoData(self,file):
        '''
        #Loads the deco from a file into a list
        '''
        file1 = open("levels/decoration/"+str(file)+".txt","r")
        deco_contents = file1.read().split("\n")
        deco_contents.pop()
        for Loop1 in range(0,len(deco_contents),1):
            deco_contents[Loop1] = deco_contents[Loop1].split(" ") #Splits into a 2D list
        file1.close()
        return deco_contents

    def ImportEnemyData(self,file):
        '''
        #Loads the deco from a file into a list
        '''
        file1 = open("levels/enemies/"+str(file)+".txt","r")
        enemy_contents = file1.read().split("\n")
        enemy_contents.pop()
        for Loop1 in range(0,len(enemy_contents),1):
            enemy_contents[Loop1] = enemy_contents[Loop1].split(" ") #Splits into a 2D list
        file1.close()
        return enemy_contents

    def DrawDeco(self,deco_contents,Display):
        '''
        #Draws decoration
        '''
        center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Minus so camera moves right when pos_x moves up 
        center_y = -((self.pos_y/self.scale) - ((1080/2)/self.scale))
        if center_x > 0:
            center_x = 0
        elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
            center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        if center_y > 0:
            center_y = 0
        elif center_y < -(((self.b_height*60)/self.scale)-(1080/self.scale)):
            center_y = -(((self.b_height*60)/self.scale)-(1080/self.scale))
        
        if len(deco_contents) >= 1:
            x = y = 0
            decos = []
            for Loop1 in range(0,len(deco_contents),1): #For how many lines of text are in the text file
                DecoID = deco_contents[Loop1][0]
                x = int(deco_contents[Loop1][1])/self.scale + center_x ###########################
                y = int(deco_contents[Loop1][2])/self.scale + center_y
                #center_x = x - int((self.w_centre * 60/self.scale))
                #center_y = y - int((self.h_centre * 60/self.scale))
            
                temp = Deco(x,y,DecoID,self.deco_image,self.scale) #Object generation, self.deco_image is dictionary for all decoration images
                decos = temp.Append(decos)  

            for deco in decos:
                if -800 <= deco.pos[0] <= 2721/self.scale:
                    if -60 <= deco.pos[1] <= 1081/self.scale:
                        Display.screen.blit(deco.image,deco.pos)

    def DrawWalls(self,contents,Display):
        '''
        #Draws the screen using other class functions
        '''
        center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Minus so camera moves right when pos_x moves up 
        center_y = -((self.pos_y/self.scale) - ((1080/2)/self.scale))
        if center_x > 0:
            center_x = 0
        elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
            center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        if center_y > 0:
            center_y = 0
        elif center_y < -(((self.b_height*60)/self.scale)-(1080/self.scale)):
            center_y = -(((self.b_height*60)/self.scale)-(1080/self.scale))

        if self.level_change == True:
            self.level_change = False
            
            self.walls = []
            for Loop1 in range(0,self.b_height,1): #For the amount of boxes high the level is iterate
                for Loop2 in range(0,self.b_width,1):  #For the amount of boxes wide the level is iterate
                    WallID = contents[Loop1][(Loop2)*3:((Loop2)*3)+3] #Contents is the text file split into a list with each item being one line of text
                    '''
                    #temp will be overidden every time but it is ok as we
                    handle the objects when they are appended to walls
                    '''
                    temp = Wall(center_x,center_y,self.scale,WallID,self.image) #Object is created
                    self.walls = temp.Append(self.walls) #That wall is appened to the walls list attribute
                    
                    center_x += (60/self.scale)
                center_y += (60/self.scale)
                center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Next row of walls 
                if center_x > 0:
                    center_x = 0
                elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
                    center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        else: #Re-maps the wall when the level is static, no new walls just moving the current walls
            for Loop1 in range(0,self.b_height,1):
                for Loop2 in range(0,self.b_width,1):
                    self.walls[(Loop1*self.b_width)+Loop2].SetPos(center_x,center_y)
                    center_x += (60/self.scale)
                center_y += (60/self.scale)
                center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Next row of walls
                if center_x > 0:
                    center_x = 0
                elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
                    center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        for wall in self.walls:
            if -60 <= wall.pos[0] <= 1921/self.scale:
                if -60 <= wall.pos[1] <= 1081/self.scale:
                    Display.screen.blit(wall.image,wall.pos)

    def DrawOverworld(self,contents,Display):
        '''
        #Draws the screen using other class functions
        '''
        center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Minus so camera moves right when pos_x moves up 
        center_y = -((self.pos_y/self.scale) - ((1080/2)/self.scale))
        if center_x > 0:
            center_x = 0
        elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
            center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        if center_y > 0:
            center_y = 0
        elif center_y < -(((self.b_height*60)/self.scale)-(1080/self.scale)):
            center_y = -(((self.b_height*60)/self.scale)-(1080/self.scale))

        if self.level_change == True:
            self.level_change = False
            
            self.walls = []
            for Loop1 in range(0,self.b_height,1):
                for Loop2 in range(0,self.b_width,1): #
                    WallID = contents[Loop1][(Loop2)*3:((Loop2)*3)+3]
                    '''
                    #temp will be overidden every time but it is ok as we
                    handle the objects when they are appended to walls
                    '''
                    temp = Wall(center_x,center_y,self.scale,WallID,self.image)
                    self.walls = temp.Append(self.walls)
                    
                    center_x += (60/self.scale)
                center_y += (60/self.scale)
                center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Next row of walls 
                if center_x > 0:
                    center_x = 0
                elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
                    center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        else:
            for Loop1 in range(0,self.b_height,1):
                for Loop2 in range(0,self.b_width,1):
                    self.walls[(Loop1*self.b_width)+Loop2].SetPos(center_x,center_y)
                    center_x += (60/self.scale)
                center_y += (60/self.scale)
                center_x = -((self.pos_x/self.scale) - ((1920/2)/self.scale)) #Next row of walls
                if center_x > 0:
                    center_x = 0
                elif center_x < -(((self.b_width*60)/self.scale)-(1920/self.scale)):
                    center_x = -(((self.b_width*60)/self.scale)-(1920/self.scale))

        
        for wall in self.walls:
            if -60 <= wall.pos[0] <= 1921/self.scale:
                if -60 <= wall.pos[1] <= 1081/self.scale:
                    #pass
                    Display.screen.blit(wall.image,wall.pos)

    def DrawEnemies(self,enemy_contents,Display,enemy_index): #Addboss
        '''
        #Instantiates enemies
        PARAMETERS
        LIST enemy_contents - 2D list of enemies in level (make so all levels from graph traversal)
        '''
        x = y = 0
        behaviour = ""
        for Loop1 in range(0,len(enemy_contents),1): #For how many lines of text in enemy text file for that level
            

            EnemyID = enemy_contents[Loop1][0]

            x = int(enemy_contents[Loop1][1])
            y = int(enemy_contents[Loop1][2])

            Enemy = GetEnemyTableDetails(EnemyID) 
            behaviour = str(Enemy[10])
            
            if behaviour == "Stationary": #(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale)
                #temp = StaticEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.b_width,self.b_height,enemy_index[Loop1],self.scale) #Object generation
                temp = StaticEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.width_dict[enemy_index[Loop1]],self.height_dict[enemy_index[Loop1]],enemy_index[Loop1],self.scale)
            elif behaviour == "Random":
                #temp = RandomEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.b_width,self.b_height,enemy_index[Loop1],self.scale)
                #print(self.height_dict)
                #print(self.height_dict[enemy_index[Loop1]])
                temp = RandomEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.width_dict[enemy_index[Loop1]],self.height_dict[enemy_index[Loop1]],enemy_index[Loop1],self.scale)

            elif behaviour == "Chase":
                #temp = ChaseEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.b_width,self.b_height,enemy_index[Loop1],self.scale)
                temp = ChaseEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.width_dict[enemy_index[Loop1]],self.height_dict[enemy_index[Loop1]],enemy_index[Loop1],self.scale)

            elif behaviour == "Projectile":
                #temp = ProjectileEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.b_width,self.b_height,enemy_index[Loop1],self.scale) #jumpto321
                temp = ProjectileEnemy(EnemyID,x,y,self.pos_x,self.pos_y,self.width_dict[enemy_index[Loop1]],self.height_dict[enemy_index[Loop1]],enemy_index[Loop1],self.scale)
                
                #self.height[Loop] = b_height
            #temp = EnemyMaster(EnemyID,x,y,center_x,center_y,enemy_index[Loop1],self.scale) #Object generation ,name,x,y,level
            if EnemyID == "BossOrc":
                if self.bosses[0] == False:
                    self.enemies = temp.Append(self.enemies)
            elif EnemyID == "BossDemonOrc":
                if self.bosses[1] == False:
                    self.enemies = temp.Append(self.enemies)
            else:
                self.enemies = temp.Append(self.enemies)

        #Only when on level, draw, but instantiate all when in graph

    def UpdateEnemies(self,Display,Player): #jumptoenemies
        '''
        Updates enemies and calls the method to draw the enemy
        '''
        for enemy in self.enemies:
            if enemy.GetDead() == True:
                if enemy.ReturnName() == "BossOrc":
                    if enemy.ReturnDeathTick() == 0:
                        self.bosses[0] = True
                elif enemy.ReturnName() == "BossDemonOrc":
                    if enemy.ReturnDeathTick() == 0:
                        self.bosses[1] = True
                if enemy.ReturnGiveExp() == True: #If the enemy died to player or other means
                    if enemy.ReturnDeathTick() == 0:
                        self.DropChance(enemy)
                    enemy.DeathExp(Display)
                    if enemy.ReturnDeathTick() > 40:
                        #self.DropChance(enemy)
                        self.exp += enemy.ReturnExp()
                        self.enemies.remove(enemy)
                else:
                    self.enemies.remove(enemy)
            else:
                if enemy.ReturnType() == "Projectile":
                    if enemy.ReturnShoot() == True: #When enough frames have gone by, shoot will be true, and time dependant on enemy projectile in enemies database
                        name,direction,x,y,attack = enemy.ReturnEssentials()
                        #x,y = Player.ReturnPlayerPos()
                        if direction == "Left":
                            vel = -8
                        else:
                            vel = 8 #(x,y,velocity,type_projectile,scale,b_height):
                        if enemy.ReturnName() == "BossDemonOrc":
                            y = y+(60//self.scale)
                        temp = EnemyProjectile(x,y,vel,name,self.scale,self.b_height,self.b_width,attack)
                        temp.CalculateProjPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                        self.projectiles = temp.Append(self.projectiles)
                
                if enemy.level == self.location_dict[self.location[len(self.location)-1]]: #If file is same as the file of the current level, then draw stuff
                    #print(enemy.pos)
                    if -60 <= enemy.pos[0] <= 1981/self.scale:
                        if -60 <= enemy.pos[1] <= 1141/self.scale:
                            self.EnemiesMethod(enemy,Display,Player)
                        else:
                            enemy.CentralEnemy(self.pos_x,self.pos_y,self.b_width,self.b_height)
                            enemy.Draw(Display,self.pos_x,self.pos_y)
                    else:
                        enemy.CentralEnemy(self.pos_x,self.pos_y,self.b_width,self.b_height)
                        enemy.Draw(Display,self.pos_x,self.pos_y)


    def DrawDrops(self,Display,Player): #jumpback2
        for Drops in self.temp_drops:
            if Drops.CollisionCheck(Player):
                Drops.SetPickedUp()
            if Drops.ReturnGone() == True:
                self.temp_drops.remove(Drops)
            elif Drops.ReturnPickedUp() == True:
                Drops.PickedUp(Display)
                if Drops.ReturnPickedFrame() > 40:
                    self.items_dict[Drops.ReturnItem()] += 10
                    if self.items_dict[Drops.ReturnItem()] >= 30:
                        self.items_dict[Drops.ReturnItem()] = 30
                    self.temp_drops.remove(Drops)
            else:
                #Drops.CalculateDropPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                Drops.Draw(Display)
                Drops.CalculateDropPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)


    def DropChance(self,Enemy):
        rand = random.randint(1,100)
        if rand <= 20: #20% chance
            random_list = []
            if self.items["Bombs"] == True:
                random_list.append("Bombs")
            if self.items["Bow"] == True:
                random_list.append("Bow")
            if len(random_list) != 0:
                item = random.choice(random_list)
                if item == "Bombs":
                    temp = EnemyDrops(Enemy.ReturnPos()[0],Enemy.ReturnPos()[1],self.scale,"Bombs")
                    self.temp_drops = temp.Append(self.temp_drops)
                elif item == "Bow":
                    temp = EnemyDrops(Enemy.ReturnPos()[0],Enemy.ReturnPos()[1],self.scale,"Arrows")
                    self.temp_drops = temp.Append(self.temp_drops)

    def DrawBreakables(self,Display,Player):
        for Breakable in self.temp_walls:
            if Breakable.ReturnDestroyed() == True:

                index = 0
                for ListData in self.temp_data: #Removes from list
                    if ListData[0] == Breakable.ReturnDBData()[0] and ListData[1] == Breakable.ReturnDBData()[1] and ListData[2] == Breakable.ReturnDBData()[2]: #If match database
                        
                        self.temp_data[index] = (str(self.temp_data[index][0]),int(self.temp_data[index][1]),int(self.temp_data[index][2]),str(self.temp_data[index][3]),'True')
                        self.temp_walls.remove(Breakable) #Removes from list
                    index += 1

            else: #Draw
                if Breakable.ReturnBlock() == "Door":
                    Breakable.CheckOpened()

                Breakable.CalculateWallPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                Breakable.Draw(Display)

                
    def WallDictionaryCreation(self): #ChangeLevel
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

    def DecoDictionaryCreation(self):
        '''
        #All images of walls preloaded into a dictionary
        '''
        deco_image = {}
        DecoID = ""
        for Loop in range(0,30,1): #Second number for how many walls there are
            if Loop < 10:
                DecoID = "0" + "0" + str(Loop)
            else:
                DecoID = "0" + str(Loop)
            deco_image[DecoID] = pygame.image.load("images/decoration/"+DecoID+".png").convert_alpha()
        self.deco_image = deco_image

    def InputDictionaryCreation(self):
        input_dict = {}
        input_contents = self.ControlsDB.QueryTable()
        for Loop1 in input_contents:
            if Loop1[1] != "":
                input_dict[Loop1[1]] = Loop1[0]
            if Loop1[2] != "":
                input_dict[Loop1[2]] = Loop1[0]
        self.input_dict = input_dict

    def EnemiesMethod(self,enemy,Display,Player):
        '''
        PARAMETERS
        OBJ enemy - Instance of one enemy in list
        '''
        #enemy.EnemyMain()
        enemy.CentralEnemy(self.pos_x,self.pos_y,self.b_width,self.b_height)
        enemy.SwordCollide(Player)
        enemy.PlayerCollide(Player,self)
        if len(self.projectiles) != 0:
            for Proj in self.projectiles:
                if Proj.ReturnType() == "Player Bombs":
                    if Proj.ReturnExploded() == True: #jumpback10
                        enemy.BombCollide(Proj)
                elif Proj.ReturnType() == "Player Arrow":
                    enemy.ArrowCollide(Proj)
        if enemy.ReturnSpeed() != 0 or enemy.ReturnType() == "Stationary": #jumpback21
            enemy.Move(self.walls,self.level_walls,self.temp_walls)

        enemy.Border(self.b_width,self.b_height)
        enemy.Draw(Display,self.pos_x,self.pos_y)

    def ChangePos(self,pos_x,pos_y,Player):
        self.pos_x = pos_x
        self.pos_y = pos_y
        Player.CalculatePlayerPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
        return pos_x,pos_y

    def ReturnItems(self):
        return self.items

    def ResetHookshot(self):
        self.hookshot = None
        self.hook_travel = False

    def GetHit(self,hp_loss):
        self.health -= hp_loss



class PlayerClass(object):
    def __init__(self,x,y,scale):
        self.LoadPlayerModel(scale)
        self.player_x = x
        self.player_y = y
        self.scale = scale
        self.h_width = 0
        self.h_height = 0
        #self.width = 60/scale
        #self.height = 60/scale
        self.vel = 8/scale
        self.air_x_vel = 3/scale
        #self.acceleration = 4
        self.is_jump = False
        self.jump_vel = 30/scale
        #self.jump_acc = -2/scale
        self.jump_vel_cap = -30/scale
        self.is_ground = True
        self.left = False
        self.right = True
        self.walk_count = 0
        self.x_vel = self.y_vel = 0
        self.walk = 0
        self.over_walk_tic = 16
        self.over_speed = 60/self.over_walk_tic
        self.over_x_vel = self.over_y_vel = 0
        self.invul_time = 90

        self.attack_stat = 0 #(*1.5)+2
        self.speed_stat = 0

        self.stopped = False
        
        #Animation variables
        self.idle = True
        self.idle_frame = 0
        self.idle_index = 1
        self.walking = False
        self.walk_frame = 0
        self.walk_index = 1
        self.attacking = False
        self.attack_frame = 0
        self.attack_index = 1
        self.duck = False
        self.duck_frame = 0
        self.duck_index = 1
        self.duck_attack = False
        self.duck_attack_frame = 0
        self.duck_attack_index = 1
        
        self.overworld_frame = 0
        self.overworld_index = 1

        self.duck_x = 0
        self.duck_y = 0

        self.using_item = False #jumpback
        self.pulling = False

        self.Sword = Sword()

        #player = pygame.image.load("images/player/Idle1.png").convert_alpha() #For player width and height
        #self.width = player.get_size()[0] #* int(5//scale) #Hitbox
        #self.height = (player.get_size()[1]-1) #* int(5//scale)

        self.hook_original_image_1 = pygame.image.load("images/useitems/hookshot/HookshotAim1.png").convert_alpha()
        self.hook_width_1 = int(self.hook_original_image_1.get_size()[0] * 5//scale)
        self.hook_height_1 = int(self.hook_original_image_1.get_size()[1] * 5//scale)
        self.hook_original_image_1 = pygame.transform.scale(self.hook_original_image_1,(self.hook_width_1,self.hook_height_1))
        self.hook_image_1 = self.hook_original_image_1
        self.hook_rect_1 = self.hook_image_1.get_rect()

        self.hook_original_image_2 = pygame.image.load("images/useitems/hookshot/HookshotAim2.png").convert_alpha()
        self.hook_width_2 = int(self.hook_original_image_2.get_size()[0] * 5//scale)
        self.hook_height_2 = int(self.hook_original_image_2.get_size()[1] * 5//scale)
        self.hook_original_image_2 = pygame.transform.scale(self.hook_original_image_2,(self.hook_width_2,self.hook_height_2))
        self.hook_image_2 = self.hook_original_image_2
        self.hook_rect_2 = self.hook_image_2.get_rect() #jumpback9

        
        getsize = pygame.image.load("images/useitems/bow/BowPull1.png").convert_alpha()
        self.bow_width_1 = int(getsize.get_size()[0] * 5//scale)
        self.bow_height_1 = int(getsize.get_size()[1] * 5//scale)
        self.bow_original_image_1 = {}
        for Loop1 in range(1,7,1):
            self.bow_original_image_1[Loop1] = pygame.image.load("images/useitems/bow/BowPull"+str(Loop1)+".png").convert_alpha()
            self.bow_original_image_1[Loop1] = pygame.transform.scale(self.bow_original_image_1[Loop1],(self.bow_width_1,self.bow_height_1))
        self.bow_image_1 = self.bow_original_image_1[1]
        self.bow_rect_1 = self.bow_image_1.get_rect()

        getsize = pygame.image.load("images/useitems/bow/BowRelease1.png").convert_alpha()
        self.bow_width_2 = int(getsize.get_size()[0] * 5//scale)
        self.bow_height_2 = int(getsize.get_size()[1] * 5//scale)
        self.bow_original_image_2 = {}
        for Loop2 in range(1,3,1):
            self.bow_original_image_2[Loop2] = pygame.image.load("images/useitems/bow/BowRelease"+str(Loop2)+".png").convert_alpha()
            self.bow_original_image_2[Loop2] = pygame.transform.scale(self.bow_original_image_2[Loop2],(self.bow_width_2,self.bow_height_2))
        self.bow_image_2 = self.bow_original_image_2[1]
        self.bow_rect_2 = self.bow_image_2.get_rect()

        self.bow_index = 1
        self.bow_frame = 0
        self.bow_shooting = False
        self.bow_release = False


    def LoadPlayerModel(self,scale):
        
        player = pygame.image.load("images/player/IdleHitbox.png").convert_alpha() #For player width and height
        self.width = player.get_size()[0] * int(5//scale) #Hitbox
        self.height = (player.get_size()[1]-1) * int(5//scale) #Hitbox
        
        self.player_frame = {}
        
        player_list = ["Idle1","Idle2","SwordIdle1","SwordIdle2","Walk1","Walk2","Walk3","Walk4","SwordWalk1","SwordWalk2","SwordWalk3","SwordWalk4","Fall1","SwordFall1",
                       "Attack1","Attack2","Attack3","Attack4","Attack5","Attack6","Duck1","SwordDuck1","AttackDuck1","AttackDuck2","AttackDuck3","AttackDuck4","IdleHitbox",
                       "DuckHitbox","BowPullCharacter"] #All file names
        
        for Frame in player_list:
            
            self.player_frame[Frame] = pygame.image.load("images/player/"+str(Frame)+".png").convert_alpha()

            self.image_width = self.player_frame[Frame].get_size()[0] * int(5//scale)
            self.image_height = self.player_frame[Frame].get_size()[1] * int(5//scale)
            
            self.player_frame[Frame] = pygame.transform.scale(self.player_frame[Frame],(int(self.image_width),int(self.image_height))) #Scales up image


    def LoadOverworldModel(self,scale):
        
        overworld_frames = ["Overworld1","Overworld2"]
        self.overworld_image = {}

        for Frame in overworld_frames:

            self.overworld_image[Frame] = pygame.image.load("images/player/"+str(Frame)+".png").convert_alpha()
            
            self.width = 60/scale
            self.height = 60/scale

            self.overworld_image[Frame] = pygame.transform.scale(self.overworld_image[Frame],(int(self.width),int(self.height)))

    def IdleHitBox(self,scale):
        self.h_width = self.player_frame["IdleHitbox"].get_size()[0] #* int(5//scale)
        self.h_height = self.player_frame["IdleHitbox"].get_size()[1] #* int(5//scale)
        self.duck_x = 0
        self.duck_y = 0


    def DuckHitBox(self,scale):
        self.h_width = self.player_frame["DuckHitbox"].get_size()[0] #* int(5//scale)
        self.h_height = self.player_frame["DuckHitbox"].get_size()[1] #* int(5//scale)
        self.duck_x = 0
        self.duck_y = self.player_frame["IdleHitbox"].get_size()[1] - self.player_frame["DuckHitbox"].get_size()[1]
        

    def PlayerMethod(self,Display,pos_x,pos_y,b_width,b_height,scale,Game):
        #self.LoadPlayerModel(scale)
        self.CalculatePlayerPos(pos_x,pos_y,b_width,b_height,scale)
        self.Draw(Display,self.right,self.left,scale,Game)
        #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(self.pos_x,self.pos_y,10,10))

    def PlayerOverworldMethod(self,Display,pos_x,pos_y,b_width,b_height,scale):
        self.LoadOverworldModel(scale)
        self.CalculatePlayerPos(pos_x,pos_y,b_width,b_height,scale)
        self.DrawOverworldHitbox(Display)

    def CalculatePlayerPos(self,pos_x,pos_y,b_width,b_height,scale):
        '''
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #FLOAT scale - The scaling of the screen due to a smaller chosen resolution
        Calculates the player's drawn position in relation to all the parameters above
        '''
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if pos_x/scale <= half_horizontal: #(Native Res) 0-960
            self.player_x = pos_x/scale #Then draw them 0-960
        elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
            self.player_x = half_horizontal #Continually make the character in the middle
        elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
            self.player_x = half_horizontal + (pos_x/scale -(width-half_horizontal)) #Draw him on 960-1920

        if pos_y/scale <= half_vertical:
            self.player_y = pos_y/scale
        elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
            self.player_y = half_vertical
        elif pos_y/scale >= (height-half_vertical):
            self.player_y = half_vertical + (pos_y/scale -(height-half_vertical))

    def Draw(self,Display,right,left,scale,Game):
        '''
        Method that handles the different animation
        '''
        #player = pygame.image.load("images/player/Idle1.png").convert_alpha() #Make dict of all frames
        #player = pygame.transform.scale(player,(int(self.width),int(self.height)))
        self.LoadPlayerModel(scale)

        #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(self.player_x-(self.h_width/2),self.player_y-(self.h_height/2)+self.duck_y,self.h_width,self.h_height))
        
        #self.DrawSwordHitbox(Display)

        items = Game.ReturnItems()
        if self.using_item == False:
            if self.is_ground == True:
                if self.attacking == False:
                    if self.idle == True:
                        self.CalculateIdleFrame()
                        if items["Sword"] == True:
                            if self.duck == True:
                                self.DuckHitBox(scale)
                                if self.duck_attack == False:
                                    if self.left == True:
                                        frame = pygame.transform.flip(self.player_frame["SwordDuck1"],True,False) #Flips horizontally
                                        self.image_width = self.player_frame["SwordDuck1"].get_size()[0]
                                        self.image_height = self.player_frame["SwordDuck1"].get_size()[1]
                                        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                        Display.screen.blit(frame,pos)
                                    elif self.right == True:
                                        frame = self.player_frame["SwordDuck1"]
                                        self.image_width = self.player_frame["SwordDuck1"].get_size()[0]
                                        self.image_height = self.player_frame["SwordDuck1"].get_size()[1]
                                        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                        Display.screen.blit(frame,pos)
                            else:
                                self.IdleHitBox(scale)
                                if self.left == True:
                                    frame = pygame.transform.flip(self.player_frame["SwordIdle"+str(self.idle_index)],True,False) #Flips horizontally
                                    self.image_width = self.player_frame["SwordIdle"+str(self.idle_index)].get_size()[0]
                                    self.image_height = self.player_frame["SwordIdle"+str(self.idle_index)].get_size()[1]
                                    pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                    Display.screen.blit(frame,pos)
                                elif self.right == True:
                                    frame = self.player_frame["SwordIdle"+str(self.idle_index)]
                                    self.image_width = self.player_frame["SwordIdle"+str(self.idle_index)].get_size()[0]
                                    self.image_height = self.player_frame["SwordIdle"+str(self.idle_index)].get_size()[1]
                                    pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                    Display.screen.blit(frame,pos)

                        else:
                            if self.duck == True:
                                self.DuckHitBox(scale)
                                if self.left == True:
                                    frame = pygame.transform.flip(self.player_frame["Duck1"],True,False) #Flips horizontally
                                    self.image_width = self.player_frame["Duck1"].get_size()[0]
                                    self.image_height = self.player_frame["Duck1"].get_size()[1]
                                    pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                    Display.screen.blit(frame,pos)
                                elif self.right == True:
                                    frame = self.player_frame["Duck1"]
                                    self.image_width = self.player_frame["Duck1"].get_size()[0]
                                    self.image_height = self.player_frame["Duck1"].get_size()[1]
                                    pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                    Display.screen.blit(frame,pos) 
                            else:
                                self.IdleHitBox(scale)
                                if self.left == True:
                                    frame = pygame.transform.flip(self.player_frame["Idle"+str(self.idle_index)],True,False) #Flips horizontally
                                    self.image_width = self.player_frame["Idle"+str(self.idle_index)].get_size()[0]
                                    self.image_height = self.player_frame["Idle"+str(self.idle_index)].get_size()[1]
                                    pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                    Display.screen.blit(frame,pos)
                                elif self.right == True:
                                    frame = self.player_frame["Idle"+str(self.idle_index)]
                                    self.image_width = self.player_frame["Idle"+str(self.idle_index)].get_size()[0]
                                    self.image_height = self.player_frame["Idle"+str(self.idle_index)].get_size()[1]
                                    pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                    Display.screen.blit(frame,pos)

                    else:
                        self.idle_frame = 0 #If moving, reset idle frames

                    if self.walking == True:
                        self.IdleHitBox(scale)
                        self.CalculateWalkFrame()
                        if items["Sword"] == True:
                            if self.left == True:
                                frame = pygame.transform.flip(self.player_frame["SwordWalk"+str(self.walk_index)],True,False) #Flips horizontally
                                self.image_width = self.player_frame["SwordWalk"+str(self.walk_index)].get_size()[0]
                                self.image_height = self.player_frame["SwordWalk"+str(self.walk_index)].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)
                            elif self.right == True:
                                frame = self.player_frame["SwordWalk"+str(self.walk_index)]
                                self.image_width = self.player_frame["SwordWalk"+str(self.walk_index)].get_size()[0]
                                self.image_height = self.player_frame["SwordWalk"+str(self.walk_index)].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)
                        else:
                            
                            if self.left == True:
                                frame = pygame.transform.flip(self.player_frame["Walk"+str(self.walk_index)],True,False) #Flips horizontally
                                self.image_width = self.player_frame["Walk"+str(self.walk_index)].get_size()[0]
                                self.image_height = self.player_frame["Walk"+str(self.walk_index)].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)
                            elif self.right == True:
                                frame = self.player_frame["Walk"+str(self.walk_index)]
                                self.image_width = self.player_frame["Walk"+str(self.walk_index)].get_size()[0]
                                self.image_height = self.player_frame["Walk"+str(self.walk_index)].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)

                    else:
                        self.walk_frame = 0
                    
            else: #If mid air
                if items["Sword"] == True: #
                    if self.attacking == False:
                        if self.duck_attack == False:
                            self.IdleHitBox(scale)
                            if self.left == True:
                                frame = pygame.transform.flip(self.player_frame["SwordFall1"],True,False) #Flips horizontally
                                self.image_width = self.player_frame["SwordFall1"].get_size()[0]
                                self.image_height = self.player_frame["SwordFall1"].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)
                            elif self.right == True:
                                frame = self.player_frame["SwordFall1"]
                                self.image_width = self.player_frame["SwordFall1"].get_size()[0]
                                self.image_height = self.player_frame["SwordFall1"].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)

                else:       
                    if self.attacking == False:
                        if self.duck_attack == False:
                            self.IdleHitBox(scale)
                            if self.left == True:
                                frame = pygame.transform.flip(self.player_frame["Fall1"],True,False) #Flips horizontally
                                self.image_width = self.player_frame["Fall1"].get_size()[0]
                                self.image_height = self.player_frame["Fall1"].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)
                            elif self.right == True:
                                frame = self.player_frame["Fall1"]
                                self.image_width = self.player_frame["Fall1"].get_size()[0]
                                self.image_height = self.player_frame["Fall1"].get_size()[1]
                                pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                                Display.screen.blit(frame,pos)
                
                            
            if items["Sword"] == True:
                if self.attacking == True:
                    self.IdleHitBox(scale)
                    self.CalculateAttackFrame()
                    if self.left == True:
                        frame = pygame.transform.flip(self.player_frame["Attack"+str(self.attack_index)],True,False) #Flips horizontally
                        self.image_width = self.player_frame["Attack"+str(self.attack_index)].get_size()[0]
                        self.image_height = self.player_frame["Attack"+str(self.attack_index)].get_size()[1]
                        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                        Display.screen.blit(frame,pos)
                    elif self.right == True:
                        frame = self.player_frame["Attack"+str(self.attack_index)]
                        self.image_width = self.player_frame["Attack"+str(self.attack_index)].get_size()[0]
                        self.image_height = self.player_frame["Attack"+str(self.attack_index)].get_size()[1]
                        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                        Display.screen.blit(frame,pos)
                        
                elif self.duck_attack == True:
                    self.DuckHitBox(scale)
                    self.CalculateDuckAttackFrame()
                    if self.left == True:
                        frame = pygame.transform.flip(self.player_frame["AttackDuck"+str(self.duck_attack_index)],True,False) #Flips horizontally
                        self.image_width = self.player_frame["AttackDuck"+str(self.duck_attack_index)].get_size()[0]
                        self.image_height = self.player_frame["AttackDuck"+str(self.duck_attack_index)].get_size()[1]
                        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                        Display.screen.blit(frame,pos)
                    elif self.right == True:
                        frame = self.player_frame["AttackDuck"+str(self.duck_attack_index)]
                        self.image_width = self.player_frame["AttackDuck"+str(self.duck_attack_index)].get_size()[0]
                        self.image_height = self.player_frame["AttackDuck"+str(self.duck_attack_index)].get_size()[1]
                        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
                        Display.screen.blit(frame,pos)
                        
            self.DrawSwordHitbox(Display)
        #self.Sword.SetAttributes(x,y,width,height,active_frames)

    def PulledByHookshot(self,x_vel,y_vel,walls,level_walls,pos_x,pos_y,breakables,Game,Display):
        self.pulling = True
        x_vel *= 2
        y_vel *= 2
        pos_x,pos_y = Game.ChangePos(pos_x+x_vel,pos_y+y_vel,self)
        if self.Collision(walls,level_walls,0,0,breakables):
            pos_x,pos_y = Game.ChangePos(pos_x-(x_vel*2),pos_y-(y_vel*2),self)
            self.pulling = False
            self.Draw(Display,self.right,self.left,self.scale,Game)
            self.SetUsingItem(False)
            return True
        
        return False
        #Move it, if colliding, move back it, then set dead and stuff

    def DrawUseItem(self,Display,flip):
        frame = self.player_frame["BowPullCharacter"]
        self.image_width = self.player_frame["BowPullCharacter"].get_size()[0]
        self.image_height = self.player_frame["BowPullCharacter"].get_size()[1]
        pos = (self.player_x-(self.image_width/2),self.player_y-(self.image_height/2))
        #Display.screen.blit(frame,pos)
        Display.screen.blit(pygame.transform.flip(frame,flip,False),pos)

    def DrawHookshot(self,Display,mouse_pos):
        self.CalculateAngle(self.hook_rect_1.center[0],self.hook_rect_1.center[1],mouse_pos[0],mouse_pos[1])
        self.x_vel = self.y_vel = 0
        self.hook_rect_1.center = (self.player_x,self.player_y)

        rot_angle = 0
        if 90 < self.angle < 270:
            rot_angle = self.angle

        else:
            rot_angle = -self.angle     

        image = pygame.transform.rotate(self.hook_original_image_1,rot_angle)
        x, y = self.hook_rect_1.center
        rect = image.get_rect()
        rect.center = (x, y)

        if 90 < self.angle < 270:
            #image = pygame.transform.rotate(original_image,-angle)
            #Display.screen.blit(pygame.transform.flip(character_image,True,False),static)
            self.DrawUseItem(Display,True)
            Display.screen.blit(pygame.transform.flip(image,False,True),rect)
        else:
            #image = pygame.transform.rotate(original_image,angle)
            #Display.screen.blit(character_image,static)
            self.DrawUseItem(Display,False)
            Display.screen.blit(image,rect)

    def DrawHookshotLess(self,Display):
        self.hook_rect_2.center = (self.player_x,self.player_y)

        rot_angle = 0
        if 90 < self.angle < 270:
            rot_angle = self.angle

        else:
            rot_angle = -self.angle     

        image = pygame.transform.rotate(self.hook_original_image_2,rot_angle)
        x, y = self.hook_rect_2.center
        rect = image.get_rect()
        rect.center = (x, y)

        if 90 < self.angle < 270:
            #image = pygame.transform.rotate(original_image,-angle)
            #Display.screen.blit(pygame.transform.flip(character_image,True,False),static)
            self.DrawUseItem(Display,True)
            Display.screen.blit(pygame.transform.flip(image,False,True),rect)
        else:
            #image = pygame.transform.rotate(original_image,angle)
            #Display.screen.blit(character_image,static)
            self.DrawUseItem(Display,False)
            Display.screen.blit(image,rect)

    def DrawBowPull(self,Display,mouse_pos):
        self.CalculateAngle(self.bow_rect_1.center[0],self.bow_rect_1.center[1],mouse_pos[0],mouse_pos[1])
        self.x_vel = self.y_vel = 0

        self.bow_rect_1.center = (self.player_x,self.player_y)

        rot_angle = 0
        if 90 < self.angle < 270:
            rot_angle = self.angle

        else:
            rot_angle = -self.angle     

        image = pygame.transform.rotate(self.bow_original_image_1[self.bow_index],rot_angle)
        x, y = self.bow_rect_1.center
        rect = image.get_rect()
        rect.center = (x, y)

        if 90 < self.angle < 270:
            #image = pygame.transform.rotate(original_image,-angle)
            #Display.screen.blit(pygame.transform.flip(character_image,True,False),static)
            self.DrawUseItem(Display,True)
            Display.screen.blit(pygame.transform.flip(image,False,True),rect)
        else:
            #image = pygame.transform.rotate(original_image,angle)
            #Display.screen.blit(character_image,static)
            self.DrawUseItem(Display,False)
            Display.screen.blit(image,rect)

    def DrawBowLess(self,Display,mouse_pos):
        self.CalculateAngle(self.bow_rect_1.center[0],self.bow_rect_1.center[1],mouse_pos[0],mouse_pos[1])
        self.x_vel = self.y_vel = 0
        
        self.bow_rect_2.center = (self.player_x,self.player_y)

        rot_angle = 0
        if 90 < self.angle < 270:
            rot_angle = self.angle

        else:
            rot_angle = -self.angle     

        image = pygame.transform.rotate(self.bow_original_image_2[self.bow_index],rot_angle)
        x, y = self.bow_rect_2.center
        rect = image.get_rect()
        rect.center = (x, y)

        if 90 < self.angle < 270:
            #image = pygame.transform.rotate(original_image,-angle)
            #Display.screen.blit(pygame.transform.flip(character_image,True,False),static)
            self.DrawUseItem(Display,True)
            Display.screen.blit(pygame.transform.flip(image,False,True),rect)
        else:
            #image = pygame.transform.rotate(original_image,angle)
            #Display.screen.blit(character_image,static)
            self.DrawUseItem(Display,False)
            Display.screen.blit(image,rect)

    def DrawOverworldHitbox(self,Display):
        self.CalculateOverworldFrame()
        if self.left == True:
            #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(self.player_x-(self.width/2),self.player_y-(self.height/2),self.width,self.height))
            frame = pygame.transform.flip(self.overworld_image["Overworld"+str(self.overworld_index)],True,False)
            Display.screen.blit(frame,(self.player_x-(self.width/2),self.player_y-(self.height/2)))

        if self.right == True:
            #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(self.player_x-(self.width/2),self.player_y-(self.height/2),self.width,self.height))
            frame = self.overworld_image["Overworld"+str(self.overworld_index)]
            Display.screen.blit(frame,(self.player_x-(self.width/2),self.player_y-(self.height/2)))
        
        #Display.screen.blit(self.player_frame["Idle1"],pos)

    def DrawSwordHitbox(self,Display):
        if self.attacking == True:
            #self.width = player.get_size()[0] * int(5//scale) #Hitbox
            #self.height = (player.get_size()[1]-1) * int(5//scale) #Hitbox
            if self.right == True:
                self.Sword.SetAttributes(self.player_x-((14//self.scale)-((self.attack_index*5)//self.scale)),self.player_y-(10//self.scale),52//self.scale,8//self.scale,self.attack_frame)
                #pygame.draw.rect(Display.screen,red,pygame.Rect(self.player_x-((14//self.scale)-((self.attack_index*5)//self.scale)),self.player_y-(10//self.scale),52//self.scale,8//self.scale))
            elif self.left == True:
                self.Sword.SetAttributes(self.player_x-((38//self.scale)+((self.attack_index*5)//self.scale)),self.player_y-(10//self.scale),52//self.scale,8//self.scale,self.attack_frame)
                #pygame.draw.rect(Display.screen,red,pygame.Rect(self.player_x-((38//self.scale)+((self.attack_index*5)//self.scale)),self.player_y-(10//self.scale),52//self.scale,8//self.scale))
        elif self.duck_attack == True:
            if self.right == True:
                self.Sword.SetAttributes(self.player_x-((2//self.scale)-((self.duck_attack_index*5)//self.scale)),self.player_y+(22//self.scale),52//self.scale,8//self.scale,self.duck_attack_frame)
                #pygame.draw.rect(Display.screen,red,pygame.Rect(self.player_x-((2//self.scale)-((self.duck_attack_index*5)//self.scale)),self.player_y+(22//self.scale),52//self.scale,8//self.scale))
            elif self.left == True:
                self.Sword.SetAttributes(self.player_x-((50//self.scale)+((self.duck_attack_index*5)//self.scale)),self.player_y+(22//self.scale),52//self.scale,8//self.scale,self.duck_attack_frame)
                #pygame.draw.rect(Display.screen,red,pygame.Rect(self.player_x-((50//self.scale)+((self.duck_attack_index*5)//self.scale)),self.player_y+(22//self.scale),52//self.scale,8//self.scale))


    def CalculateIdleFrame(self):
        if self.idle_frame > 60: #If counter goes more than 60, reset to 1
            self.idle_frame = 1
        else:
            for Index in range(1,3,1): #Frame 1 and 2
                if self.idle_frame <= (60/2)*Index:
                    #Below 30 or below 60, breaks if below 30 and then is first frame
                    self.idle_index = Index
                    break
                
            self.idle_frame += 1


    def CalculateWalkFrame(self):
        if self.walking == True:
            if self.walk_frame > 40:
                self.walk_frame = 1
            else:
                for Index in range(1,5,1):
                    if self.walk_frame <= (40/4)*Index:
                        #Below 15 or below 30, breaks if below 30 and then is first frame
                        self.walk_index = Index
                        break

                self.walk_frame += 1
                
        else:
            self.walk_frame = 0

    def CalculateBowFrame(self):
        if self.bow_shooting == True:
            if self.bow_frame > 20:
                
                self.bow_shooting = False
                #self.bow_release = True
                #self.bow_frame = 0
                #self.bow_index = 2
                '''
                if release == True:
                    bow_frame = 1
                    shooting = False
                    release = False
                    bow_index = 0
                '''
            else:
                for Index in range(1,6,1):
                    if self.bow_frame <= (20/5)*Index:
                        self.bow_index = Index
                        break

                self.bow_frame += 1
                
        elif self.bow_release == True:
            if self.bow_frame > 20:
                #if self.bow_index == 7:
                self.bow_frame = 1
                self.bow_shooting = False
                self.bow_release = False
                self.bow_index = 2
            else:
                for Index in range(1,3,1):
                    if self.bow_frame <= (20/2)*Index:
                        self.bow_index = Index
                        break

                self.bow_frame += 1
        else:
            self.bow_frame = 0


    def CalculateAttackFrame(self):
        if self.attacking == True:
            if self.attack_frame > 20:
                self.attacking = False
                self.attack_frame = 0
                
            else:
                for Index in range(1,7,1):
                    if self.attack_frame <= (20/6)*Index:
                        #Below 15 or below 30, breaks if below 30 and then is first frame
                        self.attack_index = Index
                        break

                self.attack_frame += 1
                
        else:
            self.attack_frame = 0

    def CalculateDuckAttackFrame(self):
        if self.duck_attack == True:
            if self.duck_attack_frame > 20:
                self.duck_attack = False
                self.duck_attack_frame = 0
                
            else:
                for Index in range(1,5,1):
                    if self.duck_attack_frame <= (20/4)*Index:
                        #Below 15 or below 30, breaks if below 30 and then is first frame
                        self.duck_attack_index = Index
                        break

                self.duck_attack_frame += 1
                
        else:
            self.duck_attack_frame = 0

    def CalculateOverworldFrame(self):
        if self.overworld_frame > 60: #If counter goes more than 60, reset to 1
            self.overworld_frame = 1
        else:
            for Index in range(1,3,1): #Frame 1 and 2
                if self.overworld_frame <= (60/2)*Index:
                    #Below 30 or below 60, breaks if below 30 and then is first frame
                    self.overworld_index = Index
                    break
                
            self.overworld_frame += 1


    def PlayerLevelMove(self,walls,level_walls,pos_x,pos_y,b_input,m_input,breakables,Game):
        '''
        #LIST walls - List of every wall object on the level
        #DICT level_walls - Dictionary on whether a wall has collision properties or not
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #STR b_input - Command from button
        #STR m_input - Command from mouse
        #OBJ Game - So i can change pos_x and pos_y centrally
        '''
        if self.pulling == False:
        
            self.y_vel += 2/(self.scale**2)

            if self.using_item == False:
                if self.is_ground == True:
                    if b_input == "Move Right" or m_input == "Move Right":
                        if self.duck == False:
                            if self.Collision(walls,level_walls,self.vel,0,breakables) == False:
                                self.x_vel = self.vel+(self.speed_stat/2)
                                self.walk = 1 #Buffer
                                self.right = True
                                self.left = False
                                self.idle = False
                                self.walking = True #For animation
                                #self.move_x = self.x_vel
                            elif self.Collision(walls,level_walls,1,0,breakables) == False:
                                self.x_vel = 1
                                self.walk = 1
                                self.right = True
                                self.left = False
                                self.idle = False
                                self.walking = True
                                #self.move_x = self.x_vel
                            else:
                                self.x_vel = 0
                                     
                    elif b_input == "Move Left" or m_input == "Move Left":
                        if self.duck == False:
                            if self.Collision(walls,level_walls,-self.vel,0,breakables) == False:
                                self.x_vel = -(self.vel+(self.speed_stat/2))
                                self.walk = 1
                                self.right = False
                                self.left = True
                                self.idle = False
                                self.walking = True
                                #self.move_x = self.x_vel
                            elif self.Collision(walls,level_walls,1,0,breakables) == False:
                                self.x_vel = -1
                                self.walk = 1
                                self.right = False
                                self.left = True
                                self.idle = False
                                self.walking = True
                                #self.move_x = self.x_vel
                            else:
                                self.x_vel = 0

                    elif b_input == "Duck" or m_input == "Duck":
                        if self.duck_attack == False:
                            self.x_vel = 0
                            self.idle = True
                            self.walking = False
                            self.duck = True
                        
                    else:
                        if self.walk == 0: #1 tick delay as can only have 1 movement input
                            self.idle = True
                            self.walking = False
                            self.x_vel = 0
                            if self.duck_attack == False:
                                self.duck = False
                        self.walk = 0
                else:
                    if b_input == "Move Right" or m_input == "Move Right": #self.air_x_vel
                        if self.Collision(walls,level_walls,self.vel,0,breakables) == False:
                            if self.x_vel == 0:
                                self.x_vel = self.air_x_vel
                            elif self.x_vel == -8/self.scale -(self.speed_stat/2):
                                self.x_vel = 0
                                     
                    elif b_input == "Move Left" or m_input == "Move Left":
                        if self.Collision(walls,level_walls,-self.vel,0,breakables) == False:
                            if self.x_vel == 0:
                                self.x_vel = -self.air_x_vel
                            elif self.x_vel == 8/self.scale +(self.speed_stat/2):
                                self.x_vel = 0

                    if self.Collision(walls,level_walls,self.x_vel,0,breakables) == False:
                        pass
                    else:
                        self.x_vel = 0

                if b_input == "Attack" or m_input == "Attack":
                    if Game.items["Sword"] == True:
                        if self.duck == True:
                            if self.duck_attack == False:
                                self.idle = True
                                self.walking = False
                                self.duck_attack = True
                                
                        else:
                            if self.attacking == False:
                                self.idle = True
                                self.walking = False
                                self.attacking = True
                                #self.AttackAnimation()
          
            if self.Collision(walls,level_walls,self.x_vel,0,breakables) == False:
                pos_x,pos_y = Game.ChangePos(pos_x+self.x_vel,pos_y,self)

            if self.Collision(walls,level_walls,0,0,breakables) == True:  
                #if self.Collision(walls,level_walls,0,-self.y_vel) == True:
                pos_x,pos_y = Game.ChangePos(pos_x,pos_y-1,self)
                if self.Collision(walls,level_walls,0,0,breakables) == True:
                    pos_x,pos_y = Game.ChangePos(pos_x,pos_y-1,self)
                    if self.Collision(walls,level_walls,0,0,breakables) == True:
                        pos_x,pos_y = Game.ChangePos(pos_x,pos_y-1,self)
                        if self.Collision(walls,level_walls,0,0,breakables) == True:
                            pos_x,pos_y = Game.ChangePos(pos_x,pos_y-1,self)
                            if self.Collision(walls,level_walls,0,0,breakables) == True:
                                pos_x,pos_y = Game.ChangePos(pos_x,pos_y-1,self)
                                if self.Collision(walls,level_walls,0,0,breakables) == True:
                                    pos_x,pos_y = Game.ChangePos(pos_x,pos_y-1,self)
                                    if self.Collision(walls,level_walls,0,0,breakables) == True:
                                        pos_x,pos_y = Game.ChangePos(pos_x,pos_y+6,self)
                                        if self.Collision(walls,level_walls,0,0,breakables) == True:
                                            self.y_vel = 0

            pos_x,pos_y = Game.ChangePos(pos_x,pos_y+self.y_vel,self) #Chucks down, if not in wall reverse, then not in wall
            self.is_ground = False

            if self.Collision(walls,level_walls,0,self.y_vel,breakables) == True:
      
                self.is_ground = True
                pos_x,pos_y = Game.ChangePos(pos_x,pos_y-self.y_vel,self)
                #self.fall = self.y_vel
                self.y_vel = 0


            if self.using_item == False:     
                if b_input == "Jump" or m_input == "Jump": #Allowed to jump
                    if self.Collision(walls,level_walls,0,5,breakables) == True:
                        self.y_vel = -self.jump_vel
                        self.is_jump = True
                        self.is_ground = False
                    
            if self.y_vel < self.jump_vel_cap: #Capped fall speed
                self.y_vel = self.jump_vel_cap
   

    def PlayerOverworldMove(self,walls,overworld_walls,pos_x,pos_y,b_input,m_input,breakables,Game): #self.overworld_walls
        if self.over_walk_tic == 16: #If not mid-movement
            if b_input == "Move Right" or m_input == "Move Right":
                if self.Collision(walls,overworld_walls,60/self.scale,0,breakables) == False:
                    self.over_x_vel = self.over_speed #= 60/16, so 16 frames means 60 pixels moved
                    self.over_y_vel = 0
                    self.right = True
                    self.left = False
                else:
                    self.over_x_vel = self.over_y_vel = 0
                    
            elif b_input == "Move Left" or m_input == "Move Left":
                if self.Collision(walls,overworld_walls,-60/self.scale,0,breakables) == False:
                    self.over_x_vel = -self.over_speed
                    self.over_y_vel = 0
                    self.right = False
                    self.left = True
                else:
                    self.over_x_vel = self.over_y_vel = 0
                    
            elif b_input == "Duck" or m_input == "Duck":
                if self.Collision(walls,overworld_walls,0,60/self.scale,breakables) == False:
                    self.over_y_vel = self.over_speed
                    self.over_x_vel = 0
                else:
                    self.over_x_vel = self.over_y_vel = 0
                    
            elif b_input == "Jump" or m_input == "Jump":
                if self.Collision(walls,overworld_walls,0,-60/self.scale,breakables) == False:
                    self.over_y_vel = -self.over_speed
                    self.over_x_vel = 0
                else:
                    self.over_x_vel = self.over_y_vel = 0
            else:
                self.over_x_vel = self.over_y_vel = 0

        if self.over_walk_tic > 0: #Move 1 block takes 16 frames
            if self.over_x_vel != 0 or self.over_y_vel != 0:
                pos_x,pos_y = Game.ChangePos(pos_x+self.over_x_vel,pos_y+self.over_y_vel,self)
                self.over_walk_tic -= 1 #Counts down each frame
        else:
            self.over_walk_tic = 16 #When movement is done, reset frame counter
        if self.over_walk_tic == 16:
            self.stopped = True
        else:
            self.stopped = False

    def Collision(self,walls,level_walls,x_move,y_move,breakables):
        for wall in walls:
            if level_walls[wall.WallID] == True:                
                if self.player_y - self.height/2 + y_move < wall.pos[1] + wall.dimentions[1] and self.player_y + self.height/2 + y_move > wall.pos[1]: #Y
                    if self.player_x + self.width/2 + x_move > wall.pos[0] and self.player_x - self.width/2 + x_move < wall.pos[0] + wall.dimentions[0]: #X
                        return True

        #THEN FOR COLLISION WITH BREAKABLES, IF NOT THEN MAKE IT RETURN FALSE AFTER BOTH CHECKS
        for breakable in breakables:
            if self.player_y - self.height/2 + y_move < breakable.pos[1] + breakable.dimentions[1] and self.player_y + self.height/2 + y_move > breakable.pos[1]: #Y
                if self.player_x + self.width/2 + x_move > breakable.pos[0] and self.player_x - self.width/2 + x_move < breakable.pos[0] + breakable.dimentions[0]: #X
                    return True
                
        return False

    def CalculateAngle(self,x,y,mouse_x,mouse_y):
        '''
        Uses trigonometry from the module math to calculate the angle at which the arrow should travel at from west

        self.x = x
        mouse_x = m_x

        a = m_y - y
        b = m_x - x
        a = Opposite
        b = Adjacent
        All assuming clockwise rotation from right
        '''
        def M(number): #Modulus, makes number positive
            return (number**2)**(1/2)
    
        a = mouse_y - y
        b = mouse_x - x
        if (a == 0 and b > 0) or (a == 0 and b == 0): #>
            angle = 0
        elif b == 0 and a > 0: #^
            angle = 90
        elif a == 0 and b < 0: #<
            angle = 180
        elif b == 0 and a < 0: #v
            angle = 270
        else: #If not on any axis
            if a > 0 and b > 0:
                angle = math.degrees(math.atan(M(a)/M(b)))
            elif a > 0 and b < 0:
                angle = 90 + (90 - math.degrees(math.atan(M(a)/M(b))))
            elif a < 0 and b < 0:
                angle = 180 + math.degrees(math.atan(M(a)/M(b)))
            elif a < 0 and b > 0:
                angle = 270 + (90 - math.degrees(math.atan(M(a)/M(b))))

        self.angle = angle

    
    def ChangeVel(self,x,y):
        self.x_vel = x
        self.y_vel = y

    def DDraw(self,Display,Game):
        self.using_item = False
        self.Draw(Display,self.right,self.left,self.scale,Game)
        self.using_item = True

    def ReturnPlayerPos(self):
        return self.player_x,self.player_y

    def ReturnDuck(self):
        return self.duck

    def ReturnSword(self):
        return self.Sword

    def ReturnPos(self):
        return self.player_x,self.player_y,self.width,self.height

    def ReturnGrounded(self):
        return self.is_ground

    def ReturnDraw(self):
        return self.player_x,self.player_y,self.width,self.height

    def ReturnUsingItem(self):
        return self.using_item

    def DecreaseInvul(self):
        #if self.invul_time != 0:
        self.invul_time -= 1

    def SetUsingItem(self,boolean):
        self.using_item = boolean 

    def SetInvul(self,Game):
        Game.ResetHookshot()
        self.using_item = False
        self.invul_time = 90

    def SetBowVariables(self):
        self.bow_shooting = False
        self.bow_release = False
        self.bow_frame = 0

    def ReturnInvul(self):
        return self.invul_time

    def ReturnBowShooting(self): #jumpback10
        return self.bow_shooting

    def SetGround(self):
        self.is_ground = False

    def SetToIdle(self):
        self.idle = True
        self.walking = False

    def SetStats(self,attack_stat,speed_stat):
        self.attack_stat = attack_stat
        self.speed_stat = speed_stat

    def SetBowShooting(self,boolean):
        self.bow_shooting = boolean

    def SetBowRelease(self,boolean):
        self.bow_release = boolean

    def GetAttack(self):
        return self.attack_stat

    def GetOverworldStopped(self):
        return self.stopped

    def SetDirection(self,direction):
        if direction == "Left":
            self.left = True
            self.right = False
        elif direction == "Right":
            self.right = True
            self.left = False

class Sword:
    def __init__(self):
        self.active = False
        self.draw_x = 0
        self.draw_y = 0
        self.width = 0
        self.height = 0

    def SetAttributes(self,x,y,width,height,active_frames):
        self.active = True
        self.draw_x = x
        self.draw_y = y
        self.width = width
        self.height = height
        if active_frames > 20:
            self.active = False

    def GetActive(self):
        return self.active
    
    def GetAttributes(self):
        return self.draw_x,self.draw_y,self.width,self.height

class EnemyMaster:
    #Enemy will be instantiated here and then will be passed into different classes
    def __init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale):
        
        Enemy = GetEnemyTableDetails(name)

        self.id = int(Enemy[0])
        self.name = str(Enemy[1])
        self.attack = int(Enemy[2])
        self.hp = int(Enemy[3])
        self.max_hp = self.hp
        self.speed = int(Enemy[4])/scale
        self.exp = int(Enemy[5])
        self.idle_animation = int(Enemy[6])
        self.walk_animation = int(Enemy[7])
        self.animation_speed = int(Enemy[8])
        self.walk_animation_speed = int(Enemy[9])
        self.behaviour = str(Enemy[10])
        self.projectiles = int(Enemy[11])
        self.knockback = int(Enemy[12])

        self.scale = scale

        self.GetImageDict(scale) #Creates dictionary of image frames for the enemy along with scale them to correct size dependant on screen res

        if b_width == 32:
            self.x = x/scale + (self.width/2)/scale
        else:
            self.x = x + (self.width/2)#/scale
        if b_height == 18: #Make dict
            self.y = (y+(self.height/2))/scale
        else:
            self.y = y + (self.height/2)

        self.b_height = b_height
        self.b_width = b_width
        
        self.draw_x = x/scale
        self.draw_y = y/scale

        self.is_ground = True
        
        self.left = True
        self.right = False
        self.move_left = False
        self.move_right = False


        self.x_vel = self.y_vel = 0
        self.air_x_vel = self.speed / 1.5
        self.jump_vel_cap = 10/scale
        #Animation variables
        self.idle = True
        self.idle_frame = 0
        self.idle_index = 1
        self.walking = False
        self.walk_frame = 0
        self.walk_index = 1

        self.invul_frames = 30
        self.event_death_tick = 0
        self.give_exp = False

        self.level = level #Which level this instance of the enemy is in (file name, so 2 or 3)

        self.dead = False

        self.frame = self.idle_image[0]
        
        #self.pos = ((self.x-(self.width/2))/self.scale + self.center_x,(self.y-(self.height/2))/self.scale + self.center_y)
        self.pos = (self.draw_x-(self.width/2),self.draw_y-(self.height/2))
        #self.pos = ((self.x)/self.scale + self.center_x,(self.y)/self.scale + self.center_y)

        #Only inherits from the class with the correct behaviours
        
    def GetImageDict(self,scale):
        idle_image = {}
        walk_image = {}
        for IdleFrame in range(0,self.idle_animation,1): #To how many idle frames there are
            idle_image[IdleFrame] = pygame.image.load("images/enemies/"+self.name+"/idle/"+str(IdleFrame)+".png").convert_alpha()
            self.width = idle_image[IdleFrame].get_size()[0] // scale
            self.height = idle_image[IdleFrame].get_size()[1] // scale
            idle_image[IdleFrame] = pygame.transform.scale(idle_image[IdleFrame],(int(self.width),int(self.height)))
        for WalkFrame in range(0,self.walk_animation,1): #To how many walk frames there are
            walk_image[WalkFrame] = pygame.image.load("images/enemies/"+self.name+"/walk/"+str(WalkFrame)+".png").convert_alpha()
            walk_image[WalkFrame] = pygame.transform.scale(walk_image[WalkFrame],(int(self.width),int(self.height)))
            
        self.idle_image = idle_image
        self.walk_image = walk_image

    def Append(self,enemies):
        enemies.append(self)
        return enemies

    def CentralEnemy(self,pos_x,pos_y,b_width,b_height):
        if self.idle == True:
            self.CalculateIdleFrame()
        elif self.walking == True:
            self.CalculateWalkFrame()
        self.CalculateEnemyPos(pos_x,pos_y,b_width,b_height,self.scale)
        self.EnemyMain() 

    def SwordCollide(self,Player):
        Sword = Player.ReturnSword()
        if self.invul_frames != 0:
            self.invul_frames -= 1
        else:
            if Sword.GetActive() == True:
                x,y,width,height = Sword.GetAttributes()
                #self.GeneralCollision(self,x,y,width,height)
                if self.GeneralCollision(x,y,width,height) == True: #4 param
                    self.hp -= (int(Player.GetAttack())*1.5)+2
                    if self.hp > 0:
                        x,y,width,height = Player.ReturnPos()
                        self.invul_frames = 30
                        #self.hit = True #
                        self.is_ground = False
                        #self.move_right = True
                        self.y_vel = -16/(self.scale**2)
                        #if self.direction == "Left":
                        if x < self.draw_x:
                            self.x_vel = self.knockback
                        #elif self.direction == "Right":
                        elif x >= self.draw_x:
                            self.x_vel = -self.knockback
                    else:
                        self.give_exp = True
                        self.dead = True

    def PlayerCollide(self,Player,Game):
        #self.GeneralCollision(self,x,y,width,height)
        if Player.ReturnInvul() != 0:
            Player.DecreaseInvul()
        else:
            if self.exploded == True:
                x,y,width,height = Player.ReturnPos()
                if self.GeneralCollision(x-(width/2),y-(height/2),width,height) == True: #4 param jumpback6
                    Player.SetGround()
                    if x > self.draw_x:
                        Player.ChangeVel(15,-15) #x,y
                    elif x <= self.draw_x:
                        Player.ChangeVel(-15,-15)
                    Player.SetInvul(Game)
                    Game.GetHit(self.attack)

    def BombCollide(self,Bomb):
        if self.invul_frames != 0:
            pass
        else:
            x,y,width,height = Bomb.GetAttributes()
            #self.GeneralCollision(self,x,y,width,height)
            if self.GeneralCollision(x,y,width,height) == True: #4 param
                self.hp -= 10
                if self.hp > 0:
                    #x,y,width,height = Player.ReturnPos()
                    self.invul_frames = 30
                    #self.hit = True #
                    self.is_ground = False
                    #self.move_right = True
                    self.y_vel = -16
                    #if self.direction == "Left":
                    if x < self.draw_x:
                        self.x_vel = 9
                    #elif self.direction == "Right":
                    elif x >= self.draw_x:
                        self.x_vel = -9
                else:
                    self.give_exp = True
                    self.dead = True

    def ArrowCollide(self,Arrow): #jumpback10
        if self.invul_frames != 0:
            pass
        else:
            #x,y,width,height = Arrow.GetAttributes()
            #self.GeneralCollision(self,x,y,width,height)
            #if self.GeneralCollision(x,y,width,height) == True:
            rectangle = pygame.Rect(self.draw_x - self.width/2,self.draw_y - self.height/2,self.width,self.height)
            if rectangle.colliderect(Arrow.rect):
                self.hp -= 5
                if self.hp > 0:
                    #x,y,width,height = Player.ReturnPos()
                    self.invul_frames = 30
                    #self.hit = True #
                    self.is_ground = False
                    #self.move_right = True
                    self.y_vel = -16
                    #if self.direction == "Left":
                    if Arrow.rect.center[0] < self.draw_x:
                        self.x_vel = 9
                    #elif self.direction == "Right":
                    elif Arrow.rect.center[0] >= self.draw_x:
                        self.x_vel = -9
                else:
                    self.give_exp = True
                    self.dead = True


    def PlayerCollide(self,Player,Game):
        x,y,width,height = Player.ReturnPos()
        #self.GeneralCollision(self,x,y,width,height)
        if Player.ReturnInvul() != 0:
            Player.DecreaseInvul()
        else:
            if self.GeneralCollision(x-(width/2),y-(height/2),width,height) == True: #4 param jumpback6
                Player.SetGround()
                if x > self.draw_x:
                    Player.ChangeVel(15,-15) #x,y
                elif x <= self.draw_x:
                    Player.ChangeVel(-15,-15)
                Player.SetInvul(Game)
                Game.GetHit(self.attack)
                #def ChangePos(self,pos_x,pos_y,Player):
                #self.pos_x = pos_x
                #self.pos_y = pos_y
                #Player.CalculatePlayerPos(self.pos_x,self.pos_y,self.b_width,self.b_height,self.scale)
                #return pos_x,pos_y

    def CalculateEnemyPos(self,pos_x,pos_y,b_width,b_height,scale):
        '''
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #FLOAT scale - The scaling of the screen due to a smaller chosen resolution
        Calculates the player's drawn position in relation to all the parameters above
        '''

        #self.draw_x = self.x - pos_x
        
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if width != 1920/scale:
            if pos_x/scale <= half_horizontal: #(Native Res) 0-960
                self.draw_x = self.x/scale #Then draw them 0-960
            elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
                self.draw_x = self.x/scale - (pos_x/scale-half_horizontal) #Continually make the character in the middle
            elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
                self.draw_x = self.x/scale -(width-(half_horizontal*2)) #Draw him on 960-1920
        else:
            self.draw_x = self.x
            
        if height != 1080/scale:
            if pos_y/scale <= half_vertical:
                self.draw_y = self.y/scale
                #self.draw_y = self.y/scale - (height-(half_vertical*2))
                #print("WOAH")
            elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
                self.draw_y = self.y/scale - (pos_y/scale-half_vertical)
            elif pos_y/scale >= (height-half_vertical):
                #self.draw_y = self.y/scale
                self.draw_y = self.y/scale - (height-(half_vertical*2))

        else:
            self.draw_y = self.y
    

    def Draw(self,Display,pos_x,pos_y):
        #self.pos = ((self.x-(self.width/2))/self.scale + self.center_x,(self.y-(self.height/2))/self.scale + self.center_y)
        #self.pos = ((self.x)/self.scale + self.center_x,(self.y)/self.scale + self.center_y)

        #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(self.draw_x-(self.width/2),self.draw_y-(self.height/2),self.width,self.height))
        
        self.pos = (self.draw_x-(self.width/2),self.draw_y-(self.height/2))
        
        #self.pos = ((self.draw_x-(self.width/2))/self.scale + self.center_x,(self.draw_y-(self.height/2))/self.scale + self.center_y)
        self.Facing(pos_x,pos_y)
        Display.screen.blit(self.frame,self.pos)

    def Collision(self,walls,level_walls,x_move,y_move,breakables):
        for wall in walls:
            if level_walls[wall.WallID] == True:                
                if self.draw_y - self.height/2 + y_move < wall.pos[1] + wall.dimentions[1] and self.draw_y + self.height/2 + y_move > wall.pos[1]: #Y
                    if self.draw_x + self.width/2 + x_move > wall.pos[0] and self.draw_x - self.width/2 + x_move < wall.pos[0] + wall.dimentions[0]: #X
                        return True

        for breakable in breakables:
            if self.draw_y - self.height/2 + y_move < breakable.y + breakable.dimentions[1] and self.draw_y + self.height/2 + y_move > breakable.y: #Y
                if self.draw_x + self.width/2 + x_move > breakable.x and self.draw_x - self.width/2 + x_move < breakable.x + breakable.dimentions[0]: #X
                    return True
                
        return False

    def GeneralCollision(self,x,y,width,height):
        if self.draw_y - self.height/2 < y + height and self.draw_y + self.height/2 > y: #Y
            if self.draw_x + self.width/2 > x and self.draw_x - self.width/2 < x + width: #X
                return True
        return False

    def Move(self,walls,level_walls,breakables):
        
        self.y_vel += 2/(self.scale**2)

        if self.is_ground == True:
            if self.move_right == True and self.move_left == False:
                if self.Collision(walls,level_walls,self.speed,0,breakables) == False:
                    self.x_vel = self.speed
                    self.right = True
                    self.left = False
                    self.idle = False
                    self.walking = True #For animation
                elif self.Collision(walls,level_walls,1,0,breakables) == False:
                    self.x_vel = 1
                    self.right = True
                    self.left = False
                    self.idle = False
                    self.walking = True
                else:
                    self.x_vel = 0
                             
            elif self.move_left == True and self.move_right == False:
                if self.Collision(walls,level_walls,-self.speed,0,breakables) == False: #Find2
                    self.x_vel = -self.speed
                    self.right = False
                    self.left = True
                    self.idle = False
                    self.walking = True
                elif self.Collision(walls,level_walls,1,0,breakables) == False:
                    self.x_vel = -1
                    self.right = False
                    self.left = True
                    self.idle = False
                    self.walking = True
                else:
                    self.x_vel = 0

            else:
                self.x_vel = 0

        else:
            if self.move_right == True and self.move_left == False: #self.air_x_vel
                if self.Collision(walls,level_walls,self.speed,0,breakables) == False:
                    if self.x_vel == 0:
                        self.x_vel = self.air_x_vel
                    elif self.x_vel == -8/self.scale:
                        self.x_vel = 0
                             
            elif self.move_left == True and self.move_right == False:
                if self.Collision(walls,level_walls,-self.speed,0,breakables) == False:
                    if self.x_vel == 0:
                        self.x_vel = -self.air_x_vel
                    elif self.x_vel == 8/self.scale:
                        self.x_vel = 0

            if self.Collision(walls,level_walls,self.x_vel,0,breakables) == False:
                pass
            else:
                self.x_vel = 0
           
                
        if self.Collision(walls,level_walls,self.x_vel,0,breakables) == False:
            self.x += self.x_vel

        if self.Collision(walls,level_walls,0,0,breakables) == True:  
            #if self.Collision(walls,level_walls,0,-self.y_vel) == True:
            self.y -= 1
            if self.Collision(walls,level_walls,0,0,breakables) == True:
                self.y -= 1
                if self.Collision(walls,level_walls,0,0,breakables) == True:
                    self.y -= 1
                    if self.Collision(walls,level_walls,0,0,breakables) == True:
                        self.y -= 1
                        if self.Collision(walls,level_walls,0,0,breakables) == True:
                            self.y -= 1
                            if self.Collision(walls,level_walls,0,0,breakables) == True:
                                self.y -= 1
                                if self.Collision(walls,level_walls,0,0,breakables) == True:
                                    self.y += 6
                                    if self.Collision(walls,level_walls,0,0,breakables) == True:
                                        self.y_vel = 0

        

        self.y += self.y_vel #Chucks down, if not in wall reverse, then not in wall
        self.is_ground = False

        if self.Collision(walls,level_walls,0,self.y_vel,breakables) == True:
            
            self.is_ground = True
            self.y -= self.y_vel
            self.y_vel = 0
        
        if self.y_vel > self.jump_vel_cap: #Capped fall speed
            self.y_vel = self.jump_vel_cap

    def Border(self,b_width,b_height):
        if self.x - 60 < 0:
            self.x_vel = 0
            self.x = 60
            self.move_right = False
            self.move_left = False
        elif self.x + 60 > b_width*60:
            self.x_vel = 0
            self.x = b_width*60 - 60
            self.move_right = False
            self.move_left = False

        if self.y > b_height*60:
            self.dead = True

    def CalculateIdleFrame(self):
        if self.idle_frame > self.animation_speed: #If counter goes more than 60, reset to 1
            self.idle_frame = 1
        else:
            for Index in range(0,self.idle_animation,1):
                if self.idle_frame <= (self.animation_speed/self.idle_animation)*Index: #60 frames of 4 animations typically, so 15 frames each image frame
                    #Below 30 or below 60, breaks if below 30 and then is first frame
                    self.idle_index = Index
                    break
                
            self.idle_frame += 1


    def CalculateWalkFrame(self):
        if self.walking == True:
            if self.walk_frame > self.walk_animation_speed:
                self.walk_frame = 1
                
            else:
                for Index in range(0,self.walk_animation,1):
                    if self.walk_frame <= (self.walk_animation_speed/self.walk_animation)*Index:
                        self.walk_index = Index
                        break

                self.walk_frame += 1
                
        else: #If not walking, reset the frame counter
            self.walk_frame = 0
                    
    def DeathExp(self,Display): #jumptoexp
        if self.give_exp == True:
            self.event_death_tick += 1
            self.move_right = self.move_left = False

            font = pygame.font.SysFont("georgia", int((40-(self.event_death_tick*0.3))/self.scale))
            
            text = font.render("+"+str(self.exp)+" exp", True, black)
            text_box = text.get_rect()
            self.draw_y -= 0.5
            text_box.center = (self.draw_x,self.draw_y-50)
     
            Display.screen.blit(text,text_box)

    def SetFrame(self):
        if self.walking == True:
            self.frame = self.walk_image[self.walk_index]
        else:
            self.frame = self.idle_image[self.idle_index]

    def ReturnSpeed(self):
        return self.speed

    def ReturnHPs(self):
        return self.hp,self.max_hp

    def ReturnName(self):
        return self.name

    def ReturnType(self):
        return self.type

    def ReturnPos(self):
        return self.x,self.y

    def ReturnDeathTick(self):
        return self.event_death_tick

    def ReturnGiveExp(self):
        return self.give_exp

    def ReturnExp(self):
        return self.exp

    def GetDead(self):
        return self.dead

class StaticEnemy(EnemyMaster):
    #Class containing all the traits and methods that a static enemy would possess
    def __init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale):
        self.type = "Stationary"
        EnemyMaster.__init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale)
        self.direction = "Left" #Where the player is

    def EnemyMain(self):
        self.SetFrame()
        self.LackMove() #Never chances x velocity

    def LackMove(self):
        self.move_left = self.move_right = False

    def Facing(self,pos_x,pos_y):
        if self.x < pos_x:
            self.direction = "Right"
        else:
            self.direction = "Left"

        if self.direction == "Left":
            self.frame = pygame.transform.flip(self.frame,True,False)
        elif self.direction == "Right":
            self.frame = self.frame

class RandomEnemy(EnemyMaster):
    #Class containing all the traits and methods that a randomly moving enemy would possess
    def __init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale):
        self.type = "Random"
        EnemyMaster.__init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale)
        self.move = False
        self.move_counter = 0
        self.move_random = 100 #Will be 0-100 and move when == 1 or something

        self.direction = "Left" #Random left or right

    def EnemyMain(self):
        self.SetFrame()
        self.MoveRandom() #Random library to choose when to move left or right
        self.MoveTickCalculation() #Changes the velocity if moving left or right

    def Facing(self,pos_x,pos_y):
        if self.move_left == True:
            self.direction = "Left"
            #self.frame = pygame.transform.flip(self.frame,True,False)
            #self.frame = pygame.transform.flip(self.player_frame["SwordFall1"],True,False) #Flips horizontally
        elif self.move_right == True:
            self.direction = "Right"
            #self.frame = self.frame
            
        if self.direction == "Left":
            self.frame = pygame.transform.flip(self.frame,True,False)
        elif self.direction == "Right":
            self.frame = self.frame

    def MoveRandom(self):
        if self.move_left == False and self.move_right == False:
            if self.is_ground == True:
                self.move_random = random.randint(0,100)
                if self.move_random == 0:
                    if random.randint(0,1) == 0:
                        self.move_left = True
                        self.move_right = False
                    else:
                        self.move_right = True
                        self.move_left = False
                else:
                    self.idle = True
                    self.walking = False

    def MoveTickCalculation(self):
        if self.move_left == True or self.move_right == True:
            if self.move_counter > 100//self.speed:
                self.move_counter = 0
                self.move_left = self.move_right = False
            else:
                self.move_counter += 1


class ChaseEnemy(EnemyMaster):
    #Class containing all the traits and methods that a chasing enemy would possess
    def __init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale):
        self.type = "Chase"
        EnemyMaster.__init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale)
        self.direction = "Left" #Where player is

    def EnemyMain(self): 
        self.SetFrame()
        self.MoveTowards() #Move towards player

    def Facing(self,pos_x,pos_y):
        if self.b_width == 32:
            if self.x < pos_x/self.scale:
                self.direction = "Right"
            else:
                self.direction = "Left"
        else:
            if self.x < pos_x:
                self.direction = "Right"
            else:
                self.direction = "Left"

        if self.direction == "Left":
            self.frame = pygame.transform.flip(self.frame,True,False)
        elif self.direction == "Right":
            self.frame = self.frame

    def MoveTowards(self):
        if self.direction == "Right":
            self.move_right = True
            self.move_left = False
        elif self.direction == "Left":
            self.move_right = False
            self.move_left = True

class ProjectileEnemy(EnemyMaster): #jumpback5
    #Class containing all the traits and methods that a enemy that shoot projectiles would possess
    def __init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale):
        self.type = "Projectile"
        EnemyMaster.__init__(self,name,x,y,pos_x,pos_y,b_width,b_height,level,scale)
        self.direction = "Left"
        self.shoot = False
        self.shoot_alter = 0
        self.shoot_tick = 0
        if self.speed == 0:
            self.walking = False
        else:
            self.walking = True
        

    def EnemyMain(self):
        self.SetFrame()
        self.ShootTimer() #Timed counter to shoot
        self.MoveTowards()

    def Facing(self,pos_x,pos_y):
        if self.x < pos_x:
            self.direction = "Right"
        else:
            self.direction = "Left"

        if self.direction == "Left":
            self.frame = pygame.transform.flip(self.frame,True,False)
        elif self.direction == "Right":
            self.frame = self.frame

    def ImportProjectile(self):
        #self.proj_image = pygame.image.load("images/projectiles/"+str(self.name)+"/0.png").convert_alpha()
        return pygame.image.load("images/projectiles/"+str(self.name)+"/0.png").convert_alpha()
        

    def ShootTimer(self):
        #print(self.idle_index,self.shoot_alter,self.shoot_tick)
        if self.walking == True:
            if self.walk_index == 1:
                self.shoot_alter = 1
            if self.walk_index == 3 and self.shoot_alter == 1:
                self.shoot_tick += 1
                self.shoot_alter = 0

            if self.shoot_tick == self.projectiles: #6
                self.shoot_tick = 0
                self.shoot_alter = 1
                self.shoot = True

        else:
            if self.idle_index == 1:
                self.shoot_alter = 1
            if self.idle_index == 3 and self.shoot_alter == 1:
                self.shoot_tick += 1
                self.shoot_alter = 0

            if self.shoot_tick == self.projectiles: #6
                self.shoot_tick = 0
                self.shoot_alter = 1
                self.shoot = True

    def MoveTowards(self):
        if self.direction == "Right":
            self.move_right = True
            self.move_left = False
        elif self.direction == "Left":
            self.move_right = False
            self.move_left = True

    def ReturnShoot(self):
        return self.shoot

    def ReturnEssentials(self): #image,direction
        self.shoot = False
        return self.name,self.direction,self.x,self.y,self.attack


class Dialogue: #Used as a queue outside jumptotext
    def __init__(self,file,line,scale,Display):
        self.file = file
        self.line = line
        self.scale = scale
        self.total_width = 0
        self.max_width = 1700/scale
        self.draw = False

        self.font1 = pygame.font.SysFont("georgia", int(80/self.scale))
        self.font2 = pygame.font.SysFont("georgia", int(60/self.scale))

        self.GetText(Display)

    def Append(self,text):
        text.append(self)
        return text

    def GetText(self,Display):
        file = open("events/"+self.file+".txt","r")
        text_file = file.read()
        line_text = text_file.split("\n")[self.line]

        line_text = line_text.split(":") #List is then ["Character","All Text"]
        self.character = line_text[0]
        self.whole_text = line_text[1]
        self.text_queue = self.whole_text.split(" ")

        #print(self.assembled_text)
        #self.text_queue = self.split_text
        self.assembled_text = ""
        self.prev_assembled  = ""

        #self.DrawTextBox(Display)


    def DrawTextBox(self,Display):
        #60,1020
        pygame.draw.rect(Display.screen, black, pygame.Rect((60/self.scale) -2, (780/self.scale) -2, (1800/self.scale) +4, (240/self.scale) +4))
        pygame.draw.rect(Display.screen, white, pygame.Rect((60/self.scale), (780/self.scale), (1800/self.scale), (240/self.scale)))

    def DrawOtherBox(self,Display): #The NPC's name
        text = self.font1.render(self.character, True, black)
        text_box = text.get_rect()
        width,height = text.get_size()
        width += 100/self.scale
        text_box.center = (((1860/self.scale)-(width/2)),(690/self.scale))

        
        pygame.draw.rect(Display.screen, black, pygame.Rect((((1860/self.scale)-width)) -2, (630/self.scale) -2, (width) +4, (120/self.scale) +4))
        pygame.draw.rect(Display.screen, white, pygame.Rect((((1860/self.scale)-width)), (630/self.scale), (width), (120/self.scale)))
        
        
        Display.screen.blit(text,text_box)
        

    def DrawHeroBox(self,char_name,Display): #The player's name
        full_name = ""
        for Item in char_name:
            full_name += Item

        text = self.font1.render(full_name, True, black)
        text_box = text.get_rect()
        width,height = text.get_size()
        width += 100/self.scale
        #text_box.center = ((60+(width/2))/self.scale,(690/self.scale))
        text_box.center = (((60/self.scale)+((width)/2)),(690/self.scale))
        
        pygame.draw.rect(Display.screen, black, pygame.Rect((60/self.scale) -2, (630/self.scale) -2, (width) +4, (120/self.scale) +4))
        pygame.draw.rect(Display.screen, white, pygame.Rect((60/self.scale), (630/self.scale), (width), (120/self.scale)))


        Display.screen.blit(text,text_box)

    def Draw(self,char_name,Display):
        '''
        Important variables used
        STR self.assembled_text - Long string for one line of text
        QUEUE self.text_queue - Queue containing all words on a line of code that need to be displayed to the text box
                              - If doesnt fit in one text box, the queue is uses another text box to finish the text being displayed
        '''
        if self.character == "[Player]":
            self.DrawHeroBox(char_name,Display)
        elif self.character == "[Narrator]":
            pass
        else:
            self.DrawOtherBox(Display)

        if self.draw == False:
            self.DrawTextBox(Display)
        
        if self.assembled_text == "": #So only handles queue once and is drawn once
            #self.DrawTextBox(Display)
            for Line in range(0,2,1): #2 Lines on text currently
                self.assembled_text = ""
                self.prev_assembled = ""
                if len(self.text_queue) != 0:
                    while True:
                        
                        if len(self.text_queue) == 0: #Skip rest of while
                            break
                        
                        self.assembled_text = str(self.assembled_text) + " " + str(self.text_queue[0])

                        #print(self.assembled_text)

                        text = self.font2.render(self.assembled_text, True, black)
                        text_box = text.get_rect()
                        width,height = text.get_size()
                        #print(width)
                        
                        if width < self.max_width:
                            self.prev_assembled = self.assembled_text #If does not exceed, add to assembled
                            self.text_queue.pop(0)
                            #print(self.text_queue)
                        else:
                            drawn_text = self.font2.render(self.prev_assembled, True, black)
                            drawn_text_box = drawn_text.get_rect()
                            drawn_text_box.center = ((1920/2)/self.scale,(850/self.scale)+((Line*100)/self.scale)) #Line to go down lines
                            Display.screen.blit(drawn_text,drawn_text_box)
                            self.draw = True
                            break
                            #Draw

                        if len(self.text_queue) == 0:
                            drawn_text = self.font2.render(self.prev_assembled, True, black)
                            drawn_text_box = drawn_text.get_rect()
                            drawn_text_box.center = ((1920/2)/self.scale,(850/self.scale)+((Line*100)/self.scale)) #Line to go down lines
                            Display.screen.blit(drawn_text,drawn_text_box)
                            self.draw = True


    def EmptyAssembled(self): #When click happens, call this then draw will automatically run
        self.assembled_text = ""
        self.prev_assembled = ""

    def SetDraw(self):
        self.draw = False
                

    def ReturnLenQueue(self):
        return len(self.text_queue)
    
class Interactable: #Jumptointeract
    def __init__(self,x,y,width,height,level,event_trigger):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.event_trigger = event_trigger
        self.is_level = False #This only checks when level change is true

    def Append(self,interactable): #
        interactable.append(self)
        return interactable

    def CompareLevel(self,current_level): #Only when level change is true so runs only once
        '''
        Have 2 lists of objects, one for every interactable and one for ones that are in current level
        '''
        if current_level == self.level:
            return True
        else:
            return False

    def CheckCollision(self,pos_x,pos_y):            
        if self.y - self.height/2 < pos_y and self.y + self.height/2 > pos_y: #Y
            if self.x + self.width/2 > pos_x and self.x - self.width/2 < pos_x: #X
                return True
        return False

    def DrawInteract(self,draw_x,draw_y,scale,Display):
        font1 = pygame.font.SysFont("georgia", int(100/scale))
        text = font1.render("?", True, black)
        text_box = text.get_rect()
        text_box.center = (draw_x,draw_y-(100/scale)) #Line to go down lines
        Display.screen.blit(text,text_box)
        
    def ReturnEvent(self):
        return self.event_trigger

class CutsceneTrigger: #jumptocutscene
    def __init__(self,x,y,width,height,level,cutscene_trigger):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.cutscene_trigger = cutscene_trigger
        self.is_level = False #This only checks when level change is true

    def Append(self,cutscenetrigger): #
        cutscenetrigger.append(self)
        return cutscenetrigger

    def CompareLevel(self,current_level): #Only when level change is true so runs only once
        '''
        Have 2 lists of objects, one for every interactable and one for ones that are in current level
        '''
        if current_level == self.level:
            return True
        else:
            return False

    def CheckCollision(self,pos_x,pos_y):            
        if self.y - self.height/2 < pos_y and self.y + self.height/2 > pos_y: #Y
            if self.x + self.width/2 > pos_x and self.x - self.width/2 < pos_x: #X
                return True
        return False

    def ReturnEventSeen(self,cutscene):
        if cutscene == self.cutscene_trigger:
            return True
        else:
            return False

    def ReturnEvent(self):
        return self.cutscene_trigger


class OverworldEnemy:
    def __init__(self,pos_x,pos_y,collision_dict,scale):
        '''
        PARAMETERS:
        INT pos_x - Player's x coordinate
        INT pos_y - Player's y coordinate
        DICT collision_dict - Collision dictionary stating whether a specific tile would collide with the player/enemy on the overworld map
        INT scale - Scale factor of resolution
        '''

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.scale = scale

        valid_coords = self.GenerateStartPos(collision_dict)
        if len(valid_coords) != 0:
            self.spawn_coord = random.choice(valid_coords) #Is an index
            self.enemy_coords = ((self.spawn_coord[0]*60)+30,(self.spawn_coord[1]*60)+30) #Center of the square
        else:
            self.spawn_coord = None

        self.collision_dict = collision_dict

        self.width = 60/scale
        self.height = 60/scale

        self.over_walk_tic = 16
        self.over_speed = 60/self.over_walk_tic
        self.over_x_vel = self.over_y_vel = 0

        self.move_direction = ""
        self.animation = 1
        self.animation_index = 0

        self.collided = False
        self.remove = False

        self.map = self.ReturnMap()

        self.draw_x = ((self.enemy_coords[0] - self.pos_x) + 960)/scale #Center of box or not? Because twice center
        self.draw_y = ((self.enemy_coords[1] - self.pos_y) + 540)/scale #Maybe top left but self.enemy_coords with collision needs width/2 and stuff

        self.dimentions = (int((60//scale)),int((60//scale)))

        self.images = {} #pygame.image.load("images/blocks/"+name+".png").convert_alpha()
        self.images[1] = pygame.image.load("images/enemies/Overworld/OverworldEnemy1.png","r").convert_alpha()
        self.images[1] = pygame.transform.scale(self.images[1],self.dimentions)
        self.images[2] = pygame.image.load("images/enemies/Overworld/OverworldEnemy2.png","r").convert_alpha()
        self.images[2] = pygame.transform.scale(self.images[2],self.dimentions)

    def GenerateStartPos(self,collision_dict):
        
        player_x = int((self.pos_x-30)//60) #X index
        player_y = int((self.pos_y-30)//60) #Y index

        contents = self.ReturnMap()
        valid_coords = []
        tile_space = 6

        temp_coord = (0,0)

        while len(valid_coords) == 0: #So if there are no spawn spots in a 5 space diamond, then try 4 spaces
            for IndexX in range(-tile_space+1,tile_space,1):
                for IndexY in range(-tile_space+1,tile_space,1):
                    if (IndexX**2)**(1/2) + (IndexY**2)**(1/2) == 5: #So a diamond coordinates from player 5 moves away from player
                        temp_coord = (int(player_x+IndexX),int(player_y+IndexY))
                        tile = contents[temp_coord[1]][temp_coord[0]*3:(temp_coord[0]*3)+3] #Tile that is at that coordinate
                        if collision_dict[tile] == False:
                            valid_coords.append(temp_coord)
            tile_space -= 1

            if tile_space == 2:  #Incase there are absolutely 0, then dont freeze program
                break
            
        return valid_coords
        
        #place_x = random.randint() #With respect to empty, so random out of all valid tiles

    def ReturnMap(self):
        file = open("levels/0.txt","r")
        contents = file.read()
        contents = contents.split("\n")
        contents.pop()
        return contents

    def CalculateAnimation(self):
        if self.animation > 60: #If counter goes more than 60, reset to 1
            self.animation = 1
        else:
            for Index in range(1,3,1): #Frame 1 and 2
                if self.animation <= (60/2)*Index:
                    #Below 30 or below 60, breaks if below 30 and then is first frame
                    self.animation_index = Index
                    break
                
            self.animation += 1

    def Draw(self,Display):
        self.CalculateAnimation()
        self.draw_x = ((self.enemy_coords[0] - self.pos_x) + 960)/self.scale #Center of box or not? Because twice center
        self.draw_y = ((self.enemy_coords[1] - self.pos_y) + 540)/self.scale #Maybe top left but self.enemy_coords with collision needs width/2 and stuff

        #(self.images[self.animation])
        Display.screen.blit(self.images[self.animation_index],((self.draw_x)-30//self.scale,(self.draw_y)-30/self.scale))

        
    def Main(self):
        if self.move_direction == "":
            if self.Collision() == True:
                self.collided = True
            else:
                self.MainAlgorithm()
        if self.remove == False:
            self.Move()

    def MainAlgorithm(self): #First to determine where to go
        node_queue = self.GetValidCoords()
        adjacency_list = self.SetAdjacency(node_queue)
        distances,path = self.SetDistancesAndPaths(node_queue)

        self.Dijkstra(node_queue,adjacency_list,distances,path)

    ###1
    def Dijkstra(self,node_queue,adjacency_list,distances,path):
        current_node = (0,0)
        adjacent_nodes = []
        comparison = 0

        start_node = (int((self.enemy_coords[0]-30)//60),int((self.enemy_coords[1]-30)//60))
        end_node = (int((self.pos_x-30)//60),int((self.pos_y-30)//60)) #Where the player is currently or rounded to the nearest node if moving between two


        if (((start_node[0] - end_node[0])**2)**(1/2)) >= 7:
            self.remove = True
        elif (((start_node[1] - end_node[1])**2)**(1/2)) >= 7:
            self.remove = True
        else:
            
            distances[start_node] = 0
            node_queue = DepthFirstTraversal(adjacency_list,start_node,visited=[])

            while len(node_queue) != 0:
                current_node = node_queue.pop(0)
                if current_node == end_node:
                    break
                adjacent_nodes = adjacency_list[current_node] #All adjacent nodes
                for Node in adjacent_nodes:
                    comparison = distances[current_node] + 1 #+1 as all adjacent nodes are 1 distance
                    if comparison < distances[Node]:
                        distances[Node] = comparison
                        path[Node] = current_node
                if len(node_queue) > 2:
                    node_queue = self.MergeSort(distances,node_queue)

            next_coord = self.RecurPath(start_node,end_node,path,end_node)
            self.FindNextMove(start_node,next_coord)
            #Then method to set move left or up or wherever that is

    def RecurPath(self,start_node,end_node,path,current_node):
        '''
        Used to go through the path dictionary to determine the first move the enemy should take to reach the destination
        '''
        if path[current_node] == start_node:
            return current_node #This is the first tile to move to, so this is the place the monster should move to
        else:
            return self.RecurPath(start_node,end_node,path,path[current_node])

    def FindNextMove(self,start_node,next_coord): #Direction
        #print(start_node,next_coord)
        if start_node[0] == next_coord[0]: #If x is the same
            if start_node[1] == next_coord[1] + 1:
                self.move_direction = "Up"
            else:
                self.move_direction = "Down"
        else:
            if start_node[0] == next_coord[0] + 1: #If it is to the left
                self.move_direction = "Left"
            else:
                self.move_direction = "Right"

    def GetValidCoords(self):
        '''
        Creates a list containing every single empty space (node)
        '''
        #self.map = contents
        
        start_x = int((self.pos_x-30)//60)-7
        if start_x < 0:
            start_x = 0
        elif start_x > 127:
            start_x = 127
        start_y = int((self.pos_y-30)//60) - 7
        if start_y < 0:
            start_y = 0
        elif start_y > 127:
            start_y = 127

        row = start_x
        column = start_y

        node_queue = []
        
        for Row in range(start_x,start_x+15,1):
            row += 1
            column = start_y
            for Column in range(start_y,start_y+15,1):
                column += 1
                if self.collision_dict[self.map[Column][Row*3:(Row*3)+3]] == False:
                    node_queue.append((row-1,column-1))

        return node_queue

    def SetAdjacency(self,node_queue):
        '''
        Takes node_queue and returns every adjacent empty space to each node in a list for that key
        '''
        adjacency_list = {}
        above = (0,0)
        below = (0,0)
        right = (0,0)
        left = (0,0)
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

    def SetDistancesAndPaths(self,node_queue):
        '''
        Instantiates the dictionaries distances and path to default values
        '''
        distances = {}
        path = {}
        for Coordinate in node_queue:
            distances[Coordinate] = 10000
            path[Coordinate] = (0,0)

        return distances,path

    def MergeSort(self,distances,node_queue): #dictionary,merge_list
        '''
        List is of coordinates, but when compared uses value attributed to one coorinate taken from the (distance) dictionary
        '''
        if len(node_queue) > 1:
            mid = len(node_queue) // 2
            left_half = node_queue[:mid] #Left half of list
            right_half = node_queue[mid:] #Right half of list
            #print(left_half,right_half)
            self.MergeSort(distances,left_half) #Continually splits left half until only left with 1 item on left list
            self.MergeSort(distances,right_half) 
            i = j = k = 0
            #print(left_half,right_half)

            while i < len(left_half) and j < len(right_half): #
                if distances[left_half[i]] < distances[right_half[j]]:
                    node_queue[k] = left_half[i]
                    i += 1
                else:
                    node_queue[k] = right_half[j]
                    j += 1

                k += 1

            #Checks if left half has elements not merged (Into same value)
            while i < len(left_half):
                node_queue[k] = left_half[i]
                i += 1
                k += 1

            #Checks if right half has elements not merged
            while j < len(right_half):
                node_queue[k] = right_half[j]
                j += 1
                k += 1

            return node_queue #Nodes are now sorted according to distances

    def Move(self):
        if self.over_walk_tic == 16: #If not mid-movement
            if self.move_direction == "Right":
                self.over_x_vel = self.over_speed #= 60/16, so 16 frames means 60 pixels moved
                self.over_y_vel = 0
                    
            elif self.move_direction == "Left":
                self.over_x_vel = -self.over_speed
                self.over_y_vel = 0
  
            elif self.move_direction == "Down":
                self.over_y_vel = self.over_speed
                self.over_x_vel = 0

            elif self.move_direction == "Up":
                self.over_y_vel = -self.over_speed
                self.over_x_vel = 0

            else:
                self.over_x_vel = self.over_y_vel = 0

        if self.over_walk_tic > 0: #Move 1 block takes 16 frames
            if self.over_x_vel != 0 or self.over_y_vel != 0:
                #pos_x,pos_y = Game.ChangePos(pos_x+self.over_x_vel,pos_y+self.over_y_vel,self)
                self.enemy_coords = (self.enemy_coords[0] + self.over_x_vel,self.enemy_coords[1] + self.over_y_vel)
                #self.enemy_coords[1] = self.enemy_coords[1] + self.over_y_vel
                self.over_walk_tic -= 1 #Counts down each frame
        else:
            self.over_walk_tic = 16 #When movement is done, reset frame counter
            self.move_direction = ""

    def Collision(self):             
        if self.enemy_coords[1] - self.height/2 < self.pos_y + 30 and self.enemy_coords[1] + self.height/2 > self.pos_y - 30: #Y
            if self.enemy_coords[0] + self.width/2 > self.pos_x - 30 and self.enemy_coords[0] - self.width/2 < self.pos_x + 30: #X
                return True
        return False

    def ReturnCollided(self):
        return self.collided

    def ReturnRemoved(self):
        return self.remove

    def ChangePlayerPos(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class ProjectileObject: #Enemy spit, or arrows
    def __init__(self,x,y,velocity,type_projectile,scale,b_height,b_width):
        #self.x = x
        #self.y = y
        #self.draw_x = x
        #self.draw_y = y
        self.type_projectile = type_projectile
        self.scale = scale
        self.GetImages()
        if type_projectile != "Player Arrow":
            if b_width == 32:
                self.x = x/scale
            else:
                self.x = x #+ (self.width/2) #/scale
            self.y = y
            #print(b_height)
            '''
            if b_height == 18: #Make dict
                self.y = (y+(self.height/2))/scale
            else:
                self.y = y + (self.height/2)
            '''
        
        self.draw_x = x/scale
        self.draw_y = y/scale
        self.velocity = velocity
        self.index = 0
        self.frame = 0

        #self.pos = (self.draw_x-(self.width/2),self.draw_y-(self.height/2))
        self.pos = (self.draw_x/self.scale,self.draw_y/self.scale)
        #self.width,self.height = self.image[0].get_size()

        self.dead = False

    def Append(self,projectiles):
        projectiles.append(self)
        return projectiles

    def CalculateCenter(self,pos_x,pos_y,b_width,b_height):
        center_x = -((pos_x/self.scale) - ((1920/2)/self.scale)) #Minus so camera moves right when pos_x moves up 
        center_y = -((pos_y/self.scale) - ((1080/2)/self.scale))
        if center_x > 0:
            center_x = 0
        elif center_x < -(((b_width*60)/self.scale)-(1920/self.scale)):
            center_x = -(((b_width*60)/self.scale)-(1920/self.scale))

        if center_y > 0:
            center_y = 0
        elif center_y < -(((b_height*60)/self.scale)-(1080/self.scale)):
            center_y = -(((b_height*60)/self.scale)-(1080/self.scale))

        

        x = y = 0


        x = int(self.x)/self.scale + center_x
        y = int(self.y)/self.scale + center_y

        self.pos = (x,y)

    def CalculateProjPos(self,pos_x,pos_y,b_width,b_height,scale):
        '''
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #FLOAT scale - The scaling of the screen due to a smaller chosen resolution
        Calculates the player's drawn position in relation to all the parameters above
        '''

        #self.draw_x = self.x - pos_x
        
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if width != 1920/scale:
            if pos_x/scale <= half_horizontal: #(Native Res) 0-960
                self.draw_x = self.x/scale #Then draw them 0-960
            elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
                self.draw_x = self.x/scale - (pos_x/scale-half_horizontal) #Continually make the character in the middle
            elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
                self.draw_x = self.x/scale -(width-(half_horizontal*2)) #Draw him on 960-1920
        else:
            self.draw_x = self.x
            

        if pos_y/scale <= half_vertical:
            self.draw_y = self.y/scale
        elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
            self.draw_y = self.y/scale - (pos_y/scale-half_vertical)
        elif pos_y/scale >= (height-half_vertical):
            #self.draw_y = self.y/scale
            self.draw_y = self.y/scale - (height-(half_vertical*2))


        if self.x < 0 or self.x > b_width * 60:
            self.dead = True

        if self.y < 0 or self.y > b_height * 60:
            self.dead = True
    

    def Draw(self,Display,pos_x,pos_y):
        self.pos = (self.draw_x,self.draw_y)
        Display.screen.blit(self.image[self.index],self.pos) #jumpback

    def Move(self):
        '''
        Basic properties of movement, such as moving in the direction at self.velocity
        '''
        self.x += self.velocity

    def SetDead(self):
        self.dead = True

    def ReturnType(self):
        return self.type_projectile

    def ReturnDead(self):
        return self.dead

class PlayerArrows(ProjectileObject): #When let go on right click jumpback9
    def __init__(self,x,y,velocity,type_projectile,mouse_pos,scale,b_height,b_width,player_x,player_y):
        '''
        ProjectileObject.__init__(self,x,y,velocity,type_projectile,scale,b_height,b_width)
        
        angle = 0
        image = original_image
        rect = image.get_rect()
        rect.center = (800,500)
        mouse_pos = (0,0)
        speed = 20
        x_vel = y_vel = 0

        self.CalculateAngle(mouse_pos[0],mouse_pos[1])
        '''
        self.x = x
        self.y = y

        self.player_x = player_x
        self.player_y = player_y

        self.addx = self.addy = 0

        self.angle,self.addx,self.addy = self.CalculateAngle(mouse_pos[0],mouse_pos[1],16//scale)

        self.addx = (self.addx* 5 / scale)
        self.addy = (self.addy* 5 / scale)
        
        ProjectileObject.__init__(self,x+(self.addx),y+(self.addy),velocity,type_projectile,scale,b_height,b_width)

        self.CalculateProjPos(x,y,b_width,b_height,scale)
        
        self.imag = self.image[0]
        self.rect = self.imag.get_rect()
        self.rect.center = (self.draw_x+(self.addx),self.draw_y+(self.addy))

        self.collision_delay = 2
        #speed = 20
        #self.x_vel = self.y_vel = 0

        self.angle,self.x_vel,self.y_vel = self.CalculateAngle(mouse_pos[0],mouse_pos[1],velocity)

    def ProjMain(self,Player,Display,walls,level_walls):
        '''
        So each object can behave differently while only calling projectile.main()
        '''
        self.CalculateAnimationFrame()
        self.Move()
        if self.collision_delay == 0:
            self.Collision(Player,walls,level_walls)
        else:
            self.collision_delay -= 1

    def CalculateAnimationFrame(self):
        self.index = 0

    def GetImages(self):
        '''
        self.image = {}
        for Loop1 in range(0,1,1):
            self.image[Loop1] = pygame.image.load("images/projectiles/playerarrow/Arrow"+str(Loop1)+".png").convert_alpha()
        '''
        self.image = {}

        self.image[0] = pygame.image.load("images/projectiles/playerarrow/Arrow1.png").convert_alpha()
        self.width = int((self.image[0].get_size()[0] * 5) //self.scale)
        self.height = int((self.image[0].get_size()[1] * 5) //self.scale)
        self.image[0] = pygame.transform.scale(self.image[0],(int(self.width),int(self.height)))

    def CalculateProjPos(self,pos_x,pos_y,b_width,b_height,scale):
        '''
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #FLOAT scale - The scaling of the screen due to a smaller chosen resolution
        Calculates the player's drawn position in relation to all the parameters above
        '''

        #self.draw_x = self.x - pos_x
        
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if width != 1920/scale:
            if pos_x/scale <= half_horizontal: #(Native Res) 0-960
                self.draw_x = self.x/scale #Then draw them 0-960
            elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
                self.draw_x = self.x/scale - (pos_x/scale-half_horizontal) 
            elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
                self.draw_x = self.x/scale -(width-(half_horizontal*2)) #Draw him on 960-1920
        else:
            self.draw_x = self.x
            
        if height != 1080/scale:
            if pos_y/scale <= half_vertical:
                self.draw_y = self.y/scale
                #self.draw_y = self.y/scale - (height-(half_vertical*2))
                #print("WOAH")
            elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
                self.draw_y = self.y/scale - (pos_y/scale-half_vertical)
            elif pos_y/scale >= (height-half_vertical):
                self.draw_y = self.y/scale - (height-(half_vertical*2))
        else:
            self.draw_y = self.y



        if self.x < 0 or self.x > b_width * 60:
            self.dead = True

        if self.y < 0 or self.y > b_height * 60:
            self.dead = True


    def CalculateAngle(self,mouse_x,mouse_y,multiplier):
        '''
        Uses trigonometry from the module math to calculate the angle at which the arrow should travel at from west

        self.x = x
        mouse_x = m_x

        a = m_y - y
        b = m_x - x
        a = Opposite
        b = Adjacent
        All assuming clockwise rotation from right
        '''
        def M(number): #Modulus, makes number positive
            return (number**2)**(1/2)
    
        a = mouse_y - (self.player_y)#+self.addy)
        b = mouse_x - (self.player_x)#+self.addx)
        if (a == 0 and b > 0) or (a == 0 and b == 0): #>
            angle = 0
        elif b == 0 and a > 0: #^
            angle = 90
        elif a == 0 and b < 0: #<
            angle = 180
        elif b == 0 and a < 0: #v
            angle = 270
        else: #If not on any axis
            if a > 0 and b > 0:
                angle = math.degrees(math.atan(M(a)/M(b)))
            elif a > 0 and b < 0:
                angle = 90 + (90 - math.degrees(math.atan(M(a)/M(b))))
            elif a < 0 and b < 0:
                angle = 180 + math.degrees(math.atan(M(a)/M(b)))
            elif a < 0 and b > 0:
                angle = 270 + (90 - math.degrees(math.atan(M(a)/M(b))))

        hyp = (a**2 + b**2)**(1/2) #To help find the unit vector

        x_vel = y_vel = 0
        
        if hyp != 0:
            y_vel = (a/hyp)**2 * multiplier
            
            if a < 0:
                y_vel = -y_vel
            x_vel = (b/hyp)**2 * multiplier
            
            if b < 0:
                x_vel = -x_vel
        else:
            x_vel = y_vel = 0

        return -angle,x_vel,y_vel

    def Collision(self,Player,walls,level_walls): #Outside method, so enemy can check if colliding or with a box jumpback10
        
        #rectangle = playerframe.get_rect()
        #hit_image = pygame.transform.rotate(hitbox,angle)
        for wall in walls:
            if level_walls[wall.WallID] == True:  
                rectangle = pygame.Rect(wall.pos[0],wall.pos[1],wall.dimentions[0],wall.dimentions[1])
                if rectangle.colliderect(self.rect):
                    self.dead = True

    def Move(self):
        self.x += self.x_vel
        self.y += self.y_vel


    def Draw(self,Display,pos_x,pos_y):
        '''
        Polymorphism as for arrows it will be a full 360 directional that it could go
        '''
        self.img = pygame.transform.rotate(self.image[self.index],self.angle)
        #x, y = rect.center
        #x += x_vel
        #pos = (self.draw_x-(self.width/2),self.draw_y-(self.height/2))
        #y += y_vel
        #self.x += self.x_vel
        #self.y += self.y_vel
        self.rect = self.img.get_rect()
        #self.rect.center = (self.x,self.y)
        self.rect.center = (self.draw_x,self.draw_y)
        Display.screen.blit(self.img,self.rect)

class PlayerHookshot(ProjectileObject): #jumpback3
    def __init__(self,x,y,velocity,type_projectile,mouse_pos,scale,b_height,b_width):
        self.x = x
        self.y = y

        self.addx = self.addy = 0

        self.angle,self.addx,self.addy = self.CalculateAngle(mouse_pos[0],mouse_pos[1],16//scale)

        self.addx = (self.addx* 5 / scale)
        self.addy = (self.addy* 5 / scale)
        
        ProjectileObject.__init__(self,x+(self.addx),y+(self.addy),velocity,type_projectile,scale,b_height,b_width)
        
        self.imag = self.image[0]
        self.rect = self.imag.get_rect()
        self.rect.center = (self.x,self.y)
        #speed = 20
        #self.x_vel = self.y_vel = 0

        self.angle,self.x_vel,self.y_vel = self.CalculateAngle(mouse_pos[0],mouse_pos[1],velocity)
        self.way_back = False
        self.reel_in = False
        self.reset_hook = False
        self.pulling = False

        self.hook_walls = ["060","061","073"]

        #+16 for starting

    def ProjMain(self,Player,Display,walls,level_walls):
        '''
        So each object can behave differently while only calling projectile.main()
        '''
        self.CalculateAnimationFrame()
        #if self.pulling == False:
        self.Move()
        #else:
        #    self.NegMove()
        self.DrawTrail(Player,Display)
        self.Collision(Player,walls,level_walls)

    def DrawTrail(self,Player,Display):
        x,y = Player.ReturnPlayerPos()
        pygame.draw.line(Display.screen, light_grey, (x+(self.addx),y+(self.addy)), (self.x,self.y))

    def CalculateAnimationFrame(self):
        self.index = 0

    def GetImages(self):
        self.image = {}

        self.image[0] = pygame.image.load("images/projectiles/hookshot/HookshotShot1.png").convert_alpha()
        self.width = int((self.image[0].get_size()[0] * 5) //self.scale)
        self.height = int((self.image[0].get_size()[1] * 5) //self.scale)
        self.image[0] = pygame.transform.scale(self.image[0],(int(self.width),int(self.height)))

    def CalculateAngle(self,mouse_x,mouse_y,multiplier):
        '''
        Uses trigonometry from the module math to calculate the angle at which the arrow should travel at from west

        self.x = x
        mouse_x = m_x

        a = m_y - y
        b = m_x - x
        a = Opposite
        b = Adjacent
        All assuming clockwise rotation from right
        '''
        def M(number): #Modulus, makes number positive
            return (number**2)**(1/2)
    
        a = mouse_y - (self.y+self.addy)
        b = mouse_x - (self.x+self.addx)
        if (a == 0 and b > 0) or (a == 0 and b == 0): #>
            angle = 0
        elif b == 0 and a > 0: #^
            angle = 90
        elif a == 0 and b < 0: #<
            angle = 180
        elif b == 0 and a < 0: #v
            angle = 270
        else: #If not on any axis
            if a > 0 and b > 0:
                angle = math.degrees(math.atan(M(a)/M(b)))
            elif a > 0 and b < 0:
                angle = 90 + (90 - math.degrees(math.atan(M(a)/M(b))))
            elif a < 0 and b < 0:
                angle = 180 + math.degrees(math.atan(M(a)/M(b)))
            elif a < 0 and b > 0:
                angle = 270 + (90 - math.degrees(math.atan(M(a)/M(b))))

        hyp = (a**2 + b**2)**(1/2) #To help find the unit vector

        x_vel = y_vel = 0
        
        if hyp != 0:
            y_vel = (a/hyp)**2 * multiplier
            
            if a < 0:
                y_vel = -y_vel
            x_vel = (b/hyp)**2 * multiplier
            
            if b < 0:
                x_vel = -x_vel
        else:
            x_vel = y_vel = 0

        return angle,x_vel,y_vel

    def Collision(self,Player,walls,level_walls): #Outside method, so enemy can check if colliding or with a box
        for wall in walls:
            if level_walls[wall.WallID] == True:  
                rectangle = pygame.Rect(wall.pos[0],wall.pos[1],wall.dimentions[0],wall.dimentions[1])
                if rectangle.colliderect(self.rect):
                    if self.way_back == False:
                        #print(((self.x+(self.addx)-x)**2)+((self.y+(self.addy)-y)**2)**1/2)
                        if wall.WallID in self.hook_walls:
                            self.reel_in = True
                            self.reset_hook = False
                        
                        else:
                            self.reel_in = False
                            self.reset_hook = True
                        break
                    else:
                        break
                    
        x,y = Player.ReturnPlayerPos()
        #print(((self.x+(self.addx)-x)**2)+((self.y+(self.addy)-y)**2)**1/2)
        if ((self.x-x)**2)+((self.y+(self.addy)-y)**2)**1/2 >= 500000/self.scale:
            #+(self.addx)
            self.reel_in = False
            self.reset_hook = True

                
                #return True
        #return False

    def CheckPos(self,Player):
        x,y = Player.ReturnPlayerPos()
        if self.way_back == True:
            #print(((self.x+(self.addx)-x)**2)+((self.y+(self.addy)-y)**2)**1/2)
            if ((self.x+(self.addx)-x)**2)+((self.y+(self.addy)-y)**2)**1/2 <= 10000/self.scale:
                self.dead = True
                #print("WEW")

    def Move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def NegMove(self):
        self.x -= self.x_vel
        self.y -= self.y_vel


    def Draw(self,Display,pos_x,pos_y):
        '''
        Polymorphism as for arrows it will be a full 360 directional that it could go
        '''
        rot_angle = 0
        if 90 < self.angle < 270:
            rot_angle = -self.angle

        else:
            rot_angle = -self.angle  
        self.img = pygame.transform.rotate(self.image[self.index],rot_angle)
        #x, y = rect.center
        #x += x_vel
        #pos = (self.draw_x-(self.width/2),self.draw_y-(self.height/2))
        #y += y_vel
        #self.x += self.x_vel
        #self.y += self.y_vel
        self.rect = self.img.get_rect()
        self.rect.center = (self.x,self.y)
        Display.screen.blit(self.img,self.rect)


        #image = pygame.transform.rotate(self.hook_original_image_1,rot_angle)
        #x, y = self.hook_rect_1.center
        #rect = image.get_rect()
        #rect.center = (x, y)

    def SetNegativeVel(self):
        if self.way_back == False:
            self.x_vel = -self.x_vel
            self.y_vel = -self.y_vel
            self.way_back = True
            self.reset_hook = False

    def ReturnVel(self):
        return self.x_vel,self.y_vel

    def ReturnReel(self):
        return self.reel_in

    def ReturnReset(self):
        return self.reset_hook



class PlayerBombs(ProjectileObject):
    def __init__(self,x,y,velocity,type_projectile,scale,b_height,b_width):
        ProjectileObject.__init__(self,x,y,velocity,type_projectile,scale,b_height,b_width)
        self.exploded = False
        self.attack = 5
        #self.removed = False

    def ProjMain(self,Player,Display,walls,level_walls):
        '''
        So each object can behave differently while only calling projectile.main()
        '''
        self.CalculateAnimationFrame()

    def CalculateAnimationFrame(self):
        if self.frame > 220:
            self.dead = True
        else:
            for Index in range(1,12,1):
                if self.frame <= (220/11)*Index:
                    self.index = Index -  1
                    break
                
            self.frame += 1

        if self.index >= 9:
            self.exploded = True

    def GetImages(self):
        '''
        1-9 frames are fuse ticking down
        10-13 frames are blown up
        '''
        self.image = {}
        ok = pygame.image.load("images/projectiles/bombs/BombFuse1.png").convert_alpha()
        self.width,self.height = ok.get_size()
        self.width = self.width // self.scale
        self.height = self.height // self.scale
        for Loop1 in range(0,9,1):
            self.image[Loop1] = pygame.image.load("images/projectiles/bombs/BombFuse"+str(Loop1+1)+".png").convert_alpha()
            self.image[Loop1] = pygame.transform.scale(self.image[Loop1],(int(self.width),int(self.height)))
        for Loop2 in range(9,11,1):
            self.image[Loop2] = pygame.image.load("images/projectiles/bombs/BombExplode"+str(int(Loop2 - 8))+".png").convert_alpha()
            self.image[Loop2] = pygame.transform.scale(self.image[Loop2],(int((self.width)),int((self.height))))
            #self.width,self.height

    def PlayerCollide(self,Player,Game):
        #self.GeneralCollision(self,x,y,width,height)
        if Player.ReturnInvul() != 0:
            Player.DecreaseInvul()
        else:
            if self.exploded == True:
                x,y,width,height = Player.ReturnPos()
                if self.GeneralCollision(x-(width/2),y-(height/2),width,height) == True: #4 param jumpback6
                    Player.SetGround()
                    if x > self.draw_x:
                        Player.ChangeVel(15,-15) #x,y
                    elif x <= self.draw_x:
                        Player.ChangeVel(-15,-15)
                    Player.SetInvul(Game)
                    Game.GetHit(self.attack)

    def GeneralCollision(self,x,y,width,height):
        if self.draw_y < y + height and self.draw_y + self.height > y: #Y
            if self.draw_x + self.width > x and self.draw_x < x + width: #X
                return True
        return False

    def GetAttributes(self):
        return self.draw_x,self.draw_y,self.width,self.height

    def ReturnPoses(self):
        return self.pos,self.width,self.height

    def ReturnExploded(self):
        return self.exploded #jumpback


class EnemyProjectile(ProjectileObject):
    def __init__(self,x,y,velocity,type_projectile,scale,b_height,b_width,attack):
        ProjectileObject.__init__(self,x,y,velocity,type_projectile,scale,b_height,b_width)
        self.attack = attack

        #def Move(self):
        self.x_vel = velocity
        #self.removed = False
        #self.y_vel

    def ProjMain(self,Player,Display,walls,level_walls):
        '''
        So each object can behave differently while only calling projectile.main()
        '''
        self.Move()
        if self.Collision(Player,walls,level_walls):
            self.dead = True

    def Move(self):
        self.x += self.x_vel
        #self.y += self.y_vel

    def GetImages(self): #jumpback5
        #if self.type_projectile == "Spitter":
        self.image = {}
        self.image[0] = pygame.image.load("images/projectiles/"+str(self.type_projectile)+"/0.png").convert_alpha()
        self.width,self.height = self.image[0].get_size()
        self.width = self.width // self.scale
        self.height = self.height // self.scale
        self.image[0] = pygame.transform.scale(self.image[0],(int(self.width),int(self.height)))
        #self.image = 

    def Collision(self,Player,walls,level_walls):
        for wall in walls:
            if level_walls[wall.WallID] == True:
                if self.draw_y < wall.pos[1] + wall.dimentions[1] and self.draw_y + self.height > wall.pos[1]: #Y
                    if self.draw_x + self.width > wall.pos[0] and self.draw_x < wall.pos[0] + wall.dimentions[0]: #X
                        return True
        return False

    def GeneralCollision(self,x,y,width,height):
        if self.draw_y - self.height/2 < y + height and self.draw_y + self.height/2 > y: #Y
            if self.draw_x + self.width/2 > x and self.draw_x - self.width/2 < x + width: #X
                return True
        return False

    def PlayerCollide(self,Player,Game):
        x,y,width,height = Player.ReturnPos()
        #self.GeneralCollision(self,x,y,width,height)
        if Player.ReturnInvul() != 0:
            Player.DecreaseInvul()
        else: #jumpback6
            #pygame.draw.rect(Display.screen,old_yellow,pygame.Rect(x,y,width,height))
            if Player.ReturnDuck() == True:
                height -= 12//self.scale
                y += 12//self.scale
            if self.GeneralCollision(x-(width/2),y-(height/2),width,height) == True: #4 param jumpback6
                Player.SetGround()
                if x > self.draw_x:
                    Player.ChangeVel(15,-15) #x,y
                elif x <= self.draw_x:
                    Player.ChangeVel(-15,-15)
                Player.SetInvul(Game)
                Game.GetHit(self.attack)

    def ReturnPos(self):
        return self.x,self.y,self.width,self.height



class EnemyDrops: #jumpback2
    def __init__(self,x,y,scale,dropped_item):
        
        self.scale = scale
        self.x = x
        self.y = y
        self.draw_x = x/scale
        self.draw_y = y/scale
        self.dropped_item = dropped_item
        if dropped_item == "Arrows":
            self.image = pygame.image.load("images/items/Arrows_pickup.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(int(self.image.get_size()[0]/scale),int(self.image.get_size()[1]/scale)))
        elif dropped_item == "Bombs":
            self.image = pygame.image.load("images/items/Bomb_pickup.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(int(self.image.get_size()[0]/scale),int(self.image.get_size()[1]/scale)))
        self.width,self.height = self.image.get_size()
        self.gone = False
        self.picked_up = False
        self.draw = True

        self.alive_frames = 600
        self.picked_up_tick = 0

    def Append(self,drop):
        drop.append(self)
        return drop

    def CalculateDropPos(self,pos_x,pos_y,b_width,b_height,scale):
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if width != 1920/scale:
            if pos_x/scale <= half_horizontal: #(Native Res) 0-960
                self.draw_x = self.x/scale #Then draw them 0-960
            elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
                self.draw_x = self.x/scale - (pos_x/scale-half_horizontal) #Continually make the character in the middle
            elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
                self.draw_x = self.x/scale -(width-(half_horizontal*2)) #Draw him on 960-1920
        else:
            self.draw_x = self.x
            
        if height != 1080/scale:
            if pos_y/scale <= half_vertical:
                self.draw_y = self.y/scale
                #self.draw_y = self.y/scale - (height-(half_vertical*2))
                #print("WOAH")
            elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
                self.draw_y = self.y/scale - (pos_y/scale-half_vertical)
            elif pos_y/scale >= (height-half_vertical):
                self.draw_y = self.y/scale - (height-(half_vertical*2))

        else:
            self.draw_y = self.y

    def CollisionCheck(self,Player): #Player stuff
        pos_x,pos_y,width,height = Player.ReturnPos()
        if self.draw_y < pos_y + height/2 and self.draw_y + self.height > pos_y - height/2: #Y
            if self.draw_x + self.width > pos_x - width/2 and self.draw_x < pos_x + width/2: #X
                return True
        return False

    def CalculateFlashFrame(self):
        if self.alive_frames != 0:
            self.alive_frames -= 1
            self.draw = True
            if self.alive_frames < 300:
                if self.alive_frames % 60 >= 40:
                    self.draw = False
            if self.alive_frames <= 0:
                self.gone = True
    
    def Draw(self,Display):
        self.CalculateFlashFrame()
        if self.draw == True: #So the image can flash
            #self.pos = (self.draw_x-self.width/2,self.draw_y-self.height/2)
            self.pos = (self.draw_x,self.draw_y)

            Display.screen.blit(self.image,self.pos)

    def PickedUp(self,Display): #jumptoexp
        self.picked_up_tick += 1
        self.move_right = self.move_left = False

        font = pygame.font.SysFont("georgia", int((40-(self.picked_up_tick*0.3))/self.scale))
        
        text = font.render("+ 10 "+str(self.dropped_item), True, black)
        text_box = text.get_rect()
        self.draw_y -= 0.5
        text_box.center = (self.draw_x,self.draw_y-50)
 
        Display.screen.blit(text,text_box)

    def SetGone(self):
        self.gone = False

    def SetPickedUp(self):
        self.picked_up = True

    def ReturnGone(self):
        return self.gone

    def ReturnPickedFrame(self):
        return self.picked_up_tick

    def ReturnPickedUp(self):
        return self.picked_up

    def ReturnItem(self):
        return self.dropped_item


class TemporaryWalls: #For blow-up-able walls
    def __init__(self,level,wx,wy,scale,WallID,img,width,height):
        self.level = level
        self.WallID = WallID
        if self.WallID != "Door":
            self.image = img[WallID]
            self.dimentions = (int((60//scale)),int((60//scale)))
            self.image = pygame.transform.scale(self.image,self.dimentions)
        self.scale = scale
        if width == 32 and height == 18:
            self.x = wx/scale
            self.y = wy/scale
        else:
            self.x = wx
            self.y = wy
        self.draw_x = wx/scale
        self.draw_y = wy/scale
        self.destroyed = False

    def Append(self,walls):
        walls.append(self)
        return walls

    def CalculateWallPos(self,pos_x,pos_y,b_width,b_height,scale):
        '''
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #FLOAT scale - The scaling of the screen due to a smaller chosen resolution
        Calculates the player's drawn position in relation to all the parameters above
        '''
        
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if width != 1920/scale:
            if pos_x/scale <= half_horizontal: #(Native Res) 0-960
                self.draw_x = self.x/scale #Then draw them 0-960
            elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
                self.draw_x = self.x/scale - (pos_x/scale-half_horizontal) #Continually make the character in the middle
            elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
                self.draw_x = self.x/scale -(width-(half_horizontal*2)) #Draw him on 960-1920
        else:
            self.draw_x = self.x
            
        if height != 1080/scale:
            if pos_y/scale <= half_vertical:
                self.draw_y = self.y/scale
                #self.draw_y = self.y/scale - (height-(half_vertical*2))
                #print("WOAH")
            elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
                self.draw_y = self.y/scale - (pos_y/scale-half_vertical)
            elif pos_y/scale >= (height-half_vertical):
                self.draw_y = self.y/scale - (height-(half_vertical*2))

        else:
            self.draw_y = self.y
    

    def Draw(self,Display):
        #self.pos = (self.draw_x-(self.width/2),self.draw_y-(self.height/2))
        #self.pos = (self.draw_x/self.scale,self.draw_y/self.scale)
        self.pos = (self.draw_x,self.draw_y)

        Display.screen.blit(self.image,self.pos)
        

    def CollideBomb(self,pos,width,height):
        '''

        '''             
        if self.pos[1] < pos[1] + height and self.pos[1] + self.dimentions[1] > pos[1]: #Y
            if self.pos[0] + self.dimentions[0] > pos[0] and self.pos[0] < pos[0] + width: #X
                return True
                
        return False

    def SetDestroyed(self,state):
        self.destroyed = state

    def ReturnBlock(self):
        return self.WallID

    def ReturnDestroyed(self):
        return self.destroyed

    def ReturnPos(self):
        return self.pos

    def ReturnDBData(self):
        return self.level,self.x,self.y

    def SetPos(self,x,y):
        self.pos = (x,y)

class KeyDoor:
    def __init__(self,level,wx,wy,scale):
        self.level = level
        self.image = {}
        self.dimentions = (int((60//scale)),int((120//scale)))
        for Frames in range(0,7,1): #0-6
            self.image[Frames] = pygame.image.load("images/temporary/Key Door/"+str(Frames)+".png").convert_alpha()
            self.image[Frames] = pygame.transform.scale(self.image[Frames],self.dimentions)
        self.frame = 0 #0-6
        self.tick = 0 #0-60
        self.opened = False
        self.scale = scale
        self.x = wx
        self.y = wy
        self.arc_x = wx
        self.arc_y = wy
        self.draw_x = wx/scale
        self.draw_y = wy/scale
        self.pos = (self.draw_x,self.draw_y)
        self.finished = False

    def Append(self,walls):
        walls.append(self)
        return walls

    def CheckOpened(self):
        if self.opened == True:
            #self.frame = self.tick
            #frame =
            if self.tick > 60:
                self.finished = True
            else:
                for Index in range(1,8,1):
                    if self.tick <= (60/7)*Index:
                        self.frame = Index -  1
                        break
                    
                self.tick += 1

        else:
            self.frame = 0

    def CalculateWallPos(self,pos_x,pos_y,b_width,b_height,scale):
        '''
        #FLOAT pos_x - Player hypothetical x position
        #FLOAT pos_y - Player hypothetical y position
        #INT b_width - How many boxes wide the level is
        #INT b_height - How many boxes high the level is
        #FLOAT scale - The scaling of the screen due to a smaller chosen resolution
        Calculates the player's drawn position in relation to all the parameters above
        '''
        
        width = (b_width/scale)*60 #Width of level in resolution of pixels, 32 blocks = 1920
        height = (b_height/scale)*60 #Height of level in resolution of pixels
        half_horizontal = (1920/scale)/2 #Half of the width of the pygame screen
        half_vertical = (1080/scale)/2 #Half of the height of the pygame screen
        if width != 1920/scale:
            if pos_x/scale <= half_horizontal: #(Native Res) 0-960
                self.draw_x = self.x/scale #Then draw them 0-960
            elif pos_x/scale > half_horizontal and pos_x/scale < (width-half_horizontal): #If in middle of level, not on ends
                self.draw_x = self.x/scale - (pos_x/scale-half_horizontal) #Continually make the character in the middle
            elif pos_x/scale >= (width-half_horizontal): #If on the last half of the level
                self.draw_x = self.x/scale -(width-(half_horizontal*2)) #Draw him on 960-1920
        else:
            self.draw_x = self.x
            
        if height != 1080/scale:
            if pos_y/scale <= half_vertical:
                self.draw_y = self.y/scale
                #self.draw_y = self.y/scale - (height-(half_vertical*2))
                #print("WOAH")
            elif pos_y/scale > half_vertical and pos_y/scale < (height-half_vertical):
                self.draw_y = self.y/scale - (pos_y/scale-half_vertical)
            elif pos_y/scale >= (height-half_vertical):
                self.draw_y = self.y/scale - (height-(half_vertical*2))

        else:
            self.draw_y = self.y

    def Draw(self,Display):
        self.pos = (self.draw_x,self.draw_y)

        Display.screen.blit(self.image[self.frame],self.pos)

    def SetOpened(self):
        self.opened = True

    def ReturnDBData(self):
        return self.level,self.arc_x,self.arc_y

    def ReturnDestroyed(self):
        return self.finished

    def ReturnBlock(self):
        return "Door"

    def ReturnPos(self):
        return self.pos

class Wall(object):
    def __init__(self,wx,wy,scale,WallID,img):
        self.WallID = WallID
        self.image = img[WallID]
        self.dimentions = (int((60//scale)),int((60//scale)))
        self.image = pygame.transform.scale(self.image,self.dimentions)
        #self.scale = scale
        self.pos = (wx,wy)

    def Append(self,walls):
        '''
        Cannot return in __init__ so to avoid making walls global, i made this
        '''
        walls.append(self)
        return walls

    def SetPos(self,x,y):
        self.pos = (x,y)

class Deco(object):
    def __init__(self,wx,wy,DecoID,d_img,scale):
        #self.image = Display.GetDecoImage(DecoID)
        self.DecoID = DecoID
        self.image = d_img[DecoID]
        self.width,self.height = self.image.get_size()
        #print(self.width,self.height)
        self.dimentions = (int(self.width/scale),int(self.height/scale))
        
        self.image = pygame.transform.scale(self.image,self.dimentions)
        
        self.pos = (wx,wy)

    def Append(self,decos):
        '''
        Cannot return in __init__ so to avoid making walls global, i made this
        '''
        decos.append(self)
        return decos

    def GetWallImage(name,scale):
        '''
        Gets the image, scales it and returns
        '''
        image = pygame.image.load("images/blocks/"+name+".png").convert_alpha()
        dimentions = (int((60/scale)),int((60//scale)))
        image = pygame.transform.scale(image,dimentions)
        return image


class DBFile:
    def __init__(self,file):
        self.file = file

    def OpenDB(self):
        self.connection = sqlite3.connect(self.file) #:memory: for db in RAM
        self.c = self.connection.cursor()
    
    def CloseDB(self):
        self.connection.close()


class DBTable(DBFile): #Inheritance as if i have multiple files, tables will be seperate
    def __init__(self,file,table,fields,default_table): #Fields = [#,#,#,#]
        self.fields = fields
        self.table = table
        self.len_fields = len(fields)
        if default_table != "":
            self.default_table = default_table #Directory to the default table
        DBFile.__init__(self,file)

    def QueryTable(self):
        self.OpenDB()
        self.c.execute("SELECT * FROM %s" %(self.table))
        return self.c.fetchall()

    def GetDefaults(self):
        self.OpenDB()
        #Incase i have more fields in a db tblControls_Default
        if len(self.fields) == 2:
            self.c.execute("SELECT "+self.default_table+"."+self.fields[0]+","+self.default_table+"."+self.fields[1]+" FROM "+self.table+", "+self.default_table+" WHERE "+self.table+"."+self.fields[0]+" = "+self.default_table+"."+self.fields[0]+"")
            controls = self.c.fetchall()
            for Loop in range(0,len(controls),1): #thing.controls = thing2.control
                self.c.execute("UPDATE "+self.table+" SET %s = ? WHERE %s = ?" % (self.fields[1],self.fields[0]),(controls[Loop][1],controls[Loop][0],))

        elif len(self.fields) == 3:
            self.c.execute("SELECT "+self.default_table+"."+self.fields[0]+","+self.default_table+"."+self.fields[1]+","+self.default_table+"."+self.fields[2]+" FROM "+self.table+", "+self.default_table+" WHERE "+self.table+"."+self.fields[0]+" = "+self.default_table+"."+self.fields[0]+"")
            controls = self.c.fetchall()
            for Loop in range(0,len(controls),1): #thing.controls = thing2.control
                self.c.execute("UPDATE "+self.table+" SET %s = ?,%s = ? WHERE %s = ?" % (self.fields[1],self.fields[2],self.fields[0]),(controls[Loop][1],controls[Loop][2],controls[Loop][0],))

        self.connection.commit()

        self.CloseDB()

    def UpdateRecord2(self,one,two):
        self.OpenDB()
        self.c.execute("UPDATE %s SET %s = ? WHERE %s = ?" % (self.table,self.fields[1],self.fields[0]),(two,one,))
        self.connection.commit()
        self.CloseDB()

    def UpdateRecord3(self,one,two,three):
        self.OpenDB()
        self.c.execute("UPDATE %s SET %s = ?, %s = ? WHERE %s = ?" % (self.table,self.fields[1],self.fields[2],self.fields[0]),(two,three,one,))
        self.connection.commit()
        self.CloseDB()

    def UpdateDestroyed(self,one,two,three,four):        #Level,x,y,destroyed
        self.OpenDB() #                             Level,x,y
        self.c.execute("UPDATE %s SET %s = ? WHERE %s = ? AND %s = ? AND %s = ?" % (self.table,self.fields[4],self.fields[0],self.fields[1],self.fields[2]),(four,one,two,three,))
        self.connection.commit()
        self.CloseDB()

    def Count(self):
        self.OpenDB()
        self.c.execute("SELECT COUNT(*) FROM %s" %(self.table))
        return self.c.fetchall()[0][0]
        


#Database table creation
connection = sqlite3.connect("settings.db") #:memory: for db in RAM
c = connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS tblGame
(option TEXT,
state TEXT)""")
c.execute("SELECT * FROM tblGame")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblGame VALUES ('Difficulty','Easy')") #Default records:
#
c.execute("""CREATE TABLE IF NOT EXISTS tblGame_Default
(option TEXT,
state TEXT)""")
c.execute("SELECT * FROM tblGame_Default")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblGame_Default VALUES ('Difficulty','Easy')") #Default records:
#
c.execute("""CREATE TABLE IF NOT EXISTS tblControls
(control TEXT,
key TEXT,
alternate TEXT)""")
c.execute("SELECT * FROM tblControls")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblControls VALUES ('Move Left','A','LEFT')") #Default records:
    c.execute("INSERT INTO tblControls VALUES ('Move Right','D','RIGHT')")
    c.execute("INSERT INTO tblControls VALUES ('Jump','W','UP')")
    c.execute("INSERT INTO tblControls VALUES ('Duck','S','DOWN')")
    c.execute("INSERT INTO tblControls VALUES ('Interact','E','')")
    c.execute("INSERT INTO tblControls VALUES ('Attack','Mouse 1','')")
    c.execute("INSERT INTO tblControls VALUES ('Use Item','Mouse 2','')")
    c.execute("INSERT INTO tblControls VALUES ('Next Item','Scroll Up','')")
    c.execute("INSERT INTO tblControls VALUES ('Previous Item','Scroll Down','')")
    c.execute("INSERT INTO tblControls VALUES ('Inventory','RETURN','')")
    c.execute("INSERT INTO tblControls VALUES ('Menu','ESCAPE','')")
#
c.execute("""CREATE TABLE IF NOT EXISTS tblControls_Default
(control TEXT,
key TEXT,
alternate TEXT)""")
c.execute("SELECT * FROM tblControls_Default")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblControls_Default VALUES ('Move Left','A','LeftArrow')") #Default records:
    c.execute("INSERT INTO tblControls_Default VALUES ('Move Right','D','RightArrow')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Jump','W','UpArrow')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Duck','S','DownArrow')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Interact','E','')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Attack','Mouse 1','')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Use Item','Mouse 2','')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Next Item','Scroll Up','')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Previous Item','Scroll Down','')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Inventory','RETURN','')")
    c.execute("INSERT INTO tblControls_Default VALUES ('Menu','ESCAPE','')")
#
c.execute("""CREATE TABLE IF NOT EXISTS tblVideo
(option TEXT,
state TEXT)""")
c.execute("SELECT * FROM tblVideo")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblVideo VALUES ('Fullscreen','Fullscreen')") #Default records:
    c.execute("INSERT INTO tblVideo VALUES ('Resolution','1')")
#
c.execute("""CREATE TABLE IF NOT EXISTS tblVideo_Default
(option TEXT,
state TEXT)""")
c.execute("SELECT * FROM tblVideo_Default")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblVideo_Default VALUES ('Fullscreen','Fullscreen')") #Default records:
    c.execute("INSERT INTO tblVideo_Default VALUES ('Resolution','1')")
#
c.execute("""CREATE TABLE IF NOT EXISTS tblAudio
(option TEXT,
value INTEGER)""")
c.execute("SELECT * FROM tblAudio")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblAudio VALUES ('Master Volume',100)") #Default records:
    c.execute("INSERT INTO tblAudio VALUES ('Music Volume',100)")
    c.execute("INSERT INTO tblAudio VALUES ('Sound Effects',100)")
#
c.execute("""CREATE TABLE IF NOT EXISTS tblAudio_Default
(option TEXT,
value INTEGER)""")
c.execute("SELECT * FROM tblAudio_Default")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblAudio_Default VALUES ('Master Volume',100)") #Default records:
    c.execute("INSERT INTO tblAudio_Default VALUES ('Music Volume',100)")
    c.execute("INSERT INTO tblAudio_Default VALUES ('Sound Effects',100)")
connection.commit()
connection.close()
#

#
connection = sqlite3.connect("enemiesdb.db") #:memory: for db in RAM
c = connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS "tblEnemies" (
	"EnemyID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"EnemyName"	TEXT NOT NULL,
	"EnemyAttack"	INTEGER NOT NULL,
	"EnemyHP"	INTEGER NOT NULL,
	"EnemySpeed"	INTEGER NOT NULL,
	"EnemyExp"	INTEGER NOT NULL,
	"EnemyIdleAnimation"	INTEGER NOT NULL,
	"EnemyWalkAnimation"	INTEGER NOT NULL,
	"EnemyAnimationSpeed"	INTEGER NOT NULL,
	"EnemyWalkAnimationSpeed"	INTEGER,
	"EnemyBehaviour"	TEXT NOT NULL,
	"EnemyProjectiles"	INTEGER NOT NULL,
	"EnemyKnockback"	INTEGER
)""")
c.execute("SELECT * FROM tblEnemies")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblEnemies VALUES (0,'GreySlime',1,4,0,5,4,0,60,60,'Stationary',0,8)")
    c.execute("INSERT INTO tblEnemies VALUES (1,'GreenSlime',2,6,3,10,4,4,60,40,'Random',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (2,'Orc',3,10,4.5,20,4,4,60,40,'Random',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (3,'BloodOrc',3,10,4,40,4,4,60,30,'Chase',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (4,'Zombie',5,5,4,100,4,4,60,30,'Chase',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (5,'Spitter',2,5,0,50,4,0,40,40,'Projectile',6,9)")
    c.execute("INSERT INTO tblEnemies VALUES (6,'MaskedOrc',5,15,2,150,4,4,60,60,'Chase',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (7,'Knight',5,20,3,150,4,4,60,40,'Chase',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (8,'BigDemon',6,15,3,200,4,4,60,50,'Chase',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (9,'RandomZombie',5,15,5,100,4,4,60,40,'Random',0,9)")
    c.execute("INSERT INTO tblEnemies VALUES (10,'BossOrc',5,40,1,200,4,4,60,90,'Chase',0,0)")
    c.execute("INSERT INTO tblEnemies VALUES (11,'BossDemonOrc',5,60,3,400,4,4,60,60,'Projectile',2,18)")
    c.execute("INSERT INTO tblEnemies VALUES (12,'QuickSpitter',10,5,0,50,4,4,30,30,'Projectile',4,0)")
    
connection.commit()
connection.close()
#

#
connection = sqlite3.connect("destroyedwalls.db") #:memory: for db in RAM
c = connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS "tblProfile1" (
	"Level"	TEXT,
	"X"	INTEGER NOT NULL,
	"Y"	INTEGER NOT NULL,
	"Block"	TEXT,
	"Destroyed"	TEXT
)""")
c.execute("SELECT * FROM tblProfile1")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1800,660,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1800,720,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1860,720,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1800,780,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1860,780,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1800,840,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mt Komodo Level 4',1860,840,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Level 4',1260,1080,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Level 4',1260,1020,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Level 4',1260,960,'043','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Level 5',3600,2880,'Door','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',0,720,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',0,780,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',0,840,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',1860,720,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',1860,780,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',1860,840,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',60,720,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',60,780,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',60,840,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',1800,720,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',1800,780,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Mountain Camp Boss',1800,840,'033','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1740,540,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1740,600,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1740,660,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1740,720,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1800,540,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1800,600,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1800,660,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1800,720,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1860,540,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1860,600,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1860,660,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Back',1860,720,'063','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Level 3',3720,480,'Door','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Level 6',2760,600,'Door','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',0,720,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',0,780,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',0,840,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',60,720,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',60,780,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',60,840,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',2400,720,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',2400,780,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',2400,840,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',2460,720,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',2460,780,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Research Lab Boss',2460,840,'051','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Castle Level 10',2280,780,'Door','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Castle Level 10',2520,780,'Door','False')")
    c.execute("INSERT INTO tblProfile1 VALUES ('Castle Level 10',2760,780,'Door','False')")
#
c.execute("""CREATE TABLE IF NOT EXISTS "tblProfile2" (
	"Level"	TEXT,
	"X"	INTEGER NOT NULL,
	"Y"	INTEGER NOT NULL,
	"Block"	TEXT,
	"Destroyed"	TEXT
)""")
c.execute("SELECT * FROM tblProfile2")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1800,660,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1800,720,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1860,720,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1800,780,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1860,780,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1800,840,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mt Komodo Level 4',1860,840,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Level 4',1260,1080,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Level 4',1260,1020,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Level 4',1260,960,'043','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Level 5',3600,2880,'Door','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',0,720,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',0,780,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',0,840,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',1860,720,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',1860,780,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',1860,840,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',60,720,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',60,780,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',60,840,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',1800,720,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',1800,780,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Mountain Camp Boss',1800,840,'033','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1740,540,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1740,600,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1740,660,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1740,720,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1800,540,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1800,600,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1800,660,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1800,720,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1860,540,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1860,600,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1860,660,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Back',1860,720,'063','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Level 3',3720,480,'Door','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Level 6',2760,600,'Door','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',0,720,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',0,780,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',0,840,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',60,720,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',60,780,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',60,840,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',2400,720,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',2400,780,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',2400,840,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',2460,720,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',2460,780,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Research Lab Boss',2460,840,'051','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Castle Level 10',2280,780,'Door','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Castle Level 10',2520,780,'Door','False')")
    c.execute("INSERT INTO tblProfile2 VALUES ('Castle Level 10',2760,780,'Door','False')")
#
c.execute("""CREATE TABLE IF NOT EXISTS "tblProfile3" (
	"Level"	TEXT,
	"X"	INTEGER NOT NULL,
	"Y"	INTEGER NOT NULL,
	"Block"	TEXT,
	"Destroyed"	TEXT
)""")
c.execute("SELECT * FROM tblProfile3")
empty = c.fetchall()
if len(empty) == 0:
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1800,660,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1800,720,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1860,720,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1800,780,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1860,780,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1800,840,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mt Komodo Level 4',1860,840,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Level 4',1260,1080,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Level 4',1260,1020,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Level 4',1260,960,'043','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Level 5',3600,2880,'Door','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',0,720,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',0,780,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',0,840,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',1860,720,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',1860,780,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',1860,840,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',60,720,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',60,780,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',60,840,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',1800,720,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',1800,780,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Mountain Camp Boss',1800,840,'033','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1740,540,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1740,600,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1740,660,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1740,720,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1800,540,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1800,600,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1800,660,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1800,720,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1860,540,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1860,600,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1860,660,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Back',1860,720,'063','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Level 3',3720,480,'Door','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Level 6',2760,600,'Door','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',0,720,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',0,780,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',0,840,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',60,720,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',60,780,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',60,840,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',2400,720,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',2400,780,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',2400,840,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',2460,720,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',2460,780,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Research Lab Boss',2460,840,'051','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Castle Level 10',2280,780,'Door','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Castle Level 10',2520,780,'Door','False')")
    c.execute("INSERT INTO tblProfile3 VALUES ('Castle Level 10',2760,780,'Door','False')")
    
connection.commit()
connection.close()

def GetEnemyTableDetails(name):
    EnemyDB = DBTable('enemiesdb.db','tblEnemies',['EnemyID','EnemyName','EnemyAttack','EnemyHP','EnemySpeed','EnemyExp','EnemyIdleAnimation',
                                                    'EnemyWalkAnimation','EnemyAnimationSpeed','EnemyWalkAnimationSpeed','EnemyBehaviour','EnemyProjectiles'],"")
    table = EnemyDB.QueryTable()
    details = []
    for Enemy in table:
        if Enemy[1] == name:
            details = Enemy #Gets details of that enemy from the database of enemies
            return Enemy


def DepthFirstTraversal(adjacency_list,current_node,visited):
    '''
    Recursive subroutine that returns every single node in the graph attached to the start_node

    #Parameters
    DICT{LIST} adjacency_list - Coordinates of adjacent nodes from one node
    STR current_node - Current node
    LIST visited - All the nodes in this graph

    #Return
    LIST visited - All the nodes that are in this graph
    '''
    visited.append(current_node)
    for Node in adjacency_list[current_node]:
        if Node not in visited:
            DepthFirstTraversal(adjacency_list,Node,visited)

    return visited

def SetAdjacencyList(level_exits):
    '''
    Takes node_queue and returns every adjacent empty space to each node in a list for that key
    '''
    graph = {} #Nodes adjacent to a location
    adjacent = []

    for loop in level_exits:
        adjacent = []
        for loop2 in level_exits[loop]:
            if level_exits[loop][loop2][0] != "Overworld":
                adjacent.append(level_exits[loop][loop2][0])
            #print(level_exits[loop][loop2][0])
        graph[loop] = adjacent

    return graph
        

def EventGet(clickdown):
    '''
    Gets keyboard and mouse inputs from the player
    '''
    running = True
    click1 = False
    for event in pygame.event.get(): #Sees what the user does
        if event.type == pygame.QUIT: #Quit
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            click1 = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clickdown = True
        if event.type == pygame.MOUSEBUTTONUP:
            clickdown = False
    mouse_pos = pygame.mouse.get_pos()
    return running,mouse_pos,click1,clickdown

def MainMenu(Display):
    running = True
    clickdown = False
    while running:
        running,mouse_pos,click1,clickdown = EventGet(clickdown)
        if running == True:
            running = Display.StateSetter(mouse_pos,click1,clickdown,running)
            pygame.display.flip()
        if running != False:
            running = True

def Launch():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    
    pygame.display.set_caption("Trek for Atonement") #Window title
    width = 1920 #Resolution
    height = 1080

    Display = Screen(width,height)
    Display.InstantiateButtons()

    MainMenu(Display)

if __name__ == "__main__":
    Launch()
    
pygame.quit()
