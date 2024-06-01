from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon

class SearchPage(QWidget):
  
  def __init__(self, parentView) -> None:
    super().__init__()

    self.parentView = parentView

    # Créer la barre de recherche
    self.searchBar = QHBoxLayout()

    # Créer un widget conteneur pour encapsuler l'icône et le champ de recherche
    searchContainer = QWidget()
    searchContainerLayout = QHBoxLayout(searchContainer)

    # Créer le champ de texte de recherche
    self.searchInput = QLineEdit()
    self.searchInput.setPlaceholderText("Que souhaitez-vous chercher ?")
    
    # Appliquer le style au widget conteneur
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

    # Ajouter l'icône de recherche
    searchIcon = QLabel()
    searchIcon.setPixmap(QPixmap('Assets/icons/search_icon.png').scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    # Ajouter l'icône et le champ de texte au layout du widget conteneur
    searchContainerLayout.addWidget(searchIcon)
    searchContainerLayout.addWidget(self.searchInput)
    searchContainerLayout.setContentsMargins(0, 0, 0, 0)
    searchContainerLayout.setSpacing(5)
    
    # Ajouter le widget conteneur à la barre de recherche
    self.searchBar.addWidget(searchContainer)
    self.searchBar.setAlignment(Qt.AlignmentFlag.AlignLeft)

    # Créer le layout principal
    self.results = QVBoxLayout()
    self.mainLayout = QVBoxLayout()
    self.mainLayout.addLayout(self.searchBar)
    self.mainLayout.addLayout(self.results)

    # Ajouter un QSpacerItem
    spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.mainLayout.addItem(spacer)
    
    self.setLayout(self.mainLayout)