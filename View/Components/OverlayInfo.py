from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

from Model.Track import Track
from Model.Artist import Artist
from Model.Album import Album

import datetime

class OverlayInfo(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    # Make the widget fill the entire parent widget
    self.setGeometry(0, 0, parent.width(), parent.height())

    # Create a dark overlay
    self.overlay = QWidget(self)
    self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 192);")
    self.overlay.setGeometry(0, 0, parent.width(), parent.height())

    # Create a child widget for the content
    self.contentWidget = QWidget(self)
    self.contentWidget.setStyleSheet("background-color: #282828; border-radius: 10px;")
    self.contentWidget.setFixedSize(400, 400)
    self.contentWidget.move((self.width() - self.contentWidget.width()) // 2, (self.height() - self.contentWidget.height()) // 2)

    self.mainLayout = QVBoxLayout(self.contentWidget)
    # Create a close button with a cross
    closeButton = QPushButton("X")
    closeButton.clicked.connect(self.close)
    closeButton.setStyleSheet("border: none; font-size: 16px;")

    self.mainLayout.addWidget(closeButton, alignment=Qt.AlignmentFlag.AlignRight)

  def mousePressEvent(self, event):
    # Close the widget when the user clicks outside the content
    if not self.contentWidget.geometry().contains(event.pos()):
      self.close()


class OverlayTrackInfo(OverlayInfo):
  def __init__(self, parent=None):
    super().__init__(parent)


  def createContent(self, trackObject: Track):
    labelTitle = QLabel("Crédits")
    labelTitle.setStyleSheet("font-size: 20px; font-weight: bold;")
    
    label_name = QLabel(trackObject.name)
    
    labelArtitsTitle = QLabel(f"Interprété par")
    
    labelArtists = QLabel(", ".join(artist.name for artist in trackObject.artists))
    
    labelAlbumTitle = QLabel(f"Album")
    labelAlbum = QLabel(trackObject.album.name)
    
    labelLinkTitle = QLabel(f"Écouter sur Spotify")
    trackLink = trackObject.external_urls.get("spotify")
    labelLink = QLabel(f"<a href='{trackLink}' style='color: #1DB954;'>{trackLink}</a>")
    labelLink.setOpenExternalLinks(True)
    
    for component in [labelTitle, label_name, labelArtitsTitle, labelArtists, labelAlbumTitle, labelAlbum, labelLinkTitle, labelLink]:
      self.mainLayout.addWidget(component, alignment=Qt.AlignmentFlag.AlignCenter)
      
    for titleLabel in [labelArtitsTitle, labelAlbumTitle, labelLinkTitle]:
      titleLabel.setStyleSheet("font-weight: bold;")
      

class OverlayArtistInfo(OverlayInfo):
  def __init__(self, parent=None):
    super().__init__(parent)


  def createContent(self, artistObject: Artist):
    labelTitle = QLabel("Crédits")
    labelTitle.setStyleSheet("font-size: 20px; font-weight: bold;")
    
    label_name = QLabel(artistObject.name)
    
    labelPopularityTitle = QLabel(f"Popularité")
    labelPopularity = QLabel(str(artistObject.popularity))
    
    labelFollowersTitle = QLabel(f"Followers")
    labelFollowers = QLabel(str(artistObject.getFormattedFollowers()))
    
    labelGenresTitle = QLabel(f"Genres")
    labelGenres = QLabel(", ".join(genre.capitalize() for genre in artistObject.genres))
    
    labelLinkTitle = QLabel(f"Écouter sur Spotify")
    artistLink = artistObject.external_urls.get("spotify")
    labelLink = QLabel(f"<a href='{artistLink}' style='color: #1DB954;'>{artistLink}</a>")
    labelLink.setOpenExternalLinks(True)
    
    for component in [labelTitle, label_name, labelPopularityTitle, labelPopularity, labelFollowersTitle, labelFollowers, labelGenresTitle, labelGenres, labelLinkTitle, labelLink]:
      self.mainLayout.addWidget(component, alignment=Qt.AlignmentFlag.AlignCenter)
      
    for titleLabel in [labelPopularityTitle, labelFollowersTitle, labelGenresTitle, labelLinkTitle]:
      titleLabel.setStyleSheet("font-weight: bold;")


class OverlayAlbumInfo(OverlayInfo):
  def __init__(self, parent=None):
    super().__init__(parent)
    
  def createContent(self, albumObject: Album):
    labelTitle = QLabel("Crédits")
    labelTitle.setStyleSheet("font-size: 20px; font-weight: bold;")
    
    label_name = QLabel(albumObject.name)
    
    labelArtitsTitle = QLabel(f"Artistes collaborateurs")
    
    labelArtists = QLabel(", ".join(artist.name for artist in albumObject.artists))
    
    labelReleaseDateTitle = QLabel(f"Date de sortie")
    formattedDate = datetime.datetime.strptime(albumObject.release_date, "%Y-%m-%d").strftime("%A, %d %B %Y")
    labelReleaseDate = QLabel(formattedDate)
    
    labelTracksTitle = QLabel(f"Nombre de pistes")
    labelTracks = QLabel(str(albumObject.total_tracks))
    
    labelLinkTitle = QLabel(f"Écouter sur Spotify")
    albumLink = albumObject.external_urls.get("spotify")
    labelLink = QLabel(f"<a href='{albumLink}' style='color: #1DB954;'>{albumLink}</a>")
    labelLink.setOpenExternalLinks(True)
    
    for component in [labelTitle, label_name, labelArtitsTitle, labelArtists, labelReleaseDateTitle, labelReleaseDate, labelTracksTitle, labelTracks, labelLinkTitle, labelLink]:
      self.mainLayout.addWidget(component, alignment=Qt.AlignmentFlag.AlignCenter)
      
    for titleLabel in [labelArtitsTitle, labelReleaseDateTitle, labelTracksTitle, labelLinkTitle]:
      titleLabel.setStyleSheet("font-weight: bold;")