import json
import nltk
import re
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import pandas as pd
from gensim import corpora, models
import csv
import sys 

file_name = sys.argv[1]

with open(('test7/'+file_name), 'r') as file:
    data = json.load(file)
text = data["abstract"][0]['text']

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

text = re.sub(r'[^\w\s]', '', text)
text = re.sub(r'\d+', '', text)
text = text.lower()
text = re.sub(r'\b\w\b', '', text)
words_to_remove = ['background', 'method', 'result']
for word in words_to_remove:
    text = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.IGNORECASE)
tokens = word_tokenize(text)
tagged_words = pos_tag(tokens)
nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
stop_words = set(stopwords.words('english'))
words = nltk.word_tokenize(text)
text = ' '.join([word for word in words if word.lower() not in stop_words])
filtered_nouns = [noun for noun in nouns if noun.lower() not in stop_words]

df = pd.DataFrame({'abstract': [text],'nouns':[filtered_nouns]})
df['abstract'] = df['abstract'].apply(lambda x: nltk.word_tokenize(str(x).lower()))

data = df['nouns'].apply(lambda x: [str(x)] if not isinstance(x, list) else [str(item) for item in x])
dictionary = corpora.Dictionary(data)
corpus = [dictionary.doc2bow(doc) for doc in data]
lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

topics = lda_model.print_topics()
first_topic = lda_model.show_topic(0)
topic_list = [word for word, _ in first_topic]

csv_file_path = file_name+'.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(topic_list)