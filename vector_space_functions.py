import os ,operator, math, glob

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


def tf_processing(docsNames, docsContent, terms):
    tf = {}
    for d in docsNames:
        tf[d] = {}
        for t in terms:
            tf[d][t] = 0

    for d in docsNames:
        for char in docsContent[d]:
            if char in terms:
                tf[d][char] += 1
        maxFreq = max(tf[d].items(), key=operator.itemgetter(1))[1]
        for t in terms:
            tf[d][t] = tf[d][t] / maxFreq
    return tf    

def idf_processing(docsNames, docsContent, queryContent, terms):
    idf = {}
    df = {}
    for t in terms:
        df[t] = 0
        for d in docsNames:
            if docsContent[d].find(t) >= 0 :
                df[t] += 1
        if queryContent.find(t) >= 0 :
            df[t] += 1

        idf[t] = math.log2( ( len(docsNames) + 1 ) / df[t] )    # the PLUS ONE is for the Query .

    return idf



def tf_idf_processing(tf, idf, docsNames, terms):
    tf_idf = {}
    for d in docsNames:
        tf_idf[d] = {}
        for t in terms:
            tf_idf[d][t] = tf[d][t] * idf[t]
    return tf_idf

def getUserQuery_v(rawQuery):
    # queryContent = input("Enter the query : ex. 'A B C D E' \n")
    queryContent = rawQuery
    queryContent = queryContent.strip()
    return queryContent


def tf_idf_query_processing(terms, idf, queryContent):  
    tf_query = {}
    for t in terms:     # if there is a term in query doesn't exist in the terms list --> i ignore it :/
        tf_query[t] = 0

    for char in queryContent:
        if char in terms:
            tf_query[char] += 1
    maxFreq = max(tf_query.items(), key=operator.itemgetter(1))[1]
    for t in terms:
        tf_query[t] = tf_query[t] / maxFreq
    
    #  tf_query ready !!

    tf_idf_query = {}
    for t in terms:
        tf_idf_query[t] = tf_query[t] * idf[t]

    return tf_idf_query


def docs_similarity_processing(tf_idf, tf_idf_query, docsNames, terms):
    vertors_length = {}
    for d in docsNames:
        summation = 0
        for t in terms:
            summation += math.pow( tf_idf[d][t] , 2 )
            # print("doc sum : \n" + str(summation) )
        # print("\n")
        vertors_length[d] = math.sqrt(summation)   

    summation = 0
    for t in terms:
        summation += math.pow( tf_idf_query[t] , 2 )
    # print("query sum : \n" + str(summation) )
    vertors_length["query"] = math.sqrt(summation)

    #  vectors_length is ready !!

    docs_similarity = {}

    for d in docsNames:
        innerProduct = 0
        for t in terms:
            innerProduct += tf_idf[d][t] * tf_idf_query[t]
        if vertors_length[d] != 0 and  vertors_length["query"] != 0 :
            docs_similarity[d] = innerProduct / ( vertors_length[d] * vertors_length["query"] )
        else:
            docs_similarity[d] = 0

    sorted_docs_similarity = sorted(docs_similarity.items(), key=operator.itemgetter(1), reverse= True)

    return sorted_docs_similarity

# def print_docs_similarity(sorted_docs_similarity):
#     print("Final Result : \n")
#     for d in sorted_docs_similarity:
#         print(d[0] + " : "  + str(d[1]) )
    

# ------------------------------------------------------------------------

# print("Start Program : ")
# # print("Current dir : " + os.getcwd())

# docsContent = getDocs(docsNames)
# terms = findTerms(docsContent)

# tf = tf_processing(docsNames, docsContent, terms)
# # print("\n tf \n")
# # print(tf)
# idf = idf_processing(docsNames, docsContent, terms)
# # print("\n idf \n")
# # print(idf)
# tf_idf = tf_idf_processing(tf, idf, docsNames, terms)

# queryContent = getUserQuery_v()
# tf_idf_query = tf_idf_query_processing(terms, idf, queryContent)

# sorted_docs_similarity = docs_similarity_processing(tf_idf, tf_idf_query, docsNames, terms)
# print_docs_similarity(sorted_docs_similarity)






"""

tf = {      # freq of term i in doc j / max(freq)
    "d1" : {
        "A" : 0 ,
        "B" : 0 ,
        "C" : 0 ,
        "D" : 0 ,
        "E" : 0 
    },
    "d2" : {
        "A" : 0 ,
        "B" : 0 ,
        "C" : 0 ,
        "D" : 0 ,
        "E" : 0 
    },
    "d3" : {
        "A" : 0 ,
        "B" : 0 ,
        "C" : 0 ,
        "D" : 0 ,
        "E" : 0 
    }
}


df = {      # no of docs containing term i 
    "A" : 0 ,
    "B" : 0 ,
    "C" : 0 ,
    "D" : 0 ,
    "E" : 0 
}




tf_idf = {   # Weighted docs (tf-idf weighting)
    "d1" : {
        "A" : 0 ,
        "B" : 0 ,
        "C" : 0 ,
        "D" : 0 ,
        "E" : 0 
    },
    "d2" : {
        "A" : 0 ,
        "B" : 0 ,
        "C" : 0 ,
        "D" : 0 ,
        "E" : 0 
    },
    "d3" : {
        "A" : 0 ,
        "B" : 0 ,
        "C" : 0 ,
        "D" : 0 ,
        "E" : 0 
    }
}

q = {
    "A" : 0 ,
    "B" : 0 ,
    "C" : 0 ,
    "D" : 0 ,
    "E" : 0 
}

"""

"A B C D A C D A"