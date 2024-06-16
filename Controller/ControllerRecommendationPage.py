import random
from Model.User import User
from View.Components.ImageLabelSlider import ImageLabelSlider
from View.RecommendationPage import RecommendationPage
from Controller import SpotifyAPI
from Model import Statistics
from Model.Track import Track
from Model.Artist import Artist
from Model.Album import Album
from View.Components.ImageLabel import TrackImageLabel, ArtistImageLabel, AlbumImageLabel

class ControllerRecommendationPage:
  
  def __init__(self, user:User, view: RecommendationPage):
    self.view = view
    self.user = user
    
    self.spotify = SpotifyAPI.get_spotify_client()
    self.client = SpotifyAPI.get_spotify_client()

    self.user_top_tracks = Statistics.getTopTracks(self.client, limit=8)[:2]
    self.user_top_artists = Statistics.getTopArtists(self.client, limit=8)[:5]
    self.user_recent_genres = Statistics.getRecentListeningGenres(self.client, limit=5)
    
    self.artists_reco = {}
    
    self.recommendedTracks = self.getTracksRecommendation()
    self.recommendedArtists = self.getArtistsRecommendation()
    self.recommendedAlbums = self.getAlbumsRecommendation()

    
    self.track_image_label = []
    for track in self.recommendedTracks:
      label = TrackImageLabel(track.name)
      label.setMaximumSize(100, 100)
      label.attachedObject = track
      label.downloadAndSetImage(track.album.getBigCover(), track.id)
      self.track_image_label.append(label)
    
    trackSlider = ImageLabelSlider(self.track_image_label)
    
    self.artist_image_label = []
    for artist in self.recommendedArtists:
      label = ArtistImageLabel(artist.name)
      label.setMaximumSize(100, 100)
      label.attachedObject = artist
      label.downloadAndSetImage(artist.getBigPicture(), artist.id)
      self.artist_image_label.append(label)
      
    artistSlider = ImageLabelSlider(self.artist_image_label)
    
    self.album_image_label = []
    for album in self.recommendedAlbums:
      label = AlbumImageLabel(album.name)
      label.setMaximumSize(100, 100)
      label.attachedObject = album
      label.downloadAndSetImage(album.getBigCover(), album.id)
      self.album_image_label.append(label)
    
    albumSlider = ImageLabelSlider(self.album_image_label)
    self.view.addRecommendationRow("Titres que vous pourriez aimer", trackSlider)
    self.view.addRecommendationRow("Artistes que vous pourriez aimer", artistSlider)
    self.view.addRecommendationRow("Albums que vous pourriez aimer", albumSlider)
   
    
  def getTracksRecommendation(self):
      
    top_tracks_uri = [track.uri for track in self.user_top_tracks]
    top_artists_uri = [artist.uri for artist in self.user_top_artists[:2]]
    recent_genres_name = [self.user_recent_genres[0][0]]
    
    tracks_reco = self.spotify.recommendations(seed_artists= top_artists_uri, seed_tracks=top_tracks_uri, seed_genres=recent_genres_name, limit=20)
    tracks = set()
    for track in tracks_reco['tracks']:
      tracks.add(Track(track))
    
    return tracks
    
  def getArtistsRecommendation(self):
    artist_reco_list = set()
    for artist in self.user_top_artists:
      if artist.id in self.artists_reco:
        artists_reco = self.artists_reco[artist.id]
        print("Artist reco in cache")
      else:
        artists_reco = self.spotify.artist_related_artists(artist.id)
        self.artists_reco[artist.id] = artists_reco
      for artist in artists_reco['artists']:
        artist_reco_list.add(Artist(artist))
        
    artist_reco_list = list(artist_reco_list)
    random.shuffle(artist_reco_list)
    return artist_reco_list[:20]
  
  def getAlbumsRecommendation(self):
    album_reco_list = set()
    artist_reco_list = set()
    for artist in self.user_top_artists[:3]:
      if artist.id in self.artists_reco:
        artists_reco = self.artists_reco[artist.id]
        print("Artist reco in cache")
      else:
        artists_reco = self.spotify.artist_related_artists(artist.id)
        self.artists_reco[artist.id] = artists_reco
      [artist_reco_list.add(Artist(artist)) for artist in artists_reco['artists']]
    for artist in artist_reco_list:
      albums = self.spotify.artist_albums(artist.id, limit=2, album_type='album')
      [album_reco_list.add(Album(album)) for album in albums['items']]
        
    album_reco_list = list(album_reco_list)
    random.shuffle(album_reco_list)
    return album_reco_list[:20]
  
  def setFocusedIcon(self, focusedButton):
    for button in self.view.buttonsNavigation:
      if button == focusedButton:
        button.setStyleSheet(self.view.focusedButtonStyleSheet)
      else:
        button.setStyleSheet(self.view.buttonStyleSheet)

