import random, string, glob, os, os.path, operator

def getDocsNames():
    docsNames = glob.glob(".\docs\*.txt")
    for i in range(len(docsNames)):
        docsNames[i] = docsNames[i][7:]
    return docsNames


def getDocs(docsNames):
    docsContent = {}
    for d in docsNames:
        f = open(".\docs\\" + d) 
        docsContent[d] = f.read()
        f.close()
    return docsContent



def findTerms(docsContent):
    terms = []
    for dc in docsContent:
        for char in docsContent[dc]:
            if char not in terms and char != " " and char != "\n":
                terms.append(char)
    return terms


def processingDocs(docsNames, docsContent, terms):
    termsFreq = {}
    nChars = {}
    for d in docsNames:
        termsFreq[d] = {}
        for t in terms:
            termsFreq[d][t] = 0 

        nChars[d] = 0
        for char in docsContent[d]:
            if char != " " and char != "\n":
                nChars[d] += 1
                termsFreq[d][char] += 1 

    processedDocs = {}
    for d in docsNames:
        processedDocs[d] = {}
        for t in terms:
            # print("termsFreq[d][t] / nChars[d]   ->   " + str(d) + str(t) + " -- >  "+ str(termsFreq[d][t]) + ":" + str(nChars[d]) )
            processedDocs[d][t] =  termsFreq[d][t] / nChars[d]
    return processedDocs

def getUserQuery_s(rawQuery):
    # rawQuery = input("Enter the query : ex. '<A:0.2; B:0.9; D:0.8>' \n")
    rawQuery = rawQuery[1:-1]

    part1 = rawQuery.split(";")

    part2 = []
    for p in part1:
        part2.append( p.strip().split(":") )

    # print(part2)

    query = {}
    for p in part2:
        if len(p) == 1 :
            query[p[0]] = 1
        else:
            query[p[0]] = float(p[1])
    # print(query)
    return query




def rankingDocsByQuery(processedDocs, query, docsNames, terms): # proccessedCorpus = 2d dictionary , query = 1d dictionary
    rankedDocs = {}

    for d in docsNames:
        rankedDocs[d] = 0
        for t in terms:
            if t in query:
                rankedDocs[d] += query[t] * processedDocs[d][t] 
        
    sorted_rankedDocs = sorted(rankedDocs.items(), key=operator.itemgetter(1), reverse= True)

    return sorted_rankedDocs

# def printRankedDocs(sorted_rankedDocs):
#     print("Final Result : \n")
#     for d in sorted_rankedDocs:
#         print(d[0] + " : "  + str(d[1]) )


# ------------------------------------------------------------------------

# print("Start Program : ")
# print("Current dir : " + os.getcwd())

# -----> CONSOLE CODE <--------

# docsContent = getDocs(docsNames)
# terms = findTerms(docsContent)
# processedDocs = processingDocs(docsNames, docsContent, terms)
# query = getUserQuery_s()

# sorted_rankedDocs = rankingDocsByQuery(processedDocs, query, docsNames, terms)
# printRankedDocs(sorted_rankedDocs)












# print(query)

# for d in processedDocs:
#     print("Doc : " + d)
#     for t in processedDocs[d]:
#         print(t + " : " + str(processedDocs[d][t]) )

# print("terms")
# for x in terms:
#     print(x)





# if "B" in query:
#     rankedDocs["d1"] += query["B"] * pc["d1"]["B"] 

# if "apple" in thislist:

"""
pc = {
    "d1" : {
        "A" : 3/8 ,
        "B" : 2/8 ,
        "C" : 1/8 ,
        "D" : 0/8 ,
        "E" : 2/8
    },
    "d2" : {
        "A" : 3/8 ,
        "B" : 2/8 ,
        "C" : 1/8 ,
        "D" : 0/8 ,
        "E" : 2/8
    },
    "d3" : {
        "A" : 3/8 ,
        "B" : 2/8 ,
        "C" : 1/8 ,
        "D" : 0/8 ,
        "E" : 2/8
    }
}


q = {
    "A" : 0.2 ,
    "B" : 0.9 ,
    "D" : 0.8
}
"""

# import operator
# x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
# sorted_x = sorted(x.items(), key=operator.itemgetter(1))

# <A:0.2; B:0.9; D:0.8>