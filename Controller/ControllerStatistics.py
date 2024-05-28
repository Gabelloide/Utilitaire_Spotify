from Model.User import User
from View.StatisticsPage import StatisticsPage
from Controller import SpotifyAPI
from Controller.MainWindow import MainWindow

class ControllerStatistics:
  
  def __init__(self, user:User, view: StatisticsPage) -> None:
    self.view = view
    
    # Get model information to fill the view
    client = SpotifyAPI.get_spotify_client()
    placeholderTracks = user.getTopTracks(client, 10)
    
    # * DATAROW 1 *
    tracksRow = MainWindow.createDataRow("Plein de tracks")
    for track in placeholderTracks:
      imageLabel = MainWindow.createImageLabel(track.name)
      imageLabel.downloadAndSetImage(track.album.getBigCover(), track.id)
      tracksRow.addComponent(imageLabel)
    self.view.mainLayout.addWidget(tracksRow)
    # * ---------------- *

    # * DATAROW 2 *
    tracksRow = MainWindow.createDataRow("Plein de tracks")
    for track in placeholderTracks:
      imageLabel = MainWindow.createImageLabel(track.name)
      imageLabel.downloadAndSetImage(track.album.getBigCover(), track.id)
      tracksRow.addComponent(imageLabel)
    self.view.mainLayout.addWidget(tracksRow)
    # * ---------------- *
    
    # * DATAROW 3 *
    tracksRow = MainWindow.createDataRow("Plein de tracks")
    for track in placeholderTracks:
      imageLabel = MainWindow.createImageLabel(track.name)
      imageLabel.downloadAndSetImage(track.album.getBigCover(), track.id)
      tracksRow.addComponent(imageLabel)
    self.view.mainLayout.addWidget(tracksRow)
    # * ---------------- *
