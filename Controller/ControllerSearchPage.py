import random
from Model.User import User
from View.SearchPage import SearchPage
from View.Components.SearchResultRow import TrackResult, ArtistResult, AlbumResult
from Controller import SpotifyAPI
from Model.Track import Track
from Model.Artist import Artist
from Model.Album import Album
from PyQt6.QtCore import QTimer
import utils

class ControllerSearchPage:
  
  def __init__(self, user:User, view: SearchPage):
    self.view = view
    self.user = user
    self.timer = QTimer() 
    self.timer.setSingleShot(True)  
    self.timer.timeout.connect(self.search)  
    self.view.searchInput.textChanged.connect(lambda : self.timer.start(500))
    self.spotify = SpotifyAPI.get_spotify_client()
    
  def search(self):
    self.clearResults()
    
    search = self.view.searchInput.text()
    
    if search.strip():
      results = self.spotify.search(q=search, limit=3, type='track,artist,album')
      all_results = [] 
      relevant_results = []
      
      # To avoid duplicates of tracks when they are released as a single and in an album
      added_tracks = set()
      
      for result in results['artists']['items']:
        artist = Artist(result)
        
        artistResult = ArtistResult()
        artistResult.set_artist(artist.name)
        artistResult.downloadAndSetImage(artist.getBigPicture(), artist.id)
        artistResult.set_logo("Assets/icons/artist.png")
        artistResult.set_listeners(artist.getFormattedFollowers() + " followers")
        artistResult.attachedObject = artist
        
        # If the artist name contains the search, add the result to the relevant results list
        if(search.lower() in artist.name.lower() or search.lower() in utils.remove_accents(artist.name.lower())):
          relevant_results.append(artistResult)
        else:
          all_results.append(artistResult)
          
      for result in results['albums']['items']:
        album = Album(result)
        
        albumResult = AlbumResult()
        albumResult.set_album_title(album.name)
        albumResult.downloadAndSetImage(album.getBigCover(), album.id)
        albumResult.set_logo("Assets/icons/album.png")
        albumResult.set_artist(album.artists[0].name)
        albumResult.attachedObject = album
        
        # If the album name or artist contains the search, add the result to the relevant results list
        if(search.lower() in album.name.lower() or search.lower() in utils.remove_accents(album.name.lower()) or search.lower() in album.artists[0].name.lower()):
          relevant_results.append(albumResult)
        else:
          all_results.append(albumResult)
      
      for result in results['tracks']['items']:
        track = Track(result)
        
        if track.name in added_tracks:
            continue
        
        trackResult = TrackResult()
        trackResult.set_title(track.name)
        trackResult.downloadAndSetImage(track.album.getBigCover(), track.id)
        trackResult.set_logo("Assets/icons/track.png")
        trackResult.set_artist(track.artists[0].name)
        trackResult.set_duration(utils.set_format_duration(track.duration_ms))
        trackResult.attachedObject = track
        
        added_tracks.add(track.name)
        
        #If the track name or artist contains the search, add the result to the relevant results list
        if(search.lower() in track.name.lower() or search.lower() in utils.remove_accents(track.name.lower()) or search.lower() in track.artists[0].name.lower()):
          relevant_results.append(trackResult)
        else:
          all_results.append(trackResult)
        
      for result in relevant_results:
        self.view.results.addWidget(result)
      
      #Shuffle the non-relevant results to display them randomly
      random.shuffle(all_results)
      for result in all_results:
        self.view.results.addWidget(result)
      
  def clearResults(self):
    # Clear all the results
    while self.view.results.count():
      child = self.view.results.takeAt(0)
      if child.widget():
        child.widget().deleteLater()
        