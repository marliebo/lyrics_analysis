import re
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pickle
import math
from PIL import Image

#------------
# FUNCTIONS |
#------------

#---------------
# MAIN PROGRAM |
#---------------

# Ask user if they want to do the wordcloud by song or by album
choice = ''
while choice not in ['s', 'a']:
    choice = input('Wordcloud by song (s) or by album (a)? ')

# Correct option for each choice
if choice == 's': # user wants a wordcloud per song
    chosen_df = 'wtlyrics_df.csv'
    chosen_wordfreq = 'wt_wordfreq.pkl'

if choice == 'a': # user wants a wordcloud per album
    chosen_df = 'wtlyrics_albums_df.csv'
    chosen_wordfreq = 'wt_album_wordfreq.pkl'

# Retrieving of files

# Retrieve lyrics dataframe
lyrics_df = pd.read_csv(chosen_df)

# Retrieve wordfreq dictionary
pickle_in = open(chosen_wordfreq,'rb')
wordfreq = pickle.load(pickle_in)
pickle_in.close()

# song df header = [ , 'song_title', 'song_position', 'album_name', 
#                   'album_date', 'lyrics']

# album df header = [ , 'album_name', 'album_date', 'number_of_songs', 
#                    'all_lyrics']

# wordfreq = {index: {'word1': frequency of word1, 'word2': frequency of word 2,
#                     ...}, 
#             ...}

# Make wordclouds per song
if choice == 's':
    plot_list = {}
    for i in wordfreq.keys():
        album = lyrics_df.iloc[i, 3]
        year = lyrics_df.iloc[i, 4]
        a_y = album+' ('+str(year)+')'
        if a_y not in plot_list.keys():
            plot_list[a_y] = []
        plot_list[a_y].append(i)

    for a in plot_list.keys():
        n = len(plot_list[a])
        cols = 3
        rows = int(math.ceil(n/cols))
        gs = gridspec.GridSpec(rows, cols)
        fig = plt.figure()
        for i in plot_list[a]:
            ax = fig.add_subplot(gs[plot_list[a].index(i)])
            wordcloud = WordCloud(background_color='white').fit_words(wordfreq[i])
            title = lyrics_df.iloc[i, 1]
            plt.title(title)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
        fig.tight_layout()
        fig.suptitle(a, fontsize=14)
        plt.show()
        input('---')

# Make wordclouds per album
if choice == 'a':    
    for i in wordfreq.keys():
        album = lyrics_df.iloc[i, 1]
        mask = np.array(Image.open('wt_covers/'+album+'.jpg'))
        image_colors = ImageColorGenerator(mask)
        wordcloud = WordCloud(background_color='white').fit_words(wordfreq[i])
        title = album+' ('+str(lyrics_df.iloc[i, 2])+')'
        plt.title(title, fontsize=14)
        plt.imshow(wordcloud.recolor(color_func=image_colors), 
                   interpolation='bilinear')
        plt.axis('off')
        plt.show()
        input('---')

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
'''
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
