import numpy
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re
from html import unescape
from nltk import edit_distance

def searchFile(start_dir,target):
    os.chdir(start_dir);
    for each_file in  os.listdir(os.curdir):
        ext = os.path.splitext(each_file)[1]
        if ext in target:
            py_list.append(os.getcwd()+os.sep+each_file+os.linesep)
        if os.path.isdir(each_file):
            searchFile(each_file,target);
            #os.chdir(os.pardir)

#compare all of text
def compare():
    corpus = traincorpus;
     
    vectorizer=CountVectorizer()
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, #max_features=n_features,
                                   stop_words='english')
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(tfidf_vectorizer.fit_transform(corpus))
    word=tfidf_vectorizer.get_feature_names()
    weight=tfidf.toarray()

    SimMatrix = (tfidf * tfidf.T).A  
    #numpy.savetxt("xs.txt", SimMatrix, delimiter=",",fmt="%0.2f")
    return SimMatrix
    
def html_to_plain_text(html):
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', '', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    return unescape(text)

def readfile():
    for i in range(len(py_list)):
        f1 = open(py_list[i].replace("\n","").replace("\r",""), 'r',errors='ignore')
        t1 = f1.read()
        f1.close()
        t1 = str(t1)
        t1 = html_to_plain_text(t1)
        traincorpus.append(t1)
        print("Reading the",i+1,"web")

#print the lists of similar webs
def printfile():
    temps = [];
    n = len(py_list);
    for i in range(n):
        temps.append(True);
    for i in range(n-1):
        if temps[i]:
            for j in range(i+1,n):
                if SimMat[i,j]>=simval:
                    if temps[i]:
                        print("----------------------------");
                        print(os.path.split(py_list[i])[1]);
                    print(os.path.split(py_list[j])[1]);
                    temps[i] = False;  
                    temps[j] = False;  
    print("----------------------------");

#delete the similar webs in the list
def deletefile(n):
    global newlist;
    global traincorpus;
    global textlist;
    temps = [];    
    tl = [];    
    txtl = [];
    traincorpus = list(textlist);
    SimM = compare();
    for i in range(n):
        temps.append(True);
    for i in range(n-1):
        if temps[i]:
            temps[i] = False;
            tl.append(newlist[i]);
            txtl.append(textlist[i]);
            for j in range(i+1,n):
                if SimM[i,j]>=simval:
                    temps[j] =  False;
    if temps[n-1]:
        tl.append(newlist[n-1]);
        txtl.append(textlist[n-1]);
    newlist = list(tl);
    textlist = list(txtl);
    m = len(newlist);
    if m!=n:
        print("There're",m,"pages.");
        deletefile(len(newlist));
    else:
        print("Delete completed.")

#Find the different entre 2 words 0: a==b 1: there's one place different...
def distance(a, b):
    l = len(a);
    d = edit_distance(a.lower(), b.lower(), transpositions=True);
    return (d<=2 or (d/l)<=0.3)and((d/l)<=0.5);

#Split the words
def findinit():
    global motset;
    global motsetlist;
    print("Init...");
    for i in range(len(textlist)):
        temps = set();
        s=textlist[i].split();
        for w in s:
            mot = w.replace('(','').replace(')','').replace('.','').replace(',','').replace('!','').replace(':','').replace('<','').replace('>','').replace(':','').replace(';','').replace('/','');
            motset.add(mot);
            temps.add(mot);
        motsetlist.append(temps);
    
#Find the similar words
def findmot():
    ans = set();
    tf = True;
    s = input("Entree le cle-mot: ");  
    if len(s) == 0:
        return None;
    print("Attendez un instant...");
    for w in motset:
        if distance(s,w):
            tf = False;
            print(w);
    if tf:
        print("Il n'y a pas de mot similar.");
    print("----------------------------------------");

#Find the pages with the similar words    
def findpage():
    tf = True;
    s = input("Entree le cle-mot: ");  
    if len(s) == 0:
        return None;
    print("Attendez un instant...");
    for i in range(len(motsetlist)):
        for w in motsetlist[i]:
            if distance(s,w):
                tf = False;
                print(os.path.split(newlist[i])[1]);
                continue;
    if tf:
        print("Il n'y a pas de mot similar.");
    print("----------------------------------------");
            
    
    
if __name__ == '__main__':
    simval = 0.8;
    #Find all of files of web in file page_web
    start_dir=os.getcwd()+"\\pages_web\\";
    #start_dir=os.getcwd();
    program_dir=os.getcwd();
    target = ['.html']
    py_list=[];
    searchFile(start_dir,target);
    traincorpus=[];
    print("Read files: begin");
    readfile();
    textlist = list(traincorpus);
    print("Read files: end");
    print("----------------------------------------")
    #Compare all of pages
    print("compare files: begin");
    SimMat = compare();
    print("compare files: end");
    print("----------------------------------------")
    print("Write the list of similar files: begin")
    printfile();
    print("Write the list of similar files: end")
    print("----------------------------------------")
    print("Delete the list of similar files: begin")
    newlist = list(py_list);
    deletefile(len(newlist));
    print("Delete the list of similar files: end")
    print("----------------------------------------")
    print("Find the similar word: begin")
    motset = set();
    motsetlist = [];
    findinit();
    n = int(input("Vous voudrais chercher les proches mots combien fois( Ecrire les mots proches): "));
    for i in range(n):
        findmot();
    print("Find the similar word: end")
    print("----------------------------------------")
    print("Find the similar word of web: begin")
    n = int(input("Vous voudrais chercher les proches mots combien fois( Ecrire les webs qui ont le mot proche): "));
    for i in range(n):
        findpage();
    print("Find the similar word of web: end")
    
   # print(os.path.split(py_list[0])[1])
    

    
