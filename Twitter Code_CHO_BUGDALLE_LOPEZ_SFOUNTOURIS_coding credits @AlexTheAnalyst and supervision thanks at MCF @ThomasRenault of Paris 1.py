# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 18:57:32 2022

@author: CHO_BUGDALLE_LOPEZ_SFOUNTOURIS
"""

# -- coding: utf-8 --
import pandas as pd
import requests
import time

  
#Creating a list for the bearer token we received from Twitter API  
bearer_token = "Y.OUR TOKEN"
#Creating a list for the url of Twitter API to be able to receive from the pool of the Tweets we have obtained access to
search_url = "https://api.twitter.com/2/tweets/search/all"
#Creating a list of headers to generate the procedure of scraping using the bearer token format
headers = {"Authorization": "Bearer {}".format(bearer_token)}

from datetime import date, timedelta, datetime
yesterday = datetime.today() - timedelta(days=70) 
#We used this timeline only to be able to focus on tweets during different periods including the cop 26 meeting (First 1/3 of November 2021)


x = 0
mytext=[]
for iteration in range(0,2):

    time.sleep(5)
   #Condition when x=0 the definition of the parameters, else without timing until the oldest id's tweet
    if x == 0:
            query_params = {'query': 'lang:en (cop26)',
                    'start_time': {},
                    "end_time": yesterday.isoformat("T") + "Z",
                    'max_results': 500,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type'}    
            x = 1
       
    else:
            query_params = {'query': 'lang:en (cop26)','start_time': {},'end_time': {},
                    'max_results': 500,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id','tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified','place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'until_id': r["meta"]["oldest_id"]}
    #Creating a list of responses from the scrapping
    response = requests.request("GET", search_url, headers=headers, params=query_params)
        
    #Technical threshold to avoid potential errors in the process
    if response.status_code == 429:
            time.sleep(60)
            response = requests.request("GET", search_url, headers=headers, params=query_params)
    #Falsification like text (Automatically python sends back an error if response code!=200)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    #The "clean" responses are saved in a different list (in JSON format)
    r = response.json()
    #Saving the scrapped data as text
    for e in r["data"]:
        #print(e["text"]) 
        mytext.append(e["text"])
    #Dataframing the text, with the help of Panda, in order to be saved in an editing format whether in csv or in xlsx 
    df = pd.DataFrame(r["data"]) #correct one
    #Exporting data in an Excel and/or csv    
    df.to_excel("twitterscraping.xlsx")
    df.to_csv("twitterscraping.csv")    
    
'''
Second Part: NLP + DataViz

'''

#ANALYSIS
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
import re  
import spacy
nlp = spacy.load('en_core_web_lg')

#Part 1
df = df['text']

all_sentences = []

for word in df:
        all_sentences.append(word)

all_sentences
#df1 = df.to_string()

#df_split = df1.split()

#df_split
lines = list()
for line in all_sentences:    
    words = line.split()
    for w in words: 
       lines.append(w)


print(lines)

#Part 2
lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]

lines

lines2 = []

for word in lines:
    if word != '':
        lines2.append(word)
#Removing RT (Retweet condition within tweet)        
for word in lines:
    if word == 'RT':
        lines2.remove(word)   

print (lines)
#Snowball

# The Snowball Stemmer requires that you pass a language parameter
s_stemmer = SnowballStemmer(language='english')

stem = []
for word in lines2:
    stem.append(s_stemmer.stem(word))
    
stem

#Part 3
#Removing all Stop Words
import spacy
nlp = spacy.load('en_core_web_lg')
stem2 = []

for word in stem:
    if word not in nlp.Defaults.stop_words:
        stem2.append(word)

stem2

#st=pd.DataFrame(stem2)
#df.to_csv("stem2.csv")
#df.to_excel("stem2.xlsx")
#Part 4

df = pd.DataFrame(stem2)

df = df[0].value_counts()


from nltk.probability import FreqDist

freqdoctor = FreqDist()

for words in df:
    freqdoctor[words] += 1

freqdoctor

#Part 5
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import seaborn as sns

#This is a simple plot that shows the top 20 words being used
#df.plot(20)

df = df[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top Words Overall')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()

#Labelling (example top organizations)
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text + ' - ' + ent.label_ + ' - ' + str(spacy.explain(ent.label_)))
str1 = " " 
stem2 = str1.join(lines2)

stem2 = nlp(stem2)

label = [(X.text, X.label_) for X in stem2.ents]

df6 = pd.DataFrame(label, columns = ['Word','Entity'])

df7 = df6.where(df6['Entity'] == 'ORG')

df7 = df7['Word'].value_counts()
df = df7[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top Organizations Mentioned')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()

#co=pd.DataFrame(df7) making the frame to be able to save it
#co.to_excel("co.xlsx") saving it to excel to generate wordcloud

#Same process (But for people, or other relevant words mentioned)
str1 = " " 
stem2 = str1.join(lines2)

stem2 = nlp(stem2)

label = [(X.text, X.label_) for X in stem2.ents]

df10 = pd.DataFrame(label, columns = ['Word','Entity'])

df10 = df10.where(df10['Entity'] == 'PERSON')

df11 = df10['Word'].value_counts()
df = df11[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top People/Issues Mentioned')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()

'''
Merci beaucoup, pour votre attention!

'''