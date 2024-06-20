from Model.User import User
from Model.Track import Track

from View.TrendingPage import TrendingPage
from View.Components.LabelSubTitle import LabelSubTitle
from Controller import SpotifyAPI
from Controller.MainWindow import MainWindow

import network
import socket, pickle, json

class ControllerTrendingPage:
  
  def __init__(self, user:User, view: TrendingPage):
    self.view = view
    self.user = user
    
    self.trends = ControllerTrendingPage.fetchTrends() # Fetch the trends from the server once upon instanciation
    
    # FetchTrends also when the user clicks the refreshButton
    self.view.refreshButton.clicked.connect(lambda: self.refreshFilteredByGenre("Tous les genres"))
    self.view.genreChangedSignal.connect(lambda genre: self.refreshFilteredByGenre(genre))
    # Creating a datarow to display trends
    trendingDataRow = self.createTrends("Tous les genres")

    if trendingDataRow.getDataCount() > 0:
      self.view.containerTrends.addWidget(trendingDataRow)
    else:
      labelNothing = LabelSubTitle("On dirait qu'il n'y a rien ici pour le moment. Essayez d'ajouter des pistes aux tendances !")
      self.view.containerTrends.addWidget(labelNothing)


  def createTrends(self, selected_genre="Tous les genres"):
      """Method to create the trends datarow"""
      trackIDs = [trackID for trackID in self.trends.keys()]
      trendingDataRow = MainWindow.createDataRow("Pistes du moment")
      
      # Gathering all track objects from API
      client = SpotifyAPI.get_spotify_client()
      trackObjects = ControllerTrendingPage.trackIDs_to_Objects(trackIDs, client)
      currentUserID = self.user.id
      
      # Create a set to store unique genres and add the genres to the genreFilter(comboBox)
      self.view.clearComboBox()
      self.addGenresToFilter(trackObjects, client, selected_genre)

      # Adding the track objects to the datarow
      for track in trackObjects:
        track_genre = track.get_track_genre(client)
        # If the genre is in the selected genre or if the selected genre is "Tous les genres"
        if selected_genre in track_genre or selected_genre == "Tous les genres":
          trackScore = self.trends[track.id]['upvotes']
          addedBy = ControllerTrendingPage.userID_to_User(self.trends[track.id]['addedBy'], client)
          upvoteState = currentUserID in self.trends[track.id]['upvotedBy']

          label = MainWindow.createTrendImageLabel(f"{track.name} : ajoutée par {addedBy.display_name}", trackScore, upvoteState, track, self)
          label.downloadAndSetImage(track.album.getBigCover(), track.id)

          trendingDataRow.addComponent(label)

      return trendingDataRow


  def addGenresToFilter(self, trackObjects, client, selected_genre):
      """Method to add unique genres to the genreFilter"""
      unique_genres = set()
      for track in trackObjects:
          track_genre = track.get_track_genre(client)
          # Add the genre to the set of unique genres
          unique_genres.update(track_genre)
      # Convert the set back to a list
      unique_genres = list(unique_genres)
      # adding unique genres to the genreFilter of the DataRow
      self.view.genreFilter.addItem("Tous les genres")
      for genre in unique_genres:
            self.view.genreFilter.addItem(genre)

      self.view.genreFilter.setCurrentText(selected_genre)
      self.view.connectComboBox()


  def refreshFilteredByGenre(self, genre:str):
    """Method to filter the trends by genre"""
    # Clearing the mainLayout, rebuilding the trends and adding them to the layout
    while self.view.containerTrends.count():
      child = self.view.containerTrends.takeAt(0)
      if child.widget():
        child.widget().deleteLater() 
    # Adding the new trends
    self.trends = ControllerTrendingPage.fetchTrends()
    trendingDataRow = self.createTrends(genre)
    if trendingDataRow.getDataCount() > 0:
      self.view.containerTrends.addWidget(trendingDataRow)
    else:
      labelNothing = LabelSubTitle("On dirait qu'il n'y a rien ici pour le moment. Essayez d'ajouter des pistes aux tendances !")
      self.view.containerTrends.addWidget(labelNothing)


  def refreshView(self):
    """Method to refresh the view with the latest trends"""
    # Clearing the mainLayout, rebuilding the trends and adding them to the layout
    while self.view.containerTrends.count():
      child = self.view.containerTrends.takeAt(0)
      if child.widget():
        child.widget().deleteLater()
    # Adding the new trends
    self.trends = ControllerTrendingPage.fetchTrends()
    trendingDataRow = self.createTrends()
    if trendingDataRow.getDataCount() > 0:
      self.view.containerTrends.addWidget(trendingDataRow)
    else:
      labelNothing = LabelSubTitle("On dirait qu'il n'y a rien ici pour le moment. Essayez d'ajouter des pistes aux tendances !")
      self.view.containerTrends.addWidget(labelNothing)


  @staticmethod
  def trackIDs_to_Objects(trackIDs:list, client):
    """Method to convert a list of track IDs to a list of Track objects
    First, batches of 50 ids must be made to not exceed the API limit
    Then, calling API to fetch everything into Track objects"""
    if len(trackIDs) == 0:
      return []
    if len(trackIDs) > 50:
      # Splitting the list into batches of 50
      batches = [trackIDs[i:i+50] for i in range(0, len(trackIDs), 50)]
      trackObjects = []
      for batch in batches:
        tracks = client.tracks(batch)
        trackObjects += [Track(track) for track in tracks]
    else:
      tracks = client.tracks(trackIDs)['tracks']
      trackObjects = [Track(track) for track in tracks]
    return trackObjects


  @staticmethod
  def userID_to_User(userID:str, client):
    """Method to convert a user ID to a User object"""
    return User(client.user(userID))


  @staticmethod
  def sendTrackToTrends(track: Track):
    """Static method to send a track object to the server for trending
    This is called by the TrackRightClickMenu class, 
    regardless of any instanciation"""
    
    client = SpotifyAPI.get_spotify_client()
    currentUser = User(client.current_user())
    
    # Connecting to the server
    try:
        with network.connect_to_trends_server() as s:
          # Send the request to the server
          s.sendall(b"SEND_TRACK") # Asking the authorization to send the track to be added to trends
          
          # Waiting for the server to be ready
          response = network.receive_all(s)
          
          if response != b"READY":
            print(f"Server response: {response}")
            return
          
          # If the server is ready, sending the track
          # Sending the userID and the track ID. Tuple must be serialized w/ pickle
          data = (track.id, currentUser.id)
          serizalized_tuple = pickle.dumps(data)
          s.sendall(serizalized_tuple)

    except socket.error as e:
      print(f"Socket error: {e}")


  @staticmethod
  def fetchTrends():
    """Static method to fetch the trending tracks from the server
    This is called regardless of any instanciation"""

    try:
        with network.connect_to_trends_server() as s:
          # Send the request to the server
          s.sendall(b"ASKING_TRENDS") # Send a simple string to request the trends
          
          # Receive the data : a json dict
          data = network.receive_all(s)
          # Deserialize the data
          trends = json.loads(data)

          return trends
        
    except socket.error as e:
      print(f"Socket error while fetching trends: {e}")
      
    except Exception as e:
      print(f"Unexpected error in ControllerTrendingPage: {e}")
      
    return {}


  @staticmethod
  def getUpvoteState(trackID:str):
    """Returns the upvote state of the current user given a trackID"""
    # Fetching trends from the server
    trends = ControllerTrendingPage.fetchTrends()
    
    # Fetching the current user
    client = SpotifyAPI.get_spotify_client()
    currentUser = User(client.current_user())
    
    # If the trackID is not in the trends, return False
    if trackID not in trends:
      return False
    
    # If the trackID is in the trends, check if the current user has upvoted it
    upvotedBy = trends[trackID]['upvotedBy']
    if currentUser.id in upvotedBy:
      return True
    
    return False
  
  
  @staticmethod
  def getUpvoteCount(trackID:str):
    """Returns the upvote count of a track given its trackID"""
    # Fetching trends from the server
    trends = ControllerTrendingPage.fetchTrends()
    
    # If the trackID is not in the trends, return 0
    if trackID not in trends:
      return 0
    
    # If the trackID is in the trends, return the upvote count
    return trends[trackID]['upvotes']
  

  @staticmethod
  def upvoteTrack(trackID:str):
    """Will contact the server to upvote the track
    If the user has already upvoted the track, it will remove the upvote"""
    # Fetching the current user
    client = SpotifyAPI.get_spotify_client()
    currentUser = User(client.current_user())
    
    # Connecting to the server
    try:
        with network.connect_to_trends_server() as s:
          # Tell the server that we want to upvote a track
          s.sendall(b"ASKING_UPVOTE")
          
          # Waiting for the server to be ready
          response = network.receive_all(s)
          if response != b"READY":
            print(f"Server response: {response}")
            return

          # If the server is ready, sending the track ID & user ID
          # Sending the userID and the track ID. Tuple must be serialized w/ pickle
          data = (trackID, currentUser.id)
          serizalized_tuple = pickle.dumps(data)
          s.sendall(serizalized_tuple)

    except socket.error as e:
      print(f"Socket error: {e}")