from typing import List, Dict

class Artist:
  def __init__(self, artistDict) -> None:
    """The artistDict is composed of nested dictionaries that contains the artist's information
    external_urls, followers, genres, href, id, images, name, popularity, type, uri."""
    self.external_urls      : dict = artistDict.get('external_urls')
    self.followers          : dict = artistDict.get('followers', {})
    self.genres             : list = artistDict.get('genres', [])
    self.href               : str  = artistDict.get('href')
    self.id                 : str  = artistDict.get('id')
    self.images             : List[Dict[str, str]] = artistDict.get('images', [])
    self.name               : str = artistDict.get('name')
    self.popularity         : int = artistDict.get('popularity')
    self.uri                : str = artistDict.get('uri') # Spotify URI for the artist


  def __str__(self) -> str:
    return self.name

  def __eq__(self, other) -> bool:
    return self.id == other.id
  
  def __hash__(self) -> int:
    return hash(self.id)
  
  def getTotalFollowers(self):
    return self.followers['total']
  

  def getFormattedFollowers(self):
    """Returns a string with the number of followers formatted to space digets every 3 digits"""
    return f"{self.getTotalFollowers():,}"


  def getBigPicture(self) -> str:
    """Returns the URL of the biggest picture available for the artist."""
    imageURL = None
    max_height = 0
    for image in self.images:
      if image['height'] > max_height:
        max_height = image['height']
        imageURL = image['url']
    return imageURL