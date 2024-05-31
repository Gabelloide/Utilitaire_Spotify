from Model.User import User
from View.SearchPage import SearchPage
from View.Components.SearchResultRow import TrackResult
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI
from Model.Track import Track
import utils

class ControllerSearchPage:
  def __init__(self, user:User, view: SearchPage):
    self.view = view
    self.user = user
    self.view.searchInput.textChanged.connect(lambda : self.search())
    self.spotify = SpotifyAPI.get_spotify_client()

  def search(self):
    self.clearResults()
    
    search = self.view.searchInput.text()
    
    if search != "":
      results = self.spotify.search(q=search, limit=2, type='track,artist,album')
      # Créez des instances de SearchResultRow et les ajoutez à la SearchPage
      for result in results['tracks']['items']:
        track = Track(result)
        
        trackResult = TrackResult()
        
        trackResult.set_title(track.name)
        trackResult.downloadAndSetImage(track.album.getBigCover(), track.id)
        trackResult.set_logo("Assets/icons/search.png")
        trackResult.set_artist(track.artists[0].name)
        trackResult.set_duration(utils.set_format_duration(track.duration_ms))
        
        self.view.results.addWidget(trackResult)
        
      for result in results['artists']['items']:
        #TODO
        pass
      for result in results['albums']['items']:
        #TODO
        pass
      
  def clearResults(self):
    # Clear tous les résultats de la recherche
    while self.view.results.count():
      child = self.view.results.takeAt(0)
      if child.widget():
        child.widget().deleteLater()