from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class FriendsPage(QWidget):
  
  def __init__(self, parentView) -> None:
    super().__init__()

    self.parentView = parentView
    
    self.friendsSection = QVBoxLayout()
    self.searchSection = QVBoxLayout()
    
    self.mainLayout = QHBoxLayout()
    
    self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Mes amis")
    
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)
    
    self.containerTitleSearch = QHBoxLayout()
    self.labelSearch = QLabel("Rechercher un ami")
    
    spacerItem_left_search = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitleSearch.addItem(spacerItem_left_search)
    self.containerTitleSearch.addWidget(self.labelSearch)
    spacerItem_right_search = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitleSearch.addItem(spacerItem_right_search)
    
    # CSS
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()
    self.labelTitle.setStyleSheet(stylesheet)
    self.labelSearch.setStyleSheet(stylesheet)

    
    self.friendsSection.addLayout(self.containerTitle)
    self.searchSection.addLayout(self.containerTitleSearch)
    self.mainLayout.addLayout(self.friendsSection, 1)  # Stretch factor of 1 to spread evenly
    
    self.searchBar = QHBoxLayout()
    searchContainer = QWidget()
    searchContainerLayout = QHBoxLayout(searchContainer)
    
    self.searchInput = QLineEdit()
    self.searchInput.setPlaceholderText("Rechercher un ami...")
    
    searchContainer.setStyleSheet("""
        QWidget {
            border: 2px solid gray;
            border-radius: 20px;
            padding: 15px;
        }
        QLineEdit {
            border: none;
            border-radius: 0px;
            padding: 5px;
            margin: 5px;
            font-size: 14pt;
        }
        QLabel {
          border: none;
          background-color: transparent;
        }
        
    """)
    
    searchIcon = QLabel()
    searchIcon.setPixmap(QPixmap('Assets/icons/search_icon.png').scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    
    searchContainerLayout.addWidget(searchIcon)
    searchContainerLayout.addWidget(self.searchInput)
    searchContainerLayout.setContentsMargins(0, 0, 0, 0)
    searchContainerLayout.setSpacing(5)
    
    self.searchBar.addWidget(searchContainer)
    self.searchBar.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    self.searchSection.addWidget(searchContainer)
    
    self.results = QVBoxLayout()
    self.searchSection.addLayout(self.results)
    
    spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.searchSection.addItem(spacer)
    
    
    self.mainLayout.addLayout(self.searchSection, 1)
    
    self.setLayout(self.mainLayout)
