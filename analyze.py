import json
import re
import nltk
from nltk.corpus import stopwords
import string
import operator
from collections import Counter

emoticons_str = r"""(?:[:=;][oO\-]?[D\)\]\(\]/\\OpP])"""
regex_str = [emoticons_str, r'<[^>]+>', r'(?:@[\w_]+)', r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', r'(?:(?:\d+,?)+(?:\.?\d+)?)', r"(?:[a-z][a-z'\-_]+[a-z])", r'(?:[\w_]+)', r'(?:\S)']
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s): return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

nltk.download('words')
nltk.download('stopwords')

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT', 'rt', 'via', '…', '’', 'amp']
english_words = set(nltk.corpus.words.words())
number_of_users = 0
users = []

with open('data/words.txt', 'w+') as w:
    with open('data/stream.json', 'r') as f:
        count = Counter()
        for line in f:
            tweet = json.loads(line)
            users.append((tweet["user"])["screen_name"])
            if tweet["retweeted"]:
                continue
            if "extended_tweet" in tweet:
                extended_text = tweet["extended_tweet"]
                text = extended_text["full_text"].lower()
            else: 
                text = tweet["text"].lower()
            processed = preprocess(text)
            terms_stop = [term for term in processed if term in english_words and term not in stop]
            for word in terms_stop:
                w.write(word)
                w.write("\r\n")
            count.update(terms_stop)
users = list(set(users))
print("number of users: ", len(users))
print(count.most_common(10))