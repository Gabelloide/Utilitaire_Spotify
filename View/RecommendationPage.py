from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QStackedWidget

from View.Components.ImageLabelSlider import ImageLabelSlider
from Model import Statistics
from View.Components.LabelSubTitle import LabelSubTitle

class RecommendationPage(QWidget):
  
  def __init__(self, parentView) -> None:
    super().__init__()
    
    self.parentView = parentView
    
    self.mainLayout = QVBoxLayout()
    
    # Open style.css and set the stylesheet
    with open("Assets/style.css", "r") as file:
      self.stylesheet = file.read()

    #Title 
    self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Vos recommandations")
    self.labelTitle.setStyleSheet(self.stylesheet)
    
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)
  
    self.mainLayout.addLayout(self.containerTitle)
    self.setLayout(self.mainLayout)
    
  def addRecommendationRow(self, title, row):
    self.recommendationsLayout = QVBoxLayout()
    self.recommendationsLabel = LabelSubTitle(title)
    self.recommendationsLayout.addWidget(self.recommendationsLabel)
    self.recommendationsLayout.addWidget(row)
    self.mainLayout.addLayout(self.recommendationsLayout)