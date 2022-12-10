from datetime import datetime
import pandas as pd
import numpy as np
import nltk
import newspaper
import os
from gnewsclient import gnewsclient
from math import sqrt

nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
from urllib.parse import urlparse
from newspaper import Article


def intialaize_df():
    try:
        path = resolve_path() + "\\main_frame.csv"
        df1 = pd.read_csv(path)
        df = df1[["Article_Title", "Site_Name", "Author", "Score", "Amount_of_Sentences", "First_Person_Percentage",
                  "First_Person_Nominal", "Number_of_Neutral_Sentences_Percentage", "Balance_Ratio", "Positive_Score", "Negative_score", "Compounded_Score", "URL", "Date", "Text"]].copy()
    except:
        df = pd.DataFrame(
            columns=["Article_Title", "Site_Name", "Author", "Score", "Amount_of_Sentences", "First_Person_Percentage",
                     "First_Person_Nominal", "Number_of_Neutral_Sentences_Percentage", "Balance_Ratio", "Positive_Score", "Negative_score", "Compounded_Score", "URL", "Date", "Text"])
    return df

def get_random_news(location, topic, amount):
    if amount >= 100:
        amount = 100
    list_of_links = []


    client = gnewsclient.NewsClient(language='english', location=str(location), topic=str(topic), use_opengraph=True,
                                    max_results=int(amount))

    news_list = client.get_news()



    for item in news_list:
        try:
            if str(item['site_name']) != "None" and str(item['type']) == ("article" or "website"):


                list_of_links.append(item['url'])
        except:
            print("error acquired continuing")

    return list_of_links

def get_specific_news(url):
    papper = newspaper.build(str(url))
    articalles_list = []

    try:
        for article in papper.articles:
            articalles_list.append(article.url)
    except:
        print("somthing went wrong")
    return articalles_list


def get_one_articale(url):
    listo_of_articales = [url]
    return listo_of_articales


def autor_handling(autor_list):
    if len(autor_list) != 0:
        autor = str(autor_list[0])
    else:
        autor = "NA"
    return autor


def data_handling(data_list):
    try:
        if len(str(data_list)) != 0:
            data = data_list.date()
            data = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y")
        else:
            data = "1/1/2022"
    except:
        data = "1/1/2022"
    return data

def check_for_type(compund):
    if compund >= 0.05:
        type = 1
    elif compund <= -0.05:
        type = -1
    else:
        type = 0
    return type

def save_to_txt(list_to_save):


        for i in range(len(list_to_save)):
            try:

                curent_item = list_to_save[i]

                curent_site = curent_item[1]
                text = curent_item[len(curent_item)-1]
                sentences = nltk.sent_tokenize(text)
                path_to_save = check_for_publication(resolve_path(),curent_site)
                name = str(curent_item[0])
                for k in range(2):
                    name = name + '_' +str(curent_item[k+1])
                name = str(name).replace("-","_")
                name = str(name).replace("\\","_")
                name = str(name).replace("/","_")
                name = str(name).replace(" ","_")
                name = str(name).replace(".","_")
                completeName = os.path.join(path_to_save, name+".txt")
                f = open(completeName, "w")
                try:
                    for item in sentences:
                        f.write("%s\n" % item)
                except:
                    print("oh well")
                f.close()
            except:
                print("happens")





def finall_score(amount_of_neutrall_senteces,Amount_of_Sentences,negative,positive,ratio,Amount_of_first_persone,First_persone_percentage):
    neutral_procentage = amount_of_neutrall_senteces/Amount_of_Sentences

    balanc = sqrt((negative - positive)**2)

    score = 20 + amount_of_neutrall_senteces + 20*neutral_procentage/100 + 0.05* Amount_of_Sentences - negative*10 - positive*10 -balanc*10 -ratio*10 -2*Amount_of_first_persone - First_persone_percentage/100 * 30


    return score

def check_for_publication(path_to_save, name_of_publication):
    subfolders = [ f.name for f in os.scandir(path_to_save) if f.is_dir() ]
    if name_of_publication in subfolders:
        new_path = path_to_save + '\\' +name_of_publication

    else:
        new_path = path_to_save + '\\' +name_of_publication
        os.makedirs(new_path)

    return new_path

def resolve_path():
    cwd = os.getcwd()

    cwd = str(cwd.replace('\\', '\\\\'))

    cwd = cwd.split('\\\\')

    main_path = str(cwd[0])

    for i in range(len(cwd) - 2):
        main_path = main_path + "\\" +cwd[i+1]

    path_to_save = main_path + "\\" + "Zapisane dane"

    return path_to_save

def neutrall_handling(list_of_typse):
    counter = 0
    for i in range(len(list_of_typse)):
        if int(list_of_typse[i]) == 0:
            counter += 1
        else:
            pass
    return counter

def resolve_site(url):
    site_selection = urlparse(url).hostname
    site_options = site_selection.split(".")
    if str(site_options[1]) != ('com' or 'www'):
        curent_site = site_options[1]
    else:
        curent_site = site_options[0]
    return curent_site

def bulk_artciales_prep(list_of_urls):
    aricales_list = []
    df =intialaize_df()
    for number in range(len(list_of_urls)):
        try:
            curent_url = list_of_urls[number]

            curent_site = resolve_site(curent_url)

            curent_articale = Article(curent_url, language='en')
            curent_articale.download()
            curent_articale.html
            curent_articale.parse()
            text = curent_articale.text
            pos_list = []
            neg_list = []
            neu_list = []
            compund_list = []
            type_list = []

            if len(text) != 0:

                titel = curent_articale.title
                text_copy = text
                text_copy_2 = text
                sentences = nltk.sent_tokenize(text_copy)
                amount_of_sentences = len(sentences)
                tokens = word_tokenize(text_copy_2)
                amount_of_I = dict(pd.value_counts(np.array(tokens)))
                try:
                    first_persone = amount_of_I["I"]
                except:
                    first_persone = 0

                first_procenteg = round((first_persone / amount_of_sentences * 100), 4)
                autor = curent_articale.authors
                autor_definid = autor_handling(autor)

                publish_date = curent_articale.publish_date

                def_date = data_handling(publish_date)

                sia = SentimentIntensityAnalyzer()
                for sentence in range(len(sentences)):
                    to_be_analaized = sentences[sentence]
                    score = sia.polarity_scores(to_be_analaized)
                    pos_list.append(round(score['pos'],4))
                    neg_list.append(round(score['neg'],4))
                    neu_list.append(round(score['neu'],4))
                    compund_list.append(round(score['compound'],4))
                    result = check_for_type(score['compound'])
                    type_list.append(check_for_type(score['compound']))

                positiv = round((sum(pos_list) / amount_of_sentences) ,4)
                negative = round((sum(neg_list) / amount_of_sentences), 4)
                neutral = sum(neu_list) / amount_of_sentences
                compund = round((sum(compund_list) / amount_of_sentences), 4)

                neutral_amount = neutrall_handling(type_list)

                neutral = round((neutral_amount / amount_of_sentences * 100), 4)
                ratio = round((sum(type_list) / amount_of_sentences), 4)

                score = finall_score(neutral_amount,amount_of_sentences,negative,positiv,ratio,first_persone,first_procenteg)
                score = round(score,4)

                data_record = [titel, curent_site, autor_definid, score, amount_of_sentences, first_procenteg,
                               first_persone, neutral, ratio, positiv, negative, compund, curent_url, def_date, text]
                df.loc[len(df)] = data_record
                aricales_list.append(data_record)
        except:
            print("eroror during articale handling")
            print(curent_url)
    save_to_csv(df)
    return aricales_list

def save_to_csv(df):
    csv = resolve_path() + "\\main_frame.csv"
    df1 = df.sort_values(by=['Score'], ascending=False, ignore_index=True)
    df1.index = df1.index + 1
    df1.index.name = 'Place'
    df2 = df1.drop_duplicates(subset=["Article_Title", "Site_Name"], keep=False)

    df2.to_csv(csv)

