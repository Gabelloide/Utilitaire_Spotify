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
       # UI elements
    self.verticalLayout = QVBoxLayout()
    self.layoutProfilePicture = QHBoxLayout()
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.layoutProfilePicture.addItem(spacerItem_left)
    self.labelUsername = QLabel()
    self.layoutProfilePicture.addWidget(self.labelUsername)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.layoutProfilePicture.addItem(spacerItem_right)
    self.verticalLayout.addLayout(self.layoutProfilePicture)
    
    spacerUsernameTracks = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerUsernameTracks)
    
    self.containerTracks = MainWindow.MainWindow.createDataRow("Titres les plus écoutés")
    self.verticalLayout.addWidget(self.containerTracks)
    
    spacerTracksArtists = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerTracksArtists)

    self.containerArtists = MainWindow.MainWindow.createDataRow("Artistes les plus écoutés")
    self.verticalLayout.addWidget(self.containerArtists)
    
    spacerArtistsAlbums = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerArtistsAlbums)
    
    self.containerAlbums = MainWindow.MainWindow.createDataRow("Albums les plus écoutés")
    self.verticalLayout.addWidget(self.containerAlbums)
    
    spacerAlbumsButtons = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerAlbumsButtons)
    
    self.containerButtons = QHBoxLayout()
    self.trendingButton = QPushButton("Tendances")
    self.recommendationsButton = QPushButton("Recommandations")
    self.containerButtons.addWidget(self.trendingButton)
    self.containerButtons.addWidget(self.recommendationsButton)
    self.verticalLayout.addLayout(self.containerButtons)
    
    self.setLayout(self.verticalLayout)
    

    # Add the custom font to the QFontDatabase
    font_id = QFontDatabase.addApplicationFont("Assets/HelveticaNeueMedium.otf")
    if font_id == -1:
      print("Failed to load the custom font")
      return
    
    # Gather UI elements from the .ui file
    self.uiElements = [self.trendingButton, self.recommendationsButton]
    
    with open("Assets/style.css", "r") as file:
      css = file.read()
    
    # Set the custom font to the UI elements
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    font = QFont(custom_font, 20)
    for element in self.uiElements:
      element.setFont(font)
      element.setStyleSheet(css)

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


