from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QStackedWidget, QScrollArea
from PyQt6.QtCore import Qt
from View.Components.ImageLabelSlider import ImageLabelSlider
from Model import Statistics
from View.Components.LabelSubTitle import LabelSubTitle
import ui_utils

class RecommendationPage(QScrollArea):
  
  def __init__(self, parentView) -> None:
    super().__init__()
    
    self.parentView = parentView
    self.setStyleSheet(ui_utils.getScrollBarStyle())
    
    # ScrollPane settings
    self.setWidgetResizable(True)
    
    # Adapt the base size of the scroll area to the window size
    navBarWidth = self.parentView.getNavbarWidth()
    totalWindowWidth = self.parentView.width()
    totalWindowHeight = self.parentView.height()
    
    centralWidgetWidth = totalWindowWidth - int(navBarWidth*1.2) # 1.2 is a magic number to make this widget a little bit smaller than the window
    self.setFixedSize(centralWidgetWidth, totalWindowHeight)
    
    self.centralWidget = QWidget()

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
    self.centralWidget.setLayout(self.mainLayout)
    self.setWidget(self.centralWidget)
    
  def addRecommendationRow(self, title, row):
    self.recommendationsLayout = QVBoxLayout()
    self.recommendationsLabel = LabelSubTitle(title)
    self.recommendationsLayout.addWidget(self.recommendationsLabel)
    row.setMinimumHeight(200)
    self.recommendationsLayout.addWidget(row)
    self.mainLayout.addLayout(self.recommendationsLayout)