def findtext(list, text):
    try:
        import re
        getlen = len(list)
        for i in range(getlen):
            findtext = re.search(text, list[i])
            if findtext:
                break
        if findtext:
            return True
        else:
            return False
    except TypeError:
        return False

def findlog(list, text):
    index = -1
    for i, en in enumerate(list):
        if en == text:
            index = i
            print(index)
            return True
    
    if index == -1:
        return False
def findword(list, word):
    splitlist = []
    getlen = len(list)
    for i in range(getlen):
        String = str(list[i])
        Stringlist = String.split()
        getlen_split = len(Stringlist)
        for i in range(getlen_split):
            splitlist.append(Stringlist[i])
        for i in range(len(splitlist)):
            if isinstance(splitlist[i], str):
                splitlist[i] = splitlist[i].replace('.', '')
                splitlist[i] = splitlist[i].replace(':', '')
    if str(word) in splitlist:
        return True
    else:
        return False
            
    