from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QStackedWidget, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase

from View import LoginPage, NavBar
from View.ProfilePage import ProfilePage
from Controller import ControllerLogin


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.stackedWidget = QStackedWidget()
    self.pages = []
    self.navBar = NavBar.NavBar()

    self.setWindowTitle("Utilitaire Spotify")
    self.setStyleSheet("background-color: #211f1f;")
    self.resize(1280, 720)

    self.loginPage = LoginPage.LoginPage(self)
    self.loginPage.controller = ControllerLogin.ControllerLogin(self.loginPage)

    self.addPage(self.loginPage)

    # Créer un layout horizontal et ajouter la NavBar et le stackedWidget
    layout = QHBoxLayout()
    layout.addWidget(self.navBar)
    layout.addWidget(self.stackedWidget)

    # Créer un widget pour contenir le layout et le définir comme widget central
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)


  def addPage(self, page: QWidget):
    self.stackedWidget.addWidget(page)
    self.pages.append(page)

    # Si la page est la page de login, rendre la NavBar invisible
    if isinstance(page, LoginPage.LoginPage):
        self.navBar.setVisible(False)
    else:
        self.navBar.setVisible(True)

  def showPage(self, pagePointer: QWidget):
    for i, page in enumerate(self.pages):
      if page == pagePointer:
        self.stackedWidget.setCurrentIndex(i)
        break