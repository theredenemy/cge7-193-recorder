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
