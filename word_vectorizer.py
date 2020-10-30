import pandas as pd
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
import pickle
import spacy

#------------
# FUNCTIONS |
#------------

def lemmatizer(text):
    """Takes a string and returns a lemmatized version of it

    Args:
        text (str): text of 'lyrics' column

    Returns:
        lemma_str (str): lemmatized version of 'text' 
    """    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    lemma_str = ''

    for token in doc:
        lemma_str += token.lemma_+' '
    
    return lemma_str

def bow_dataframe(corpus, my_stop_words):
    """[summary]

    Args:
        corpus (list): list of texts to make BOW out of 
        my_stop_words (list): list of stop words to add to the pre-existing
            stop words list

    Returns:
        bow_df (dataframe): bag of words in dataframe format
    """   
    stop_words_list = text.ENGLISH_STOP_WORDS.union(my_stop_words)
    vect = text.CountVectorizer(stop_words=stop_words_list)

    bow_matrix = vect.fit_transform(corpus)

    bow_df = pd.DataFrame(bow_matrix.toarray(), columns=vect.get_feature_names())

    return bow_df 

#---------------
# MAIN PROGRAM |
#---------------

# Retrieve lyrics dataframe
lyrics_df = pd.read_csv('wtlyrics_df.csv')

# Lemmatization
lyrics_lemmatized = []
for i in lyrics_df.index: # for every line in the dataframe
    lyrics_text = lyrics_df.iloc[i,5] # take the lyrics
    lemma_str = lemmatizer(lyrics_text) # lemmatized version of the lyrics
    lyrics_lemmatized.append(lemma_str) # append the lemmatized version to a list

# add column with lemmatized lyrics to dataframe
lyrics_df['lyrics_lemmatized'] = lyrics_lemmatized

# Creation of the bag-of-words dataframe

# list of stop words to add to the pre-existing stop words list
my_stop_words = ['m', 've', 'don', 'didn', 's', 'd', 'll', 'isn', 'wasn', 
                 'weren', 't', 'aren', 'pron']

bow_df = bow_dataframe(lyrics_df.iloc[:,6], my_stop_words)

wordlist = {}

for i in bow_df.index: # loop on row
    wordlist[i] = {}
    for c in bow_df.columns: # loop on columns
        if bow_df.loc[i,c] > 0:
            wordlist[i][c] = bow_df.loc[i,c]

# wordlist = {index: {'word1': frequency of word1, 'word2': frequency of word 2,
#                     ...},
#             ...}

bow_df.to_csv('wtbow_df.csv')
pickle_out = open('wt_wordlist.pkl', 'wb')
pickle.dump(wordlist, pickle_out)
pickle_out.close()