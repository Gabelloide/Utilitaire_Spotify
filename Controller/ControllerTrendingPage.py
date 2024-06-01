from Model.User import User
from Model.Track import Track

from View.TrendingPage import TrendingPage
from View.Components.LabelSubTitle import LabelSubTitle
from Controller import SpotifyAPI
from Controller.MainWindow import MainWindow

import constants, utils
import socket, pickle, json

class ControllerTrendingPage:
  
  def __init__(self, user:User, view: TrendingPage):
    self.view = view
    self.user = user
    
    self.trends = self.fetchTrends() # Fetch the trends from the server once upon instanciation
    
    # FetchTrends also when the user clicks the refreshButton
    self.view.refreshButton.clicked.connect(lambda: self.refreshView())
    
    # Creating a datarow to display trends
    trendingDataRow = self.createTrends()
    
    if trendingDataRow.getDataCount() > 0:
      self.view.containerTrends.addWidget(trendingDataRow)
    else:
      labelNothing = LabelSubTitle("On dirait qu'il n'y a rien ici pour le moment. Essayez d'ajouter des pistes aux tendances !")
      self.view.containerTrends.addWidget(labelNothing)


  def createTrends(self):
    """Method to create the trends datarow"""
    trackIDs = [trackID for trackID in self.trends.keys()]
    trendingDataRow = MainWindow.createDataRow("Pistes du moment")
    
    # Gathering all track objects from API
    client = SpotifyAPI.get_spotify_client()
    trackObjects = ControllerTrendingPage.trackIDs_to_Objects(trackIDs, client)
    
    # Adding the track objects to the datarow
    for track in trackObjects:
      
      trackScore = self.trends[track.id]['upvotes']
      addedBy = ControllerTrendingPage.userID_to_User(self.trends[track.id]['addedBy'], client)

      label = MainWindow.createImageLabel(f"{track.name} : ajoutée par {addedBy.display_name} - {trackScore} upvotes", "track")
      label.attachedObject = track
      label.downloadAndSetImage(track.album.getBigCover(), track.id)
      trendingDataRow.addComponent(label)

    return trendingDataRow


  def refreshView(self):
    """Method to refresh the view with the latest trends"""
    # Clearing the mainLayout, rebuilding the trends and adding them to the layout
    while self.view.containerTrends.count():
      child = self.view.containerTrends.takeAt(0)
      if child.widget():
        child.widget().deleteLater()
    # Adding the new trends
    self.trends = self.fetchTrends()
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
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((constants.SERVER_ADDRESS, constants.SERVER_TREND_PORT))
        
        # Sending the userID and the track ID. Tuple must be serialized w/ pickle
        data = (track.id, currentUser.id)
        serizalized_tuple = pickle.dumps(data)
        s.sendall(serizalized_tuple)

    except socket.error as e:
      print(f"Socket error: {e}")


  def fetchTrends(self):
    """Static method to fetch the trending tracks from the server
    This is called by the TrendingPage class, regardless of any instanciation"""

    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((constants.SERVER_ADDRESS, constants.SERVER_TREND_FETCHING_PORT))
        
        # Send the request to the server
        s.sendall(b"GET_TRENDS") # Send a simple string to request the trends
        
        # Receive the data : data is a json dict
        data = utils.receive_all(s)
        
        # Deserialize the data
        trends = json.loads(data)

        return trends
        
    except socket.error as e:
      print(f"Socket error: {e}")
      
    except Exception as e:
      print(f"Unexpected error: {e}")
      
    return {}
