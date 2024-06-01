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
    self.results = QVBoxLayout()
    
    self.mainLayout = QVBoxLayout()
    self.mainLayout.addLayout(self.searchBar)
    self.mainLayout.addLayout(self.results)

    # Ajouter un QSpacerItem
    spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.mainLayout.addItem(spacer)
    
    self.setLayout(self.mainLayout)

    
    # CSS
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()

   