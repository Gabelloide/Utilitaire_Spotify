from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6 import QtCore, uic
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap
from PyQt6.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt6.QtCore import QUrl
from Model import User
from Controller import SpotifyAPI

class ProfilePage(QWidget):
  """This class is responsible for displaying the user's profile page.
  UI elements are loaded from the ProfilePage.ui file.
  CSS is loaded from the assets/style.css file."""
  
  def __init__(self, user: User.User, parentView):
    super().__init__()
    
    self.parentView = parentView
    uic.loadUi("View/ProfilePage.ui", self)
    
    # Add the custom font to the QFontDatabase
    font_id = QFontDatabase.addApplicationFont("Assets/HelveticaNeueMedium.otf")
    if font_id == -1:
      print("Failed to load the custom font")
      return
    
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    
    # Gather UI elements from the .ui file
    self.profilePicture = self.findChild(QLabel, "profilePicture")
    self.labelUsername = self.findChild(QLabel, "labelUsername")
    self.labelTracks = self.findChild(QLabel, "labelTracks")
    self.labelArtists = self.findChild(QLabel, "labelArtists")
    self.labelAlbums = self.findChild(QLabel, "labelAlbums")
    self.trendingButton = self.findChild(QPushButton, "trendingButton")
    self.recommendationsButton = self.findChild(QPushButton, "recommendationsButton")
    
    self.uiElements = [self.profilePicture, self.labelUsername, self.labelTracks, self.labelArtists, self.labelAlbums, self.trendingButton, self.recommendationsButton]
    
    with open("Assets/style.css", "r") as file:
      css = file.read()
    
    # Set the custom font to the UI elements
    font = QFont(custom_font, 20)
    for element in self.uiElements:
      element.setFont(font)
      element.setStyleSheet(css)
      
    # Filling containers
    self.containerTracks = self.findChild(QHBoxLayout, "containerTracks")
    self.containerArtists = self.findChild(QHBoxLayout, "containerArtists")
    self.containerAlbums = self.findChild(QHBoxLayout, "containerAlbums")
    
    client = SpotifyAPI.get_spotify_client()
    user_top_tracks = user.getTopTracks(client)
    user_top_artists = user.getTopArtists(client)
    user_top_albums = user.getTopAlbums(client)[:5]
    
    print([track.name for track in user_top_tracks])
    print([artist.name for artist in user_top_artists])
    print([album.name for album in user_top_albums])
    
    # TODO : replace names by images (album covers, artist pictures, track pictures)
    for track in user_top_tracks:
      self.containerTracks.addWidget(QLabel(track.name))
    for artist in user_top_artists:
      self.containerArtists.addWidget(QLabel(artist.name))
    for album in user_top_albums:
      self.containerAlbums.addWidget(QLabel(album.name))


    # TODO setup placeholder profile picture before the download is finished, or if it fails
    
    # ------ Filling UI elements with data ------
    self.labelUsername.setText(user.display_name)
    
    # Setup profile image in the QLabel
    self.manager = QNetworkAccessManager(self)
    self.manager.finished.connect(lambda reply: self.fetchPictureWhenFinished(reply, self.profilePicture)) # Fetch on the right QLabel (profilePicture)
    self.downloadPicture(user.getBigProfilePicture())


  def downloadPicture(self, url):
    """Using the QNetworkAccessManager to download the profile picture from the URL provided by the Spotify API."""
    request = QNetworkRequest(QUrl(url))
    self.manager.get(request)


  def fetchPictureWhenFinished(self, reply, component: QLabel):
    """Triggered when the download of the  picture is finished.
    Loads the image data into a QPixmap and sets it to the QLabel."""
    data = reply.readAll()
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    component.setPixmap(pixmap)
    component.setScaledContents(True)
    