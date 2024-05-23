from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase
from Model import User

class ProfilePage(QWidget):
  def __init__(self, user: User.User, parentView):
    super().__init__()
    
    self.parentView = parentView
    

    
    layout = QGridLayout()
    
    # Add the custom font to the QFontDatabase
    font_id = QFontDatabase.addApplicationFont("Assets/HelveticaNeueMedium.otf")
    if font_id == -1:
      print("Failed to load the custom font")
      return
    
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    
    self.labelTitle = QLabel("Mon profil")
    self.labelProfile = QLabel(user.display_name)
    
    layout.addWidget(self.labelTitle, 0, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(self.labelProfile, 1, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
    
    self.setLayout(layout)