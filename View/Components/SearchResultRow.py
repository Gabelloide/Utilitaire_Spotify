import threading
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
import requests
import utils, ui_utils
from View.Components.AbstractImageSetter import AbstractImageSetter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

class SearchResultRow(QWidget, AbstractImageSetter):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMaximumHeight(65)
        self.main_layout = QHBoxLayout(self)
        self.setFont(ui_utils.getFont(10))
        self.setStyleSheet("""
            color: white;
        """)
        
        # Image Track
        self.image_label = QLabel(self)
        self.image_label.setMaximumWidth(50)
        self.main_layout.addWidget(self.image_label)
        
        # Layout for the information
        self.info_layout = QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)
        
        # Logo
        self.logo_label = QLabel(self)
        self.main_layout.addWidget(self.logo_label)
        
        self.attachedObject = None

    def getParent(self):
      return self.parent()


    def set_logo(self, logo_path):
        self.logo_label.setPixmap(QPixmap(logo_path))


class TrackResult(SearchResultRow):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.title_label = QLabel("Title track", self)
        self.artist_label = QLabel("ArtistName", self)
        self.duration_label = QLabel("Duration Track", self)
        
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.artist_label)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.insertSpacerItem(2, spacer)
        self.main_layout.insertWidget(3,self.duration_label)
        self.mousePressEvent = self.showInfo


    def showInfo(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            from View.Components.OverlayInfo import OverlayTrackInfo
            mainWindow = self.window()
            overlay = OverlayTrackInfo(mainWindow)
            overlay.createContent(self.attachedObject)
            overlay.show()


    def contextMenuEvent(self, event):
        from View.Components.RightClickMenu import TrackRightClickMenu
        contextMenu = TrackRightClickMenu(self)
        contextMenu.exec(event.globalPos())


    def set_title(self, title):
        self.title_label.setText(title)


    def set_artist(self, artist):
        self.artist_label.setText(artist)


    def set_duration(self, duration):
        self.duration_label.setText(duration)



class ArtistResult(SearchResultRow):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.artist_label = QLabel("ArtistName", self)
        self.listeners_label = QLabel("Number Listeners", self)
        
        self.info_layout.addWidget(self.artist_label)
        self.info_layout.addWidget(self.listeners_label)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.insertSpacerItem(2, spacer)
        
        self.mousePressEvent = self.showInfo


    def set_artist(self, artist):
        self.artist_label.setText(artist)


    def set_listeners(self, listeners):
        self.listeners_label.setText(listeners)


    def showInfo(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            from View.Components.OverlayInfo import OverlayArtistInfo
            mainWindow = self.window()
            overlay = OverlayArtistInfo(mainWindow)
            overlay.createContent(self.attachedObject)
            overlay.show()


    def contextMenuEvent(self, event):
        from View.Components.RightClickMenu import ArtistRightClickMenu
        contextMenu = ArtistRightClickMenu(self)
        contextMenu.exec(event.globalPos())



class AlbumResult(SearchResultRow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.album_title_label = QLabel("Title album", self)
        self.artist_label = QLabel("ArtistName", self)
        
        self.info_layout.addWidget(self.album_title_label)
        self.info_layout.addWidget(self.artist_label)
    
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.insertSpacerItem(2, spacer)
        
        self.mousePressEvent = self.showInfo


    def set_album_title(self, title):
        self.album_title_label.setText(title)


    def set_artist(self, artist):
        self.artist_label.setText(artist)


    def showInfo(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            from View.Components.OverlayInfo import OverlayAlbumInfo
            mainWindow = self.window()
            overlay = OverlayAlbumInfo(mainWindow)
            overlay.createContent(self.attachedObject)
            overlay.show()


    def contextMenuEvent(self, event):
        from View.Components.RightClickMenu import AlbumRightClickMenu
        contextMenu = AlbumRightClickMenu(self)
        contextMenu.exec(event.globalPos())



class ProfileResult(SearchResultRow):
  
  def __init__(self, parent=None):
    super().__init__(parent)
    
    self.profile_label = QLabel("ProfileName", self)
    self.info_layout.addWidget(self.profile_label)
    
    spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.main_layout.insertSpacerItem(2, spacer)
    

  def set_profile(self, profile):
    self.profile_label.setText(profile)
    
  
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
      # utils.save_to_cache(filename, data)
      self.set_image(data)

    except requests.RequestException as e:
      print(f"Error downloading image, fallback on default profile picture.")
      # print(e)
      # Fallback on the image placeholder
      with open("Assets/icons/user_placeholder.png", "rb") as file:
        data = file.read()
        self.set_image(data)