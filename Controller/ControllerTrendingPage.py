from Model.User import User
from Model.Track import Track

from View.TrendingPage import TrendingPage
from Controller import SpotifyAPI

import constants
import socket, pickle

class ControllerTrendingPage:
  
  def __init__(self, user:User, view: TrendingPage):
    self.view = view
    self.user = user
    



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