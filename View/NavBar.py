from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton 
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class NavBar(QWidget):
    def __init__(self, parentView):
        super().__init__()
        
        self.parentView = parentView
        self.controller = None

        layout = QVBoxLayout()

        self.btnProfile = QPushButton()
        self.btnSearch = QPushButton()
        self.btnTrend = QPushButton()
        self.btnFriends = QPushButton()
        self.btnStats = QPushButton()
        self.btnReco = QPushButton()

        self.buttonStyleSheet = """
          QPushButton {
              border: 0px;
              background-color: #211f1f;
              border-radius: 10px;
          }
          QPushButton:hover {
              background-color: #333333;
          }
        """
        
        self.focusedButtonStyleSheet = """
          QPushButton {
            border: 0px;
            background-color: #333333;
            border-radius: 10px;
          }
          QPushButton:hover {
            background-color: #333333; 
          }
        """
        
        self.setStyleSheet("background-color: #000000;") # ! Fix, color not applied

        self.btnProfile.setIcon(QIcon("Assets/icons/profile.png"))
        self.btnSearch.setIcon(QIcon("Assets/icons/search.png"))
        self.btnTrend.setIcon(QIcon("Assets/icons/trend.png"))
        self.btnFriends.setIcon(QIcon("Assets/icons/friends.png"))
        self.btnStats.setIcon(QIcon("Assets/icons/stats.png"))
        self.btnReco.setIcon(QIcon("Assets/icons/recommendations.png"))
        
        self.buttons = [self.btnProfile, self.btnSearch, self.btnTrend, self.btnFriends, self.btnStats, self.btnReco]
        for button in self.buttons:
            button.setFixedSize(64, 64)
            button.setIconSize(QSize(64, 64))
            button.setStyleSheet(self.buttonStyleSheet)
            layout.addWidget(button)


        self.setLayout(layout)