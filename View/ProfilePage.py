from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6 import QtCore, uic
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager

# -------
from Model import User
from Controller import SpotifyAPI
from Controller import MainWindow
from View.Components.ImageLabel import ImageLabel

class ProfilePage(QWidget):
  """This class is responsible for displaying the user's profile page.
  UI elements are loaded from the ProfilePage.ui file.
  CSS is loaded from the assets/style.css file."""
  
  def __init__(self, parentView):
    super().__init__()
    
    # Attributes
    self.parentView = parentView
    # Providing a QNetworkAccessManager to download images
    self.manager = QNetworkAccessManager(self)
    
    # UI elements
    self.mainLayout = QVBoxLayout()
    
    self.layoutProfilePicture = QHBoxLayout()
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.layoutProfilePicture.addItem(spacerItem_left)
    self.labelUsername = QLabel()
    self.layoutProfilePicture.addWidget(self.labelUsername)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.layoutProfilePicture.addItem(spacerItem_right)
    
    self.mainLayout.addLayout(self.layoutProfilePicture)
    
    spacerUsernameTracks = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.mainLayout.addItem(spacerUsernameTracks)
    
    self.containerTracks = MainWindow.MainWindow.createDataRow("Titres les plus écoutés")
    self.mainLayout.addWidget(self.containerTracks)
    
    spacerTracksArtists = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.mainLayout.addItem(spacerTracksArtists)

    self.containerArtists = MainWindow.MainWindow.createDataRow("Artistes les plus écoutés")
    self.mainLayout.addWidget(self.containerArtists)
    
    spacerArtistsAlbums = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.mainLayout.addItem(spacerArtistsAlbums)
    
    self.containerAlbums = MainWindow.MainWindow.createDataRow("Albums les plus écoutés")
    self.mainLayout.addWidget(self.containerAlbums)
    
    self.setLayout(self.mainLayout)
    
    # Add the custom font
    font_id = QFontDatabase.addApplicationFont("Assets/HelveticaNeueMedium.otf")
    if font_id == -1:
      print("Failed to load the custom font")
      return
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    font = QFont(custom_font, 20)

    with open("Assets/style.css", "r") as file:
      css = file.read()
    
    self.labelUsername.setFont(font)
    self.labelUsername.setStyleSheet(css)
    self.containerTracks.setStyleSheet('font-size: 20px;')
    self.containerArtists.setStyleSheet('font-size: 20px;')
    self.containerAlbums.setStyleSheet('font-size: 20px;')

    # UI attributes for controller
    self.profilePicture = None # Manager by controller
 

  def createMoreButtons(self):
    seeMoreTracks = QPushButton("Voir plus...")
    seeMoreArtists = QPushButton("Voir plus...")
    seeMoreAlbums = QPushButton("Voir plus...")
    
    for button in [seeMoreTracks, seeMoreArtists, seeMoreAlbums]:
      button.setMinimumSize(100, 100)
      button.setMaximumSize(100, 100)
      button.setStyleSheet("color: white")
    
    self.containerTracks.addComponent(seeMoreTracks)
    self.containerArtists.addComponent(seeMoreArtists)
    self.containerAlbums.addComponent(seeMoreAlbums)


