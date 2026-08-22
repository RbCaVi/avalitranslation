# avali translation software by ralsdoge / renauli snow
# (c) 2025 probably
# modified by rbcavi - rewrite numbers window code and other small fixes
# (c) 2026
# this code is licensed under the gpl3

import pyglet
from tkinter import *
from PIL import ImageTk, Image
import GatherOptions as GO
import GatherRandChars as GRC 
import AvalianPronunciation as AP
import AvalianNumbers as AN
import random
import imageTinter as iT
import time
try:
    pyglet.font.add_file('avali-scratch.ttf')
except:
    GO.errorMsg('avali-scratch.ttf missing','The file "avali-scratch.ttf" is missing, please replace avali-scratch.ttf or reinstall program.')
    GO.exitPrgrm()
WindowRegister = []
GO.verifyiniIntegrity() #check on ini file
#Theme Loading
Theme = GO.readIni("Theme","setTheme") #Get theme from ini
try: 
    int(Theme[0])
except:
    GO.errorMsg('Illegal Character in setTheme','The setTheme option has been set to an invalid character. Please don\'t do this. \n\nIm tired of writing exceptions.')
    GO.writeIni("Theme","setTheme",'1')
    Theme = (1,Theme[1])
if int(Theme[0]) < 1:
    GO.writeIni("Theme","setTheme",'1')
    Theme = (1,Theme[1])

#print('Theme: ',Theme)
if not GO.retrieveTheme(Theme[0],Theme[1],1): #Validate 
    #print('not true Validation')
    if GO.retrieveTheme(1,Theme[1],1):
        Theme = GO.retrieveTheme(Theme[0],1) #Run theme through seperate function to populate global theme list
        GO.errorMsg("Error: Selected Theme Corupted","Selected Theme (Theme starting with: "+str(Theme[0])+") is corrupt (see previous errors). Launching program with defualt theme (Theme 1) and setting to default in .ini file.") 
        #print('1LL:',Theme)
        GO.writeIni("Theme","setTheme",'1')#set back to lowest value
    else:
        #print("Defaulting to hardcoded theme, file fallback corupt(see errors)")
        GO.errorMsg('Error: Defaulting Theme','Defaulting to hardcoded theme, ini file themes are corrupt (see previous errors)')
        #print('2LL:',Theme)
        Theme = ['#f0f0f0','#000000','#fc850f','#000000','#ff3419','#fffafa','#d3d3d3','#ffffff','#f0f0f0','#000000']

        #print('3LL:',Theme)
        GO.resetini() #Trigger .ini Reset
else: 
    #print("Start Else statement")
    Theme = GO.retrieveTheme(Theme[0],Theme[1]) #Run theme through seperate function to populate global theme list
#print('4LL:',Theme)
def AddWindowToRegister(win,type): #Add a new window to the Register, Has adorable abreviation "AWTR"
    date = time.time()
    Entry = [win,type,date]
    WindowRegister.append(Entry)
    win.iconbitmap("Images/AppIcon.ico")
    print(WindowRegister,'-AWtR line 53')## DEBUG
    return date

def RemoveWindowFromRegister(win,date,type): #Remove a specific window from the directory
    for i in range(len(WindowRegister)):
        if date == WindowRegister[i][2]:
            if type == WindowRegister[i][1]:
                if WindowRegister.pop(i):
                    win.destroy()
                    print(WindowRegister,'-RWfR line 62')## DEBUG
                    return(True)
    win.destroy()
    GO.errorMsg('Error: Failed to remove closed window from Register','Don\'t worry nothing bad. If you have trouble opening a window please restart the application.')
    return(False)

def CheckWindowRegister(type='X'): #Check if a type of window exists in the Register
    typeCount = 0
    for i in range(len(WindowRegister)):
        #print("Checking for,'"+str(type)+"':",WindowRegister[i],'---',WindowRegister[i][1]) #Debug found bug checking WindowRegister[i][2] (Datecode) instead of WindowRegister[i][1] (window type)
        if type == WindowRegister[i][1]:
            typeCount +=1
    if type == 'P' or type == 'O' or type == 'C' or type == 'N':
        if typeCount >= 1:
            return(False)
    if type == 'T' or type == 'X':
        if typeCount >= 3:
            return(False)
    return(True)

def WindowToTop(type='X'): #Move a type of window to the top
    #if type == 'P' or type == 'O' or type == 'C' or type == 'N':
    #if not CheckWindowRegister(type): #I can't tell you why this works #You find it was never necessary to begin with # one collar, two sleeves
    for i in range(len(WindowRegister)):
        #Find stupid window object
        if WindowRegister[i][1] == type:
            WindowRegister[i][0].lift() #does the same thing but I am told to use the other.. perhaps different across systems
            #WindowRegister[i][0].attributes("-topmost",True)
            #WindowRegister[i][0].attributes("-topmost",False)
                    
    #else:
    #    print('AHHHh')

def WindowRegistration(type='X'):
    print("Window Request Landed: Type("+str(type)+")",end='  Response: ')
    if type == 'M':
        WindowToTop('M')
    if type == 'P':
        print(CheckWindowRegister('P'))
        if CheckWindowRegister('P'):
            createPronunciationWin()
        
    if type == 'O':
        print(CheckWindowRegister('O'))
        if CheckWindowRegister('O'):
            createOptionsWin()
        else:
            WindowToTop('O')
    if type == 'C':
        print(CheckWindowRegister('C'))
        if CheckWindowRegister('C'):
            createCreditsWin()
        else:
            WindowToTop('C')
    if type == 'N':
        print(CheckWindowRegister('N'))
        if CheckWindowRegister('N'):
            createNumbersWin()
        else:
            WindowToTop('P')
    if type == 'T':
        print(CheckWindowRegister('T'))
        if CheckWindowRegister('T'):
            createFontTranslationWin()
        else:
            WindowToTop('T') #caused other to front actions things to break
    if type == 'X':
        print('Undocumented window type.')

class HoverButton(Button): #Used for the sidebar menu buttons
    def __init__(self, master, **kw):
        Button.__init__(self,master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class SidebarMenu(): #Class to create the menubar 
    MenuImgs = [] 
    def __init__(self,winObj,border_frame): #Creates a menubar in the specified window
        #Create Menu Sidebar    
        Sidebar = Frame(border_frame,background="#f0f0f0",borderwidth= "0")
            ##IN
        MB0 = HoverButton(Sidebar,text="Main Menu",image=SidebarMenu.MenuImgs[0], command=lambda: WindowRegistration('M'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0) #em W=0 H=2
        MB1 = HoverButton(Sidebar,text="Font Trans.",image=SidebarMenu.MenuImgs[1], command=lambda: WindowRegistration('T'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB2 = HoverButton(Sidebar,text="Number Trans.",image=SidebarMenu.MenuImgs[2], command=lambda: WindowRegistration('N'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB3 = HoverButton(Sidebar,text="Pronunciation",image=SidebarMenu.MenuImgs[3], command=lambda: WindowRegistration('P'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB4 = HoverButton(Sidebar,text="Options",image=SidebarMenu.MenuImgs[4], command=lambda: WindowRegistration('O'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB5 = HoverButton(Sidebar,text="Credits",image=SidebarMenu.MenuImgs[5], command=lambda: WindowRegistration('C'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        #SideBorder = Canvas(background=Theme[3]) #Maybe not
        MB0.grid(column=0,row=1,sticky='nesw')
        MB1.grid(column=0,row=2,sticky='nesw')
        MB2.grid(column=0,row=3,sticky='nesw')
        MB3.grid(column=0,row=4,sticky='nesw')
        MB4.grid(column=0,row=5,sticky='nesw')
        MB5.grid(column=0,row=6,sticky='nesw')
        Sidebar.grid(column=0,row=0)
    def start(win): #Runs at end of Mwin startup, initializes all menu imgs under menu window.
        #print('Loading images ','-cSM line 108')
        '''menuImg0 = PhotoImage(file='Images/sidebar/Menu.png')
        menuImg1 = PhotoImage(file='Images/sidebar/Translation.png')
        menuImg2 = PhotoImage(file='Images/sidebar/Numbers.png')
        menuImg3 = PhotoImage(file='Images/sidebar/Pronunciation Placeholder.png')
        menuImg4 = PhotoImage(file='Images/sidebar/Settings.png')
        menuImg5 = PhotoImage(file='Images/sidebar/Credits.png')'''
        menuImg0 = ImageTk.PhotoImage(iT.performTint('Images/sidebar/Menu.png',str(Theme[7])))
        menuImg1 = ImageTk.PhotoImage(iT.performTint('Images/sidebar/Translation.png',str(Theme[7])))
        menuImg2 = ImageTk.PhotoImage(iT.performTint('Images/sidebar/Numbers.png',str(Theme[7])))
        menuImg3 = ImageTk.PhotoImage(iT.performTint('Images/sidebar/Pronunciation.png',str(Theme[7]))) #Pronunciation Placeholder.png or Icon Pronunciation.png also avaliable
        menuImg4 = ImageTk.PhotoImage(iT.performTint('Images/sidebar/Settings.png',str(Theme[7])))
        menuImg5 = ImageTk.PhotoImage(iT.performTint('Images/sidebar/Credits.png',str(Theme[7])))

        #MenuImgs.clear()
        SidebarMenu.MenuImgs.append(menuImg0)
        SidebarMenu.MenuImgs.append(menuImg1)
        SidebarMenu.MenuImgs.append(menuImg2)
        SidebarMenu.MenuImgs.append(menuImg3)
        SidebarMenu.MenuImgs.append(menuImg4)
        SidebarMenu.MenuImgs.append(menuImg5)

def chunkText(text, maxsize): # splits every line at the first space after maxsize characters # used in font translation and pronounciation
    chunked = ""
    k = 0
    for c in text:
        if k >= maxsize and c == " ":
            chunked += "\n"
            k = 0
            continue
        k += 1
        chunked += c
    return chunked

def createFontTranslationWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the font translation window. Relevent support files: iT,GRC,random.md
    #Window Register Management
    if CheckWindowRegister('T') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Twin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Twin,'T') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Twin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Twin,WinCode,'T')) #Use saved code to remove from register
    Twin.title("Avalian Font Translation")
    Twin.configure(background=Theme[2])
    #End Window management

    EcoverStatus = True
    TcoverStatus = True
    ReferenceImg = ImageTk.PhotoImage(iT.performTint("Images/CharRefPlaceholderTransAdjCropResize61.png",str(Theme[2])))
    def switchCoverEnglish(): # Switches the visibility of the central elements of this page to allow for practice of translation with or without direct translation. Does this by switching the background of the English text display to the same color as its foreground color.
        nonlocal EcoverStatus    
        if EcoverStatus == True:
            English.config(fg=Theme[1])
            switch1.config(relief=RAISED)
            EcoverStatus = False
        else:
            English.config(fg=Theme[0])
            switch1.config(relief=SUNKEN)
            EcoverStatus = True
    def switchCoverTable(): # Switches the visibility of the central elements of this page to allow for practice of translation with or without the key. Does this by switching the background of the transparent image key to the same color as its foreground color.
        nonlocal TcoverStatus    
        if TcoverStatus == True:
            refimg.config(bg=Theme[0])
            switch2.config(relief=RAISED)
            TcoverStatus = False
        else:
            refimg.config(bg=Theme[2])
            switch2.config(relief=SUNKEN)
            TcoverStatus = True
    def setRandWord(category):
        changeText(GRC.ChallengeRandSample(category))
    def setUserWord():
        changeText(cInput.get("1.0", "end-1c"))
    def changeText(Ntext): #handles changing the English and scratch text displays from the user input buttons. In all cases except the custom input button being pressed the function calls ChallengeRandSample(arg) from GatherRandomCharacters.py with the index of the button as the argument the result of this function is saved to Ntext. Otherwise if the index is 22 or Custom Input the function grabs the text in the custom input text box and saves it to Ntext. Next Ntext is tested if it is > 40 characters. If it is the text is chunked to fit as well as possible into that space by each word. This is done by seeking forward until the maxsize (40) is reached and then searching for the next space and inserting a newline character. This method prevents code from breaking if the user inputs a word greater than 40 chars. Finaly this edited string is sent to update English and Scratch labels.  
        maxsize = 40
        Ftext = chunkText(Ntext, maxsize)

        Scratch.config(text=Ftext)
        English.config(text=Ftext)
    
    border_frame = Frame(Twin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    
    SidebarMenu(Twin,border_frame) #Create Menu Sidebar    

    #scrollbar = Scrollbar(content_frame, orient="vertical", command=content_frame.yview)
    #https://www.tutorialspoint.com/implementing-a-scrollbar-using-grid-manager-on-a-tkinter-window
    Scratch = Label(content_frame,text='',font=('avali scratch',30), background="white", borderwidth="10px", foreground=Theme[2])
    English = Label(content_frame,text='',font=('arial',20),bg=Theme[0],fg=Theme[0]) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    buttonFrame = Frame(content_frame,background=Theme[0])
    swichFrame = Frame(content_frame)
    switch1 = Button(swichFrame,text="Hide English",command=lambda: switchCoverEnglish(),relief=SUNKEN,bg=Theme[8],fg=Theme[9])
    switch2 = Button(swichFrame,text="Hide Table",command=lambda: switchCoverTable(),relief=SUNKEN,bg=Theme[8],fg=Theme[9])
    Option0 = Button(buttonFrame,text="4 letter word",command=lambda: setRandWord(0),bg=Theme[8],fg=Theme[9])
    Option1 = Button(buttonFrame,text="6 letter Word",command=lambda: setRandWord(1),bg=Theme[8],fg=Theme[9])
    Option2 = Button(buttonFrame,text="Sentence",command=lambda: setRandWord(2),bg=Theme[8],fg=Theme[9])
    Option3 = Button(buttonFrame,text="Paragraph",command=lambda: setRandWord(3),bg=Theme[8],fg=Theme[9])
    Option4 = Button(buttonFrame,text="Number",command=lambda: setRandWord(4),bg=Theme[8],fg=Theme[9])
    Option22 = Button(buttonFrame,text="Custom Input",command=lambda: setUserWord(),bg=Theme[8],fg=Theme[9])
    cInput = Text(content_frame, height = 3, width = 71,background=Theme[6])
    cInput.bind("<Return>",lambda event: setUserWord())
    refimg = Label(content_frame,image=ReferenceImg,width=895,height=61,background=Theme[2])
    #content_frame.bind("<Configure>", lambda e: content_frame.configure(scrollregion=content_frame.bbox("all")))
    #drawing

    border_frame.pack()
    content_frame.grid(row=0,column=1)

    English.grid(column=0,row=2,columnspan=8)
    Scratch.grid(column=0,row=3,columnspan=8)
    swichFrame.grid(column=7,row=2)
    buttonFrame.grid(column=0,row=0,columnspan=8)
    BpaddingX = 20
    switch1.grid(column=0,row=0) #,pady=5))
    switch2.grid(column=0,row=1)
    Option0.grid(column=1,row=0,padx=BpaddingX)
    Option1.grid(column=2,row=0,padx=BpaddingX)
    Option2.grid(column=3,row=0,padx=BpaddingX)
    Option3.grid(column=4,row=0,padx=BpaddingX)
    Option4.grid(column=5,row=0,padx=BpaddingX)
    Option22.grid(column=0,row=0,padx=BpaddingX)
    cInput.grid(column=0,row=1, columnspan=8)
    refimg.grid(column=0,row=4,columnspan=8)
    #cover.grid(column=0,row=0)
    Twin.mainloop()
    
def createCreditsWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the credits window. Relevent support files: None
    #Window Register Management
    if CheckWindowRegister('C') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Cwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Cwin,'C') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Cwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Cwin,WinCode,'C')) #Use saved code to remove from register
    Cwin.title("Avalian Translation Credits")
    Cwin.configure(background=Theme[2])

    #End Window management

    border_frame = Frame(Cwin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    Preamble = Label(content_frame,text="I hope some birbs can find some fun or use in this.\nYou can contact me reguarding this software via\n\
Telegram @RenauliSnow.\n\nA deep thanks goes to everyone in this community for\n\
perpetuating this amazing species. For their specific\n\
contributions to this project thank you to the following:\n",justify='left',font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    #insert line break
    Credit = Label(content_frame,text="Programed by Renauli Snow (Ralsdoge) for the community.\nVersion 1 in development from 11/23/2024 to 7/13/2025.",font=('arial',16),background=Theme[0],foreground=Theme[1])
    Credits = Label(content_frame,text=" • Cutesune (RyuujinZero) for creating the Avali Species\n \
• Avali A Comprehensive Guide: Todd Avali\n \
• Scratch Font: Icebelly and Someguynameddavid\n \
• Avali Number System: Ceital Tesai\n \
• Avali HD Icon: tikitree2\n\n\
For presenting me the joys of this community:\n \
• FelisRandomis\n \
• RitualNeo\n \
• Randomking1423\n \
• And many, many others. \
",font=('arial',16),justify='left',background=Theme[0],foreground=Theme[1]) 
    License = Label(content_frame,text="\nThis project is licensed under the GNU General Public License v3 (GPLv3).",font=('arial',14),background=Theme[0],foreground=Theme[1])
    Credit2 = Label(content_frame,text="Forked by RbCaVi on 8/20/2026. Changes: improved numbers window, fixed some spelling errors.",font=('arial',14),background=Theme[0],foreground=Theme[1])
    
    #Scratch = Label(content_frame,text="test",font=('avali scratch',30), background="white", borderwidth="10px", foreground="#fc850f")
    #English = Label(content_frame,text="test",font=('arial',20),bg='black') #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    
    border_frame.pack()
    content_frame.pack()
    Credit.grid(column=0,row=0)
    Preamble.grid(column=0,row=1)
    Credits.grid(column=0,row=2)
    License.grid(column=0,row=3)
    Credit2.grid(column=0,row=4)
    '''Credit1.grid(column=0,row=3)
    Credit2.grid(column=3,row=4)
    Credit3.grid(column=0,row=5)
    Credit3.grid(column=0,row=6)
    Credit4.grid(column=0,row=7)'''
    #.grid(column=0,row=4)
    Cwin.mainloop()

def createOptionsWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the font translation window. Relevent support files: settings.ini,
    #Window Register Management
    if CheckWindowRegister('O') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Owin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Owin,'O') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Owin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Owin,WinCode,'O')) #Use saved code to remove from register
    Owin.title("Avalian Translation Options")
    Owin.configure(background=Theme[2])

    #End Window management

    def button(setting,state): #accepts button commands and textboxes for options
        print("runing",'-cOW->b line 369')
        if setting == 0:
            if state == 1:
                input = TextBox.get("1.0",END)
                if input == '' or input == ' ':
                    return(False)
                else:
                    try:
                        input = int(input)
                    except:
                        GO.errorMsg("Error: Non Integer Input","Theme input is restricted to integer values. To create a custom theme open settings.ini and input hex color codes acordingly observing the presets. Note the position of your theme and input it in options.")
                        return(False)
                curTheme = GO.readIni("Theme","setTheme")
                Bottom = GO.readIni("Pronunciation","Hpron")
                #print("Theme:",int(curTheme[1])+input,"versus, Bottom:",Bottom[1]-1)
                if (int(curTheme[1])+input) < (Bottom[1]-1):
                    #print("valid")
                    GO.writeIni("Theme","setTheme",str(input))
                    GO.infoMsg('Success','Your theme has been updated, please restart the aplication!')
                else: 
                    GO.infoMsg('Failure','Your theme has NOT been updated, your input is outside of the range of possible selctions for themes.')
                    #print("Not")
                #if GO.retrieveTheme(Theme[0],Theme[1],1):

        if setting == 1:
            #if LSButton2.cget('relief') == FLAT:
            if state == 1:
                #print("Right")
                LSButton2.config(relief=RAISED,bg=Theme[2],activebackground=Theme[2],state=NORMAL)
                RSButton2.config(relief=FLAT,bg='lightgrey',activebackground='lightgrey',state=DISABLED)#or FLAT
            else:
                #print("Left")
                LSButton2.config(relief=FLAT,bg='lightgrey',activebackground='lightgrey',state=DISABLED)#or FLAT
                RSButton2.config(relief=RAISED,bg=Theme[2],activebackground=Theme[2],state=NORMAL)
    def setbuttons(p): #sets all buttons acording to settings in settings.ini
        O1 = GO.readIni("Theme","setTheme")
        O2 = GO.readIni("Theme","setTheme")
        O3 = GO.readIni("Pronunciation","Hpron")
        O4 = GO.readIni("Pronunciation","Cchars")
        
        
        TextBox.insert("1.0", "This is some text to insert") 
        TextBox.insert("1.0", str(O1)) 
    
    #Creating Objects:
    border_frame = Frame(Owin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    
    SidebarMenu(Owin,border_frame) #Wow this worked in its first application immediately with no bug fixing whatsoeverthisisdefinitlyatrap.
 
    Title = Label(content_frame,text="Options",font=('arial',20),background=Theme[0],foreground=Theme[1]) 
    
    Setting1 = Frame(content_frame,background=Theme[0])
    Title1 = Label(Setting1,text="Dark, Light, & Custom Themes",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc1 = Label(Setting1,text="Change the theme of the app. Enter 1 for Light and 2\nfor Dark. Make your own custom themes in 'settings.ini'.",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch1 = Frame(Setting1,highlightbackground=Theme[1],highlightthickness=3)
    TextBox = Text(toggleSwitch1,bg=Theme[6],font=("Arial",16),width=1,height=1)#Activebackground=Theme[2]
    TextBox.bind("<Return>",lambda event: button(0,1))
    RSButton1 = Button(toggleSwitch1,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='Submit',command=lambda: button(0,1))
    

    Setting5 = Frame(content_frame,background=Theme[0])
    Title5 = Label(Setting5,text="New Window Open Option        ",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc5 = Label(Setting5,text="Sets if new windows are managed (only one of each type\nopen at a time) or unmanaged (Open as many as you\nwould like at once).",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch5 = Frame(Setting5,highlightbackground=Theme[1],highlightthickness=3)
    LSButton5 = Button(toggleSwitch5,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(4,0))#Activebackground=Theme[2]
    RSButton5 = Button(toggleSwitch5,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(4,1))

    Setting2 = Frame(content_frame,background=Theme[0])
    Title2 = Label(Setting2,text="Number Canvas Orientation     ",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc2 = Label(Setting2,text="Sets if Number Camvas is set horizontaly or verticaly\nby default on opening.",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch2 = Frame(Setting2,highlightbackground=Theme[1],highlightthickness=3)
    LSButton2 = Button(toggleSwitch2,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(1,0))#Activebackground=Theme[2]
    RSButton2 = Button(toggleSwitch2,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(1,1))
    
    Setting3 = Frame(content_frame,background=Theme[0])
    Title3 = Label(Setting3,text="Pronunciation Clamping Chars. ",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc3 = Label(Setting3,text="Sets your default selction for the Pronuciation\nclamping characters. i.e. [] or ()",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch3 = Frame(Setting3,highlightbackground=Theme[1],highlightthickness=3)
    LSButton3 = Button(toggleSwitch3,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(2,0))#Activebackground=Theme[2]
    RSButton3 = Button(toggleSwitch3,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(2,1))
    
    Setting4 = Frame(content_frame,background=Theme[0])
    Title4 = Label(Setting4,text="N Pronuciation Replacement Chars.",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc4 = Label(Setting4,text='Sets your default selction for the Pronuciation\nof the letter "n". i.e. a short pause or "hthk".',font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch4 = Frame(Setting4,highlightbackground=Theme[1],highlightthickness=3)
    LSButton4 = Button(toggleSwitch4,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(3,0))#Activebackground=Theme[2]
    RSButton4 = Button(toggleSwitch4,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(3,1))
    
    #Gridding Objects # hit that griddy
    border_frame.pack()
    content_frame.grid(column=1,row=0)
    Title.grid(column=0,row=0)
    #Preamble.grid(column=0,row=0)
    ###Option 1
    Title1.grid(column=0,row=0)
    Desc1.grid(column=0,row=1,columnspan=2)
    TextBox.grid(column=0,row=0,sticky='nesw')
    RSButton1.grid(column=1,row=0)
    toggleSwitch1.grid(column=3 ,row=0)

    ###Option 5
    Title5.grid(column=0,row=0)
    Desc5.grid(column=0,row=1,columnspan=2)
    LSButton5.grid(column=0,row=0)
    RSButton5.grid(column=1,row=0)
    toggleSwitch5.grid(column=3 ,row=0)

    ###Option 2
    Title2.grid(column=0,row=0)
    Desc2.grid(column=0,row=1,columnspan=2)
    LSButton2.grid(column=0,row=0)
    RSButton2.grid(column=1,row=0)
    toggleSwitch2.grid(column=3 ,row=0)
    
    ###Option 3
    Title3.grid(column=0,row=0)
    Desc3.grid(column=0,row=1,columnspan=2)
    LSButton3.grid(column=0,row=0)
    RSButton3.grid(column=1,row=0)
    toggleSwitch3.grid(column=3 ,row=0)

    ###Option 4
    Title4.grid(column=0,row=0)
    Desc4.grid(column=0,row=1,columnspan=2)
    LSButton4.grid(column=0,row=0)
    RSButton4.grid(column=1,row=0)
    toggleSwitch4.grid(column=3 ,row=0)

    Setting1.grid(column=0,row=1)
    Setting2.grid(column=0,row=2)
    Setting5.grid(column=0,row=3)
    Setting3.grid(column=0,row=4)
    Setting4.grid(column=0,row=5)

    NotComplete1 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 
    NotComplete2 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 
    NotComplete3 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 
    NotComplete4 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 

    NotComplete1.grid(column=0,row=2)
    NotComplete2.grid(column=0,row=3)
    NotComplete3.grid(column=0,row=4)
    NotComplete4.grid(column=0,row=5)

    Owin.mainloop()

def createNumbersWin():
    #Window Register Management
    if CheckWindowRegister('N') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Nwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Nwin,'N') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Nwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Nwin,WinCode,'N')) #Use saved code to remove from register
    Nwin.configure(background=Theme[2])
    #End Window management
    
    VERT = 0
    NEG = 0
    b10Cover = 0
    b12Cover = 0
    
    border_frame = Frame(Nwin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    
    panel = Canvas(content_frame, bg=Theme[0])

    def setDirection(vert):
        nonlocal VERT
        VERT = vert
        if VERT == 0: #Horizontal 
            panel.config(width=800, height=100)
            panel.grid(column=0,row=5,columnspan=5,rowspan=1) #Wide mode
        if VERT == 1: #Vertical
            panel.config(width=100, height=600)
            panel.grid(column=0,row=0,columnspan=1,rowspan=5) #long mode
    
    #Load settings
    HV = GO.readIni("Numbers","HV") #read the options
    if HV in [0, 1]:
        setDirection(HV)
    else:
        setDirection(0)

    digitimages = {
        im: ImageTk.PhotoImage(Image.open('Images/numChars/' + im + '.png'))
        for im in
        ['Amod' + str(i * 12) for i in range(0, 12 + 1)] +
        ['Anum' + str(i) for i in range(0, 12 + 1)] +
        ['DecimalHori', 'DecimalVert'] +
        ['InbetweenHori', 'InbetweenVert'] +
        ['Negative']
    }

    def writeImg(x,y,image): #put image on canvas
        panel.create_image(x, y, image=image,anchor="nw")


    def writeNumber(x,y,manifest,vert): #write full number to canvas
        #add vertical option
        panel.delete('all') # delete all previous images to avoid memory leak
        centerlineH = 92 #maxHeight of tallest img in set
        centerlineW = 60 #maxWidth of widest img in set
        if vert == 0: #Horizontal
            # so these are arranged in a straight line somehow
            # i believe they are vertically centered, with a 10px gap in between adjacent images
            # the digit separator appears to be centered on the right edge of the digit before it
            # no that's not right it's left aligned to the center of the preceding digit and top aligned to the center line
            # i assume the decimal point would do the same
            # so for each digit:
            #   draw
            #   add separator
            #   shift origin for next
            for i,im in enumerate(manifest):
                if im == 'Decimal':
                    continue # should have been drawn by the previous iteration
                im = digitimages[im]
                w,h = im.width(), im.height()
                y = centerlineH / 2 - h / 2
                writeImg(x,y,im)
                if i != len(manifest) - 1:
                    if manifest[i + 1] == 'Decimal': 
                        sep = digitimages['DecimalHori']
                    else:
                        sep = digitimages['InbetweenHori']
                    writeImg(x + w / 2,centerlineH / 2,sep)
                x += w + 10 # shift for the next digit
        else: # vertical
            # i'll do something similar for the vertical layout
            # horizontally centered, 10px vertical gap
            # i don't know why, but i feel like the separator should go to the left
            for i,im in enumerate(manifest):
                if im == 'Decimal':
                    continue # should have been drawn by the previous iteration
                im = digitimages[im]
                w,h = im.width(), im.height()
                x = centerlineW / 2 - w / 2
                writeImg(x,y,im)
                if i != len(manifest) - 1:
                    if manifest[i + 1] == 'Decimal': 
                        sep = digitimages['DecimalVert']
                    else:
                        sep = digitimages['InbetweenVert']
                    sepw = sep.width()
                    writeImg(x + w / 2 - sepw,y + h / 2,sep) # i actually have no idea how to place it
                y += h + 10 # shift for the next digit
    
    def newNumber(b10Num):
        b10EnglishDisp.config(text=b10Num)
        negative = b10Num < 0
        if negative:
            b10Num = -b10Num
        b12num = AN.base12numberConvert(b10Num)
        b12numstr = ''.join(str(AN.toAB(d)) for d in b12num)
        if negative:
            b12numstr = '-' + b12numstr

        b12EnglishDisp.config(text=b12numstr)        
        manifest = AN.base12ImageRef(b12num,negative) 
        #print('manifest:',manifest)
        
        writeNumber(2,2,manifest,VERT)
    
    def updateNumber():
        userIn = userInput.get("1.0",END)
        #print(userIn)
        try:
            try:
                userIn = int(userIn)
            except ValueError: # not an integer, maybe a float?
                userIn = round(float(userIn), 6)
                # error here propagates to the outer try block
                # because the number is not valid
            #print(type(userIn))
            #validate
            #print('VERT: ',VERT)
            newNumber(userIn)
        except ValueError:
            pass # ignore bad numbers - don't want to throw an error to enterHandler()

        #print('Done!')
    
    def randomizeNumber():
        #do random
        #print('Do random!')
        randomNum = random.randint(int(MinSize.get()),int(MaxSize.get()))
        decLength = int(DecimalLength.get())-1
        #print(int(DecimalLength.get()),'-->',int(DecimalLength.get())-1)
        if decLength != -1:
            decimalInt = random.randint(10**decLength,(10**(decLength+1))-1)
            #print('Decimal:',decimalInt)
            decimalComponent = str(decimalInt*0.1**(decLength+1))
            #print('Decimal:',decimalComponent)
            decimalComponent = decimalComponent.split()
            #print('Decimal:',decimalComponent)
            for i in range(len(decimalComponent)):
                total = len(str(decLength))+2
                if i+1 < total:
                    pass
                else:
                    pass
                    #print(decimalComponent)
                    
            #randomNum = randomNum+decimalComponent
            #print(randomNum)
            #Add negative sign if applicable
            if NEG == 1: #add -
                randomNum = -randomNum
                #print(randomNum,'negative:',randomNum)
            elif NEG == 2:
                if random.randint(1,100) >= 46: #45/55 negative/positive # why not even 50/50?
                    #add -
                    randomNum = -randomNum
                    #print(randomNum,'negative:',randomNum)
            else:
                pass
            newNumber(randomNum)
        else:
            pass
    
    def toggleDirection():
        nonlocal VERT
        #vertical or horizontal
        #print('VERT IN:',VERT)
        if VERT == 0:
            setDirection(1)
        else: 
            setDirection(0)
        #print('VERT OUT:',VERT)
        #GO.writeIni("Numbers","HV",VERT) #write preference back to ini file
    
    def toggleSign():
        nonlocal NEG
        #Random Number Negative chance
        if NEG == 2: #Negative and positive
            NEG = 0
            NegativeState.config(text='Positive')
        elif NEG == 0:
            NEG = 1
            NegativeState.config(text='Negative')
        elif NEG == 1:
            NEG = 2
            NegativeState.config(text='Neg & Pos')
    
    def toggleBase10Display():
        nonlocal b10Cover
        #Hide unhide base 10 display
        if b10Cover == 0:
            b10Cover = 1
            b10EnglishDisp.config(background=Theme[1])
            b10EnglishDispButton.config(text='Unhide')
        else:
            b10Cover = 0
            b10EnglishDisp.config(background=Theme[0])
            b10EnglishDispButton.config(text='Hide')
    
    def toggleBase12Display():
        nonlocal b12Cover
        #Hide unhide base 12 displays
        if b12Cover == 0:
            b12Cover = 1
            b12EnglishDisp.config(background=Theme[1])
            b12EnglishDispButton.config(text='Unhide')
        else:
            b12Cover = 0
            b12EnglishDisp.config(background=Theme[0])
            b12EnglishDispButton.config(text='Hide')
    
    #Create Menu Sidebar    
    SidebarMenu(Nwin,border_frame)

    util_frame = Frame(content_frame, background=Theme[0],borderwidth= '12px')
    random_frame = Frame(content_frame, background=Theme[0],borderwidth= '12px')
    ###Title + Support
    Title = Label(content_frame,text='Avalian Base 12 System',font=('arial',18),background=Theme[0],foreground=Theme[1])
    
    ###Random Interface
    RandLabel = Label(random_frame,text='Random Num. Gen.',font=('arial',14),background=Theme[0],foreground=Theme[1])
    MaxSize = Scale(random_frame, from_=0, to=1000,orient = "horizontal",fg=Theme[1],bg=Theme[0]) #Slider 
    MinSize = Scale(random_frame, from_=0, to=1000,orient = "horizontal",fg=Theme[1],bg=Theme[0]) #Slider
    DecimalLength = Scale(random_frame, from_=0, to=10,orient = "horizontal",fg=Theme[1],bg=Theme[0]) #Slider
    DecimalLengthLabel = Label(random_frame,text="Decimal Length",font=('arial',10),background=Theme[0],foreground=Theme[1])
    DecimalLengthWarning = Label(random_frame,text="(Not added yet, confused\non how it'd work)",font=('arial',10),background=Theme[0],foreground=Theme[1])
    MaxSizeLabel = Label(random_frame,text='Max Size',font=('arial',10),background=Theme[0],foreground=Theme[1])
    MinSizeLabel = Label(random_frame,text='Min Size',font=('arial',10),background=Theme[0],foreground=Theme[1])
    MaxSize.set(125)
    MinSize.set(20)
    DecimalLength.set(1)
    NegativeState = Button(random_frame,text='Positive',command=lambda:toggleSign(),bg=Theme[8],fg=Theme[9]) #whether to generate negative numbers or not
    randomNumGo = Button(random_frame,text='Submit',command=lambda:randomizeNumber(),bg=Theme[8],fg=Theme[9]) #submit random num
    def enterHandler(event):
        updateNumber()
        return "break"
    ###Options###
    userInput = Text(util_frame,width=30,height=1,bg=Theme[6]) #User in Textbox
    userInput.bind("<Return>",enterHandler)

    userInGo = Button(util_frame,text='Submit',command=lambda:updateNumber(),bg=Theme[8],fg=Theme[9]) #submit user input from Userinput (Valideate)
    base10Label = Label(util_frame,text='Base-10:',font=('arial',10),background=Theme[0],foreground=Theme[1])
    base12Label = Label(util_frame,text='Base-12:',font=('arial',10),background=Theme[0],foreground=Theme[1])
    b12EnglishDisp = Label(util_frame,text=0,font=('arial',12), background=Theme[0], foreground=Theme[1]) #Base12 number display in english
    b10EnglishDisp = Label(util_frame,text=0,font=('arial',12), background=Theme[0], foreground=Theme[1]) #Base10 number display in english
    b10EnglishDispButton = Button(util_frame,text='Hide',command=lambda:toggleBase10Display(),bg=Theme[8],fg=Theme[9]) 
    b12EnglishDispButton = Button(util_frame,text='Hide',command=lambda:toggleBase12Display(),bg=Theme[8],fg=Theme[9]) 
    HVButton = Button(util_frame,text='Horizontal/Vertical',command=lambda:toggleDirection(),bg=Theme[8],fg=Theme[9])#Horizontal Vertical numbering toggle
    HVdescription = Label(util_frame,text="Swich between formal vertical structure and casual horizontal display.",background=Theme[0],foreground=Theme[1]) 
    ###

    
    border_frame.pack()
    content_frame.grid(column=1,row=0)

    Title.grid(column=1,row=0,columnspan=3)
    util_frame.grid(column=1,row=1,columnspan=3,rowspan=3,sticky='nesw')
    HVButton.grid(column=1,row=0)
    HVdescription.grid(column=0,row=1,columnspan=3,)
    userInput.grid(column=0,row=2,columnspan=2,sticky='e')
    userInGo.grid(column=2,row=2,columnspan=1)
    base10Label.grid(column=0,row=4)
    base12Label.grid(column=0,row=5)
    b10EnglishDisp.grid(column=1,row=4,columnspan=2)
    b12EnglishDisp.grid(column=1,row=5,columnspan=2)
    b10EnglishDispButton.grid(column=2,row=4,columnspan=1)
    b12EnglishDispButton.grid(column=2,row=5,columnspan=1)
    #Random
    random_frame.grid(column=4,row=0,columnspan=2,rowspan=3,sticky='wns')
    RandLabel.grid(column=0,row=0,columnspan=3)
    MaxSize.grid(column=1,row=2,columnspan=2)
    MinSize.grid(column=1,row=4,columnspan=2)
    DecimalLength.grid(column=1,row=6,columnspan=2)
    MaxSizeLabel.grid(column=0,row=1,columnspan=2)
    MinSizeLabel.grid(column=0,row=3,columnspan=2)
    DecimalLengthLabel.grid(column=0,row=5,columnspan=2)
    DecimalLengthWarning.grid(column=0,row=6,columnspan=2)
    NegativeState.grid(column=0,row=7,columnspan=2)
    randomNumGo.grid(column=2,row=7)
    
    Nwin.mainloop()

def createPronunciationWin():
    #Window Register Management
    if CheckWindowRegister('P') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Pwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Pwin,'P') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Pwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Pwin,WinCode,'P')) #Use saved code to remove from register
    Pwin.title("Avalian Pronunciation")    
    Pwin.configure(background=Theme[2])
    #End Window management
    Ntext = ''
    ###Functions
    def setRandWord(category):
        changeText(GRC.ChallengeRandSample(category))
    def setUserWord():
        changeText(cInput.get("1.0", "end-1c"))
    def changeText(Ntext):
        maxsize = 70
        English.config(text=chunkText(Ntext, maxsize))
        EnglishO.config(text=chunkText(AP.pronounciationDisp(Ntext,Hdropclicked.get(),ClampingCharsSelected.get()), maxsize))

    border_frame = Frame(Pwin,borderwidth="4px",background=Theme[2])#background="#fc850f"
    content_frame = Frame(border_frame,borderwidth= "12px",background=Theme[0])
    
    SidebarMenu(Pwin,border_frame)

    ###Labels
    PronunciationTableHead = Label(content_frame,text='Unpronounceable Characters',font=('arial',20), background=Theme[0], foreground=Theme[1])
    PronunciationDesc = Label(content_frame,text='Try speaking like an Avali. Avali are thought to be unable to pronounce the\nfollowing characters due to the lack of a nasal cavity. (Todd\'s Avali Lore Guide)',font=('arial',14), background=Theme[0], foreground=Theme[1])
    SpecialCharsStr = ''
    SpecialReplaceStr = ''
    for c in AP.specialpronchars:
        SpecialCharsStr += '  '+c.upper()+' =\n'
    for r in AP.replacements:
        SpecialReplaceStr += r+'\n'
    ##Objects
    
    NpronLabel = Label(content_frame,text="N Pronunciation:",font=('arial',14),background=Theme[0],foreground=Theme[1])
    ClampingLabel = Label(content_frame,text="Clamping Characters:",font=('arial',14),background=Theme[0],foreground=Theme[1])
    UPronounceChars = Label(content_frame,text=SpecialCharsStr,font=('arial',16),background=Theme[0],foreground=Theme[1])
    RPronounceChars = Label(content_frame,text=SpecialReplaceStr,font=('arial',16),background=Theme[0],foreground=Theme[1])
    ##Dropdowns
    #HPron
    HpronOptions = ["ha (ha)","Short pause (-)","Short pause (')","Short Pause ( )","Short Pause (,)"] 
    Hdropclicked = StringVar()
    Ndropbutton = OptionMenu( content_frame, Hdropclicked, *HpronOptions)
    Ndropbutton.config(bg=Theme[8],fg=Theme[9]) 
    #Ndropbutton.config(bg=Theme[0])
    #ClampingChars
    ClampingCharsOptions = ['"{-}" (Curvy Brackets)','"[-]" (Brackets)','"|-|" (Lines)','"\\-" (Backslash)','" - " (Spaces)','"-" (None)']
    ClampingCharsSelected = StringVar()
    ClampingCharsButton = OptionMenu(content_frame, ClampingCharsSelected, *ClampingCharsOptions)
    ClampingCharsButton.config(bg=Theme[8],fg=Theme[9]) 
    #Load settings
    CC = str(GO.readIni("Pronunciation","Cchars")) #read the options
    if CC in ['0', '1', '2', '3', '4', '5', '6']: #if valid entry
        if CC == '0': #Last used 
            #print('Read CC = 0')
            LCC = str(GO.readIni("Pronunciation","LastC")) #read the options
            if LCC in ['0', '1', '2', '3', '4', '5']: #if valid entry set the Clamping characters dropdown menu to set option otherwise use the program default
                clampingcharsindex = int(LCC)
        else: #Default set, set it.
            #print('Read CC =',str(CC-1))
            clampingcharsindex = int(CC)-1
    else: # invalid value
        #print('Program Default')
        clampingcharsindex = 1 # the second option - short pause (-)
    ClampingCharsSelected.set(ClampingCharsOptions[clampingcharsindex])
    HP = str(GO.readIni("Pronunciation","Hpronchars")) #read the options
    if HP in ['0', '1', '2', '3', '4', '5']: #if valid entry set the Clamping characters dropdown menu to set option otherwise use the program default
        if HP == '0': #
            #print('Read HP = 0')
            LHP = str(GO.readIni("Pronunciation","LastH")) #read the options
            if LHP in ['0', '1', '2', '3', '4']: # if valid
                hpronindex = int(LHP)
        else: #
            #print('Read HP =',str(HP-1))
            hpronindex = int(HP)-1
    else: # invalid value
        #print('HP = Program Default')
        hpronindex = 1 # the second option - [] brackets
    Hdropclicked.set(HpronOptions[hpronindex])
    #End Load settings

    ##
    English = Label(content_frame,text='',font=('arial',10),background=Theme[0],foreground=Theme[1]) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    EnglishO = Label(content_frame,text='',font=('arial',20),background=Theme[0],foreground=Theme[1]) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    #switch = Button(content_frame,text="minimize")#,command=lambda: )
    Option0 = Button(content_frame,text="4Word",command=lambda: setRandWord(0),bg=Theme[8],fg=Theme[9])
    Option1 = Button(content_frame,text="6Word",command=lambda: setRandWord(1),bg=Theme[8],fg=Theme[9])
    Option2 = Button(content_frame,text="sent.",command=lambda: setRandWord(2),bg=Theme[8],fg=Theme[9])
    Option3 = Button(content_frame,text="para.",command=lambda: setRandWord(3),bg=Theme[8],fg=Theme[9])
    Option4 = Button(content_frame,text="numb.",command=lambda: setRandWord(4),bg=Theme[8],fg=Theme[9])
    Option22 = Button(content_frame,text="Custom",command=lambda: setUserWord(),bg=Theme[8],fg=Theme[9])
    def enterHandler(event):
        updateNumber()
        return "break"
    cInput = Text(content_frame, height = 1, width = 80,bg=Theme[6])
    cInput.bind("<Return>",enterHandler)
    ##Griding
    PronunciationTableHead.grid(column=0,row=0,columnspan=6)
    PronunciationDesc.grid(column=0,row = 1,columnspan=6)
    UPronounceChars.grid(column=6,row = 0,rowspan=3,sticky='e')
    RPronounceChars.grid(column=7,row = 0,rowspan=3,columnspan=2)
    NpronLabel.grid(column=0,row = 2)
    Ndropbutton.grid(column=1,row = 2,columnspan=2)
    ClampingLabel.grid(column=3,row=2)
    ClampingCharsButton.grid(column=4,row=2,columnspan=2)
    border_frame.pack()
    content_frame.grid(column=1,row=0)
    English.grid(column=0,row=5,columnspan=8)
    EnglishO.grid(column=0,row=6,columnspan=8)
    #switch.grid(column=8,row=5)
    Option0.grid(column=1,row=4,sticky='nesw')
    Option1.grid(column=2,row=4,sticky='nesw')
    Option2.grid(column=3,row=4,sticky='nesw')
    Option3.grid(column=4,row=4,sticky='nesw')
    Option4.grid(column=5,row=4,sticky='nesw')
    Option22.grid(column=0,row=4,sticky='nesw')
    cInput.grid(column=0,row=3, columnspan=6,sticky='nesw')
    #cover.grid(column=0,row=0)
    Pwin.mainloop()

def createMainMenuWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the main menu window. Relevent support files: settings.ini
    global MenuImgs
    global Mwin
    #Window Register Management
    if CheckWindowRegister('M') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Mwin = Tk() #Make Main window
    WinCode = AddWindowToRegister(Mwin,'M') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Mwin.configure(background=Theme[2])
    Mwin.title("Avalian Translation Software (RbCaVi Fork)")
    WindowToTop('M')
    #End Window management

    border_frame = Frame(Mwin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    Title = Label(content_frame,font=('Helvetica 30 italic'),text="Avalian Translation Software",background=Theme[0],foreground=Theme[3])
    Preface = Label(content_frame,font=('Helvetica 18 italic'),text="By: Renauli Snow",background=Theme[0],foreground=Theme[3]) #Aw du Bub du day. Bah.. Blep.
    Option0 = Button(content_frame,font=('Helvetica 18 italic'),text="  Credits  ",command=createCreditsWin,background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option1 = Button(content_frame,font=('Helvetica 18 italic'),text="  Options  ",command=createOptionsWin,background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option2 = Button(content_frame,font=('Helvetica 18 normal'),text="Font Translation",command=createFontTranslationWin,background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option3 = Button(content_frame,font=('Helvetica 18 normal'),text="Avalian Numbers",command=createNumbersWin,background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option4 = Button(content_frame,font=('Helvetica 18 normal'),text="Pronunciation",command=createPronunciationWin,background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    ##db349c
    border_frame.pack()
    content_frame.pack()
    Title.grid(column=2,columnspan=3,row=0,padx=2,pady=2)
    Preface.grid(column=0,columnspan=5,row=1,padx=3,pady=2)
    Option0.grid(column=2,row=2,columnspan=2,padx=2,pady=2)
    Option1.grid(column=3,row=2,columnspan=2,padx=2,pady=2)
    Option2.grid(column=2,row=3,padx=2,pady=2)
    Option3.grid(column=3,row=3,padx=2,pady=2)
    Option4.grid(column=4,row=3,padx=2,pady=2)
    SidebarMenu.start(Mwin)
    Mwin.mainloop()

createMainMenuWin() #Anything after this will not execute