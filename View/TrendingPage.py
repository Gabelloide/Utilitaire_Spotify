from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton


class TrendingPage(QWidget):
  
  def __init__(self, parentView) -> None:
    super().__init__()

    self.parentView = parentView
    
    self.mainLayout = QVBoxLayout()
    
    self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Tendances")
    
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)

    # CSS
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()

    self.labelTitle.setStyleSheet(stylesheet)
    

    self.mainLayout.addLayout(self.containerTitle)
    self.setLayout(self.mainLayout)


    self.refreshButton = QPushButton("Refresh")
    self.refreshButton.setStyleSheet(stylesheet)
    self.mainLayout.addWidget(self.refreshButton)
    

    
    
    self.containerTrends = QVBoxLayout()
    self.mainLayout.addLayout(self.containerTrends)