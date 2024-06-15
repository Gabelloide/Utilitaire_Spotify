import random
from Model.User import User
from View.RecommendationPage import RecommendationPage
from Controller import SpotifyAPI
from Model import Statistics
from Model.Track import Track
from Model.Artist import Artist
from Model.Album import Album

class ControllerRecommendationPage:
  
  def __init__(self, user:User, view: RecommendationPage):
    self.view = view
    self.user = user
    
    self.spotify = SpotifyAPI.get_spotify_client()
    client = SpotifyAPI.get_spotify_client()


    def getTracksRecommendation(self):
      user_top_tracks = Statistics.getTopTracks(client, limit=2)
      user_top_artists = Statistics.getTopArtists(client, limit=2)
      user_recent_genres = Statistics.getRecentListeningGenres(client, limit=1)
      
      top_tracks_uri = [track.uri for track in user_top_tracks]
      top_artists_uri = [artist.uri for artist in user_top_artists]
      recent_genres_name = [genre[0] for genre in user_recent_genres]
    
      tracks_reco = self.spotify.recommendations(seed_artists= top_artists_uri, seed_tracks=top_tracks_uri, seed_genres=recent_genres_name, limit=20)
      
      tracks = ()
      for track in tracks_reco['tracks']:
        tracks.add(Track(track))
        
      return tracks
    
    def getArtistsRecommendation(self):
      artist_reco_list = set()
      user_top_artists = Statistics.getTopArtists(client, limit=5)
      for artist in user_top_artists:
        artists_reco = self.spotify.artist_related_artists(artist.id)
        for artist in artists_reco['artists']:
          artist_reco_list.add(Artist(artist))
          
      artist_reco_list = list(artist_reco_list)
      random.shuffle(artist_reco_list)
      return artist_reco_list[:20]
    
    def getAlbumsRecommendation(self):
      album_reco_list = set()
      artist_reco_list = set()
      user_top_artists = Statistics.getTopArtists(client, limit=5)
      for artist in user_top_artists:
        artists_reco = self.spotify.artist_related_artists(artist.id)
        for artist in artists_reco['artists']:
          artist_reco_list.add(Artist(artist))
      for artist in artist_reco_list:
        albums = self.spotify.artist_albums(artist.id, limit=2, album_type='album')
        for album in albums['items']:
          album_reco_list.add(Album(album))
          
      album_reco_list = list(album_reco_list)
      random.shuffle(album_reco_list)
      return album_reco_list[:20]
    
    def setFocusedIcon(self, focusedButton):
      for button in self.view.buttonsNaviguation:
        if button == focusedButton:
          button.setStyleSheet(self.view.focusedButtonStyleSheet)
        else:
          button.setStyleSheet(self.view.buttonStyleSheet)