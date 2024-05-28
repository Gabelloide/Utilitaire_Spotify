from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy

from Model.User import User
from View.Components.DataRow import DataRow

class StatisticsPage(QWidget):
  """This class is responsible for displaying the user's statistics page.
  This is a big page that contains all the statistics of the user :
  - Number of tracks listened
  - Number of artists listened
  - Number of albums listened
  - Hours when music is listened
  - ...
  """
  
  def __init__(self, parentView):
    super().__init__()

    self.parentView = parentView
    
    self.mainLayout = QVBoxLayout()
    
    # Open style.css and set the stylesheet
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()

    self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Statistiques d'écoute")
    self.labelTitle.setStyleSheet(stylesheet)
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)
    
    self.mainLayout.addLayout(self.containerTitle)
    self.setLayout(self.mainLayout)
    

