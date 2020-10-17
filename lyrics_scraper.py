#import requests
from bs4 import BeautifulSoup, NavigableString
import re
import pandas as pd

'''
No webscraper for now, there are few enough albums so that I can save the html
files manually.

page = requests.get('http://www.darklyrics.com/w/withintemptation.html')

html = page.content
'''

#------------
# FUNCTIONS |
#------------

def get_soup(filename):
    ''' Get html content of album webpage and soupify
    '''
    f = open('wt_albums\\'+filename+'.html', 'r')
    content = f.read()
    f.close()
    soup = BeautifulSoup(content, features='html.parser')
    return soup

def get_album_name(soup):
    ''' Get album name
    '''
    album_name = re.findall(r'"([^"]*)"', soup.title.text)
    return album_name[0]

def get_album_date(soup):
    ''' Get album date
    '''
    album_date = re.findall(r'\(([0-9]{4})\)', soup.title.text)
    return album_date[0]
    
def get_songs(soup):
    songs_list = soup.find_all('h3')
    songs_infos = []
    for song in songs_list:
        songs_infos.append(song.text.split('. '))

    # some of the titles have a ’ instead of a ' so we correct that
    for song in songs_infos:
        if 'â€™' in song[1]:
            p = re.compile('â€™')
            song[1] = p.sub("'", song[1])
        if 'Ã©' in song[1]: # correction of 'é' in 'Sinéad'
            p = re.compile('Ã©')
            song[1] = p.sub('é', song[1])

    return songs_list, songs_infos
   
def get_lyrics(cur, end):
    ''' Get the lyrics
    '''
    lyrics = ""
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                # some of the texts have a ’ instead of a ' so we correct that
                if 'â€™' in text:
                    p = re.compile('â€™')
                    text = p.sub("'", text)
                if 'Ã©' in text: # correction of 'é' in 'Sinéad'
                    p = re.compile('Ã©')
                    text = p.sub('é', text)
                lyrics += text+' '
        cur = cur.next_element
    return lyrics

def add_song(f, all_songs):
    ''' Add song infos and lyrics to the list
    '''
    soup = get_soup(f)
    album_name = get_album_name(soup)
    album_date = get_album_date(soup)
    songs_list, songs_infos = get_songs(soup)

    for s in range(len(songs_list)):
        song_position = int(songs_infos[s][0])
        song_title = songs_infos[s][1]
        if s < len(songs_list)-1:
            start = songs_list[s].text
            end = songs_list[s+1].text
            lyrics = get_lyrics(soup.find('h3', text=start).next_sibling,
                                soup.find('h3', text=end))
        else:
            start = songs_list[s].text
            lyrics = get_lyrics(soup.find('h3', text=start).next_sibling,
                                         soup.find('div', {'class':'thanks'}))
 
        # if the song is a cover (begins with '[original by') 
        # or instrumental ('[instrumental]'), we don't add it to the list
        # there are iTunes bonus tracks (begin with '[iTunes')
        # so we use '[in' instead of just '[i'
        if lyrics.startswith(('[o', '[in')):
            pass
        elif lyrics.startswith('[iTunes'):
            lyrics = lyrics[20:] # remove '[iTunes bonus track] '
        else:
            all_songs.append([song_title, song_position, album_name, album_date, lyrics])

    return all_songs

#---------------
# MAIN PROGRAM |
#---------------

filenames = ['WITHIN TEMPTATION LYRICS - _Enter_ (1997) album', 
             'WITHIN TEMPTATION LYRICS - _Hydra_ (2014) album',
             'WITHIN TEMPTATION LYRICS - _Mother Earth_ (2000) album', 
             'WITHIN TEMPTATION LYRICS - _Resist_ (2018) album', 
             'WITHIN TEMPTATION LYRICS - _The Heart Of Everything_ (2007) album', 
             'WITHIN TEMPTATION LYRICS - _The Silent Force_ (2004) album', 
             'WITHIN TEMPTATION LYRICS - _The Unforgiving_ (2011) album']

all_songs = []
header = ['song_title', 'song_position', 'album_name', 'album_date', 'lyrics']

# Fill the list
for f in filenames:
    all_songs = add_song(f, all_songs)

# Create dataframe
df = pd.DataFrame(all_songs, columns=header)

# Export dataframe in .csv format
df.to_csv('wtlyrics_df.csv')