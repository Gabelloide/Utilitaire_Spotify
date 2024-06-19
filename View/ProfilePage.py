from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QScrollArea
from PyQt6 import QtCore, uic
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager
import ui_utils
# -------
from Controller import MainWindow
from View.Components.FlowLayout import FlowLayout

class ProfilePage(QScrollArea):
  """This class is responsible for displaying the user's profile page.
  UI elements are loaded from the ProfilePage.ui file.
  CSS is loaded from the assets/style.css file."""
  
  def __init__(self, parentView):
    super().__init__()
    
    # Attributes
    self.parentView = parentView
    self.setStyleSheet(ui_utils.getScrollBarStyle())
    
    # ScrollPane settings
    self.setWidgetResizable(True)
    
    # Adapt the base size of the scroll area to the window size
    totalWindowWidth = self.parentView.width()
    totalWindowHeight = self.parentView.height()
    
    centralWidgetWidth = totalWindowWidth - 100 # magic number to make this widget a little bit smaller than the window
    
    self.setFixedSize(centralWidgetWidth, totalWindowHeight)
    
    self.centralWidget = QWidget()
    
    # Providing a QNetworkAccessManager to download images
    self.manager = QNetworkAccessManager(self)
    
    # UI elements
    self.mainLayout = QVBoxLayout()

    self.layoutProfilePicture = QHBoxLayout()
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.layoutProfilePicture.addItem(spacerItem_left)

    self.profilePicture = MainWindow.MainWindow.createImageLabel("", "profilePicture")
    self.labelUsername = QLabel()
    
    self.layoutProfilePicture.addWidget(self.profilePicture)
    self.layoutProfilePicture.addWidget(self.labelUsername)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.layoutProfilePicture.addItem(spacerItem_right)
    
    self.mainLayout.addLayout(self.layoutProfilePicture)
    
    self.containerTracks = MainWindow.MainWindow.createDataRow("Titres les plus écoutés récemment")
    self.mainLayout.addWidget(self.containerTracks)

    self.containerArtists = MainWindow.MainWindow.createDataRow("Artistes les plus écoutés récemment")
    self.mainLayout.addWidget(self.containerArtists)
    
    self.containerAlbums = MainWindow.MainWindow.createDataRow("Albums les plus écoutés récemment")
    self.mainLayout.addWidget(self.containerAlbums)

    self.centralWidget.setLayout(self.mainLayout)
    self.setWidget(self.centralWidget)
    
    # Add the custom font
    font = ui_utils.getFont(20)

    with open("Assets/style.css", "r") as file:
      css = file.read()
    
    self.labelUsername.setFont(font)
    self.labelUsername.setStyleSheet(css)

  def createMoreButtons(self):
    """Creates the 'see more' buttons at the end of each row of the profile page."""
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


