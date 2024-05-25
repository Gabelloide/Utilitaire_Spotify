import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget 
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class NavBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.btnProfile = QPushButton()
        self.btnSearch = QPushButton()
        self.btnTrend = QPushButton()
        self.btnFriends = QPushButton()

        self.btnProfile.setIcon(QIcon("Assets/icons/profile.png"))
        self.btnSearch.setIcon(QIcon("Assets/icons/search.png"))
        self.btnTrend.setIcon(QIcon("Assets/icons/trend.png"))
        self.btnFriends.setIcon(QIcon("Assets/icons/friends.png"))

        iconSize = QSize(50, 50) 
        self.btnProfile.setIconSize(iconSize)
        self.btnSearch.setIconSize(iconSize)
        self.btnTrend.setIconSize(iconSize)
        self.btnFriends.setIconSize(iconSize)

        self.setStyleSheet("""
            QPushButton {
                background-color: #292929;
            }
        """)
        
        layout.addWidget(self.btnProfile)
        layout.addWidget(self.btnSearch)
        layout.addWidget(self.btnTrend)
        layout.addWidget(self.btnFriends)
        
        self.setLayout(layout)
