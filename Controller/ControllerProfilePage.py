from Model.User import User
from View.ProfilePage import ProfilePage
from Controller.MainWindow import MainWindow
from Controller import SpotifyAPI

class ControllerProfilePage:
  
  def __init__(self, user: User, view: ProfilePage):
    self.view: ProfilePage = view
    self.user = user

    # ------ Filling UI elements with data ------
    self.view.labelUsername.setText(f"Bienvenue, {self.user.display_name} !")

    # Download the image and set it to the label
    self.view.profilePicture.downloadAndSetImage(self.user.getBigProfilePicture(), self.user.id)

    # Download the user's top tracks, artists and albums
    client = SpotifyAPI.get_spotify_client()
    user_top_tracks = self.user.getTopTracks(client, limit=8)
    user_top_artists = self.user.getTopArtists(client, limit=8)
    user_top_albums = self.user.getTopAlbums(client, limit=8)

    # The album/artist/track ids are passed to the download manager to get them from cache if they are already downloaded
    for i, track in enumerate(user_top_tracks):
      label = MainWindow.createImageLabel(f"{i+1}. {track.name}", "track")
      label.attachedObject = track
      label.downloadAndSetImage(track.album.getBigCover(), track.id)
      self.view.containerTracks.addComponent(label)

    for i, artist in enumerate(user_top_artists):
      label = MainWindow.createImageLabel(f"{i+1}. {artist.name}", "artist")
      label.attachedObject = artist
      label.downloadAndSetImage(artist.getBigPicture(), artist.id)
      self.view.containerArtists.addComponent(label)

    for i, album in enumerate(user_top_albums):
      label = MainWindow.createImageLabel(f"{i+1}. {album.name}", "album")
      label.attachedObject = album
      label.downloadAndSetImage(album.getBigCover(), album.id)
      self.view.containerAlbums.addComponent(label)

    # Adding "more" buttons after the last element of each container
    self.view.createMoreButtons()