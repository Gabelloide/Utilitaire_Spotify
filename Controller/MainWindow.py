from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QStackedWidget, QVBoxLayout, QMainWindow
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase

from View import LoginPage
from View.ProfilePage import ProfilePage
from Controller import ControllerLogin

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.stackedWidget = QStackedWidget()
    
    self.pages = []
    
    self.setWindowTitle("Utilitaire Spotify")
    self.resize(1280, 720)
    
    self.loginPage = LoginPage.LoginPage(self)
    self.loginPage.controller = ControllerLogin.ControllerLogin(self.loginPage)
    
    self.addPage(self.loginPage)
    
    self.centralWidget = self.stackedWidget
    self.setCentralWidget(self.centralWidget)
    
    
  def addPage(self, page: QWidget):
    self.stackedWidget.addWidget(page)
    self.pages.append(page)


  def showPage(self, pagePointer: QWidget):
    for i, page in enumerate(self.pages):
      if page == pagePointer:
        self.stackedWidget.setCurrentIndex(i)
        break