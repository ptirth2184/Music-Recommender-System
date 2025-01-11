import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "6420b911b69e486fb13c90fbc7af6bc0"
CLIENT_SECRET = "bcd413b1e90c404ca57b26e4f2b8e436"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get the album cover URL from Spotify
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"  # Query format for Spotify search
    results = sp.search(q=search_query, type="track")  # Search for the track on Spotify

    if results and results["tracks"]["items"]:  # Check if results are found
        track = results["tracks"]["items"][0]  # Get the first track result
        album_cover_url = track["album"]["images"][0]["url"]  # Extract album cover URL
        print(album_cover_url)  # Debugging line to print the URL
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image if no cover found

# Function to recommend songs
def recommend(song):
    index = music[music['song'] == song].index[0]  # Get the index of the selected song
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])  # Sort songs by similarity
    recommended_music_names = []  # List for recommended song names
    recommended_music_posters = []  # List for recommended song posters
    for i in distances[1:6]:  # Fetch top 5 recommendations
        artist = music.iloc[i[0]].artist  # Get the artist of the recommended song
        print(artist)  # Debugging line to print artist
        print(music.iloc[i[0]].song)  # Debugging line to print song
        # Get the album cover URL for the recommended song
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit app header
st.header('Music Recommender System')

# Load the dataset and similarity matrix
music = pickle.load(open('df.pkl', 'rb'))  # Load the music dataset
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load the similarity matrix

# List of available songs
music_list = music['song'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",  # Dropdown prompt
    music_list  # List of songs for selection
)

# Display recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_movie)  # Get recommendations
    # Create 5 columns for displaying recommendations
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_music_names[0])  # Display name of the first recommended song
        st.image(recommended_music_posters[0])  # Display album cover of the first recommended song
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
