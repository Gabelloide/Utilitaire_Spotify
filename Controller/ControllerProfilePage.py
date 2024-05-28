from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkRequest
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from Model.User import User
from View.ProfilePage import ProfilePage
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI
import utils

class ControllerProfilePage:
  
  def __init__(self, user: User, view: ProfilePage):
    self.view: ProfilePage = view
    self.user = user

    self.view.trendingButton.clicked.connect(self.showTrending)
    self.view.recommendationsButton.clicked.connect(self.showRecommendations)

    # ------ Filling UI elements with data ------
    self.view.labelUsername.setText(f"Bienvenue, {self.user.display_name} !")

    # ImageLabel for the profile picture before the username
    self.view.profilePicture = MainWindow.createImageLabel("")
    
    # Download the image and set it to the label
    self.view.profilePicture.downloadAndSetImage(self.user.getBigProfilePicture(), self.user.id)
    # TODO setup placeholder profile picture before the download is finished, or if it fails
    self.view.layoutProfilePicture.insertWidget(0, self.view.profilePicture)

    # Download the user's top tracks, artists and albums
    client = SpotifyAPI.get_spotify_client()
    user_top_tracks = self.user.getTopTracks(client)
    user_top_artists = self.user.getTopArtists(client)
    user_top_albums = self.user.getTopAlbums(client)

    # The album/artist/track ids are passed to the download manager to get them from cache if they are already downloaded
    for track in user_top_tracks:
      label = MainWindow.createImageLabel(track.name)
      label.downloadAndSetImage(track.album.getBigCover(), track.id)
      self.view.containerTracks.addComponent(label)

    for artist in user_top_artists:
      label = MainWindow.createImageLabel(artist.name)
      label.downloadAndSetImage(artist.getBigPicture(), artist.id)
      self.view.containerArtists.addComponent(label)

    for album in user_top_albums:
      label = MainWindow.createImageLabel(album.name)
      label.downloadAndSetImage(album.getBigCover(), album.id)
      self.view.containerAlbums.addComponent(label)

    # Adding "more" buttons after the last element of each container
    self.view.createMoreButtons()


  def showTrending(self):
    pass


  def showRecommendations(self):
    pass