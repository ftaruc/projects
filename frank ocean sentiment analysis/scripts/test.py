import sys
import spotipy
import spotipy.util as util
import re
import pandas as pd
import json
#import webbrowser

spotify = spotipy.Spotify()
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Include your username after running %s please..." % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username,scope,client_id='911b425bc8c3496297b0a66d3df0b236',client_secret='5f581823761649768f3ca1d3a7cfc6de',redirect_uri='http://google.com/')

if token:
    spotify = spotipy.Spotify(auth=token)

# User information
user = spotify.current_user()
displayName = user['display_name']
followers = user['followers']['total']

#print(user) > has all the shit to explore different dictionaries

#INTERACTIVE GUI
while True:
    print()
    #print(">>> Welcome to Build Your Own Spotify Dataset! v0 (for Pathways) " + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0 - Create csv for an artist's songs/audio features")
    print("1 - Find lyrics for an artist")
    print("2 - Exit")
    print()
    choice = input("Your choice: ")

    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get search results
        searchResults = spotify.search(searchQuery,1,0,"artist")
        # Artist details
        artist = searchResults['artists']['items'][0]
        artist_name = artist['name']
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        artist_id = artist['id'] #2h93pZq0e7k5yf4dywlkpM for Frank Ocean

        #artistURI(id) = 'spotify:artist:2h93pZq0e7k5yf4dywlkpM'

        albums = spotify.artist_albums(artist_id, country="US", limit=50)
        album_ids = [album['uri'] for album in albums['items']]
        print(artist_name + ' has ' + str(len(album_ids)) + ' albums (on spotify, might be singles)!')

        all_tracks = []
        for album_id in album_ids:
            tracks = spotify.album_tracks(album_id, limit=50)
            all_tracks.append(tracks)

        #Prints how many tracks per album on the left
        #all tracks, lists per album tracks, and the keys for the albums
        for tracks, album in zip(all_tracks, albums.get('items')):
            print(
                len(tracks.get('items')),
                "\t",
                album.get('name'))

        #Now getting each track id or uri to get features
        track_ids = []
        for tracks in all_tracks:
            album_tracks = []
            for track in tracks.get('items'):
                album_tracks.append(track.get('uri'))
            track_ids.append(album_tracks)

        #now grouping each track to album
        track_objects = []
        for track_id_list in track_ids:
            tracks = spotify.tracks(track_id_list)
            track_objects.append(tracks)

        #grabbing audio features for each track
        audio_feature_objects = []
        for track_id_list in track_ids:
            features = spotify.audio_features(track_id_list)
            audio_feature_objects.append(features)

        #create dictionary for json file
        spotify_data = {
            "audio_features": audio_feature_objects,
            "tracks": track_objects}

        #path = "~/Desktop/scholars/"
        #with open(path, "w") as outfile:
            #json.dump(spotify_data, outfile)
        with open('spotify.json', 'w') as outfile:
            json.dump(spotify_data, outfile)

        df = pd.DataFrame(columns=[
            'name',
            'duration_ms',
            'popularity',
            'num_markets',
            'album',
            'disc_number',
            'is_explicit',
            'track_number',
            'release_date',
            'artist',
            'danceability',
            'energy',
            'key',
            'loudness',
            'mode',
            'speechiness',
            'acousticness',
            'instrumentalness',
            'liveness',
            'valence',
            'tempo',
            'time_signature',
        ])
        for album_info, album_features in zip(
                spotify_data.get('tracks'),
                spotify_data.get('audio_features')):
            for track_info, track_features in zip(
                album_info.get('tracks'), album_features):
                y = {
                    'name': track_info['name'],
                    'duration_ms': track_info['duration_ms'],
                    'popularity': track_info['popularity'],
                    'num_markets': len(track_info['available_markets']),
                    'album': track_info['album']['name'],
                    'disc_number': track_info['disc_number'],
                    'is_explicit': track_info['explicit'],
                    'track_number': track_info['track_number'],
                    'release_date': track_info['album']['release_date'],
                    'artist': track_info['artists'][0]['name'],
                    'danceability': track_features['danceability'],
                    'energy': track_features['energy'],
                    'key': track_features['key'],
                    'loudness': track_features['loudness'],
                    'mode': track_features['mode'],
                    'speechiness': track_features['speechiness'],
                    'acousticness': track_features['acousticness'],
                    'instrumentalness': track_features['instrumentalness'],
                    'liveness': track_features['liveness'],
                    'valence': track_features['valence'],
                    'tempo': track_features['tempo'],
                    'time_signature': track_features['time_signature'],
                }
                df = df.append(y, ignore_index=True)
        df.to_csv("spotify.csv", index=False)
        print(df.iloc[0])

    if choice == "1":
        print()
        searchQuery2 = input("Extract Lyrics from which Artist? :")
        print()


        #Create Lyrics CSV
        import lyricsgenius as genius
        api = genius.Genius('tZhiB5ALt1qhLTWHtY_onJBHr4rLvRoFHvE8h5xSii24WJ8ioc9_-DxyuQzGbYtS') #auth code
        artist2 = api.search_artist(searchQuery2)
        #genius_lyrics = genius_artist.save_lyrics()
        #lyric_path = "~/Desktop/scholars/lyrics.csv"
        #genius_lyrics.keys()
        genius_songs = artist2.songs
        lyric_df = pd.DataFrame(columns=['title', 'album', 'year','lyrics'])
        for x in genius_songs:
            lyric_df = lyric_df.append({
                'title': x.title,
                'lyrics': x.lyrics,
                'album': x.album,
                'year': x.year
            }, ignore_index=True)
        lyric_df.to_csv("lyric.csv", index=False)
        #lyric_df.iloc[0]
        print()
        print("Lyrics saved!")

    if choice == "2":
        break







#FUNCTIONS:

def get_playlists(username):
    playlists = spotify.user_playlists(username)
    check = 1

    while True:
        for playlist in playlists['items']:
            # in rare cases, playlists may not be found, so playlists['next']
            # is None. Skip these.
            if playlist['name'] is not None:
                print('')
                print('playlist:')
                playlist_title = playlist['name'] + ' - ' + str(playlist['tracks']['total'])
                playlist_title += ' tracks'
                print(playlist_title)
                show_playlist(playlist)
                check += 1
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            break

def show_playlist(playlist):
    results = spotify.user_playlist(
        playlist['owner']['id'], playlist['id'], fields='tracks,next')

    tracks = results['tracks']
    show_tracks(tracks)


def show_tracks(tracks):
    n = 1
    while True:
        for item in tracks['items']:
            track = item['track']
            track_title = str(n) + '. '
            track_title += track['name'] + ' - ' + track['artists'][0]['name']
            print(track_title)
            n += 1
        # 1 page = 50 results
        # check if there are more pages
        if tracks['next']:
            tracks = spotify.next(tracks)
        else:
            break
