import re

specialpronchars = ['v','f','j','n']
replacements = ['hthk','y-ah','bu','short pause or "ha" sound'] #
#abcde ghi klm opqrstu wxyz  Present
#    f    j   n       v      Missing

#functions


def pronounciationDisp(ntext,npron,clampingchars):
    Npron = re.fullmatch('.* \\((.*)\\)', npron)[1]
    ClampingCharL,ClampingCharR = re.fullmatch('"(.?)-(.?)" \\(.*\\)', clampingchars).groups()
    #print(ClampingCharL)
    #print(ClampingCharR)
    #print("Npron:",Npron)
    #rint("Executing...")
    replacementdict = { # this might be slower idk
        c:ClampingCharL + r + ClampingCharR for c,r in zip(specialpronchars, replacements) for c in (c.upper(), c.lower())
    }
    for c in 'nN':
        replacementdict[c] = ClampingCharL + Npron + ClampingCharR
    return(''.join(replacementdict.get(letter, letter) for letter in ntext))

#pronounciationDisp("f j n v ",'Short Pause (-)','"{-}" (Curvy Brackets)')
#pronounciationDisp("The quick brown fox jumped over the lazy frog.")
