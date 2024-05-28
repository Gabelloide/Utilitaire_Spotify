from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase, QFont

from Controller import MainWindow

class LoginPage(QWidget):
  def __init__(self, parentView):
    super().__init__()
    
    self.parentView: MainWindow.MainWindow = parentView
    self.loggedUser = None # The user that is currently logged in (filled by ControllerLogin)
    self.controller = None

    layout = QGridLayout()
    
    # Add the custom font to the QFontDatabase
    font_id = QFontDatabase.addApplicationFont("Assets/HelveticaNeueMedium.otf")
    if font_id == -1:
      print("Failed to load the custom font")
      return
    
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    font = QFont(custom_font, 20)

    # Read CSS
    with open("Assets/style.css", "r") as file:
      css = file.read()
    
    self.labelTitle = QLabel("Bienvenue sur SpotInsights !")
    self.labelTitle.setFont(font)
    self.labelTitle.setStyleSheet(css)  # Set the font size to 40px
    layout.addWidget(self.labelTitle, 0, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)  # Add the label to the layout

    self.buttonLogin = QPushButton("Se connecter via Spotify")
    self.buttonLogin.setFont(font)
    self.buttonLogin.setStyleSheet(css)  # Set button style
    layout.addWidget(self.buttonLogin, 1, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    layout.setRowStretch(0, 1)  # Set the first row to take 100% of the vertical space
    layout.setColumnStretch(0, 1)  # Set the first column to take 100% of the horizontal space

    self.setLayout(layout)

