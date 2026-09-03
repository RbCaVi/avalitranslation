#This file's purpose is to provide support to the numbers tab in the application. It handles image fetching and base conversion.

def itob12(n): # convert an integer to a list of base 12 digits
    if n == '':
        return []
    n = int(n)
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % 12)
        n //= 12
    digits.reverse()
    return digits

def inc12(ds): # increment a list of base 12 digits
    # basically walk backwards from the end
    # if the digit is 11, increment to 0 and iterate again (carry)
    # if the "digit" is '.', skip
    # otherwise increment the digit and return
    ds = [*ds] # copy ds
    i = len(ds) - 1
    while ds[i] == 11 or ds[i] == '.':
        if ds[i] == 11:
            ds[i] = 0
        i -= 1
    ds[i] += 1
    return ds

# ok let's try somethng else
# precision math
# pass a string
# convert the integer part as normal
# use integer math instead of float math for the decimal part
# multiply by 12
# divmod by a power of 10

def base12numberConvert(num): #Converts base 10 numbers into base 12 numbers.  Working on support for decimal. v2! To support A B extra characters since I never did that originaly??
    print('base10:',num)
    if '.' in num: # decimal
        iNum,dNum = num.split('.')
        result = itob12(iNum)
        result.append('.')
        if len(dNum) != 0:
            # take the length of dNum as the power
            top = 10 ** len(dNum)
            d10 = int(dNum)
            for i in range(12):
                print(top, d10)
                d10 *= 12
                digit,d10 = divmod(d10, top)
                result.append(int(digit))
            if d10 * 2 >= top: # round up
                result = inc12(result)
            while result[-1] == 0: # remove trailing zeros
                result.pop()
    else: # no decimal (integer)
        result = itob12(num)

    print('base12:',result)
    return(result)

def toAB(n):
    return {10: 'A', 11: 'B'}.get(n, n) # key n / default n

def subB12num(num):
    return("Anum"+str(num))

def superB12num(num):
    return("Amod"+str(num*12))

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
# Maybe instead of trying to decode to base10 try converting to base 12 sounds obvious.

# ----------------- Images Test Group -----------------
#print(base12ImageRef(base12numberConvert(1372521)))
#print(base12ImageRef(base12numberConvert(144))) # ['Amod12', 'Amod0', 'Anum0']
#isplit: [1, 0, 0] #['Amod12', 'Amod0', 'Anum0']
#print(base12ImageRef(base12numberConvert(36))) #['Amod36', 'Anum0']
#print(base12ImageRef(base12numberConvert(13))) #['Amod12', 'Anum1']
#Rules to implement:
#if evenly divisible dont use only modx should use mod(x-1),Anum12
#if 
# Drop leading zeros 
#I understand now. The number system is directly analagous to B12 reprentation, why did i not see it before
#[5, 6, 2, 3, 4, 9]
#[12x5,12x6,12x2]'''

def uncarry12(b12): # zeros borrow 12 from the digit to their left
    # walk backwards from the end again
    # if the digit is 0, change to 12 and decrement the digit to the left (unless this is the first digit)
    # if the digit is -1 (from a decrement), change to 11 and decrement the digit to the left
    # split decimal part and handle separately (?)
    # i'm assuming this applies to all digits, not just the last two

    if b12 == [0]:
        return b12

    b12 = [*b12] # copy b12

    while b12[0] == 0: # remove leading zeros if they were given for some reason
        b12.pop(0)

    if '.' in b12:
        end = b12.index('.')
    else:
        end = len(b12)

    for i in reversed(range(1, end)): # the 1 can be changed to max(1, end - 2) for the old behavior
        if b12[i] == 0 or b12[i] == -1:
            b12[i] += 12
            b12[i - 1] -= 1

    if b12[0] == 0: # remove the possible leading zero from uncarrying a first digit of 1
        b12.pop(0)

    return b12

def base12ImageRef(b12,negative): #reworkedImageRef finisged 5/28/2025
    #if less than 144
        #match with numbers until total is 0
        #at any time if total is =< 12 then add the final image as number image.
    #else
        #match base to
    print('------',b12,'-->',uncarry12(b12),'------')
    b12 = uncarry12(b12)
    if '.' in b12: # twelvimal (dodecimal) point
        print(b12, 'has a decimal :)')
        i = b12.index('.')
        b12,d12 = b12[:i], b12[i + 1:]
        print('split into', b12, d12)
    else:
        d12 = None
    result = []
    if negative:
        result.append('Negative')
    if len(b12) > 0:
        for d in b12[:-1]: # all but the last
            result.append(superB12num(d))
        result.append(subB12num(b12[-1]))
    print('d12 is', d12)
    if d12 is not None:
        result.append('Decimal')
        # i don't know how twelvimal display works
        # apparently the same way??? weird
        # what about repeating twelvimals like 0.1111... (1 / 11)
        # we use a bar
        # idk i could round or ... for now
        # or a bar
        # or brackets like 1 / 5 = 0.[2497]
        # but that has to be returned from base12numberConvert()
        if len(d12) > 0:
            for d in d12[:-1]:
                result.append(subB12num(d))
            result.append(subB12num(d12[-1]))
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