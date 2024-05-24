from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6 import QtCore, uic
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager

# -------
from Model import User
from Controller import SpotifyAPI
from View.Components.ImageLabel import ImageLabel

class ProfilePage(QWidget):
  """This class is responsible for displaying the user's profile page.
  UI elements are loaded from the ProfilePage.ui file.
  CSS is loaded from the assets/style.css file."""
  
  def __init__(self, user: User.User, parentView):
    super().__init__()
    
    # Attributes
    self.parentView = parentView
    self.user = user    
    # Providing a QNetworkAccessManager to download images
    self.manager = QNetworkAccessManager(self)
    
    # Load the UI elements from the .ui file
    uic.loadUi("View/ProfilePage.ui", self)

    # Add the custom font to the QFontDatabase
    font_id = QFontDatabase.addApplicationFont("Assets/HelveticaNeueMedium.otf")
    if font_id == -1:
      print("Failed to load the custom font")
      return
    
    # Gather UI elements from the .ui file
    self.labelUsername = self.findChild(QLabel, "labelUsername")
    self.labelTracks = self.findChild(QLabel, "labelTracks")
    self.labelArtists = self.findChild(QLabel, "labelArtists")
    self.labelAlbums = self.findChild(QLabel, "labelAlbums")
    self.trendingButton = self.findChild(QPushButton, "trendingButton")
    self.recommendationsButton = self.findChild(QPushButton, "recommendationsButton")
    self.uiElements = [self.labelUsername, self.labelTracks, self.labelArtists, self.labelAlbums, self.trendingButton, self.recommendationsButton]
    
    with open("Assets/style.css", "r") as file:
      css = file.read()
    
    # Set the custom font to the UI elements
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    font = QFont(custom_font, 20)
    for element in self.uiElements:
      element.setFont(font)
      element.setStyleSheet(css)

    # ImageLabel without text for the profile picture before the username
    self.profilePicture = ImageLabel("", manager=self.manager)
    self.profilePicture.setMaximumSize(100, 100)
    self.profilePicture.downloadAndSetImage(self.user.getBigProfilePicture(), self.user.id)
    self.layoutProfilePicture = self.findChild(QHBoxLayout, "containerUsername")
    usernameLabel_index = self.layoutProfilePicture.indexOf(self.labelUsername)
    self.layoutProfilePicture.insertWidget(usernameLabel_index, self.profilePicture)
      
    # Filling containers
    self.containerTracks = self.findChild(QHBoxLayout, "containerTracks")
    self.containerArtists = self.findChild(QHBoxLayout, "containerArtists")
    self.containerAlbums = self.findChild(QHBoxLayout, "containerAlbums")
    
    client = SpotifyAPI.get_spotify_client()
    user_top_tracks = self.user.getTopTracks(client)
    user_top_artists = self.user.getTopArtists(client)
    user_top_albums = self.user.getTopAlbums(client)

    # The album/artist/track ids are passed to the download manager to get them from cache if they are already downloaded
    for track in user_top_tracks:
      label = ImageLabel(track.name, manager=self.manager)
      label.setMaximumSize(100, 100)
      label.downloadAndSetImage(track.album.getBigCover(), track.id)
      self.containerTracks.addWidget(label)

    for artist in user_top_artists:
      label = ImageLabel(artist.name, manager=self.manager)
      label.setMaximumSize(100, 100)
      label.downloadAndSetImage(artist.getBigPicture(), artist.id)
      self.containerArtists.addWidget(label)

    for album in user_top_albums:
      label = ImageLabel(album.name, manager=self.manager)
      label.setMaximumSize(100, 100)
      label.downloadAndSetImage(album.getBigCover(), album.id)
      self.containerAlbums.addWidget(label)
      
    # Adding "see more..." buttons for each row
    seeMoreTracks = QPushButton("Voir plus...")
    seeMoreArtists = QPushButton("Voir plus...")
    seeMoreAlbums = QPushButton("Voir plus...")
    
    for button in [seeMoreTracks, seeMoreArtists, seeMoreAlbums]:
      button.setMinimumSize(100, 100)
      button.setMaximumSize(100, 100)
    
    self.containerTracks.addWidget(seeMoreTracks)
    self.containerArtists.addWidget(seeMoreArtists)
    self.containerAlbums.addWidget(seeMoreAlbums)
  

    # TODO setup placeholder profile picture before the download is finished, or if it fails
    
    # ------ Filling UI elements with data ------
    self.labelUsername.setText(f"Bienvenue, {self.user.display_name} !")
    









