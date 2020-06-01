import random
import string
import glob, os, os.path

def generateDocs():
    filelist = glob.glob(os.path.join('docs', "*.txt"))
    for f in filelist:
        os.remove(f)

    num = 10
    for i in range(10):
        f = open(".\docs\\d"+ str(i+1) +".txt", "x") 
        f.write(''.join(random.choices(string.ascii_uppercase, k=random.randrange(50, 100, 1))))
        f.close()

generateDocs()
