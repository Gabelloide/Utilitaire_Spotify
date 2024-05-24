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


  def downloadAndSetPicture(self, url, component: QLabel, filename: str):
    """Using the QNetworkAccessManager to download the profile picture from the URL provided by the Spotify API.
    If the picture is already in the cache, it is fetched from there. Otherwise, it is downloaded and saved to the cache."""
    if utils.exists_in_cache(filename):
      data = utils.load_from_cache(filename)
      self.fetchFromCache(data, component)
      return

    request = QNetworkRequest(QUrl(url))
    reply = self.view.manager.get(request)
    reply.finished.connect(lambda: self.fetchPicture(reply, component, filename))


  def fetchPicture(self, reply, component: QLabel, filename: str):
    """Triggered when the download of the  picture is finished.
    Loads the image data into a QPixmap and sets it to the QLabel."""
    data = reply.readAll()
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    component.setPixmap(pixmap)
    component.setScaledContents(True)
    reply.deleteLater()
    utils.save_to_cache(filename, data)


  def fetchFromCache(self, data, component: QLabel):
    """Fetches the picture from the cache and sets it to the QLabel."""
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    component.setPixmap(pixmap)
    component.setScaledContents(True)