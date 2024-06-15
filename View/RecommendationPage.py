from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QStackedWidget

from View.Components.ImageLabelSlider import ImageLabelSlider
from Model import Statistics

class RecommendationPage(QWidget):
  
  def __init__(self, parentView) -> None:
    super().__init__()
    
    self.parentView = parentView
    
    self.mainLayout = QVBoxLayout()
    
    # Open style.css and set the stylesheet
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()

    #Title 
    self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Vos recommandations")
    self.labelTitle.setStyleSheet(stylesheet)
    
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)
    
    #Recommendation navigation
    self.recommendationNavigation = QHBoxLayout()
    
    self.albumButton = QPushButton("Albums")
    self.artistButton = QPushButton("Artistes")
    self.trackButton = QPushButton("Titres")
    
    self.buttonStyleSheet = """
    QPushButton {
      border: 0px;
      background-color: #211f1f;
      font-size: 25px;
      padding: 10px;
      margin-right: 30px;
      color: white;
      border-radius: 10px;
    }
    QPushButton:hover {
      background-color: #333333;
    }
    """
    
    self.focusedButtonStyleSheet = """
          QPushButton {
            border: 0px;
            text-decoration: underline;
            text-decoration-color: green;
          }
          
        """
    self.recommendationNavigation.addItem(spacerItem_left)
    self.recommendationNavigation.addWidget(self.trackButton)
    self.recommendationNavigation.addWidget(self.albumButton)
    self.recommendationNavigation.addWidget(self.artistButton)
    self.recommendationNavigation.addItem(spacerItem_right)

    self.buttonsNavigation = [self.trackButton, self.albumButton, self.artistButton]
    self.mainLayout.addLayout(self.containerTitle)
    self.mainLayout.addLayout(self.recommendationNavigation)
    
    self.setStyleSheet(self.buttonStyleSheet)
    self.setLayout(self.mainLayout)
    
  def addRecommendationRow(self, title, row):
    self.recommendationsLayout = QVBoxLayout()
    self.recommendationsLabel = QLabel(title)
    self.recommendationsLayout.addWidget(self.recommendationsLabel)
    self.recommendationsLayout.addWidget(row)
    self.mainLayout.addLayout(self.recommendationsLayout)