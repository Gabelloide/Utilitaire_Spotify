from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt
import ui_utils

class ZipUploadPage(QWidget):
    def __init__(self, parentView):
        super().__init__()

        self.parentView = parentView
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)  # Set the margins

        with open("Assets/style.css", "r") as file:
            stylesheet = file.read()
            
        self.labelTitle = QLabel("Pourquoi importer mes données ?")
        # Add the custom font to the QFontDatabase
        font = ui_utils.getFont(20)

        textLabelInfo = """
        <p>Spotify fournit des données concernant vos écoutes à travers leur API (Application Programming Interface), mais ne permet pas de préciser le nombre de fois que vous avez écouté un titre, un album ou un artiste. Pour avoir accès à des fonctionnalités plus précises, vous devrez importer votre historique d'écoutes.</p>

        <p>Si vous fournissez un fichier de données Spotify, vous aurez accès à :
        <ul>
        <li>Le nombre d'écoutes d'un morceau/artiste/album</li>
        <li>Votre historique d'écoutes au delà de 50 musiques, ce qui permet de calculer plus précisément tout le reste</li>
        </ul>
        </p>

        <p>Veuillez noter que nous ne prendrons pas en compte les écoutes ayant duré moins de 30 secondes, et l'écoute de podcasts.</p>

        """

        self.labelTitle.setFont(font)
        self.labelTitle.setFixedHeight(50)
        self.labelTitle.setStyleSheet("""
            font-size: 30px;
            color: white;
        """)

        self.labelInformations= QLabel(textLabelInfo)
        self.labelInformations.setWordWrap(True)  # Enable word wrapping
        self.labelInformations.setFont(font)  # Set the custom font
        self.labelInformations.setStyleSheet("""
            margin: 10px;
            font-size: 20px;
            color: white;
        """) # Center the text

        self.btnZipUpload = QPushButton("Téléverser mon fichier de données Spotify")
        self.setStyleSheet("""
        QPushButton {
          font-size: 20px;
          background-color: #1DB954;
          border: none;
          border-radius: 30px;
          padding: 20px 20px;
          color: black;
          min-width: 300px;

        }

        QPushButton:hover {
            font-weight: bold;
        }
        """)  # Style the button

        self.mainLayout.addWidget(self.labelTitle,  alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelInformations)
        self.mainLayout.addWidget(self.btnZipUpload)
        
        self.setLayout(self.mainLayout)