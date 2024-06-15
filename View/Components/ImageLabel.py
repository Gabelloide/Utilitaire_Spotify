from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
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
    spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.layout.addItem(spacer)


  def downloadAndSetImage(self, url, filename):
    """Downloads the image from the internet and sets it to the QLabel.
    - Checks for the image existence in the cache.
    - If the image is not in the cache, it downloads it in a separate thread.
    """
    if url is None:
      # Fallback on the image placeholder
      with open("Assets/icons/user_placeholder.png", "rb") as file:
        data = file.read()
        self.setImage(data)
        return
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
      response = requests.get(url)
      response.raise_for_status()
      data = response.content
      utils.save_to_cache(filename, data)
      self.setImage(data)

    except requests.RequestException as e:
      print(f"Error downloading image: {e}")
      


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
    self.image_label.mousePressEvent = self.showInfo

  # Overriding the context menu event to display a custom context menu
  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import TrackRightClickMenu
    contextMenu = TrackRightClickMenu(self)
    contextMenu.exec(event.globalPos())

  def showInfo(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      from View.Components.OverlayInfo import OverlayTrackInfo
      mainWindow = self.window()
      overlay = OverlayTrackInfo(mainWindow)
      overlay.createContent(self.attachedObject)
      overlay.show()


class ArtistImageLabel(ImageLabel):
  def __init__(self, artist, parent=None):
    super().__init__(artist, parent)
    self.image_label.mousePressEvent = self.showInfo

  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import ArtistRightClickMenu
    contextMenu = ArtistRightClickMenu(self)
    contextMenu.exec(event.globalPos())

  def showInfo(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      from View.Components.OverlayInfo import OverlayArtistInfo
      mainWindow = self.window()
      overlay = OverlayArtistInfo(mainWindow)
      overlay.createContent(self.attachedObject)
      overlay.show()

class AlbumImageLabel(ImageLabel):
  def __init__(self, album, parent=None):
    super().__init__(album, parent)
    self.image_label.mousePressEvent = self.showInfo

  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import AlbumRightClickMenu
    contextMenu = AlbumRightClickMenu(self)
    contextMenu.exec(event.globalPos())

  def showInfo(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      from View.Components.OverlayInfo import OverlayAlbumInfo
      mainWindow = self.window()
      overlay = OverlayAlbumInfo(mainWindow)
      overlay.createContent(self.attachedObject)
      overlay.show()


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


class TrendImageLabel(ImageLabel):
  def __init__(self, text, upvoteCount, upvoteState, attachedTrack, attachedController, parent=None):
    super().__init__(text, parent)
    
    self.attachedObject = attachedTrack
    self.upvoteState = upvoteState
    self.attachedController = attachedController

    # Removed inherited widgets to add a custom layout
    self.layout.removeWidget(self.text_label)
    self.layout.removeWidget(self.image_label)

    self.container_upvote_text = QHBoxLayout()
    self.image_label = QLabel()
    
    self.upvote_counter = QLabel("0")
    self.upvote_counter.setStyleSheet("color: white; font-size: 20px;")
    self.setUpvoteCounter(upvoteCount)
    
    self.upvote_icon = QLabel()
    
    if self.upvoteState:
      self.upvote_icon.setPixmap(QPixmap("Assets/icons/trend_like_full.png").scaled(50, 50))
    else:
      self.upvote_icon.setPixmap(QPixmap("Assets/icons/trend_like_empty.png").scaled(50, 50))
    
    self.text_label = QLabel(text)
    self.text_label.setWordWrap(True)
    self.text_label.setStyleSheet("color: white;")
    
    self.container_upvote_text.addWidget(self.upvote_counter)
    self.container_upvote_text.addWidget(self.upvote_icon)
    self.container_upvote_text.addWidget(self.text_label)
    
    self.layout.addWidget(self.image_label)
    self.layout.addLayout(self.container_upvote_text)
    
    self.upvote_icon.mousePressEvent = self.upvote


  # Trends are tracks, same behavior as TrackImageLabel
  def contextMenuEvent(self, event):
    from View.Components.RightClickMenu import TrackRightClickMenu
    contextMenu = TrackRightClickMenu(self)
    contextMenu.exec(event.globalPos())


  def showInfo(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      from View.Components.OverlayInfo import OverlayTrackInfo
      mainWindow = self.window()
      overlay = OverlayTrackInfo(mainWindow)
      overlay.createContent(self.attachedObject)
      overlay.show()


  def setMaximumSize(self, width, height):
    """Overrides the setMaximumSize method to apply it to both the image and text labels."""
    self.image_label.setMaximumSize(width, height)
    self.upvote_icon.setMaximumSize(50, 50)
    self.upvote_counter.setMaximumSize(50, 50)
    self.text_label.setMaximumWidth(width-100)


  def setUpvoteCounter(self, count):
    self.upvote_counter.setText(str(count))
    self.repaint()


  def upvote(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      from Controller.ControllerTrendingPage import ControllerTrendingPage
      ControllerTrendingPage.upvoteTrack(self.attachedObject.id)
      
      # Refreshing the view
      if self.getUpvoteState():
        self.upvote_icon.setPixmap(QPixmap("Assets/icons/trend_like_full.png").scaled(50, 50))
      else:
        self.upvote_icon.setPixmap(QPixmap("Assets/icons/trend_like_empty.png").scaled(50, 50))

      self.setUpvoteCounter(ControllerTrendingPage.getUpvoteCount(self.attachedObject.id))
      self.attachedController.refreshView()
  
  
  def getUpvoteState(self):
    from Controller.ControllerTrendingPage import ControllerTrendingPage
    return ControllerTrendingPage.getUpvoteState(self.attachedObject.id)