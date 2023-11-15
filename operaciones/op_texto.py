import os
import re
import csv
from nltk import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.downloader import download
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from wordcloud import WordCloud
nltk.download('punkt')
nltk.download('stopwords')
nltk.download("vader_lexicon")


class ProcesoTexto:

    def abrir_muchos_archivos(self,filename):
        data = []
        for i in os.listdir(fr"{filename}"):
            with open(fr"{filename}/"+i,encoding="utf-8") as f:
                data.append(f.read())
        f.close()
        return data


    def abrir_archivo(archivo):
        texto= archivo
        with open(texto,'r',encoding='utf-8') as f:
            doc=f.read()
            f.close()
        return doc


    def lista_documentos(texto):
        doc = texto
        doc1 = re.split(r'[ \W\t\n]+',doc)
        lista_vacia=[]
        for i in enumerate(doc1):
            lista_vacia.append(i)     
  

        with open('text_file_busqueda.csv','w',newline='') as csvfile:
            spamwriter = csv.writer(csvfile,dialect='excel',
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['columna;id'])
            for item, row in lista_vacia:
                spamwriter.writerow([f"{row};{item}"])
    
        return doc1


    def conteo_frase(texto,frase):
        doc = texto
        doc = doc.split()
        #print(doc)
        conteo = doc.count(frase)
        doc2 = list(set(doc))
        lista_vacia=[]
        for i in enumerate(doc):
            lista_vacia.append(i)          

        return conteo,doc2


    def riqueza_lexica(texto):
        return len(set(texto))/len(texto)


    def porcentaje_palabra(palabra, texto):
        return 100*texto.count(palabra)/len(texto)


    def estadistica_lenguaje(texto):
        conteo_palabras = [palabra for palabra in texto if len(palabra)>5]
        vocabulario_f= sorted(conteo_palabras)

        #print(vocabulario_f)
        dic = {}
        for palabra in vocabulario_f:
            dic[palabra.lower()] = vocabulario_f.count(palabra)

        with open('text_conteo_palabras.csv','w',newline='') as csvfile:
            spamwriter = csv.writer(csvfile,dialect='excel',
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['palabra;cantidad'])

            for item, row in dic.items():
                spamwriter.writerow([f"{item};{row}"])

        return dic


    def ngramas(text):
        conteo_palabras = text.lower()
        doc1 = re.split(r'[ \W\t\n]+',conteo_palabras)
        lista_x = [i for i in doc1 if len(i)>5]
        
        #vocabulario_f= sorted(conteo_palabras)
        fdist = FreqDist(lista_x)

        return fdist.plot(25)


    def ngramas2_2(text):
        lower_case = text.lower()
        clean_text = lower_case.translate(str.maketrans("","",string.punctuation))
        tokenized_words = word_tokenize(clean_text,"spanish")
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words("spanish"):
                final_words.append(word)
        mb_bigrams = list(ngrams(final_words,2))
        threshold = 3
        filter_bigrams = [bigram for bigram in mb_bigrams if len(bigram[0])>threshold and len(bigram[1])>threshold]
        #fdist = FreqDist(mb_bigrams)
        #fdist.most_common(25)
        fdist = FreqDist(filter_bigrams)
        fdist.most_common(25)
        return fdist.plot(25)     


    def ngramas2(text):
        conteo_palabras = text.lower()
        doc1 = re.split(r'[ \W\t\n]+',conteo_palabras)
        mb_bigrams =list(ngrams(doc1,2))
        threshold = 3
        filter_bigrams = [bigram for bigram in mb_bigrams if len(bigram[0])>threshold and len(bigram[1])>threshold]
        #fdist = FreqDist(mb_bigrams)
        #fdist.most_common(25)
        fdist = FreqDist(filter_bigrams)
        fdist.most_common(25)
        return fdist.plot(25)


    def colocaciones(text):
        lower_case = text.lower()
        clean_text = lower_case.translate(str.maketrans("","",string.punctuation))
        tokenized_words = word_tokenize(clean_text,"spanish")
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words("spanish"):
                final_words.append(word)
        # conteo_palabras = text.lower()
        # text1 = re.split(r'[ \W\t\n]+',conteo_palabras)
        md_bigrams = list(bigrams(final_words))

        threshold = 2
        #distribution of bi-grams
        filtered_bigrams = [bigram for bigram in md_bigrams if len(bigram[0])>threshold and len(bigram[1])>threshold]
        filtered_bigram_dist = FreqDist(filtered_bigrams)
        #distribution of words
        filtered_words = [word for word in tokenized_words if len(word)>threshold]
        filtered_word_dist = FreqDist(filtered_words)

        resul_colocacion1 = list(set(filtered_bigrams))
        #print(resul_colocacion1)

        df = pd.DataFrame()
        df['bi_gram'] = list(set(filtered_bigrams))
        df['word_0'] = df['bi_gram'].apply(lambda x: x[0]) # funcion que trae primer elemento de la tupla
        df['word_1'] = df['bi_gram'].apply(lambda x: x[1]) # funcion que trae el segundo elemento de la tupla 
        df['bi_gram_freq'] = df['bi_gram'].apply(lambda x: filtered_bigram_dist[x])
        df['word_0_freq'] = df['word_0'].apply(lambda x: filtered_word_dist[x])
        df['word_1_freq'] = df['word_1'].apply(lambda x: filtered_word_dist[x])
        df['PMI'] = df[['bi_gram_freq', 'word_0_freq', 'word_1_freq']].apply(lambda x:np.log2(x.values[0]/(x.values[1]*x.values[2])), axis = 1)
        df['log(bi_gram_freq)'] = df['bi_gram_freq'].apply(lambda x: np.log2(x))
        df.sort_values(by = 'PMI', ascending=False)

        fig = px.scatter(x = df['PMI'].values, y = df['log(bi_gram_freq)'].values, color = df['PMI']+df['log(bi_gram_freq)'], 
                        size = (df['PMI']+df['log(bi_gram_freq)']).apply(lambda x: 1/(1+abs(x))).values, 
                        hover_name = df['bi_gram'].values, width = 600, height = 600, labels = {'x': 'PMI', 'y': 'Log(Bigram Frequency)'})
        #df.to_csv("colocaciones.csv", sep=";",encoding="utf-8",index=False)
        df.to_excel("colocaciones.xlsx",index=False)
        return fig.show()


    def load_nltk():
        import nltk
        palabras = nltk.download('punkt')
        return palabras


    def coloc2(text):
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        text.lower()
        #token = re.findall('\w+',text)
        tokenizer=RegexpTokenizer('\w+')
        tokens=tokenizer.tokenize(text)
        colocaciones = nltk.Text(tokens)
        colocaciones.collocations()
        h = colocaciones.collocation_list()

        return h


    def sentimientos_v(texto):
        lower_case = texto.lower()
        clean_text = lower_case.translate(str.maketrans("","",string.punctuation))
        tokenized_words = word_tokenize(clean_text,"spanish")
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words("spanish"):
                final_words.append(word)

        # counter_final_words = Counter(final_words)
        # print(type(counter_final_words))
        score = SentimentIntensityAnalyzer().polarity_scores(clean_text)
        print(score)
        scoredf = pd.DataFrame()
        scoredf['Nombres']= [i for i in score.keys()]
        scoredf['resultado']=[i for i in score.values()]
        ax1 = plt.subplot()
        ax1.bar(scoredf['Nombres'],scoredf['resultado'])
        return plt.show()


    def nube(texto):
        try:
            lower_case = texto.lower()
            st_word = stopwords.words("spanish")
            wc = WordCloud(width=600,height=400,prefer_horizontal=0.9,stopwords=st_word).generate(lower_case)
            plt.imshow(wc)
            plt.axis("off")
            return plt.show()
        except ValueError as e:
            print(e)

        return fdist.plot(25)

        # mb_bigrams =list(ngrams(final_words,2))
        # threshold = 3
        # filter_bigrams = [bigram for bigram in mb_bigrams if len(bigram[0])>threshold and len(bigram[1])>threshold]
        #fdist = FreqDist(mb_bigrams)
        #fdist.most_common(25)
        # fdist = FreqDist(filter_bigrams)
        # fdist.most_common(25)

        # return fdist.plot(25)


#def run():
    #r = ProcesoTexto.abrir_archivo('./INICIO3.txt')
    #r = ProcesoTexto.abrir_muchos_archivos(ProcesoTexto)
    #d = ProcesoTexto.lista_documentos(r)
    #print(d)
    #co = ProcesoTexto.conteo_frase(r,'estadounidense')
    #ri = ProcesoTexto.riqueza_lexica(r)
    #por=ProcesoTexto.porcentaje_palabra('estadounidense',r)
    #est_palabras= ProcesoTexto.estadistica_lenguaje(d)
    #print(type(est_palabras))
    #for key,value in est_palabras.items():
        #print(key, "|", value)
    
    #pl=ProcesoTexto.ngramas(r)
    #print(pl)
    #pl=ProcesoTexto.ngramas2(r)
    #print(pl)
    #colocacion = ProcesoTexto.colocaciones(r)
    #print(colocacion)
    #col = ProcesoTexto.nube(r)
    #print(len(r))
    #sentimientos = ProcesoTexto.sentimientos_v(r[0])
    #ProcesoTexto.nube(r[0])

   
        



# if __name__=='__main__':
#     run()

