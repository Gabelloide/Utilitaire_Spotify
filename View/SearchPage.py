from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLineEdit 
from PyQt6.QtGui import QIcon

class SearchPage(QWidget):
  
  def __init__(self, parentView) -> None:
    super().__init__()

    self.parentView = parentView
    self.searchBar = QHBoxLayout()
    self.searchInput = QLineEdit()
    self.searchButton = QPushButton("Rechercher")
    
    self.searchBar.addWidget(self.searchInput)
    self.searchBar.addWidget(self.searchButton)

    self.mainLayout = QVBoxLayout()
    
    def generateSearchResults(self, results):
      for idx, track in enumerate(results['tracks']['items']):
        print(f"{idx+1} - {track['name']} by {track['artists'][0]['name']}")
    
    """self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Rechercher")
    
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)
    """
    
    # CSS
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()

    #self.labelTitle.setStyleSheet(stylesheet)
    
    
    
    self.mainLayout.addLayout(self.searchBar)
    self.setLayout(self.mainLayout)