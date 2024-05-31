from Model.User import User
from View.SearchPage import SearchPage
from View.Components.SearchResultRow import TrackResult
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI

class ControllerSearchPage:
  def __init__(self, user:User, view: SearchPage):
    self.view = view
    self.user = user
    self.view.searchButton.clicked.connect(lambda : self.search())
    self.spotify = SpotifyAPI.get_spotify_client()

  def search(self):
    search = self.view.searchInput.text()
  
    results = self.spotify.search(q=search, limit=20, type='track,artist,album')

    # Créez des instances de SearchResultRow et les ajoutez à la SearchPage
    for result in results['tracks']['items']:
      trackResult = TrackResult()
      trackResult.set_title(result['name'])
      trackResult.set_artist(result['artists'][0]['name'])
      trackResult.set_duration(result['duration_ms'])
      self.view.mainLayout.addWidget(trackResult)