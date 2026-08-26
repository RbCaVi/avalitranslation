# avali translation software by ralsdoge / renauli snow
# (c) 2025 probably
# modified by rbcavi - rewrite numbers window code and other small fixes
# (c) 2026
# this code is licensed under the gpl3

import pyglet
from tkinter import Button, Label, Frame, Tk, Toplevel, FLAT, DISABLED, RAISED, NORMAL, StringVar, OptionMenu, SUNKEN, Text, Canvas, Scale, END
from PIL import ImageTk, Image
import GatherOptions as GO
import GatherRandChars as GRC 
import AvalianPronunciation as AP
import AvalianNumbers as AN
import random
import imageTinter as iT
import time
import functools
from tkbuilder import TkBuilderLeaf, Grid, FrameBuilder, TkBuilder, Pack, LabelBuilder, ButtonBuilder, TextBuilder, OptionMenuBuilder
try:
    pyglet.font.add_file('avali-scratch.ttf')
except:
    GO.errorMsg('avali-scratch.ttf missing','The file "avali-scratch.ttf" is missing, please replace avali-scratch.ttf or reinstall program.')
    GO.exitPrgrm()
#GO.verifyiniIntegrity() #check on ini file
GO.repairIni() # fix the ini file if it is broken
#Theme Loading
ThemeName = GO.readIni("Theme","setTheme") #Get theme from ini
#print('Theme: ',ThemeName)
if not GO.retrieveTheme(ThemeName,1): #Validate 
    #print('not true Validation')
    if GO.retrieveTheme('Light',1):
        Theme = GO.retrieveTheme('Light') #Run theme through seperate function to populate global theme list
        GO.errorMsg("Error: Selected Theme Corrupted","Selected Theme ("+Theme+") is corrupt (see previous errors). Launching program with default theme (Light) and setting to default in .ini file.") 
        #print('1LL:',Theme)
        GO.writeIni("Theme","setTheme",'Light')#set back to default value
    else:
        #print("Defaulting to hardcoded theme, file fallback corupt(see errors)")
        GO.errorMsg('Error: Defaulting Theme','Defaulting to hardcoded theme, ini file themes are corrupt (see previous errors)')
        #print('2LL:',Theme)
        Theme = ['#f0f0f0','#000000','#fc850f','#000000','#ff3419','#fffafa','#d3d3d3','#ffffff','#f0f0f0','#000000']
        GO.writeIni("Theme","setTheme",'Light')
        GO.writeIni("Theme","Light",'['+','.join(Theme)+']')

        #print('3LL:',Theme)
        #GO.resetini() #Trigger .ini Reset
else: 
    #print("Start Else statement")
    Theme = GO.retrieveTheme(ThemeName) #Run theme through seperate function to populate global theme list
#print('4LL:',Theme)

buttonstyle = {'bg': Theme[8],'fg': Theme[9]}
textstyle = {'bg': Theme[0],'fg': Theme[1]}

HpronOptions = ["ha (ha)","Short pause (-)","Short pause (')","Short Pause ( )","Short Pause (,)"] 
ClampingCharsOptions = ['"{-}" (Curvy Brackets)','"[-]" (Brackets)','"|-|" (Lines)','"\\-" (Backslash)','" - " (Spaces)','"-" (None)']

windowregister = {type:{} for type in 'MPOCNT'} # type -> id (date) -> window

def AddWindowToRegister(win,type): #Add a new window to the Register, Has adorable abreviation "AWTR"
    date = time.time()
    windowregister[type][date] = win
    win.iconbitmap("Images/AppIcon.ico")
    print(windowregister,'-AWtR line 53')## DEBUG
    return date

def RemoveWindowFromRegister(win,date,type): #Remove a specific window from the directory
    if type in windowregister:
        if date in windowregister[type]:
            del windowregister[type][date] # remove the entry from the register
            win.destroy()
            print(windowregister,'-RWfR line 62')## DEBUG
            return(True)
    win.destroy()
    GO.errorMsg('Error: Failed to remove closed window from Register','Don\'t worry nothing bad. If you have trouble opening a window please restart the application.')
    return(False)


WindowsUnmanaged = GO.readIniBool("Windows","Unmanaged") #read the options
def CheckWindowRegister(type='X'): #Check if a type of window is allowed to be created in the Register
    if WindowsUnmanaged:
        return(True)
    typeCount = len(windowregister[type])
    maxTypeCount = {
        'P': 1,
        'O': 1,
        'C': 1,
        'N': 1,
        'T': 3,
        'X': 3,
    }
    if type in maxTypeCount:
        if typeCount >= maxTypeCount[type]:
            return(False)
    return(True)

def WindowToTop(type='X'): #Move a type of window to the top
    #if type == 'P' or type == 'O' or type == 'C' or type == 'N':
    #if not CheckWindowRegister(type): #I can't tell you why this works #You find it was never necessary to begin with # one collar, two sleeves
    for win in windowregister[type].values():
        #Find stupid window object s
            win.lift() #does the same thing but I am told to use the other.. perhaps different across systems
            #win.attributes("-topmost",True)
            #win.attributes("-topmost",False)
                    
    #else:
    #    print('AHHHh')

def WindowRegistration(type='X'):
    print("Window Request Landed: Type("+str(type)+")",end='  Response: ')
    if type == 'M':
        WindowToTop('M')
    createWinType = {
        'P': createPronunciationWin,
        'O': createOptionsWin,
        'C': createCreditsWin,
        'N': createNumbersWin,
        'T': createFontTranslationWin,
    }
    if type in createWinType:
        print(CheckWindowRegister(type))
        if CheckWindowRegister(type):
            createWinType[type]()
        else:
            WindowToTop(type)
    if type == 'X':
        print('Undocumented window type.')

class WindowInnerWithMenuBuilder(TkBuilder):
    childrenargs = ['inner']

    def __init__(self, geometry = Pack(), key = None, inner = None, inner_key = None):
        super().__init__(geometry = geometry, key = key, inner = inner, inner_key = inner_key)

    def constructor(self, root, table):
        childrenroots = {}
        thisroot = FrameBuilder(background=Theme[2],borderwidth="4px",children=[
            SidebarBuilder(geometry=Grid(row=0,column=0)),
            FrameBuilder(background=Theme[0],borderwidth= "12px",key='inner',geometry=Grid(row=0,column=1)),
        ],geometry=self.geometry).build(root, childrenroots)
        return thisroot, childrenroots

class WindowInnerWithoutMenuBuilder(TkBuilder):
    childrenargs = ['inner']
    
    def __init__(self, geometry = Pack(), key = None, inner = None, inner_key = None):
        super().__init__(geometry = geometry, key = key, inner = inner, inner_key = inner_key)

    def constructor(self, root, table):
        childrenroots = {}
        thisroot = FrameBuilder(background=Theme[2],borderwidth="4px",children=[
            FrameBuilder(background=Theme[0],borderwidth= "12px",key='inner',geometry=Pack()),
        ],geometry=self.geometry).build(root, childrenroots)
        return thisroot, childrenroots

def createWin(type, title):
    #Window Register Management
    if CheckWindowRegister(type) == False: #Clear creating the window with the register, True means its allowed
        return None, None #killbind
    if type == 'M': # main window
        win = Tk()
    else:
        win = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(win,type) #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return None, None #explode
    if type != 'M':
        win.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(win,WinCode,type)) #Use saved code to remove from register
    win.title(title)
    win.configure(background=Theme[2])
    #End Window management

    border_frame = Frame(win,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    if type not in ['C', 'M']: # credits window does not include a sidebar # don't know why
        SidebarBuilder(geometry=Grid(row=0,column=0)).build(border_frame, None) #Create Menu Sidebar
    border_frame.pack()
    if type not in ['C', 'M']:
        content_frame.grid(row=0,column=1)
    else:
        content_frame.pack()

    return win, content_frame

def newWinAllowed(type):
    return CheckWindowRegister(type)

def createWin2(type, title):
    #Window Register Management
    if CheckWindowRegister(type) == False: #Clear creating the window with the register, True means its allowed
        return None #killbind
    if type == 'M': # main window
        win = Tk()
    else:
        win = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(win,type) #Ask to register with the Register, Save Date as unique code.
    if type != 'M':
        win.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(win,WinCode,type)) #Use saved code to remove from register
    win.title(title)
    win.configure(background=Theme[2])
    #End Window management

    return win

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

class HoverButtonBuilder(TkBuilderLeaf):
    element = HoverButton

class SidebarBuilder(TkBuilderLeaf):
    def __init__(self, geometry = None, key = None):
        super().__init__(geometry = geometry, key = key)

    def constructor(self, root, table):
        options = lambda type, index: {
            'image':SidebarMenu.MenuImgs[index],
            'command':lambda: WindowRegistration(type),
            'relief':FLAT,
            'foreground':Theme[5],'background':Theme[2],
            'activebackground':Theme[4],
            'height':60,
            'width':0,
            'geometry':Grid(column = 0, row = index, sticky = 'nesw')
        }
        return FrameBuilder(background="#f0f0f0",borderwidth="0",children=[
            HoverButtonBuilder(text="Main Menu",**options(type = 'M', index = 0)),
            HoverButtonBuilder(text="Font Trans.",**options(type = 'T', index = 1)),
            HoverButtonBuilder(text="Number Trans.",**options(type = 'N', index = 2)),
            HoverButtonBuilder(text="Pronunciation",**options(type = 'P', index = 3)),
            HoverButtonBuilder(text="Options",**options(type = 'O', index = 4)),
            HoverButtonBuilder(text="Credits",**options(type = 'C', index = 5)),
        ]).build(root, table), {}

class SidebarMenu(): #Class to create the menubar 
    MenuImgs = [] 
    def start(win): #Runs at end of Mwin startup, initializes all menu imgs under menu window.
        #print('Loading images ','-cSM line 108')
        SidebarMenu.MenuImgs = [
            ImageTk.PhotoImage(iT.performTint('Images/sidebar/' + icon + '.png',Theme[7]))
            for icon in
            ['Menu', 'Translation', 'Numbers', 'Pronunciation', 'Settings', 'Credits']
        ]

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

def toggleable(initialstate = None, values = (True, False)): # add persistent state and a .toggle attribute to a function
    # the function is assumed to take one argument with a value in values
    # toggle cycles through all of them # i did this to cover togglenegative in the numbers window
    def toggleable(f):
        @functools.wraps(f) # keep the name of f for debugging purposes
        def newf(state): # version of f that sets the value as well as whatever it did originally
            newf.state = state
            f(state)

        # initialize the state
        if initialstate is not None: # if an initial state is given
            assert initialstate in values
            newf(initialstate) # set the state to it

        def toggle(): # cycle through the values
            try:
                idx = values.index(newf.state) # find the index the state is currently at
            except AttributeError:
                raise RuntimeError(f.__name__ + ' was toggled before being initialized with a value')
            newf(values[(idx + 1) % len(values)]) # choose the next index # remember */% bind tighter than +-
        newf.toggle = toggle

        return newf # the original function will be replaced with this

    if callable(initialstate): # trickery to allow you to use this decorator as @toggleable instead of @toggleable()
        f = initialstate
        initialstate = None
        return toggleable(f)

    return toggleable # if proper arguments were given

def createFontTranslationWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the font translation window. Relevent support files: iT,GRC,random.md
    Twin = createWin2('T', 'Avalian Font Translation')
    if Twin is None:
        return False # nope

    ReferenceImg = ImageTk.PhotoImage(iT.performTint("Images/CharRefPlaceholderTransAdjCropResize61.png",str(Theme[2])))
    @toggleable
    def setCoverEnglish(EcoverStatus): # Switches the visibility of the central elements of this page to allow for practice of translation with or without direct translation. Does this by switching the background of the English text display to the same color as its foreground color.
        if EcoverStatus:
            English.config(fg=Theme[0])
            switch1.config(relief=SUNKEN)
        else:
            English.config(fg=Theme[1])
            switch1.config(relief=RAISED)
        GO.writeIni('Translation', 'EnglishView', EcoverStatus)
    @toggleable
    def setCoverTable(TcoverStatus): # Switches the visibility of the central elements of this page to allow for practice of translation with or without the key. Does this by switching the background of the transparent image key to the same color as its foreground color.
        if TcoverStatus:
            refimg.config(bg=Theme[2])
            switch2.config(relief=SUNKEN)
        else:
            refimg.config(bg=Theme[0])
            switch2.config(relief=RAISED)
        GO.writeIni('Translation', 'TableView', TcoverStatus)
    def setRandWord(category):
        changeText(GRC.ChallengeRandSample(category))
    def setUserWord():
        changeText(cInput.get("1.0", "end-1c"))
    def changeText(Ntext): #handles changing the English and scratch text displays from the user input buttons. In all cases except the custom input button being pressed the function calls ChallengeRandSample(arg) from GatherRandomCharacters.py with the index of the button as the argument the result of this function is saved to Ntext. Otherwise if the index is 22 or Custom Input the function grabs the text in the custom input text box and saves it to Ntext. Next Ntext is tested if it is > 40 characters. If it is the text is chunked to fit as well as possible into that space by each word. This is done by seeking forward until the maxsize (40) is reached and then searching for the next space and inserting a newline character. This method prevents code from breaking if the user inputs a word greater than 40 chars. Finaly this edited string is sent to update English and Scratch labels.  
        maxsize = 40
        Ftext = chunkText(Ntext, maxsize)

        Scratch.config(text=Ftext)
        English.config(text=Ftext)  

    #scrollbar = Scrollbar(content_frame, orient="vertical", command=content_frame.yview)
    #https://www.tutorialspoint.com/implementing-a-scrollbar-using-grid-manager-on-a-tkinter-window 

    BpaddingX = 20
    elements = {}
    WindowInnerWithMenuBuilder(inner=[
        TextBuilder( # entry textbox
            height = 3, width = 71,background=Theme[6],
            key='Input',geometry=Grid(column=0,row=1, columnspan=8)
        ),
        LabelBuilder( # english display
            text='',font=('arial',20), #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
            bg=Theme[0],fg=Theme[0],
            key='English',geometry=Grid(column=0,row=2,columnspan=8)
        ),
        LabelBuilder( # scratch display
            text='',font=('avali scratch',30),
            background="white",foreground=Theme[2],borderwidth="10px",
            key='Scratch',geometry=Grid(column=0,row=3,columnspan=8)
        ),
        FrameBuilder(
            children=[
                ButtonBuilder(text="Hide English",command=lambda: setCoverEnglish.toggle(),relief=SUNKEN,**buttonstyle,key='switch1',geometry=Grid(column=0,row=0)),
                ButtonBuilder(text="Hide Table",command=lambda: setCoverTable.toggle(),relief=SUNKEN,**buttonstyle,key='switch2',geometry=Grid(column=0,row=1)),
            ],geometry=Grid(column=7,row=2)
        ),
        FrameBuilder(
            background=Theme[0],children=[
                ButtonBuilder(text="Custom Input",command=lambda: setUserWord(),**buttonstyle,geometry=Grid(column=0,row=0,padx=BpaddingX)),
                ButtonBuilder(text="4 letter word",command=lambda: setRandWord(0),**buttonstyle,geometry=Grid(column=1,row=0,padx=BpaddingX)),
                ButtonBuilder(text="6 letter Word",command=lambda: setRandWord(1),**buttonstyle,geometry=Grid(column=2,row=0,padx=BpaddingX)),
                ButtonBuilder(text="Sentence",command=lambda: setRandWord(2),**buttonstyle,geometry=Grid(column=3,row=0,padx=BpaddingX)),
                ButtonBuilder(text="Paragraph",command=lambda: setRandWord(3),**buttonstyle,geometry=Grid(column=4,row=0,padx=BpaddingX)),
                ButtonBuilder(text="Number",command=lambda: setRandWord(4),**buttonstyle,geometry=Grid(column=5,row=0,padx=BpaddingX)),
            ],geometry=Grid(column=0,row=0,columnspan=8)
        ),
        LabelBuilder(
            image=ReferenceImg,
            width=895,height=61,
            background=Theme[2],
            key='Reference',geometry=Grid(column=0,row=4,columnspan=8),
        ),
    ]).build(Twin, elements)

    cInput = elements['Input']
    English = elements['English']
    Scratch = elements['Scratch']
    refimg = elements['Reference']
    switch1 = elements['switch1']
    switch2 = elements['switch2']

    setCoverEnglish(GO.readIniBool('Translation', 'EnglishView'))
    setCoverTable(GO.readIniBool('Translation', 'TableView'))

    def enterHandler():
        setUserWord()
        return 'break'
    cInput.bind("<Return>",lambda event: enterHandler())
    #content_frame.bind("<Configure>", lambda e: content_frame.configure(scrollregion=content_frame.bbox("all"))) # i assume this is for the scrollbar?

    Twin.mainloop()
    
def createCreditsWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the credits window. Relevent support files: None
    Cwin = createWin2('C', 'Avalian Translation Credits')
    if Cwin is None:
        return False # nope

    WindowInnerWithoutMenuBuilder(inner=[
        LabelBuilder(
            text="Programed by Renauli Snow (Ralsdoge) for the community.\n"
                 "Version 1 in development from 11/23/2024 to 7/13/2025.",
            font=('arial',16),**textstyle,geometry=Grid(column=0,row=0)
        ),
        LabelBuilder(
            text="I hope some birbs can find some fun or use in this.\n"
                 "You can contact me regarding this software via\n"
                 "Telegram @RenauliSnow.\n\n"
                 "A deep thanks goes to everyone in this community for\n"
                 "perpetuating this amazing species. For their specific\n"
                 "contributions to this project thank you to the following:\n",
            justify='left',font=('arial',16),**textstyle,geometry=Grid(column=0,row=1)
        ),
        LabelBuilder(
            text=" • Cutesune (RyuujinZero) for creating the Avali Species\n"
                 " • Avali A Comprehensive Guide: Todd Avali\n"
                 " • Scratch Font: Icebelly and Someguynameddavid\n"
                 " • Avali Number System: Ceital Tesai\n"
                 " • Avali HD Icon: tikitree2\n\n"
                 "For presenting me the joys of this community:\n"
                 " • FelisRandomis\n"
                 " • RitualNeo\n"
                 " • Randomking1423\n"
                 " • And many, many others. ",
            font=('arial',16),justify='left',**textstyle,geometry=Grid(column=0,row=2)
        ),
        LabelBuilder(
            text="\nThis project is licensed under the GNU General Public License v3 (GPLv3).",
            font=('arial',14),**textstyle,geometry=Grid(column=0,row=3)
        ),
        LabelBuilder(
            text="Forked by RbCaVi on 8/20/2026. Changes: improved numbers window, fixed some spelling errors.",
            font=('arial',14),**textstyle,geometry=Grid(column=0,row=4)
        ),
    ]).build(Cwin, None)

    Cwin.mainloop()

def createOptionsWin(): #This function contains all of the tkinter widgets and functions necessary to be defined before them in order to create the font translation window. Relevent support files: settings.ini,
    Owin = createWin2('O', 'Avalian Translation Options')
    if Owin is None:
        return False # nope

    def setTheme(ThemeName):
        if ThemeName == '':
            return False # put a real theme next time
        if GO.retrieveTheme(ThemeName, 1):
            GO.writeIni("Theme","setTheme",ThemeName)
            GO.infoMsg('Success','Your theme has been updated, please restart the application!')
        else: 
            GO.infoMsg('Failure','Your theme has NOT been updated, your input is outside of the range of possible selctions for themes.') # there is no way

    offoptions = {'relief':FLAT,'bg':Theme[6],'activebackground':Theme[6],'state':NORMAL}
    onoptions = {'relief':RAISED,'bg':Theme[2],'activebackground':Theme[2],'state':DISABLED}
    def togglebuilder(setfunc, geometry):
        def build(root, table):
            @toggleable
            def setfunc2(state):
                if state:
                    LSButton.config(**offoptions)
                    RSButton.config(**onoptions)
                else:
                    LSButton.config(**onoptions)
                    RSButton.config(**offoptions)
                setfunc(state)
            toggleSwitch = Frame(root,highlightbackground=Theme[1],highlightthickness=3)
            LSButton = Button(toggleSwitch,text='   ',command=lambda: setfunc2.toggle())
            RSButton = Button(toggleSwitch,text='   ',command=lambda: setfunc2.toggle())
            LSButton.grid(column=0,row=0)
            RSButton.grid(column=1,row=0)
            geometry.manage(toggleSwitch)
            setfunc.toggleset = setfunc2
            return toggleSwitch
        return build

    def setDirection(vert):
        GO.writeIni('Numbers', 'HV', vert)

    def setClampingChars(CCStr):
        GO.writeIni('Pronunciation', 'Cchars', CCOptions.index(CCStr))

    def setNpron(HPStr):
        GO.writeIni('Pronunciation', 'Hpronchars', HPOptions.index(HPStr))

    def setWindowsUnmanaged(wu):
        global WindowsUnmanaged
        WindowsUnmanaged = wu
        GO.writeIni('Windows', 'Unmanaged', wu)

    def setECover(ecover):
        GO.writeIni('Translation', 'EnglishView', ecover)

    def setTCover(tcover):
        GO.writeIni('Translation', 'TableView', tcover)
    
    #Creating Objects:

    offoptions = {'relief':FLAT,'bg':Theme[6],'activebackground':Theme[6],'text':'   '}
    onoptions = {'relief':RAISED,'bg':Theme[2],'activebackground':Theme[2],'text':'   '}

    CCOptions = ['Last Used'] + ClampingCharsOptions
    HPOptions = ['Last Used'] + HpronOptions

    ThemeVar = StringVar()
    NpronVar = StringVar()
    ClampingCharsVar = StringVar()


    WindowInnerWithMenuBuilder(inner=[
        LabelBuilder(text="Options",font=('arial',20),**textstyle,geometry=Grid(column=0,row=0)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="Dark, Light, & Custom Themes",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text="Change the theme of the app. Enter 1 for Light and 2\nfor Dark. Make your own custom themes in 'settings.ini'.",font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            FrameBuilder(highlightbackground=Theme[1],highlightthickness=3,children=[
                OptionMenuBuilder(ThemeVar, *GO.retrieveThemeList(), command = setTheme, **buttonstyle, geometry=Grid(column=0,row=0)),
            ],geometry=Grid(column=3 ,row=0)),
        ],geometry=Grid(column=0,row=1)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="Number Canvas Orientation     ",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text="Sets if Number Canvas is set horizontally or vertically\nby default on opening.",font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            togglebuilder(setDirection, geometry = Grid(column=3,row=0)),
        ],geometry=Grid(column=0,row=2)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="New Window Open Option        ",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text="Sets if new windows are managed (only one of each type\nopen at a time) or unmanaged (Open as many as you\nwould like at once).",font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            togglebuilder(setWindowsUnmanaged, geometry = Grid(column=3,row=0)),
        ],geometry=Grid(column=0,row=3)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="Pronunciation Clamping Chars. ",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text="Sets your default selction for the Pronunciation\nclamping characters. i.e. [] or ()",font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            FrameBuilder(highlightbackground=Theme[1],highlightthickness=3,children=[
                OptionMenuBuilder(ClampingCharsVar, *CCOptions, command = setClampingChars, **buttonstyle, geometry=Grid(column=0,row=0)),
            ],geometry=Grid(column=3 ,row=0)),
        ],geometry=Grid(column=0,row=4)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="N Pronuciation Replacement Chars.",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text='Sets your default selction for the Pronuciation\nof the letter "n". i.e. a short pause or "hthk".',font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            FrameBuilder(highlightbackground=Theme[1],highlightthickness=3,children=[
                OptionMenuBuilder(NpronVar, *HPOptions, command = setNpron, **buttonstyle, geometry=Grid(column=0,row=0)),
            ],geometry=Grid(column=3 ,row=0)),
        ],geometry=Grid(column=0,row=5)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="Hide English Display     ",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text="Sets if the original English text is hidden\nby default on opening.",font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            togglebuilder(setECover, geometry = Grid(column=3,row=0)),
        ],geometry=Grid(column=0,row=6)),
        FrameBuilder(background=Theme[0],children=[
            LabelBuilder(
                text="Hide Translation Table     ",font=('arial',16),**textstyle,
                geometry=Grid(column=0,row=0)
            ),
            LabelBuilder(
                text="Sets if the translation table is hidden\nby default on opening.",font=('arial',10),**textstyle,
                geometry=Grid(column=0,row=1,columnspan=2)
            ),
            togglebuilder(setTCover, geometry = Grid(column=3,row=0)),
        ],geometry=Grid(column=0,row=7)),
    ]).build(Owin, None)

    ThemeVar.set(ThemeName)
    setDirection.toggleset(GO.readIniBool('Numbers', 'HV'))
    ClampingCharsVar.set(CCOptions[GO.readIniChecked('Pronunciation', 'Cchars', 6)])
    NpronVar.set(HPOptions[GO.readIniChecked('Pronunciation', 'Hpronchars', 5)])
    setWindowsUnmanaged.toggleset(WindowsUnmanaged)
    setECover.toggleset(GO.readIniBool('Translation', 'EnglishView'))
    setTCover.toggleset(GO.readIniBool('Translation', 'TableView'))

    Owin.mainloop()

def createNumbersWin():
    Nwin,content_frame = createWin('N', 'Avalian Number Translation')
    if Nwin is None:
        return False # nope
    
    panel = Canvas(content_frame, bg=Theme[0])

    @toggleable
    def setDirection(vert):
        if vert: #Vertical
            panel.config(width=100, height=600)
            panel.grid(column=0,row=0,columnspan=1,rowspan=5) #long mode
        else: #Horizontal 
            panel.config(width=800, height=100)
            panel.grid(column=0,row=5,columnspan=5,rowspan=1) #Wide mode
        writeNumber(2, 2, lastManifest, vert)

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

    lastManifest = []
    def writeNumber(x,y,manifest,vert): #write full number to canvas
        nonlocal lastManifest
        lastManifest = manifest
        #add vertical option
        panel.delete('all') # delete all previous images to avoid memory leak
        centerlineH = 92 #maxHeight of tallest img in set
        centerlineW = 60 #maxWidth of widest img in set
        if not vert: #Horizontal
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
        
        writeNumber(2,2,manifest,setDirection.state)
    
    def updateNumber():
        userIn = userInput.get("1.0",END)
        print('user input:', userIn)
        try:
            try:
                userIn = int(userIn)
            except ValueError: # not an integer, maybe a float?
                userIn = round(float(userIn), 6)
                # error here propagates to the outer try block
                # because the number is not valid
            #print(type(userIn))
            #validate
            #print('VERT: ',setDirection.state)
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
            if setSign.state == 1: #add -
                randomNum = -randomNum
                #print(randomNum,'negative:',randomNum)
            elif setSign.state == 2:
                if random.randint(1,100) >= 46: #45/55 negative/positive # why not even 50/50?
                    #add -
                    randomNum = -randomNum
                    #print(randomNum,'negative:',randomNum)
            else:
                pass
            newNumber(randomNum)
        else:
            pass
    
    @toggleable(values = (0, 1, 2))
    def setSign(neg):
        #Random Number Negative chance
        if neg == 0:
            NegativeState.config(text='Positive')
        elif neg == 1:
            NegativeState.config(text='Negative')
        elif neg == 2:
            NegativeState.config(text='Neg & Pos')
    
    @toggleable
    def setBase10Display(b10Cover):
        #Hide unhide base 10 display
        if b10Cover:
            b10EnglishDisp.config(background=Theme[1])
            b10EnglishDispButton.config(text='Unhide')
        else:
            b10EnglishDisp.config(background=Theme[0])
            b10EnglishDispButton.config(text='Hide')
    
    @toggleable
    def setBase12Display(b12Cover):
        #Hide unhide base 12 displays
        if b12Cover:
            b12EnglishDisp.config(background=Theme[1])
            b12EnglishDispButton.config(text='Unhide')
        else:
            b12EnglishDisp.config(background=Theme[0])
            b12EnglishDispButton.config(text='Hide')

    util_frame = Frame(content_frame, background=Theme[0],borderwidth= '12px')
    random_frame = Frame(content_frame, background=Theme[0],borderwidth= '12px')
    ###Title + Support
    Title = Label(content_frame,text='Avalian Base 12 System',font=('arial',18),**textstyle)
    
    ###Random Interface
    RandLabel = Label(random_frame,text='Random Num. Gen.',font=('arial',14),**textstyle)
    MaxSize = Scale(random_frame, from_=0, to=1000,orient = "horizontal",**textstyle) #Slider 
    MinSize = Scale(random_frame, from_=0, to=1000,orient = "horizontal",**textstyle) #Slider
    DecimalLength = Scale(random_frame, from_=0, to=10,orient = "horizontal",**textstyle) #Slider
    DecimalLengthLabel = Label(random_frame,text="Decimal Length",font=('arial',10),**textstyle)
    DecimalLengthWarning = Label(random_frame,text="(Not added yet, confused\non how it'd work)",font=('arial',10),**textstyle)
    MaxSizeLabel = Label(random_frame,text='Max Size',font=('arial',10),**textstyle)
    MinSizeLabel = Label(random_frame,text='Min Size',font=('arial',10),**textstyle)
    MaxSize.set(125)
    MinSize.set(20)
    DecimalLength.set(1)
    NegativeState = Button(random_frame,text='Positive',command=lambda:setSign.toggle(),**buttonstyle) #whether to generate negative numbers or not
    randomNumGo = Button(random_frame,text='Submit',command=lambda:randomizeNumber(),**buttonstyle) #submit random num
    def enterHandler(event):
        updateNumber()
        return "break"
    ###Options###
    userInput = Text(util_frame,width=30,height=1,bg=Theme[6]) #User in Textbox
    userInput.bind("<Return>",enterHandler)

    userInGo = Button(util_frame,text='Submit',command=lambda:updateNumber(),**buttonstyle) #submit user input from Userinput (Valideate)
    base10Label = Label(util_frame,text='Base-10:',font=('arial',10),**textstyle)
    base12Label = Label(util_frame,text='Base-12:',font=('arial',10),**textstyle)
    b12EnglishDisp = Label(util_frame,text=0,font=('arial',12), **textstyle) #Base12 number display in english
    b10EnglishDisp = Label(util_frame,text=0,font=('arial',12), **textstyle) #Base10 number display in english
    b10EnglishDispButton = Button(util_frame,text='Hide',command=lambda:setBase10Display.toggle(),**buttonstyle) 
    b12EnglishDispButton = Button(util_frame,text='Hide',command=lambda:setBase12Display.toggle(),**buttonstyle) 
    HVButton = Button(util_frame,text='Horizontal/Vertical',command=lambda:setDirection.toggle(),**buttonstyle)#Horizontal Vertical numbering toggle
    HVdescription = Label(util_frame,text="Swich between formal vertical structure and casual horizontal display.",**textstyle) 
    ###
    
    #Load settings
    setDirection(GO.readIniBool("Numbers","HV")) #read the options

    setSign(0)
    setBase10Display(False)
    setBase12Display(False)

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
    Pwin,content_frame = createWin('P', 'Avalian Pronunciation')
    if Pwin is None:
        return False # nope

    Ntext = ''
    ###Functions
    def setRandWord(category):
        changeText(GRC.ChallengeRandSample(category))
    def setUserWord():
        changeText(cInput.get("1.0", "end-1c"))
    lasttext = ''
    def updateWord():
        changeText(lasttext)
    def changeText(Ntext):
        nonlocal lasttext
        lasttext = Ntext
        maxsize = 70
        English.config(text=chunkText(Ntext, maxsize))
        EnglishO.config(text=chunkText(AP.pronounciationDisp(Ntext,Hdropclicked.get(),ClampingCharsSelected.get()), maxsize))
    def setHpron(Hpron):
        GO.writeIni('Pronunciation', 'LastH', HpronOptions.index(Hpron))
        updateWord()
    def setClampingChars(ClampingChars):
        GO.writeIni('Pronunciation', 'LastC', ClampingCharsOptions.index(ClampingChars))
        updateWord()

    ###Labels
    PronunciationTableHead = Label(content_frame,text='Unpronounceable Characters',font=('arial',20), **textstyle)
    PronunciationDesc = Label(content_frame,text='Try speaking like an Avali. Avali are thought to be unable to pronounce the\nfollowing characters due to the lack of a nasal cavity. (Todd\'s Avali Lore Guide)',font=('arial',14), **textstyle)
    SpecialCharsStr = ''
    SpecialReplaceStr = ''
    for c in AP.specialpronchars:
        SpecialCharsStr += '  '+c.upper()+' =\n'
    for r in AP.replacements:
        SpecialReplaceStr += r+'\n'
    ##Objects
    
    NpronLabel = Label(content_frame,text="N Pronunciation:",font=('arial',14),**textstyle)
    ClampingLabel = Label(content_frame,text="Clamping Characters:",font=('arial',14),**textstyle)
    UPronounceChars = Label(content_frame,text=SpecialCharsStr,font=('arial',16),**textstyle)
    RPronounceChars = Label(content_frame,text=SpecialReplaceStr,font=('arial',16),**textstyle)
    ##Dropdowns
    #HPron
    Hdropclicked = StringVar()
    Ndropbutton = OptionMenu( content_frame, Hdropclicked, *HpronOptions, command=setHpron)
    Ndropbutton.config(**buttonstyle) 
    #Ndropbutton.config(bg=Theme[0])
    #ClampingChars
    ClampingCharsSelected = StringVar()
    ClampingCharsButton = OptionMenu(content_frame, ClampingCharsSelected, *ClampingCharsOptions, command=setClampingChars)
    ClampingCharsButton.config(**buttonstyle) 
    #Load settings
    CC = GO.readIniChecked("Pronunciation","Cchars",6,2) #read the options # 2 is the second option - short pause (-) # because 0 is use last set
    if CC == 0:
        #print('Read CC = 0')
        clampingcharsindex = GO.readIniChecked("Pronunciation","LastC",5,1) #read the options # 1 is the second option - short pause (-)
    else: #Default set, set it.
        #print('Read CC =',str(CC-1))
        clampingcharsindex = CC-1
    ClampingCharsSelected.set(ClampingCharsOptions[clampingcharsindex])
    HP = GO.readIniChecked("Pronunciation","Hpronchars",5,2) #read the options # 2 is the second option - [] brackets # because 0 is use last set
    if HP == 0: #
        #print('Read HP = 0')
        hpronindex = GO.readIniChecked("Pronunciation","LastH",4,1) #read the options # 1 is the second option - [] brackets
    else: #
        #print('Read HP =',str(HP-1))
        hpronindex = HP-1
    Hdropclicked.set(HpronOptions[hpronindex])
    #End Load settings

    ##
    English = Label(content_frame,text='',font=('arial',10),**textstyle) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    EnglishO = Label(content_frame,text='',font=('arial',20),**textstyle) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    #switch = Button(content_frame,text="minimize")#,command=lambda: )
    Option0 = Button(content_frame,text="4Word",command=lambda: setRandWord(0),**buttonstyle)
    Option1 = Button(content_frame,text="6Word",command=lambda: setRandWord(1),**buttonstyle)
    Option2 = Button(content_frame,text="sent.",command=lambda: setRandWord(2),**buttonstyle)
    Option3 = Button(content_frame,text="para.",command=lambda: setRandWord(3),**buttonstyle)
    Option4 = Button(content_frame,text="numb.",command=lambda: setRandWord(4),**buttonstyle)
    Option22 = Button(content_frame,text="Custom",command=lambda: setUserWord(),**buttonstyle)
    def enterHandler(event):
        setUserWord()
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
    Mwin,content_frame = createWin('M', 'Avalian Translation Software (RbCaVi Fork)')
    if Mwin is None:
        return False # nope

    Title = Label(content_frame,font=('Helvetica 30 italic'),text="Avalian Translation Software",background=Theme[0],foreground=Theme[3])
    Preface = Label(content_frame,font=('Helvetica 18 italic'),text="By: Renauli Snow",background=Theme[0],foreground=Theme[3]) #Aw du Bub du day. Bah.. Blep.
    mainbuttonstyle = {'background':Theme[2], 'foreground':Theme[1], 'activebackground':Theme[4], 'activeforeground':Theme[5]}
    Option0 = Button(content_frame,font=('Helvetica 18 italic'),text="  Credits  ",command=createCreditsWin,**mainbuttonstyle)
    Option1 = Button(content_frame,font=('Helvetica 18 italic'),text="  Options  ",command=createOptionsWin,**mainbuttonstyle)
    Option2 = Button(content_frame,font=('Helvetica 18 normal'),text="Font Translation",command=createFontTranslationWin,**mainbuttonstyle)
    Option3 = Button(content_frame,font=('Helvetica 18 normal'),text="Avalian Numbers",command=createNumbersWin,**mainbuttonstyle)
    Option4 = Button(content_frame,font=('Helvetica 18 normal'),text="Pronunciation",command=createPronunciationWin,**mainbuttonstyle)
    ##db349c
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