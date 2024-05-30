from Model.User import User
from View.SearchPage import SearchPage
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
    for idx, track in enumerate(results['tracks']['items']):
        print(f"{idx+1} - {track['name']} by {track['artists'][0]['name']}")

    
  
    


