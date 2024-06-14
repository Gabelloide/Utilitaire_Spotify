from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

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
    self.mainLayout.addLayout(self.searchSection, 1)
    
    self.setLayout(self.mainLayout)
