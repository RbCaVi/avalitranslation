import random
from GatherOptions import absolute_path,errorMsg
rawData = ""
try:
    #nonlocal rawData
    with open(absolute_path("random.md")) as randomData:
        rawData = randomData.read().splitlines()
except:
    errorMsg('random.md missing','The file "random.md" is missing, please replace random.md or reinstall program.')
    BackupData = "#0-4word\nrandom.md missing\n#1-6word\nrandom.md missing\n#2-Sentences\nrandom.md missing\n#3-Paragraps\nrandom.md missing\n"
    rawData = BackupData.splitlines()
def myFunc(e):
    return e['year']
all = []
workingEvents = []
fourWord = []
sixWord = []
sentences = []
paragraphs = []
numbers = []

# shuffle a list and return its elements one at a time
# when the list is exhausted, reshuffle
# modifies the original list (shuffles it repeatedly)
def bag(l):
    while True:
        random.shuffle(l)
        yield from l

def event(iname,itype):
    item = (itype, iname)
    if itype == '0':
        fourWord.append(iname)
    if itype == '1':
        sixWord.append(iname)
    if itype == '2':
        sentences.append(iname)
    if itype == '3':
        paragraphs.append(iname)
    if itype == '4':
        numbers.append(iname)
        
def ChallengeRandSample(type): #line 49
    if type == 0:
        return(next(SampleList0))
    if type == 1:
        return(next(SampleList1))
    if type == 2:
        return(next(SampleList2))
    if type == 3:
        return(next(SampleList3))
    if type == 4:
        return(next(SampleList4))
    
    return('blank')


curType = 'Unknown'
for line in rawData:
   
    #Pair = line.splitlines()
    #Pair = line.split(':')
    #print(Pair)
    #if ',' in line:
        #Date = Pair[1].split(',')
        #event(Pair[0],Date[0],curType)
    if '#' in line:
        curType = line.strip('#')
        pair=curType.split('-')
        curType = pair[0]
    elif line == '':
        pass
    else:
        event(line,curType)
SampleList0 = bag(fourWord)
SampleList1 = bag(sixWord)
SampleList2 = bag(sentences)
SampleList3 = bag(paragraphs)
SampleList4 = bag(numbers)
#events.sort(key=lambda x: x.order, reverse=False)
#print(len(paragraphs),' items registered')
#for item in all:
#    print(item.read(1))

