import os ,operator, math, glob, numpy as np

def getDocsNames():
    docsNames = glob.glob(".\\docs\\*.txt")
    for i in range(len(docsNames)):
        docsNames[i] = docsNames[i][7:]
    return docsNames


def getDocs(docsNames):
    docsContent = {}
    for d in docsNames:
        f = open(".\\docs\\" + d) 
        docsContent[d] = f.read()
        f.close()
    return docsContent


def findTerms(docsContent):
    terms = []
    for dc in docsContent:
        for char in docsContent[dc]:
            if char not in terms and char != " " and char != "\n":
                if char not in ['1','2','3','4','5'] :
                    terms.append(char)
    print("terms : " + str(terms))
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
    print("tf : " + str(tf))
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

def print_docs_similarity(sorted_docs_similarity):
    print("Final Result : \n")
    for d in sorted_docs_similarity:
        print(d[0] + " : "  + str(d[1]) )
    



# ------------------------------------------------------------------------



def findLinks(docsContent,docsNames):
    links = []
    docNum = 0
    for dc in docsContent:
        docNum += 1
        links_doc = []
        for i in range( len(docsContent) ):
            links_doc.append(0)
        for char in docsContent[dc]:
            if (char + '.txt') in docsNames :
                if links_doc[int(char)-1] == 0  and int(char) != docNum :    # int(char) != docNum --> delete loops
                    links_doc[ int(char)-1 ] = 1
        links.append( links_doc )
    return links


def HITS_Iterative_Algorithm(docsNames, links):
    A = np.array( links )      # i don't how to calculate it yet !!
    A_t = A.transpose()    # i don't how to calculate it yet !!

    h0 = np.ones( len(docsNames) )
    a0 = np.ones( len(docsNames) )

    
    h_list, a_list = h0, a0

    for i in range(20):
        h_old = h_list

        a_list = np.matmul(A_t, h_old)
        norm_part = 0
        for a in a_list:
            norm_part += math.pow(a, 2)
        norm_a = math.sqrt( norm_part ) 

        for i in range( len(a_list) ):
            if norm_a != 0 :
                a_list[i] = a_list[i] / norm_a



        h_list = np.matmul(A, a_list)
        norm_part = 0
        for h in h_list:
            norm_part += math.pow(h, 2)
        norm_h = math.sqrt( norm_part ) 

        for i in range( len(h_list) ):
            if norm_h != 0 :
                h_list[i] = h_list[i] / norm_h



    a_result = {}
    counter = 0
    for x in a_list:
        counter += 1
        a_result[ str(counter) ] = x    # index = string !!

    h_result = {}
    counter = 0
    for x in h_list:
        counter += 1
        h_result[ str(counter) ] = x    # index = string !!

    # print("\na_result  : " + str(a_result))
    # print("\nh_result  : " + str(h_result))

    a_sorted_result = sorted(a_result.items(), key=operator.itemgetter(1), reverse= True)
    h_sorted_result = sorted(h_result.items(), key=operator.itemgetter(1), reverse= True)

    # print("\n")
    print("\na_sorted_result  : " + str(a_sorted_result))
    print("\nh_sorted_result  : " + str(h_sorted_result))
    print("\n")
    # print("\n")

    auth_hub = []
    auth_hub.append( a_sorted_result )
    auth_hub.append( h_sorted_result )


    return auth_hub


# ------------------------------------------------------------------------

# print("Start Program : ")
# # print("Current dir : " + os.getcwd())

# docsNames = getDocsNames()

# docsContent = getDocs(docsNames)
# terms = findTerms(docsContent)
# queryContent = getUserQuery_v( input("Enter Query : \n") )

# tf = tf_processing(docsNames, docsContent, terms)
# # print("\n tf \n")
# # print(tf)
# idf = idf_processing(docsNames, docsContent, queryContent, terms)
# # print("\n idf \n")
# # print(idf)
# tf_idf = tf_idf_processing(tf, idf, docsNames, terms)

# tf_idf_query = tf_idf_query_processing(terms, idf, queryContent)

# sorted_docs_similarity = docs_similarity_processing(tf_idf, tf_idf_query, docsNames, terms)
# print_docs_similarity(sorted_docs_similarity)



# print("\n -------------------------- \n")

# links = findLinks(docsContent, docsNames)
# HITS_Iterative_Algorithm(docsNames, links)

