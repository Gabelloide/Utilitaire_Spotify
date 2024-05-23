from View import LoginPage
from Controller import SpotifyAPI
from Model import User
from View import ProfilePage
from Controller import MainWindow

class ControllerLogin:
  
  def __init__(self, view: LoginPage):
    self.view: LoginPage.LoginPage = view

    buttonLogin = view.buttonLogin
    buttonLogin.clicked.connect(self.logUser)

  def logUser(self):
    self.view.buttonLogin.setText("Connexion en cours...")
    
    client_id, client_secret, redirect_uri, scopes = SpotifyAPI.getClientParameters()
    if SpotifyAPI.get_spotify_client() is None:
      SpotifyAPI.setup_client(client_id, client_secret, redirect_uri, scopes)
    client = SpotifyAPI.get_spotify_client()
  

    user = User.User(client.current_user())
    self.view.loggedUser = user
    
    # Getting client user is done after the user logs in
    self.view.buttonLogin.setText("Connexion réussie !")
    
    profilePage = ProfilePage.ProfilePage(user, self.view.parentView)
    self.view.parentView.addPage(profilePage)
    self.view.parentView.showPage(profilePage)
    
    
