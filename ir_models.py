from statistical_functions import getDocsNames, getDocs, findTerms, processingDocs, getUserQuery_s, rankingDocsByQuery
from vector_space_functions import getDocsNames, getDocs, findTerms, tf_processing, idf_processing, tf_idf_processing, getUserQuery_v, tf_idf_query_processing, docs_similarity_processing
from link_analysis_functions import getDocsNames, getDocs, findTerms, tf_processing, idf_processing, tf_idf_processing, getUserQuery_v, tf_idf_query_processing, docs_similarity_processing, findLinks, HITS_Iterative_Algorithm

from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import random, string, glob, os, os.path, operator, ast

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class QueryForm(Form):
    rawQuery = StringField('rawQuery', [validators.DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/statistical_model", methods=['GET', 'POST'])
def statistical():
    form = QueryForm(request.form)

    if request.method == 'POST' and form.validate():
        docsNames = getDocsNames()
        docsContent = getDocs(docsNames)
        terms = findTerms(docsContent)
        processedDocs = processingDocs(docsNames, docsContent, terms)

        query = getUserQuery_s(form.rawQuery.data)

        sorted_rankedDocs = rankingDocsByQuery(processedDocs, query, docsNames, terms)
        print(sorted_rankedDocs)

        return redirect(url_for('result', result=sorted_rankedDocs, model_name="Statistical"))

    print("Normal <-----------------")
    return render_template('statistical.html', form=form)


@app.route("/vector_space_model", methods=['GET', 'POST'])
def vector_space():
    form = QueryForm(request.form)

    if request.method == 'POST' and form.validate():
        docsNames = getDocsNames()
        docsContent = getDocs(docsNames)
        terms = findTerms(docsContent)
        queryContent = getUserQuery_v(form.rawQuery.data)
        tf = tf_processing(docsNames, docsContent, terms)
        idf = idf_processing(docsNames, docsContent, queryContent, terms)
        tf_idf = tf_idf_processing(tf, idf, docsNames, terms)
        tf_idf_query = tf_idf_query_processing(terms, idf, queryContent)
        sorted_docs_similarity = docs_similarity_processing(tf_idf, tf_idf_query, docsNames, terms)
        # print(sorted_docs_similarity)

        return redirect(url_for('result', result=sorted_docs_similarity, model_name="Vector Space"))

    print("Normal <-----------------")
    return render_template('vector_space.html', form=form)

@app.route("/link_analysis_model", methods=['GET', 'POST'])
def link_analysis():
    form = QueryForm(request.form)

    if request.method == 'POST' and form.validate():
        docsNames = getDocsNames()
        docsContent = getDocs(docsNames)
        terms = findTerms(docsContent)
        queryContent = getUserQuery_v(form.rawQuery.data)
        tf = tf_processing(docsNames, docsContent, terms)
        idf = idf_processing(docsNames, docsContent, queryContent, terms)
        tf_idf = tf_idf_processing(tf, idf, docsNames, terms)
        tf_idf_query = tf_idf_query_processing(terms, idf, queryContent)
        sorted_docs_similarity = docs_similarity_processing(tf_idf, tf_idf_query, docsNames, terms)
        # print(sorted_docs_similarity)

        links = findLinks(docsContent, docsNames)
        auth_hub = HITS_Iterative_Algorithm(docsNames, links)

        return redirect(url_for('result2', result=sorted_docs_similarity, auth_hub=auth_hub, model_name="Link Analysis"))

    print("Normal <-----------------")
    return render_template('link_analysis.html', form=form)


@app.route("/result/<result>/<model_name>", methods=['GET', 'POST'])
def result(result,model_name):
    result = ast.literal_eval(result)
    print( "\n" + str(result) + "\n" )

    return render_template('result.html', result=result, model_name=model_name)

@app.route("/result2/<result>/<auth_hub>/<model_name>", methods=['GET', 'POST'])
def result2(result, auth_hub, model_name):
    result = ast.literal_eval(result)
    auth_hub = ast.literal_eval(auth_hub)
    # print( "\n" + str(result) + "\n" )
    # print( "\n" + str(auth_hub) + "\n" )

    return render_template('result2.html', result=result, auth_hub=auth_hub, model_name=model_name)

# @app.route("/generate_docs", methods=['GET', 'POST'])
# def generateDocs():
#     filelist = glob.glob(os.path.join('docs', "*.txt"))
#     for f in filelist:
#         os.remove(f)

#     num = 10
#     for i in range(10):
#         f = open(".\docs\\d"+ str(i+1) +".txt", "x") 
#         f.write(''.join(random.choices(string.ascii_uppercase, k=random.randrange(5, 20, 1))))
#         f.close()

#     flash("Docs Generated Successfully")
#     print(" ## Docs Generated OK ## ")

#     return redirect(url_for('index'))

@app.route("/generate_docs", methods=['GET', 'POST'])
def generateDocs():
    filelist = glob.glob(os.path.join('docs', "*.txt"))
    for f in filelist:
        os.remove(f)

    rand_list = ["A","B","C","D","E",'1','2','3','4','5']
    # rand_list = string.ascii_uppercase + ['1','2','3','4','5']

    numOfDocs = 5
    for i in range(numOfDocs):
        f = open(".\\docs\\"+ str(i+1) +".txt", "x") 
        f.write(''.join( random.choices(rand_list, k=random.randrange(5, 10, 1)) ))
        f.close()

    flash("Docs Generated Successfully")
    print(" ## Docs Generated OK ## ")

    return redirect(url_for('index'))








