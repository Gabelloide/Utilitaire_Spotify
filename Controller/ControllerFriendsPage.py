from Model.User import User
from View.FriendsPage import FriendsPage


class ControllerFriendsPage:
  
  def __init__(self, user:User, view: FriendsPage):
    self.view = view
    self.user = user
    
    # ! Don't think there is a way to get private followers
    # ! Maybe cook a friend system with the app and server?