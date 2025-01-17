from Model.User import User
from Model import Statistics
from Model.AudioFeature import AudioFeature, AudioFeatureAverage
from View.StatisticsPage import StatisticsPage
from View.Components.PieGenre import PieChartGenre
from Controller import SpotifyAPI
from Controller.MainWindow import MainWindow
import os

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

    canvasDataRow = MainWindow.createDataRow("Vos écoutes visuellement")
    genres_data = Statistics.getRecentListeningGenres(client)

    chartGenre = PieChartGenre(genres_data)
    canvasDataRow.addComponent(chartGenre.generateView())
    
    # Music acoustic features
    top_tracks = Statistics.get_50_recently_played_tracks(client)
    acoustics = [AudioFeature(track) for track in top_tracks]
    average = AudioFeatureAverage(acoustics)

    values_between_0_1 = {
      "Dancabilité": average.danceability,
      "Energie": average.energy,
      "Instrumentalité": average.instrumentalness,
      "Taux de paroles": average.speechiness,
      "Positivité": average.valence
    }

    # Creating polar chart for values between 0 and 1
    # Only on windows
    if os.name == 'nt':
      from View.Components.PolarChart import PolarChart
      polarChart = PolarChart(values_between_0_1)
      canvasDataRow.addComponent(polarChart)
    
    # Figure datarow for audio features in %
    featuresDataRow = MainWindow.createDataRow("Vos écoutes sont en moyenne...")
    
    labelDanceability = MainWindow.createFigureLabel(f"{average.danceability * 100:.1f}%", "dansantes")
    featuresDataRow.addComponent(labelDanceability)
    
    labelEnergy = MainWindow.createFigureLabel(f"{average.energy * 100:.1f}%", "énergiques")
    featuresDataRow.addComponent(labelEnergy)
    
    labelInstrumentalness = MainWindow.createFigureLabel(f"{average.instrumentalness * 100:.1f}%", "instrumentales")
    featuresDataRow.addComponent(labelInstrumentalness)
    
    labelSpeechiness = MainWindow.createFigureLabel(f"{average.speechiness * 100:.1f}%", "parlées")
    featuresDataRow.addComponent(labelSpeechiness)
    
    labelValence = MainWindow.createFigureLabel(f"{average.valence * 100:.1f}%", "positives")
    featuresDataRow.addComponent(labelValence)
    
    self.view.mainLayout.addWidget(figuresDataRow)
    self.view.mainLayout.addWidget(featuresDataRow)
    self.view.mainLayout.addWidget(canvasDataRow)