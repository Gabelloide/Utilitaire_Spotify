from Model.User import User
from Model import Statistics
from View.StatisticsPage import StatisticsPage
from Controller import SpotifyAPI
from Controller.MainWindow import MainWindow

class ControllerStatistics:
  
  def __init__(self, user:User, view: StatisticsPage) -> None:
    self.view = view
    
    self.view.labelImport.linkActivated.connect(lambda: self.view.parentView.showPage("ZipUploadPage"))
    # Get model information to fill the view

    client = SpotifyAPI.get_spotify_client()

    figuresDataRow = MainWindow.createDataRow("Vos écoutes en chiffres")

    duration_ms = Statistics.getRecentListeningDuration(client)
    duration_mn = duration_ms // 60000
    duration_h = duration_mn // 60

    labelStreams = MainWindow.createFigureLabel(f"{Statistics.getNbPlayedTracks(client)}", "écoutes")
    figuresDataRow.addComponent(labelStreams)

    label_hours = MainWindow.createFigureLabel(f"{duration_h}", "heures écoutées")
    figuresDataRow.addComponent(label_hours)

    label_minutes = MainWindow.createFigureLabel(f"{duration_mn}", "minutes écoutées")
    figuresDataRow.addComponent(label_minutes)
    
    labelUniqueTracks = MainWindow.createFigureLabel(f"{Statistics.getNbPlayedTracks(client)}", "titres écoutés")
    figuresDataRow.addComponent(labelUniqueTracks)

    labelArtists = MainWindow.createFigureLabel(f"{Statistics.getNbPlayedArtists(client)}", "artistes différents écoutés")
    figuresDataRow.addComponent(labelArtists)
    
    labelAlbums = MainWindow.createFigureLabel(f"{Statistics.getNbPlayedAlbums(client)}", "albums différents écoutés")
    figuresDataRow.addComponent(labelAlbums)
    
    self.view.mainLayout.addWidget(figuresDataRow)

