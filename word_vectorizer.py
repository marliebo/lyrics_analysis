import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle

lyrics_df = pd.read_csv('wtlyrics_df.csv')

vect = CountVectorizer(stop_words='english')
# find how to keep pronouns

# df header = [ ,'song_title', 'song_position', 'album_name', 'album_date', 
#              'lyrics']

bow_matrix = vect.fit_transform(lyrics_df.iloc[:,5])

bow_df = pd.DataFrame(bow_matrix.toarray(), columns=vect.get_feature_names())

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