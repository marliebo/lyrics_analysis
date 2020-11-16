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
    """Creates a bag-of-words dataframe from a list of texts

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

def wordfreq_song(bow_df):
    """Creates a dictionary containing, for each song, a list of the words in 
        this song and their frequency

    Args:
        bow_df (dataframe): bag-of-words dataframe

    Returns:
        wordfreq (dict): for each song, list of words occurring and their
            frequency
            # wordfreq = {index: {'word1': frequency of word1, 
            #                     'word2': frequency of word 2, ...},
            #             ...}
    """    
    wordfreq = {}

    for i in bow_df.index: # loop on row
        wordfreq[i] = {}
        for c in bow_df.columns: # loop on columns
            if bow_df.loc[i,c] > 0:
                wordfreq[i][c] = bow_df.loc[i,c]

    return wordfreq

#---------------
# MAIN PROGRAM |
#---------------

# Ask user if they want to do the vectorizer by song or by album
choice = ''
while choice not in ['s', 'a']:
    choice = input('Vectorize by song (s) or by album (a)? ')

# Correct option for each choice
if choice == 's': # user wants to vectorize by song
    chosen_df = 'wtlyrics_df.csv'
    lyrics_col = 5
    export_bow_df_name = 'wtbow_df.csv'
    export_wordfreq_name = 'wt_wordfreq.pkl'

if choice == 'a': # user wants to vectorize by album
    chosen_df = 'wtlyrics_albums_df.csv'
    lyrics_col = 4
    export_bow_df_name = 'wtbow_albums_df.csv'
    export_wordfreq_name = 'wt_album_wordfreq.pkl'

# Retrieve lyrics dataframe
lyrics_df = pd.read_csv(chosen_df)

# Lemmatization
lyrics_lemmatized = []
for i in lyrics_df.index: # for every line in the dataframe
    lyrics_text = lyrics_df.iloc[i,lyrics_col] # take the lyrics
    lemma_str = lemmatizer(lyrics_text) # lemmatized version of the lyrics
    lyrics_lemmatized.append(lemma_str) # append the lemmatized version to a list

# add column with lemmatized lyrics to dataframe
lyrics_df['lyrics_lemmatized'] = lyrics_lemmatized

# Creation of the bag-of-words dataframe

# list of stop words to add to the pre-existing stop words list
my_stop_words = ['m', 've', 'don', 'didn', 's', 'd', 'll', 'isn', 'wasn', 
                 'weren', 't', 'aren', 'pron']

bow_df = bow_dataframe(lyrics_df.iloc[:,lyrics_col+1], my_stop_words)

# Saving of BOW dataframe
bow_df.to_csv(export_bow_df_name)

# Creation of the wordfreq dictionary
wordfreq = wordfreq_song(bow_df)

# Saving of wordfreq dictionary
pickle_out = open(export_wordfreq_name, 'wb')
pickle.dump(wordfreq, pickle_out)
pickle_out.close()