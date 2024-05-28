from Model.User import User

from View.LoginPage import LoginPage
from View.ProfilePage import ProfilePage
from View.StatisticsPage import StatisticsPage

from Controller.ControllerProfilePage import ControllerProfilePage
from Controller.ControllerStatistics import ControllerStatistics
from Controller import SpotifyAPI


class ControllerLogin:
  
  def __init__(self, view: LoginPage):
    self.view: LoginPage = view

    buttonLogin = view.buttonLogin
    buttonLogin.clicked.connect(self.logUser)

  def logUser(self):
    self.view.buttonLogin.setText("Connexion en cours...")
    # Repaint the button to refresh the text
    self.view.buttonLogin.repaint()
    
    client_id, client_secret, redirect_uri, scopes = SpotifyAPI.getClientParameters()
    if SpotifyAPI.get_spotify_client() is None:
      SpotifyAPI.setup_client(client_id, client_secret, redirect_uri, scopes)
    client = SpotifyAPI.get_spotify_client()
  
    user = User(client.current_user())
    self.view.loggedUser = user
    
    # Getting client user is done after the user logs in    
    self.view.buttonLogin.setText("Chargement de votre profil...")
    self.view.buttonLogin.repaint()
    
    profilePage = ProfilePage(self.view.parentView)
    ControllerProfilePage(user, profilePage) # Controller for the profile page
    self.view.parentView.addPage("ProfilePage", profilePage)
    self.view.parentView.showPage("ProfilePage")
    
    statsPage = StatisticsPage(self.view.parentView)
    ControllerStatistics(user, statsPage)
    self.view.parentView.addPage("StatisticsPage", statsPage)

