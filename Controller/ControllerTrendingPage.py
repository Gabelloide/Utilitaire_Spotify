from Model.User import User
from View.TrendingPage import TrendingPage
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI


class ControllerTrendingPage:
  
  def __init__(self, user:User, view: TrendingPage):
    self.view = view
    self.user = user