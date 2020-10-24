import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pickle

# Retrieve lyrics dataframe
lyrics_df = pd.read_csv('wtlyrics_df.csv')

# Retrieve wordlist dictionary
pickle_in = open('wt_wordlist.pkl','rb')
wordlist = pickle.load(pickle_in)
pickle_in.close()

# wordlist = {index: {'word1': frequency of word1, 'word2': frequency of word 2,
#                     ...}, 
#             ...}

# Lemmatization? But I need to keep the pronouns
# Lemmatization may be more interesting for similarity analysis
'''
for i in wordlist.keys():
    wordcloud = WordCloud(background_color='white').fit_words(wordlist[i])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    input()
'''
# fig, axs = plt.subplots(4,4, sharex=True, sharey=True)
# axs = axs.flatten()
# for i in range(4*4):
#     song = list(wordlist.keys())[i]
#     ax =axs[i]

#     liste = [wordlist[song][word] for word in wordlist[song].keys()]

#     # plotting
#     ax.hist(liste)
# fig.tight_layout()
# plt.show()
# input()

# Calculate entropy
entropy = []
for song in wordlist.keys():
    a = [wordlist[song][word] for word in wordlist[song].keys()]
    a = np.array(a)
    # go to proba
    a = a/np.sum(a)
    entropy.append(-np.sum(a*np.log(a)))

fig, ax = plt.subplots()
ax.plot(entropy)
#plt.show()

for i in range(len(entropy)):
    print(lyrics_df.iloc[i, 1]+'\t'+lyrics_df.iloc[i, 3]+'\t'+str(entropy[i]))