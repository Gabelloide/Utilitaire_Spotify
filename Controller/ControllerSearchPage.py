from Model.User import User
from View.SearchPage import SearchPage
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI


class ControllerSearchPage:
  
  def __init__(self, user:User, view: SearchPage):
    self.view = view
    self.user = user
