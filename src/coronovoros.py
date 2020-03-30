def indentifierTable(filename):    
    f = None
    try:
        f = open(filename, 'r')
    except:
        print("Error: can\'t open input file!")
        return