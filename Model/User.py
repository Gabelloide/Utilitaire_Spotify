import Controller.SpotifyAPI as SpotifyAPI
from Model import Artist, Track, Album
from typing import List

class User:

  def __init__(self, userDict) -> None:
    self.display_name   : str  = userDict.get('display_name')
    self.external_urls  : dict = userDict.get('external_urls', {})
    self.followers      : dict = userDict.get('followers', {})
    self.href           : str  = userDict.get('href')
    self.id             : str  = userDict.get('id')
    self.images         : list = userDict.get('images', [])
    self.uri            : str  = userDict.get('uri')
    self.followers      : dict = userDict.get('followers', {})


  def __str__(self) -> str:
    return self.display_name
  

  def getBigProfilePicture(self) -> str:
    imageURL = None
    max_height = 0
    for image in self.images:
      if image['height'] > max_height:
        max_height = image['height']
        imageURL = image['url']
    return imageURL