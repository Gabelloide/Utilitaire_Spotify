from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase, QIcon

from View import LoginPage, NavBar
from View.ProfilePage import ProfilePage
from View.Components.ImageLabel import ImageLabel
from View.Components.DataRow import DataRow
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
  def createImageLabel(text:str):
    """Creates an ImageLabel with the given text."""
    label = ImageLabel(text)
    label.setMaximumSize(100, 100)
    return label
  
  @staticmethod
  def createDataRow(title: str):
    """Creates a DataRow component."""
    return DataRow(title)