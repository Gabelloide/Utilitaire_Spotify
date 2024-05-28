from Model.User import User
from View.RecommendationPage import RecommendationPage
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI


class ControllerRecommendationPage:
  
  def __init__(self, user:User, view: RecommendationPage):
    self.view = view
    self.user = user
