from tkinter import messagebox
import os, sys
import re
def absolute_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    if getattr(sys, 'frozen', False):  # running as .exe
        return os.path.join(os.path.dirname(sys.executable),relative_path)

    else:  # running as .py
        return relative_path

def errorMsg(Title,Desc):  #Error: 
    messagebox.showerror(Title,Desc)
def infoMsg(Title,Desc): #Info
    messagebox.showinfo(Title, Desc)

# match a section of at least one character surrounded by brackets # spaces are probably ignored
sectionregex = '\\s*\\[\\s*(?P<section>\\w+)\\s*\\]\\s*'

# match an initial part consisting of an attribute name and an equals sign (with optional spaces)
# then any text
# then an optional comment starting with //
lineregex = '(?P<initial>\\s*(?P<attribute>\\w+)\\s*=\\s*)(?P<value>.*?)(?P<final>\\s*(//.*)?)'

def writeIni(Rsection,Ratribute,Rvalue):
    with open("settings.ini", "r") as file:
        rawData = file.read()
    rawDataS = rawData.splitlines()
    curSection = ""
    count = 0

    lines = enumerate(rawDataS) # lines is an iterator instead of a plain list, so the position in the lines is saved between the loops
    foundsection = False
    for i,line in lines:
        m = re.fullmatch(sectionregex, line)
        if m is not None:
            if m['section'] == Rsection:
                foundsection = True
                break # i could nest it, but i don't want 5 levels of indents
    if foundsection:
        # found a matching section
        # lines starts at the first line in section now
        # search for a matching attribute
        foundattribute = False
        for i,line in lines:
            m = re.fullmatch(lineregex, line)
            if m is not None and m['attribute'] == Ratribute:
                # found it
                rawDataS[i] = m['initial'] + str(Rvalue) + m['final']
                foundattribute = True
                break
            if re.fullmatch('\\s*\\[\\s*(?P<section>\\w+)\\s*\\]\\s*', line) is not None: # oops we're in the next section
                break
        else: # the loop went to the end of lines # i is the last valid index # i want it to be one more to insert the new attribute after the end
            i += 1
        if not foundattribute:
            # didn't find a matching attribute, add it
            # i will either be the index of the line containing the next section marker
            # or the index of the (non existent) line past the end of the file
            infoMsg('settings.ini Attribute Created', 'The missing attribute ' + Ratribute + ' in the section ' + Rsection + ' in settings.ini was created.')
            rawDataS.insert(i, Ratribute + '=' + Rvalue)
    else:
        # there was no matching section, add it at the end
        # this could happen if a user creates an empty settings.ini file
        infoMsg('settings.ini Section Created', 'The missing section ' + Rsection + ' in settings.ini was created.')
        rawDataS.append('[' + Rsection + ']')
        rawDataS.append(Ratribute + '=' + Rvalue)

    # write the content back to settings.ini
    with open("settings.ini", "w") as file:
        file.write('\n'.join(rawDataS))

def readIni(Rsection,Ratribute): #read the ini file and return value and line
    with open("settings.ini", "r") as file:
        rawData = file.read()
    rawDataS = rawData.splitlines()
    lines = iter(rawDataS) # lines is an iterator instead of a plain list, so the position in the lines is saved between the loops
    foundsection = False
    for line in lines:
        m = re.fullmatch(sectionregex, line)
        if m is not None:
            if m['section'] == Rsection:
                foundsection = True
                break
    if foundsection:
        # found a matching section
        # lines starts at the first line in section now
        # search for a matching attribute
        foundattribute = False
        for line in lines:
            m = re.fullmatch(lineregex, line)
            if m is not None and m['attribute'] == Ratribute:
                # found it
                return m['value']
                break
            if re.fullmatch('\\s*\\[\\s*(?P<section>\\w+)\\s*\\]\\s*', line) is not None: # oops we're in the next section
                break
    # nothing was found - i could copy the code from writeIni()
    # but maybe just show a message and set it to a default value?
    # idk
def exitPrgrm():
    sys.exit()
def resetini():
    debug = 0 #If set to 1 then it bypasses this func when its called.
    if debug == 1:
        print('DEBUG MODE ON resetini() line 134')
        return 'debug'
    iniBackup = '''[Theme]
//Dont be deterred by the amount of colors you need to choose, I just wanted to ensure full customizability. Most should be quite similar to another
setTheme=Light
    Light=[#f0f0f0,#000000,#fc850f,#000000,#ff3419,#fffafa,#d3d3d3,#ffffff,#f0f0f0,#000000] //1
    Dark=[#1f1f1f,#ffffff,#fc850f,#ffffff,#ff3419,#fffafa,#d3d3d3,#ffffff,#f0f0f0,#000000] //2
customTheme1=[#5f1352,#ffffff,#ffffff,#ffffff,#ffffff,#2de2aa,] 
    TestTheme=[#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7]
    customTheme=[] //Main, Text, Accent, Accent Text, ActiveAccent, ActiveAccentText, Textbox, Icons, Button/Menu, Contrasting Button/Menu Text
[Translation]
TableView = 0 //0-1 Visible by default
EnglishView = 1 //0-1 Visible by default
[Pronunciation]
Hpronchars=0 //0-5
Cchars=0 //0-6
LastH=0 //0-4
LastC=0 //0-5
[Numbers]
HV=0 //Horizontal&Vertical 0&1 respectivly'''
    eraseProtect=0
    status='Clear'
    try:
        os.rename("settings.ini","settingsOLD.ini") # try to rename the settings file
    except FileNotFoundError:
        # it did not exist # it will be created below this try/except block
        infoMsg('settings.ini Created', '"settings.ini" file did not exist. A new one was created automatically.') # notify the user of this development
    except:
        # something else went wrong # probably settingsOLD.ini already existed
        errorMsg('Errpr', e + 'Please empty settingsOLD.ini of wanted data before deleting.') #store error for reporting
        return # do not write the file
    with open("settings.ini", "w") as file: #if successful in renaming or settings.ini did not exist, create a new settings.ini file
        file.write(iniBackup) #and populate it
    #save old file as settingsOLD.ini  #check availibility of .old
    #Restore original .ini with hardcoded backup in this function

def verifyiniIntegrity():
    debug = 0 #If set to 1 then it bypasses this func when its called.
    if debug == 1:
        print('DEBUG MODE ON verifyiniIntegrity() line 165')
        return 'debug'
    status = 'Correct'
    skip = 0
    #Check if file exists 
    try:
        rawData = open("settings.ini").read()#.splitlines()
    except:
        status = '"settings.ini" file did not exist. A new one was created automatically.'
        skip = 1
    if skip == 0:
        #See if it has minimum amount of characters and linescontents
        rawData = open("settings.ini").read()#.splitlines()
        print('Length of "settings.ini":',len(rawData))
        if len(rawData) < 133:
            status = 'File missing info (character count check failed)'
        rawData = rawData.splitlines()
        print('# of lines in "settings.ini":',len(rawData))
        if len(rawData) < 12:
            status = 'File missing info (line count check failed)'
        #Checks go here any descrepancy will be identified and stored in status, then shown in error message
    if status != 'Correct':
        resetini()
        errorMsg('Error opening "settings.ini"',status)
verifyiniIntegrity()

def validateHexCode(index, hexcode):
    hexdigits = '0123456789abcdefABCDEF'
    if len(hexcode) != 7:
        errorMsg("invalidLength","Hex code " + str(index + 1) + " in theme "+str(Theme)+" is an invalid length. There should be a # followed by 6 characters.")
        return False
    if hexcode[0] != '#':
        errorMsg("missingHash","Hex code " + str(index + 1) + " in theme "+str(Theme)+" is missing its hash symbol.")
        return False
    for c in hexcode[1:]:
        if c not in hexdigits: # any but the first character are not hex digits
            errorMsg("invalidCharacter","Hex code " + str(index + 1) + " in theme "+str(Theme)+" contains the invalid character " + repr(c) + ". Hex values should only include the characters 0-9 and A-F.")
            return False
    m = re.fullmatch('#[0-9a-fA-F]{6}', hexcode) # a hash followed by six hexadecimal digits (uppercase or lowercase)
    if m is None:
        errorMsg("invalidHex","Hex code " + str(index + 1) + " in theme "+str(Theme)+" is not valid.") # catch all
    return m is not None

def retrieveTheme(Theme,checkValidity=0): #returns the currently selected theme as a list of hex values by default or validates that a theme is properly formated and alerts the user if not.
    print('retrieving theme ', repr(Theme))
    themeLine = readIni('Theme', Theme)
    if themeLine is None: # there was no theme with that name
        errorMsg("invalidTheme","Theme "+str(Theme)+" does not exist. Check settings.ini for valid theme names.")
        return False
    print('retrieved theme ', repr(themeLine))
    themeLine = themeLine.split("[")
    themeLine = themeLine[1].split("]")
    themeLine.pop(1)
    themeLine = themeLine[0].split(",")
    if checkValidity == True: #with check validity set to 1: 
        if len(themeLine) < 10:
            errorMsg("invalidCodeAmount","One or more hex codes in theme "+str(Theme)+" are not present. There should be 10 html color codes.")
            return False
        if any(not validateHexCode(i,code) for i,code in enumerate(themeLine)):
            return False
        print("Selected Theme",str(Theme),"is valid.")
        return True
    else:
        print("Using Theme",str(Theme)+":",themeLine)
        return themeLine

'''singer = readIni('Numerical','testParamater')
print(singer)
writeIni('Numerical','testParamater','1')
singer = readIni('Numerical','testParamater')
print(singer)'''
#Theme = readIni('Theme','setTheme')
#retrieveTheme(Theme[0],Theme[1],1)