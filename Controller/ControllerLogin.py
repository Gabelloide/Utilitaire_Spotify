from Model.User import User

from View.LoginPage import LoginPage
from View.ProfilePage import ProfilePage
from View.StatisticsPage import StatisticsPage
from View.FriendsPage import FriendsPage
from View.TrendingPage import TrendingPage
from View.RecommendationPage import RecommendationPage
from View.SearchPage import SearchPage
from View.ZipUploadPage import ZipUploadPage

from Controller.ControllerProfilePage import ControllerProfilePage
from Controller.ControllerStatistics import ControllerStatistics
from Controller.ControllerFriendsPage import ControllerFriendsPage
from Controller.ControllerTrendingPage import ControllerTrendingPage
from Controller.ControllerRecommendationPage import ControllerRecommendationPage
from Controller.ControllerSearchPage import ControllerSearchPage
from Controller.ControllerZipUpload import ControllerZipUpload
from Controller import SpotifyAPI

import socket, pickle, utils
import network

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
    
    # TODO : abort connection if insert in SQL fails, but not crash the app, asking to restart
    infosSent = self.sendUserInfo(user)
    if not infosSent:
      self.view.buttonLogin.setText("Impossible de se connecter au serveur ! Réessayez")
      self.view.buttonLogin.repaint()
      return
    
    profilePage = ProfilePage(self.view.parentView)
    ControllerProfilePage(user, profilePage) # Controller for the profile page
    self.view.parentView.addPage("ProfilePage", profilePage)
    
    statsPage = StatisticsPage(self.view.parentView)
    ControllerStatistics(user, statsPage)
    self.view.parentView.addPage("StatisticsPage", statsPage)

    friendsPage = FriendsPage(self.view.parentView)
    ControllerFriendsPage(user, friendsPage)
    self.view.parentView.addPage("FriendsPage", friendsPage)
    
    trendingPage = TrendingPage(self.view.parentView)
    ControllerTrendingPage(user, trendingPage)
    self.view.parentView.addPage("TrendingPage", trendingPage)
    
    recommendationPage = RecommendationPage(self.view.parentView)
    ControllerRecommendationPage(user, recommendationPage)
    self.view.parentView.addPage("RecommendationPage", recommendationPage)

    searchPage = SearchPage(self.view.parentView)
    ControllerSearchPage(user, searchPage)
    self.view.parentView.addPage("SearchPage", searchPage)

    zipUploadPage = ZipUploadPage(self.view.parentView)
    ControllerZipUpload(zipUploadPage)
    self.view.parentView.addPage("ZipUploadPage", zipUploadPage)

    # Showing page after everything loaded
    self.view.parentView.showPage("ProfilePage")


  def sendUserInfo(self, user: User):
    """Sends userinfo to server via socket.
    Returns True/False if the operations failed/succeeded"""
    try:
      with network.connect_to_userinfo_server() as s:
        s.sendall(b"SEND_USERINFO") # Waiting for approval
        
        response = utils.receive_all(s)
        
        if response !=  b"READY":
          print(f"Server response: {response}")
          return

        data = (user.id, user.display_name)
        serialized_tuple = pickle.dumps(data)
        s.sendall(serialized_tuple)
        
        # Waiting for server response to know if SQL succeeded
        response = utils.receive_all(s)
        if response != b"SQL_OK":
          return False

        return True
      
    except socket.error as e:
      print(f"Socket error: {e}")
      return False