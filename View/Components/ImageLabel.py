from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap,  QTextOption, QTextDocument
from PyQt6.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt
import utils

class ImageLabel(QWidget):
  """This class is a custom widget that displays an image and a text label.
  The image is downloaded from the internet using a URL.
  """
  
  def __init__(self, text:str, parent=None, manager:QNetworkAccessManager=None):
    super().__init__(parent)
    self.layout = QVBoxLayout(self)
    self.image_label = QLabel()
    self.text_label = QLabel(text)
    self.text_label.setStyleSheet("color: white;")
    self.layout.addWidget(self.image_label)
    self.layout.addWidget(self.text_label)
    self.manager = manager



  def downloadAndSetImage(self, url, filename):
    """Downloads the image from the internet and sets it to the QLabel by calling setImage().
    If the image is already in the cache, it is fetched from there. Otherwise, it is downloaded and saved to the cache."""
    if utils.exists_in_cache(filename):
      data = utils.load_from_cache(filename)
      self.setImageFromCache(data)
      return
    
    request = QNetworkRequest(QUrl(url))
    reply = self.manager.get(request)
    reply.finished.connect(lambda: self.setImage(reply, filename))


  def setImage(self, reply, filename: str):
    """Sets the image to the QLabel when the download is finished.
    Is triggered by the QNetworkAccessManager.finished signal."""
    data = reply.readAll()
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)
    reply.deleteLater()
    utils.save_to_cache(filename, data)


  def setImageFromCache(self, data):
    """Sets the image to the QLabel from the cache."""
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)


  def setMaximumSize(self, width, height):
    """Overrides the setMaximumSize method to apply it to both the image and text labels."""
    self.image_label.setMaximumSize(width, height)
    self.text_label.setMaximumSize(width, height)