import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pickle

#------------
# FUNCTIONS |
#------------

#---------------
# MAIN PROGRAM |
#---------------

# Retrieving of files

# Retrieve lyrics dataframe
lyrics_df = pd.read_csv('wtlyrics_df.csv')

# Retrieve wordfreq dictionary
pickle_in = open('wt_wordfreq.pkl','rb')
wordfreq = pickle.load(pickle_in)
pickle_in.close()

# df header = [ ,'song_title', 'song_position', 'album_name', 'album_date', 
#              'lyrics']

# wordfreq = {index: {'word1': frequency of word1, 'word2': frequency of word 2,
#                     ...}, 
#             ...}

# Lemmatization? But I need to keep the pronouns
# Lemmatization may be more interesting for similarity analysis

# Make wordclouds per song
'''
for i in wordfreq.keys():
    wordcloud = WordCloud(background_color='white').fit_words(wordfreq[i])
    title = lyrics_df.iloc[i, 1]+' ('+lyrics_df.iloc[i, 3]+')'
    plt.title(title)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    input()
'''

# Keep only most frequents words per songs
most_freq = {}
for i in wordfreq.keys():
    most_freq[i] = [(word, freq) for word, freq in wordfreq[i].items()]
    # for word in wordfreq[i].keys():
    #     most_freq[i].append((word, wordfreq[i][word]))
    most_freq[i].sort(key=lambda x: x[1], reverse=False)

# Make barplots per song
for i in most_freq.keys():
    words = []
    freq = []
    for tup in most_freq[i]:
        words.append(tup[0])
        freq.append(tup[1])
    plt.yticks(range(len(freq)), words)
    plt.xticks(range(max(freq)+1))
    plt.xlabel('Word frequency')
    plt.barh(range(len(freq)), freq)
    title = lyrics_df.iloc[i, 1]+' ('+lyrics_df.iloc[i, 3]+')'
    plt.title(title)
    plt.show()
    input('---')

# print barplots from highest to lowest freq

# fig, axs = plt.subplots(4,4, sharex=True, sharey=True)
# axs = axs.flatten()
# for i in range(4*4):
#     song = list(wordfreq.keys())[i]
#     ax =axs[i]

#     liste = [wordfreq[song][word] for word in wordfreq[song].keys()]

#     # plotting
#     ax.hist(liste)
# fig.tight_layout()
# plt.show()
# input()

'''
# Calculate entropy
entropy = []
for song in wordfreq.keys():
    a = [wordfreq[song][word] for word in wordfreq[song].keys()]
    a = np.array(a)
    # go to proba
    a = a/np.sum(a)
    entropy.append(-np.sum(a*np.log(a)))

fig, ax = plt.subplots()
ax.plot(entropy)
#plt.show()

for i in range(len(entropy)):
    print(lyrics_df.iloc[i, 1]+'\t'+lyrics_df.iloc[i, 3]+'\t'+str(entropy[i]))
'''
