import random
import string
import glob, os, os.path

def generateDocs():
    filelist = glob.glob(os.path.join('docs', "*.txt"))
    for f in filelist:
        os.remove(f)

    rand_list = ["A","B","C","D","E",'1','2','3','4','5']
    # rand_list = string.ascii_uppercase + ['1','2','3','4','5']

    numOfDocs = 5
    for i in range(numOfDocs):
        f = open(".\\docs\\"+ str(i+1) +".txt", "x") 
        f.write(''.join( random.choices(rand_list, k=random.randrange(10, 20, 1)) ))
        f.close()

generateDocs()
