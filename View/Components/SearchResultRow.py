from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap

class SearchResultRow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Layout principal
        self.main_layout = QHBoxLayout(self)
        
        # Image Track
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("default_image.png"))  # Remplacez par une image par défaut
        self.main_layout.addWidget(self.image_label)
        
        # Layout pour les informations
        self.info_layout = QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)
        
        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("default_logo.png"))  # Remplacez par un logo par défaut
        self.main_layout.addWidget(self.logo_label)
        
    def set_image(self, image_path):
        self.image_label.setPixmap(QPixmap(image_path))
    
    def set_logo(self, logo_path):
        self.logo_label.setPixmap(QPixmap(logo_path))


class TrackResult(SearchResultRow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.title_label = QLabel("Title track", self)
        self.artist_label = QLabel("ArtistName", self)
        self.duration_label = QLabel("Duration Track", self)
        
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.artist_label)
        self.info_layout.addWidget(self.duration_label)
    
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
    
    def set_album_title(self, title):
        self.album_title_label.setText(title)
    
    def set_artist(self, artist):
        self.artist_label.setText(artist)
