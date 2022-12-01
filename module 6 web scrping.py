#!/usr/bin/env python
# coding: utf-8

# ## CSIS 44620 Web Mining and Applied Natural Language Processing
# ## homework for Module 6
# ## Presented by Ramon Torres
# ## DEC 1, 2022

# In[96]:


import requests

response = requests.get('https://web.archive.org/web/20210327165005/https://hackaday.com/2021/03/22/how-laser-headlights-work/')
# Uncomment next line to print the full HTML text;  it's long so when done, recomment
# print(response.text)
print(response.status_code)
print(response.headers['content-type'])


# In[97]:


from bs4 import BeautifulSoup
# Uncomment next lines to explore full page contents; it's long so when done, recomment
# print(soup)
# print(soup.prettify())
# parser = 'html5lib'
parser = 'html.parser'

soup = BeautifulSoup(response.text, parser)


# In[98]:


for header in soup.findAll('h1'):
    print('h1 header:', header)
    print('h1 text:', header.text)


# In[99]:


article_page = requests.get('https://web.archive.org/web/20210327165005/https://hackaday.com/2021/03/22/how-laser-headlights-work/')
article_html = article_page.text

# pickle works similar to json, but stores information in a binary format
# json files are readable by humans, pickle files, not so much

# BeautifulSoup objects don't pickle well, so it's appropriate and polite to web developers to cache the text of the web page, or just dump it to an html file you can read in later as a regular file
import pickle
with open('python-match.pkl', 'wb') as f:
    pickle.dump(article_page.text, f)


# In[100]:


with open('python-match.pkl', 'rb') as f:
    article_html = pickle.load(f)


# In[101]:


soup = BeautifulSoup(article_html, parser)


# In[103]:


article_element = soup.find('article').get_text()
# Uncomment to see the entire article element html; again, it's long
# print(article_element)


# In[104]:


print(article_element).get_text()


# In[105]:


import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
# why not, let's add some fun sentiment analysis, because we can
nlp.add_pipe('spacytextblob')
doc = nlp(article_element)
print(f'Polarity: {doc._.polarity}')


# In[106]:


for lexeme in doc[:10]: # just the first 10 for now
    print('---',lexeme)


# In[107]:


non_ws_tokens = []
for token in doc:
    if not token.is_space:
        non_ws_tokens.append(token)
print(non_ws_tokens)


# In[108]:


def we_care_about(token):
    return not (token.is_space or token.is_punct)

interesting_tokens = [token for token in doc if we_care_about(token)]
print(interesting_tokens)


# In[109]:


from collections import Counter
word_freq = Counter(map(str,interesting_tokens))
print(word_freq.most_common(10))


# In[110]:


def we_care_about(token):
    return not (token.is_space or token.is_punct or token.is_stop)

interesting_tokens = [token for token in doc if we_care_about(token)]
word_freq = Counter(map(str,interesting_tokens))
print(word_freq.most_common(10))


# In[111]:


interesting_lemmas = [token.lemma_ for token in doc if we_care_about(token)]
lemma_freq = Counter(interesting_lemmas)
print(lemma_freq.most_common(10))


# In[112]:


interesting_lemmas = [token.lemma_.lower() for token in doc if we_care_about(token)]
lemma_freq = Counter(interesting_lemmas)
print(lemma_freq.most_common(10))


# In[113]:


cool_words = set()
for lemma, freq in lemma_freq.most_common(5):
    cool_words.add(lemma)
print(cool_words)


# In[114]:


sentences = list(doc.sents) # Thanks spaCy for just giving us our sentences
for sentence in sentences:
    count = 0
    for token in sentence:
        if token.lemma_.lower() in cool_words:
            count += 1
    # because there's a bunch of junk newlines, we'll replace those with nothing, as well as a little bit of whitespace
    sent_str = str(sentence).replace('\n','').replace('  ',' ')
    print(count,':', sent_str)


# In[116]:


def sentence_length (sent):
    count = 0
    for token in sent:
        if not(token.is_space or token.is_punct):
            count += 1
    return count
print(sentence_length(sentences[0]), sentences[0])


# 
