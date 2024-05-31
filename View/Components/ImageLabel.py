from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
import requests
import threading

import utils

class ImageLabel(QWidget):
  """This class is a custom widget that displays an image and a text label.
  The image is a QPixmap.
  """
  
  def __init__(self, text:str, parent=None):
    super().__init__(parent)

    self.attachedObject = None # The object attached to the image label, will be defined by Controllers (Track, Artist, Album, etc.)

    self.layout = QVBoxLayout(self)
    self.image_label = QLabel()
    self.text_label = QLabel(text)
    self.text_label.setWordWrap(True)
    self.text_label.setStyleSheet("color: white;")
    self.layout.addWidget(self.image_label)
    self.layout.addWidget(self.text_label)


  def downloadAndSetImage(self, url, filename):
    """Downloads the image from the internet and sets it to the QLabel.
    - Checks for the image existence in the cache.
    - If the image is not in the cache, it downloads it in a separate thread.
    """
    if utils.exists_in_cache(filename):
      data = utils.load_from_cache(filename)
      self.setImage(data)
    else:
      # Downloading the image in a separate thread
      threading.Thread(target=self.thread_download, args=(url, filename)).start()


  def thread_download(self, url, filename):
    """Used by a separate thread to download the image from the internet.
    - Gets the image data from the URL via a GET request.
    - Saves the image data to the cache.
    - Sets the image to the QLabel using the data downloaded.
    """
    try:
      if url is None:
        return
      response = requests.get(url)
      response.raise_for_status()
      data = response.content
      utils.save_to_cache(filename, data)
      self.setImage(data)

    except requests.RequestException as e:
      print(f"Error downloading image: {e}")
      # Fallback on the image placeholder
      with open("Assets/icons/cover_placeholder.png", "rb") as file:
        data = file.read()
        self.setImage(data)


  def setImage(self, data):
    """Sets the image to the QLabel."""
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)


  def setMaximumSize(self, width, height):
    """Overrides the setMaximumSize method to apply it to both the image and text labels."""
    self.image_label.setMaximumSize(width, height)
    self.text_label.setMaximumWidth(width)


  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import RightClickMenu
    """Reimplement the context menu event to display a custom context menu."""
    contextMenu = RightClickMenu(self)
    contextMenu.exec(event.globalPos()) # Show the context menu at the event position


class TrackImageLabel(ImageLabel):    
  def __init__(self, track, parent=None):
    super().__init__(track, parent)
    
  # Overriding the context menu event to display a custom context menu
  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import TrackRightClickMenu
    contextMenu = TrackRightClickMenu(self)
    contextMenu.exec(event.globalPos())


class ArtistImageLabel(ImageLabel):
  def __init__(self, artist, parent=None):
    super().__init__(artist, parent)

  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import ArtistRightClickMenu
    contextMenu = ArtistRightClickMenu(self)
    contextMenu.exec(event.globalPos())


class AlbumImageLabel(ImageLabel):
  def __init__(self, album, parent=None):
    super().__init__(album, parent)

  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import AlbumRightClickMenu
    contextMenu = AlbumRightClickMenu(self)
    contextMenu.exec(event.globalPos())


class ProfilePictureImageLabel(ImageLabel):
  def __init__(self, text, parent=None):
    super().__init__(text, parent)
    
  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import ProfilePictureRightClickMenu
    contextMenu = ProfilePictureRightClickMenu(self)
    contextMenu.exec(event.globalPos())

  # Overriding the method to use the profile picture placeholder
  def thread_download(self, url, filename):
    try:
      response = requests.get(url)
      response.raise_for_status()
      data = response.content
      utils.save_to_cache(filename, data)
      self.setImage(data)

    except requests.RequestException as e:
      print(f"Error downloading image: {e}")
      # Fallback on the image placeholder
      with open("Assets/icons/user_placeholder.png", "rb") as file:
        data = file.read()
        self.setImage(data)