import socket, pickle
from Model.User import User
from View.FriendsPage import FriendsPage
from View.Components.LabelSubTitle import LabelSubTitle
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI
import network

class ControllerFriendsPage:
  
  def __init__(self, user:User, view: FriendsPage):
    self.view = view
    self.user = user

    self.buildFriendsDisplay()


  def fetchFriends(self):
    """Asks the server for the list of friends of the user, and returns it"""
    try:
      with network.connect_to_userinfo_server() as s:
        
        s.sendall(b"GET_FRIENDS") # Asking for the friends list
        
        response = network.receive_all(s)
        
        if response != b"READY":
          print(f"Server response: {response}")
          return
        
        # Sending the user ID to the server to get the friends list
        s.sendall(self.user.id.encode())
        
        # Waiting for the server to send the friends list
        data = network.receive_all(s)
        
        friendsList = pickle.loads(data)
        return friendsList

    except socket.error as e:
      print(f"Socket error on fetchFriends: {e}")
      return
  
    except Exception as e:
      print(f"Unexpected error in ControllerFriendsPage, fetchFriends: {e}")


  def buildFriendsDisplay(self):
    """Builds the display of the friends list"""
    friendsList = self.fetchFriends()

    friendsDataRow = MainWindow.createDataRow("Les amis de " + self.user.display_name)
    
    client = SpotifyAPI.get_spotify_client()
    
    if friendsList is None or len(friendsList) == 0:
      labelNothing = LabelSubTitle("Vous n'avez pas encore d'amis. Essayez de chercher quelqu'un !")
      self.view.friendsSection.addWidget(labelNothing)
      return
    
    for friend in friendsList:
      friend_user = User(client.user(friend))
      
      friendImageLabel = MainWindow.createImageLabel(f"{friend_user.display_name}", "profilePicture")
      friendImageLabel.attachedObject = friend_user
      friendImageLabel.downloadAndSetImage(friend_user.getBigProfilePicture(), friend_user.id)

      friendsDataRow.addComponent(friendImageLabel)
    
    self.view.friendsSection.addWidget(friendsDataRow)