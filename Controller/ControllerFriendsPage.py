import socket, pickle
from Model.User import User
from View.FriendsPage import FriendsPage
from View.Components.SearchResultRow import ProfileResult
from View.Components.LabelSubTitle import LabelSubTitle
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI
import network
from PyQt6.QtCore import QTimer

class ControllerFriendsPage:
  
  def __init__(self, user:User, view: FriendsPage):
    self.view = view
    self.user = user
    
    self.friendsList = self.fetchFriends() # Fetching once upon init
    self.buildFriendsDisplay(self.friendsList)
    
    # Search bar logic : when the user types in the search bar, we search for the user, only one request every 500ms
    
    self.timer = QTimer()
    self.timer.setSingleShot(True)
    self.timer.timeout.connect(self.searchFriends)
    self.view.searchInput.textChanged.connect(lambda : self.timer.start(500))
    self.view.refreshButton.clicked.connect(self.refreshFriends)


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


  def buildFriendsDisplay(self, friendsList):
    """Builds the display of the friends list"""

    friendsDataRow = MainWindow.createDataRow("Les amis de " + self.user.display_name, self.view)
    
    client = SpotifyAPI.get_spotify_client()
    
    if friendsList is None or len(friendsList) == 0:
      labelNothing = LabelSubTitle("Vous n'avez pas encore d'amis. Essayez de chercher quelqu'un !")
      self.view.dataFriends.addWidget(labelNothing)
      return
    
    for friend in friendsList:
      friend_user = User(client.user(friend))
      
      friendImageLabel = MainWindow.createImageLabel(f"{friend_user.display_name}", "profilePicture")
      friendImageLabel.attachedObject = friend_user
      friendImageLabel.downloadAndSetImage(friend_user.getBigProfilePicture(), friend_user.id)

      friendsDataRow.addComponent(friendImageLabel)
    
    self.view.dataFriends.addWidget(friendsDataRow)


  def searchFriends(self):
    """Searches for users in the database according to the query.
    We are looking for users present inside the database.
    Client must ask the server to search for users in the database. (self.fetchUsers(query))"""
    self.clearResults()
    
    search = self.view.searchInput.text()
    client = SpotifyAPI.get_spotify_client()
    currentUserID = User(client.current_user()).id

    if search.strip():
      
      usersIDs = self.fetchUsers(search)
      
      if usersIDs is None:
        return
      
      usersObjects = [User(client.user(userID)) for userID in usersIDs if userID != currentUserID] # We don't want to display the current user in the search results
      
      relevantUsers : list[User] = []
      for user in usersObjects:
        # Can be found via name / ID
        if search.lower() in user.display_name.lower():
          relevantUsers.append(user)
      
      for user in relevantUsers:
        userResult = ProfileResult()
        userResult.set_profile(user.display_name)
        userResult.downloadAndSetImage(user.getBigProfilePicture(), user.id)
        userResult.attachedObject = user
        
        self.view.results.addWidget(userResult)


  def clearResults(self):
    """Clears the search results"""
    while self.view.results.count():
      child = self.view.results.takeAt(0)
      if child.widget():
        child.widget().deleteLater()


  def fetchUsers(self, query):
    """Asks the server for the users present in the database according to the query"""
    try:
      with network.connect_to_userinfo_server() as s:
        
        s.sendall(b"SEARCH_USERS") # Asking for the users list
        
        response = network.receive_all(s)
        
        if response != b"READY":
          print(f"Server response: {response}")
          return
        
        # Sending the query to the server to get the users list
        s.sendall(query.encode())
        
        # Waiting for the server to send the users list
        data = network.receive_all(s)
        
        usersIDs = pickle.loads(data)
        return usersIDs

    except socket.error as e:
      print(f"Socket error on fetchUsers: {e}")
      return
  
    except Exception as e:
      print(f"Unexpected error in ControllerFriendsPage, fetchUsers: {e}")
      return


  def refreshFriends(self):
    """Refreshes the friends list"""
    # Clearing the dataFriends
    while self.view.dataFriends.count():
      child = self.view.dataFriends.takeAt(0)
      if child.widget():
        child.widget().deleteLater()
    
    # Fetching the friends list again
    self.friendsList = self.fetchFriends()
    # Rebuilding the friends display
    self.buildFriendsDisplay(self.friendsList)


  def addFriend(self, friend: User):
    """Adds a friend to the user's friend list
    Will interrogate the server to ask it to perform the SQL operation"""
    try:
      with network.connect_to_userinfo_server() as s:
        
        s.sendall(b"ADD_FRIEND") # Asking for the users list
        
        response = network.receive_all(s)
        
        if response != b"READY":
          print(f"Server response: {response}")
          return
        
        # Sending the friend ID to the server to add the friend
        data = (self.user.id, friend.id)
        serialized_data = pickle.dumps(data)
        s.sendall(serialized_data)
        
        # Waiting for the server to say that the SQL operation is OK
        response = network.receive_all(s)
        
        if response != b"SQL_OK":
          print("SQL operation failed")
          return
        
        # Refreshing the friends list
        self.refreshFriends()
    
    except socket.error as e:
      print(f"Socket error on addFriend: {e}")
      return
    
    except Exception as e:
      print(f"Unexpected error in ControllerFriendsPage, addFriend: {e}")
      return


  def removeFriend(self, friend: User):
    """Removes a friend from the user's friend list
    Will interrogate the server to ask it to perform the SQL operation"""
    try:
      with network.connect_to_userinfo_server() as s:
        
        s.sendall(b"REMOVE_FRIEND") # Asking for the users list
        
        response = network.receive_all(s)
        
        if response != b"READY":
          print(f"Server response: {response}")
          return
        
        # Sending the friend ID to the server to remove the friend
        data = (self.user.id, friend.id)
        serialized_data = pickle.dumps(data)
        s.sendall(serialized_data)
        
        # Waiting for the server to say that the SQL operation is OK
        response = network.receive_all(s)
        
        if response != b"SQL_OK":
          print("SQL operation failed")
          return
        
        # Refreshing the friends list
        self.refreshFriends()
    
    except socket.error as e:
      print(f"Socket error on removeFriend: {e}")
      return
    
    except Exception as e:
      print(f"Unexpected error in ControllerFriendsPage, removeFriend: {e}")
      return