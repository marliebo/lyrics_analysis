import pandas as pd

#------------
# FUNCTIONS |
#------------

def gather_albums_lyrics(songs_df):
    """Gathers all lyrics for each album.

    Args:
        songs_df (pandas dataframe): df containing the lyrics (1 line = 1 song) 
            + other info such as album, date, song title...

    Returns:
        albums_lyrics (list): for each album, information + all lyrics
            # albums_lyrics = [[name of album, date of album, 
            #                   number of songs with lyrics in album, 
            #                   lyrics of all songs in one string]]
    """    
    albums = []
    albums_lyrics = []
    for i in songs_df.index:
        if songs_df.iloc[i,3] not in albums:
            albums.append(songs_df.iloc[i,3])
            albums_lyrics.append([songs_df.iloc[i,3], songs_df.iloc[i,4], 0, ''])
        for a in albums_lyrics:
            if a[0] == songs_df.iloc[i,3]:
                a[2] += 1
                a[3] += songs_df.iloc[i,5]

    return albums_lyrics

#---------------
# MAIN PROGRAM |
#---------------

# Retrieve lyrics dataframe
songs_df = pd.read_csv('wtlyrics_df.csv')

# Gather all lyrics for each album
albums_lyrics = gather_albums_lyrics(songs_df)

# Transform albums_lyrics into a dataframe
header = ['album_name', 'album_date', 'number_of_songs', 'all_lyrics']
albums_df = pd.DataFrame(albums_lyrics, columns=header)

# Save albums lyrics dataframe
albums_df.to_csv('wtlyrics_albums_df.csv')