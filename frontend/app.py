import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
stop=list(stopwords.words('english'))
import string
stop.extend(('&amp;', '-', '…', '’', '“', '—', '”', 'amp'))
snow_stemmer = SnowballStemmer(language='english')
import streamlit as st
from PIL import Image
import pickle
import pandas as pd


def create_corpus_column(tweet):
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    cleaned_corpus = []
    corpus = tokenizer.tokenize(tweet)
    for word in corpus:
        if (word not in stop) and (word not in string.punctuation):
             cleaned_corpus.append(snow_stemmer.stem(word))
    return cleaned_corpus

def process_tweet(tweet, model, vectorizer):
    your_tweet_series = pd.Series(tweet)
    tfidf_custom_test  = vectorizer.transform(your_tweet_series)
    pred = model.predict(tfidf_custom_test)
    pred_word = 'Republican' if pred==0 else 'Democrat'
    confidence = max(model.predict_proba(tfidf_custom_test)[0])

    return pred_word, confidence

model = pickle.load(open('../model/logistic_regression_model.pkl', 'rb'))
vectorizer = pickle.load(open('../model/vectorizer.pkl', 'rb'))

# Title
st.title("Political party classification with tweets")

# Subheader
st.subheader("Try it yourself!")

# Text Input
 
# save the input text in the variable 'name'
# first argument shows the title of the text input box
# second argument displays a default text inside the text input area
tweet = st.text_input("Enter your tweet", "")
 
# display the name when the submit button is clicked
# .title() is used to get the input text string
if(st.button('Submit')):
    pred_word, confidence = process_tweet(tweet, model, vectorizer)
    result = f'Your tweet is {pred_word} with a confidence of {confidence:.2%}'
    st.info(result)
    if pred_word == 'Republican':
        img = Image.open("../imgs/trumpmeme2.jpg")
 
        st.image(img, width=500)
    else:
        img = Image.open("../imgs/bidenmeme.jpg")
 
        st.image(img, width=500)




