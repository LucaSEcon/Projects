"""
Created on Thu Jan 13 18:57:32 2022

@author: CHO_BUGDALLE_LOPEZ_SFOUNTOURIS
"""
import os
os.chdir("C:/Users/Sunbin/Python Group Project MEDE") #Use your directory here
os.system('cls')
path=os.getcwd()
print(path)

# ### Import packages
# In[6]:
#pip install selenium
from bs4 import BeautifulSoup

# In[7]:

from selenium import webdriver
import time



# In[68]:

#Call the web page and maximise
driver = webdriver.Chrome()
web_url = 'https://www4.unfccc.int/sites/submissionsstaging/Pages/Home.aspx'
time.sleep(1)
driver.get(web_url)
driver.maximize_window()
time.sleep(5)




# In[69]:


#Click and select years
x_path = '//*[@id="searchyear"]/button'
year_button = driver.find_element_by_xpath(x_path).click()
driver.find_element_by_xpath('//*[@id="Open"]').click()
#driver.find_element_by_xpath('//*[@id="2022"]').click()
#driver.find_element_by_xpath('//*[@id="2021"]').click()
driver.find_element_by_xpath('//*[@id="2020"]').click()
driver.find_element_by_xpath('//*[@id="2019"]').click()
driver.find_element_by_xpath('//*[@id="2018"]').click()
driver.find_element_by_xpath('//*[@id="2017"]').click()
driver.find_element_by_xpath('//*[@id="2016"]').click()
driver.find_element_by_xpath('//*[@id="2015"]').click()



# ### Search 'opening'

# In[70]:


search_box = driver.find_element_by_xpath('//*[@id="accordion"]/div[2]/div/div/div[2]/div/div/input')
search_box.click()
search_box.send_keys("opening")
driver.find_element_by_xpath('//*[@id="accordion"]/div[2]/div/div/div[2]/div/div/div/button/i').click()


# ### Click upcoming and past tab and store the html code

# In[71]:


driver.find_element_by_xpath('//*[@id="headingOnea"]/h4/a').click()
time.sleep(1)

html = driver.page_source
upcoming_soup = BeautifulSoup(html, 'html.parser')

driver.find_element_by_xpath('//*[@id="headingOne"]/h4/a').click()
time.sleep(1)

html = driver.page_source
past_soup = BeautifulSoup(html, 'html.parser')


# In[67]:


upcoming_soup.find("div", {"class":"a"})
upcoming_soup


# In[ ]:


pdf_link = []

for a in upcoming_soup.find_all('a', href=True):
     a_string = a['href']
     if a_string.find('.pdf') >= 0:
         if a_string.find('COP26') >= 0:
             pdf_link.append(a_string)

# In[ ]:
    #Setting for pdf scraping
    
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from bs4 import BeautifulSoup
import re

import os
os.chdir("C:/Users/Sunbin/Python Group Project MEDE/Opening")

sites = []
for i in pdf_link :
    site = "https://www4.unfccc.int" + i
    print(site)
    sites.append(site)
    print(sites)

#### to exclude spanish version --> Now we have 12 Opening statements (English)
leng="_esp"
for item in sites:
    if leng in item:
        sites.remove(item)
# In[ ]:

## Read web file and Save opening statements into pdf files
#pip install urllib3
import urllib.request

for text in sites :
#    driver = webdriver.Chrome()
#    driver.get(report)
#    time.sleep(5)
    report = text.replace(' ','%20')
    webFile = urllib.request.urlopen(report)
    pdfFile = open(report.split('/')[-1], 'wb')
    pdfFile.write(webFile.read())
    webFile.close()
    pdfFile.close()


## Extracting text and split from pdf and save into csv files
import pandas as pd
path = r"C:/Users/Sunbin/Python Group Project MEDE/Opening" #Where to save
dirs = os.listdir(path)
mytext = []
for item in dirs :
    item_path = os.path.join(path, item)
    with open(item_path, mode='rb') as f:
        reader = PdfFileReader(f)
        for page in reader.pages:
            pass
        text = page.extractText()#.encode('utf-8')
        print(text)
        mytext.append(text)
        text = text.split()
        text = [text[i].lower() for i in range(len(text))]
        print(text)
        mytext.append(text) 
    
df=pd.DataFrame(mytext)
df.to_csv("C:/Users/Sunbin/Python Group Project MEDE/pdfscrap.csv")
df.to_excel("C:/Users/Sunbin/Python Group Project MEDE/pdfscrapex.xlsx")

import os
os.chdir("C:/Users/Sunbin/Python Group Project MEDE")
data_csv="C:/Users/Sunbin/Python Group Project MEDE/pdfscrap.csv"




# In[ ]: 
    # Import CSV and create word list
import csv
from collections import Counter
words= []
with open(data_csv, 'rt') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for col in reader:
         csv_words = col[1].split(" ")
         for i in csv_words:
              words.append(i)
              
# In[ ]: From Loukas Download packages for analysis
    #ANALYSIS
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
#pip install spacy
import spacy

nlp = spacy.load('en_core_web_lg')

import spacy

nlp = spacy.load("en_core_web_sm")
# In[ ]:        
    # Data Cleansing
df2=pd.DataFrame(words)
df3=df2[0] #To extract the words from the Column 0 (The name of the column that includes words is 0)

all_sentences = []

for word in df3:
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

#Exclude special characters
lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]

lines

lines2 = []

for word in lines:
    if word != '':
        lines2.append(word)
#Snowball
# The Snowball Stemmer requires that you pass a language parameter
s_stemmer = SnowballStemmer(language='english')

stem = []
for word in lines2:
    stem.append(s_stemmer.stem(word))
       
stem

    #Stopwords

import spacy
nlp = spacy.load('en_core_web_lg')
stem2 = []

for word in stem:
    if word not in nlp.Defaults.stop_words:
        stem2.append(word)

df2=pd.DataFrame(stem2)
df2.to_csv("C:/Users/Sunbin/Python Group Project MEDE/cleansing.csv")
data_csv2="C:/Users/Sunbin/Python Group Project MEDE/cleansing.csv"
# In[ ]: 
    # Counting words frequency and create csv

words_counted=[]              
with open('data_csv2',  'a+') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in stem2:
        x = stem2.count(i)
        words_counted.append((i,x))    
    writer.writerow(words_counted)    
set(words_counted)
df_words=pd.DataFrame(words_counted)
df_words.to_csv("C:/Users/Sunbin/Python Group Project MEDE/wordfreq.csv")
# In[ ]: VISUALIAZTION

#count words again with nltk

df = df2[0].value_counts()

#df
#df['freq'] = df.groupby(0)[0].transform('count')
#df['freq'] = df.groupby(0)[0].transform('count')
#df.sort_values(by = ('freq'), ascending=False)
#This will give frequencies of our words

from nltk.probability import FreqDist

freqdoctor = FreqDist()

for words in df:
    freqdoctor[words] += 1

freqdoctor

##plot

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import seaborn as sns

#This is a simple plot that shows the top 20 words being used
#df.plot(20)

df = df[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top Words Overall')
plt.ylabel('Word from Opening Statements', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()

#other plots
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
df = df7[:3,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top 3 Organizations Mentioned')
plt.ylabel('Word from Opening statements COP26', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()