specialpronchars = ['f','F','j','J','n','N','v','V']
replacements = ['y-ah','bu','short pause or "ha" sound','hthk'] #
#abcde ghi klm opqrstu wxyz  Present
#    f    j   n       v      Missing

#functions


def pronounciationDisp(ntext,npron,clampingchars):
    Npron = npron.split(' ') 
    Npron = Npron[len(Npron)-1].replace('(','').replace(')','')
        #
    ClampingChars = clampingchars.split('" (')
    ClampingChars = ClampingChars[0].replace('"',"").split('-')
    ClampingCharL,ClampingCharR = ClampingChars
    #print(ClampingCharL)
    #print(ClampingCharR)
    #print("Npron:",Npron)
    #rint("Executing...")
    replacements2 = replacements.copy()
    replacements2[2] = Npron
    replacementdict = { # this might be slower idk
        c:ClampingCharL + r + ClampingCharR for c,r in zip('fjnv', replacements2) for c in (c.upper(), c.lower())
    }
    return(''.join(replacementdict.get(letter, letter) for letter in ntext))

#pronounciationDisp("f j n v ",'Short Pause (-)','"{-}"(Curvy Brackets)')
#pronounciationDisp("The quick brown fox jumped over the lazy frog.")
