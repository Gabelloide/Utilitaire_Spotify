from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt


class ZipUploadPage(QWidget):
    def __init__(self, parentView):
        super().__init__()

        self.parentView = parentView
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)  # Set the margins

        with open("Assets/style.css", "r") as file:
            stylesheet = file.read()
            
        self.labelTitle = QLabel("Pourquoi Importer mes données ?")
        # Add the custom font to the QFontDatabase
        font_id = QFontDatabase.addApplicationFont("Assets/fonts/HelveticaNeueMedium.otf")
        if font_id == -1:
            print("Failed to load the custom font")
            return

        font_families = QFontDatabase.applicationFontFamilies(font_id)
        custom_font = font_families[0]
        font = QFont(custom_font, 14)

        textLabelInfo = """
        <p>Dans le cadre de notre engagement à fournir des statistiques précises et détaillées sur votre utilisation de Spotify, nous vous demandons de fournir un fichier zip de vos données Spotify. Ce fichier contient des informations détaillées sur votre historique d'écoute, vos playlists, vos recherches, et plus encore. Ces données nous permettent de générer des statistiques plus précises et personnalisées.</p>

        <p>Sans ces données, nous sommes limités à utiliser l'API Spotify, qui ne fournit que les 50 dernières chansons écoutées, les 20 meilleurs artistes et les 20 meilleures chansons sur une période de 4 semaines ou 6 mois. De plus, l'API ne fournit pas d'informations sur les recherches ou les playlists.</p>

        <p>En fournissant le fichier zip de vos données Spotify, vous nous permettez d'analyser votre historique d'écoute sur une période plus longue et de prendre en compte des informations supplémentaires, comme vos recherches et vos playlists. Cela nous permet de fournir des statistiques plus précises et détaillées.</p>

        <p>Nous tenons à vous assurer que vos données seront utilisées uniquement à des fins d'analyse. Nous respectons le Règlement Général sur la Protection des Données (RGPD) et nous nous engageons à protéger vos données. Vous avez le droit d'accéder à vos données, de les rectifier, de demander leur suppression, de limiter leur traitement et de vous opposer à leur traitement.</p>
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

        self.btnZipUpload = QPushButton("Upload un zip")
        self.btnZipUpload.setStyleSheet("""
            background-color: #1DB954;
            color: white;
            border-radius: 25px;
            padding: 15px;
            font-size: 14px;
            margin-top : 100px;
        """)  # Style the button

        self.mainLayout.addWidget(self.labelTitle,  alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelInformations)
        self.mainLayout.addWidget(self.btnZipUpload)
        
        self.setLayout(self.mainLayout)