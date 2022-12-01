#!/usr/bin/env python
# coding: utf-8

# In[20]:


## CSIS 44620 Web Mining and Applied Natural Language Processing
## homework for Module 6
## Presented by Ramon Torres
## DEC 1, 2022


# In[21]:


import requests

response = requests.get('https://web.archive.org/web/20210327165005/https://hackaday.com/2021/03/22/how-laser-headlights-work/')
print(response.status_code)
print(response.headers['content-type'])


# In[22]:


from bs4 import BeautifulSoup

parser = 'html.parser'

soup = BeautifulSoup(response.text, parser)


# In[23]:


for header in soup.findAll('h1'):
    print('h1 header:', header)
    print('h1 text:', header.text)


# In[24]:


article_page = requests.get('https://web.archive.org/web/20210327165005/https://hackaday.com/2021/03/22/how-laser-headlights-work/')
article_html = article_page.text

import pickle
with open('python-match.pkl', 'wb') as f:
    pickle.dump(article_page.text, f)


# In[25]:


with open('python-match.pkl', 'rb') as f:
    article_html = pickle.load(f)


# In[26]:


soup = BeautifulSoup(article_html, parser)


# In[27]:


article_element = soup.find('article').get_text()


# In[28]:


print(article_element).get_text()


# In[29]:


import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')
doc = nlp(article_element)
print(f'Polarity: {doc._.polarity}')


# In[30]:


for lexeme in doc[:10]: # just the first 10 for now
    print('---',lexeme)


# In[31]:


non_ws_tokens = []
for token in doc:
    if not token.is_space:
        non_ws_tokens.append(token)
print(non_ws_tokens)


# In[32]:


def we_care_about(token):
    return not (token.is_space or token.is_punct)

interesting_tokens = [token for token in doc if we_care_about(token)]
print(interesting_tokens)


# In[33]:


from collections import Counter
word_freq = Counter(map(str,interesting_tokens))
print(word_freq.most_common(10))


# In[34]:


def we_care_about(token):
    return not (token.is_space or token.is_punct or token.is_stop)

interesting_tokens = [token for token in doc if we_care_about(token)]
word_freq = Counter(map(str,interesting_tokens))
print(word_freq.most_common(10))


# In[35]:


interesting_lemmas = [token.lemma_ for token in doc if we_care_about(token)]
lemma_freq = Counter(interesting_lemmas)
print(lemma_freq.most_common(10))


# In[36]:


interesting_lemmas = [token.lemma_.lower() for token in doc if we_care_about(token)]
lemma_freq = Counter(interesting_lemmas)
print(lemma_freq.most_common(10))


# In[37]:


cool_words = set()
for lemma, freq in lemma_freq.most_common(5):
    cool_words.add(lemma)
print(cool_words)


# In[38]:


sentences = list(doc.sents) # Thanks spaCy for just giving us our sentences
for sentence in sentences:
    count = 0
    for token in sentence:
        if token.lemma_.lower() in cool_words:
            count += 1
    # because there's a bunch of junk newlines, we'll replace those with nothing, as well as a little bit of whitespace
    sent_str = str(sentence).replace('\n','').replace('  ',' ')
    print(count,':', sent_str)


# In[39]:


def sentence_length (sent):
    count = 0
    for token in sent:
        if not(token.is_space or token.is_punct):
            count += 1
    return count
print(sentence_length(sentences[0]), sentences[0])


# 

# In[ ]:




