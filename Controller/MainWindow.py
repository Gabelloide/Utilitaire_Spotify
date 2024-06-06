from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase, QIcon

from View import LoginPage, NavBar
from View.ProfilePage import ProfilePage
from View.Components.ImageLabel import ImageLabel, AlbumImageLabel, ArtistImageLabel, TrackImageLabel, ProfilePictureImageLabel, TrendImageLabel
from View.Components.DataRow import DataRow
from View.Components.FigureLabel import FigureLabel
from Controller import ControllerLogin
from Controller import ControllerNavBar


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.stackedWidget = QStackedWidget()
    self.pages = {} # Dict of String:QWidget to store the pages by name
    self.navBar = NavBar.NavBar(self) # Transmetting the parent to the NavBar
    self.navBar.controller = ControllerNavBar.ControllerNavBar(self.navBar)

    self.setWindowTitle("SpotInsights")
    self.setStyleSheet("background-color: #211f1f;")
    self.resize(1280, 720)

    self.loginPage = LoginPage.LoginPage(self)
    self.loginPage.controller = ControllerLogin.ControllerLogin(self.loginPage)

    self.addPage("LoginPage", self.loginPage)

    # Create a layout to hold the NavBar and the stackedWidget
    layout = QHBoxLayout()
    layout.addWidget(self.navBar)
    layout.addWidget(self.stackedWidget)

    # Create a container widget to hold the layout
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)


  def addPage(self, pageName: str, page: QWidget):
    self.stackedWidget.addWidget(page)
    self.pages[pageName] = page

    # If we are on the login page, hide the NavBar
    if isinstance(page, LoginPage.LoginPage):
        self.navBar.setVisible(False)
    else:
        self.navBar.setVisible(True)


  def showPage(self, pageName: str):
    self.stackedWidget.setCurrentWidget(self.pages[pageName])
    self.repaint()


  # Utils - Controllers themselves are not supposed to create UI elements, so we provide a way to create them here
  @staticmethod
  def createImageLabel(text:str, labelType: str = "default"):
    """Creates an ImageLabel with the given text. Type is used to specify which daughter class to use."""
    allowedTypes = ["default", "track", "artist", "album", "profilePicture"]
    if labelType not in allowedTypes:
      raise ValueError(f"Label type must be one of {allowedTypes}")
    match labelType:
      case "track":
        label = TrackImageLabel(text)
      case "artist":
        label = ArtistImageLabel(text)
      case "album":
        label = AlbumImageLabel(text)
      case "profilePicture":
        label = ProfilePictureImageLabel(text)
      case _:
        label = ImageLabel(text)
    label.setMaximumSize(100, 100)
    return label


  @staticmethod
  def createTrendImageLabel(text:str, counter:int, upvoteState:bool, attachedTrack):
    """Creates a TrendImageLabel with the given text and counter."""
    label = TrendImageLabel(text, counter, upvoteState, attachedTrack)
    label.setMaximumSize(200,200)
    return label
  

  @staticmethod
  def createDataRow(title: str):
    """Creates a DataRow component."""
    return DataRow(title)


  @staticmethod
  def createFigureLabel(number: str, text: str):
    """Creates a FigureLabel component."""
    return FigureLabel(number, text)