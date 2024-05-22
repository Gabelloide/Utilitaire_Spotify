from View import LoginPage
from Controller import SpotifyAPI

class ControllerLogin:
  
  def __init__(self, view: LoginPage):
    self.view = view

    buttonLogin = view.buttonLogin
    buttonLogin.clicked.connect(self.logUser)

  def logUser(self):
    client_id, client_secret, redirect_uri, scopes = SpotifyAPI.getClientParameters()
    if SpotifyAPI.get_spotify_client() is None:
      SpotifyAPI.setup_client(client_id, client_secret, redirect_uri, scopes)

    client = SpotifyAPI.get_spotify_client()
    user = client.current_user()
    print(user)