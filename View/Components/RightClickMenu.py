from PyQt6.QtWidgets import QMenu, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QFontDatabase, QFont
import ui_utils
from View.Components.ImageLabel import ImageLabel
from View.Components.OverlayInfo import OverlayTrackInfo, OverlayArtistInfo, OverlayAlbumInfo

class RightClickMenu(QMenu):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.parentComponent: ImageLabel = parent

    # Import font
    font = ui_utils.getFont(20)
    self.setFont(font)

    self.setStyleSheet("""
      QMenu {
        background-color: #282828;
        color: #fff; /* White text */
        border: 3px solid #282828;
        border-radius: 10px;
        font-size: 15px;
      }
      
      QMenu::item {
        padding: 10px 20px;
      }

      QMenu::item:selected {
        background-color: #3E3E3E;
        border-radius: 10px;
      }
    """)


class TrackRightClickMenu(RightClickMenu):
  def __init__(self, parent: ImageLabel =None):
    super().__init__(parent)
    
    self.infoTrack = QAction(f"Informations sur ce titre...", self)
    self.addAction(self.infoTrack)
    self.infoTrack.triggered.connect(self.showOverlay)

    self.addToTrends = QAction("Ajouter ce titre aux tendances...", self)
    self.addAction(self.addToTrends)
    
    
  def showOverlay(self):
    mainWindow = self.parentComponent.window()
    overlay = OverlayTrackInfo(mainWindow)
    overlay.createContent(self.parentComponent.attachedObject)
    overlay.show()


class ArtistRightClickMenu(RightClickMenu):
  def __init__(self, parent=None):
    super().__init__(parent)
    
    self.infoArtist = QAction("Informations sur cet artiste...", self)
    self.addAction(self.infoArtist)
    self.infoArtist.triggered.connect(self.showOverlay)
    
  def showOverlay(self):
    mainWindow = self.parentComponent.window()
    overlay = OverlayArtistInfo(mainWindow)
    overlay.createContent(self.parentComponent.attachedObject)
    overlay.show()


class AlbumRightClickMenu(RightClickMenu):
  def __init__(self, parent=None):
    super().__init__(parent)
    
    self.infoAlbum = QAction("Informations sur cet album...", self)
    self.addAction(self.infoAlbum)
    self.infoAlbum.triggered.connect(self.showOverlay)
    
  def showOverlay(self):
    mainWindow = self.parentComponent.window()
    overlay = OverlayAlbumInfo(mainWindow)
    overlay.createContent(self.parentComponent.attachedObject)
    overlay.show()


class ProfilePictureRightClickMenu(RightClickMenu):
  def __init__(self, parent=None):
    super().__init__(parent)
    
    self.itsYou = QAction("C'est vous !", self)
    self.addAction(self.itsYou)


