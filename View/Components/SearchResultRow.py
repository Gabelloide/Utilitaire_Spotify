import threading
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
import requests
import utils
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

class SearchResultRow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMaximumHeight(65)
        self.main_layout = QHBoxLayout(self)
        
        # Image Track
        self.image_label = QLabel(self)
        self.main_layout.addWidget(self.image_label)
        
        # Layout for the information
        self.info_layout = QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)
        
        # Logo
        self.logo_label = QLabel(self)
        self.main_layout.addWidget(self.logo_label)
    
    def set_logo(self, logo_path):
        self.logo_label.setPixmap(QPixmap(logo_path))

    def downloadAndSetImage(self, url, filename):
        """Downloads the image from the internet and sets it to the QLabel.
        - Checks for the image existence in the cache.
        - If the image is not in the cache, it downloads it in a separate thread.
        """
        if utils.exists_in_cache(filename):
            data = utils.load_from_cache(filename)
            self.set_image(data)
        else:
            # Downloading the image in a separate thread
            threading.Thread(target=self.thread_download, args=(url, filename)).start()

    def thread_download(self, url, filename):
        """Used by a separate thread to download the image from the internet.
        - Gets the image data from the URL via a GET request.
        - Saves the image data to the cache.
        - Sets the image to the QLabel using the data downloaded.
        """
        try:
            print(f"Downloading image: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.content
            self.set_image(data)
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            
    def set_image(self, data):
        """Sets the image to the QLabel."""
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setMaximumWidth(50)


class TrackResult(SearchResultRow):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.title_label = QLabel("Title track", self)
        self.artist_label = QLabel("ArtistName", self)
        self.duration_label = QLabel("Duration Track", self)
        
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.artist_label)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.insertSpacerItem(2, spacer)
        self.main_layout.insertWidget(3,self.duration_label)
    
    def set_title(self, title):
        self.title_label.setText(title)
    
    def set_artist(self, artist):
        self.artist_label.setText(artist)
    
    def set_duration(self, duration):
        self.duration_label.setText(duration)


class ArtistResult(SearchResultRow):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.artist_label = QLabel("ArtistName", self)
        self.listeners_label = QLabel("Number Listeners", self)
        
        self.info_layout.addWidget(self.artist_label)
        self.info_layout.addWidget(self.listeners_label)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.insertSpacerItem(2, spacer)
        
    def set_artist(self, artist):
        self.artist_label.setText(artist)
    
    def set_listeners(self, listeners):
        self.listeners_label.setText(listeners)


class AlbumResult(SearchResultRow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.album_title_label = QLabel("Title album", self)
        self.artist_label = QLabel("ArtistName", self)
        
        self.info_layout.addWidget(self.album_title_label)
        self.info_layout.addWidget(self.artist_label)
    
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.main_layout.insertSpacerItem(2, spacer)
        
    def set_album_title(self, title):
        self.album_title_label.setText(title)
    
    def set_artist(self, artist):
        self.artist_label.setText(artist)
