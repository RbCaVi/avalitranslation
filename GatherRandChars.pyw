import random
from GatherOptions import absolute_path,errorMsg
import collections

try:
    #nonlocal rawData
    with open(absolute_path("random.md")) as randomData:
        rawData = randomData.read().splitlines()
except:
    errorMsg('random.md missing','The file "random.md" is missing, please replace random.md or reinstall program.')
    BackupData = "#0-4word\nrandom.md missing\n#1-6word\nrandom.md missing\n#2-Sentences\nrandom.md missing\n#3-Paragraphs\nrandom.md missing\n"
    rawData = BackupData.splitlines()

words = collections.defaultdict(list)

# shuffle a list and return its elements one at a time
# when the list is exhausted, reshuffle
# modifies the original list (shuffles it repeatedly)
def bag(l):
    while True:
        random.shuffle(l)
        yield from l

curType = 'None'
for line in rawData:
    if line == '':
        continue
    if '#' in line:
        curType,_ = line.strip('#').split('-')
    else:
        words[curType].append(line)

samplers = {key:bag(group) for key,group in words.items()}
        
def ChallengeRandSample(type): #line 49
    if str(type) in samplers:
        return next(samplers[str(type)])
    
    return '<blank>'
