from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkRequest
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from View.ProfilePage import ProfilePage
import utils

class ControllerProfilePage:
  
  def __init__(self, view: ProfilePage):
    self.view: ProfilePage = view

    self.view.trendingButton.clicked.connect(self.showTrending)
    self.view.recommendationsButton.clicked.connect(self.showRecommendations)



  def showTrending(self):
    pass


  def showRecommendations(self):
    pass