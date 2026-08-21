#This file's purpose is to provide support to the numbers tab in the application. It handles image fetching and base conversion.

def itob12(n):
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % 12)
        n //= 12
    digits.reverse()
    return digits

def base12numberConvert(num): #Converts base 10 numbers into base 12 numbers.  Working on support for decimal. v2! To support A B extra characters since I never did that originaly??
    print('base10:',num)
    if "." in str(num):     #seperate decimal
        numList = str(num).split(".")
        iNum = int(numList[0])
        dNum = int(numList[1])
    else:
        iNum = int(num)
        dNum = 0
    result = itob12(iNum)
    #resultAB = result
    #print('resultAB:',resultAB)
    if dNum > 0:
        res = itob12(dNum)
    
        result.append(".")
        result += res
    
    resultAB = result.copy()

    for i in range(len(resultAB)):
        if resultAB[i] == 10:
            resultAB[i] = 'A'
        elif resultAB[i] == 11:
            resultAB[i] = 'B'
        
    print('base12AB:',resultAB)
    #print('base12ABdec:',resultAB)
    print('base12:',result)
    return(resultAB)


def subB12num(num):
    #print('subB12:',num)
    strung = 0
    if num == 'A' or num == 'B' or num == 'C': 
        if num == 'A':
            strung = 10
        if num == 'B':
            strung = 11
        if num == 'C':
            strung = 12
    else: 
        if int(num) > 9:
            return("Num>9")
        strung = str(num)
    result = "Anum"+str(strung)
    return(result)

def superB12num(num):
    #print('superB12:',num)
    strung = 0
    if num == 'A' or num == 'B' or num == 'C': 
        if num == 'A':
            strung = 10
        if num == 'B':
            strung = 11
        if num == 'C':
            strung = 12
    else: 
        if int(num) > 9:
            return("Num>9")
        strung = int(num)
    result = "Amod"+str(strung*12)
    return(result)

'''#print(base12numberConvert(1372521.13))
#print(base12ImageRef(base12numberConvert(1372521)))
#print(base12numberConvert(1372521), '= 562349')
    #6032712 -> 202B1A0
#print(base12numberConvert(6032712), '= 202B1A0' )
#print(base12ImageRef(base12numberConvert(6032712)))
    #124 -> A4
#print(base12numberConvert(124), '= A4')
#print(base12ImageRef(base12numberConvert(124)))
#base12ImageRef(base12numberConvert(5121))

#base12ImageRef(base12numberConvert(1472521))
#Recieved: 5B0B01 #Correct: 5B01A1
#Recieved: 5B0B0 #Correct: 5B01A1
#Recieved: 51A1A1 #Correct: 5B01A1
#Recieved: 5B01A1 #Correct: 5B01A1 #Hooray

#print(base12ImageRef(base12numberConvert(10.101)))
#print(base12ImageRef(base12numberConvert(10.10)))
#print(base12ImageRef(base12numberConvert(11.11)))
#print(base12ImageRef(base12numberConvert(12.12)))
#print(base12ImageRef(base12numberConvert(13.13)))
#print(base12ImageRef(base12numberConvert(14.14)))

#6032712 resultAB: [2, 0, 2, 'B', 1, 'A', 0]
#['Amod24', 'Amod0', 'Amod24', 'Amod132', 'Amod12', 'Amod120', 'Anum0']
#  12*24

#1372521 resultAB: [5, 6, 2, 3, 4, 9] [12*5,12*6,12*2]
# ['Amod60', 'Amod72', 'Amod24', 'Amod36', 'Amod48', 'Anum9']
# 12*5   >    12*6   >   12*2  >   12*3  >   12*4  >    9
# added in sequence == 249
# multiplied in bulk == 1612431360
# multiplied in sequence == 1612431360
# only mods multiplied in sequence == 179159049
# 12*5*5   >    12*6*4   >   12*2*3  >   12*3*2  >   12*4  >    9
# 12*5*5+12*6*4+12*2*3+12*3*2+12*4+9 = 1080345

# 12*11  >  12 added in sequence == 144 b10
# Maybe instead of trying to decode to base10 try converting to basee 12 sounds obvious.

# ----------------- Images Test Group -----------------
#print(base12ImageRef(base12numberConvert(1372521)))
#print(base12ImageRef(base12numberConvert(144))) # ['Amod12', 'Amod0', 'Anum0']
#isplit: [1, 0, 0] #['Amod12', 'Amod0', 'Anum0']
#print(base12ImageRef(base12numberConvert(36))) #['Amod36', 'Anum0']
#print(base12ImageRef(base12numberConvert(13))) #['Amod12', 'Anum1']
#Rules to implement:
#if evenly divisiable dont use only modx should use mod(x-1),Anum12
#if 
# Drop leading zeros 
#I understand now. The number system is directly analagous to B12 reprentation, why did i not see it before
#[5, 6, 2, 3, 4, 9]
#[12x5,12x6,12x2]'''

def base12ImageRef(b10,b12,negitiveSign): #reworkedImageRef finisged 5/28/2025
    #if less than 144
        #match with numbers until total is 0
        #at any time if total is =< 12 then add the final image as number image.
    #else
        #match base to
    print('------',b10,b12,'------')
    result = []
    if negitiveSign == 1:
        result.append('Negative')
    if b10 <= 12:
        print(b10,'<= 12')
        result.append('Anum'+str(b10))
    elif b10 <= 156:
        print(b10,'<= 156')
        remainder = b10 % 12 
        maxdiv = int(b10/12)
        #print('maxdiv',maxdiv)
        #print('remainder',remainder)
        if maxdiv > 1 and remainder == 0:
            #print('maxdiv > 1 and remainder == 0')
            modCall = (maxdiv-1)
            if modCall == 10:
                modCall = 'A'
            if modCall == 11:
                modCall = 'B'
            if modCall == 12:
                modCall = 'C'
            '''numCall = 12
            print('modCall',modCall)
            print('numCall',numCall)'''
            result.append(superB12num(modCall)) #Reduce by 12
            result.append(subB12num("C")) #"add 12"
        else: 
            modCall = maxdiv
            '''numCall = remainder
            print('modCall',modCall)
            print('numCall',numCall)'''
            if modCall == 10:
                modCall = 'A'
            if modCall == 11:
                modCall = 'B'
            if modCall == 12:
                modCall = 'C'
            result.append(superB12num(modCall))
            if remainder == 10:
                remainder = 'A'
            elif remainder == 11:
                remainder = 'B'
            elif remainder == 12:
                remainder = 'C'
            result.append(subB12num(remainder))
    else:
        print(b10,'> 156')
        b12split = list(b12)
        for i in range(len(b12split)):
            if i+1 == len(b12split):
                result.append(subB12num(b12split[i]))
            else:
                result.append(superB12num(b12split[i]))
    print(result)
    return result


'''base12ImageRef(12,10)
base12ImageRef(13,11)
base12ImageRef(36,30)
base12ImageRef(144,100)'''
#base12ImageRef(122,base12numberConvert(122))
#reworkedImageRef(1372521,base12numberConvert(1372521))
# ['Amod60', 'Amod72', 'Amod24', 'Amod36', 'Amod48', 'Anum9']
# ['Amod60', 'Amod72', 'Amod24', 'Amod36', 'Amod48', 'Anum9'] #

#base12numberConvert(12)