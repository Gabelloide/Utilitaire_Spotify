from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from View.Components.LabelSubTitle import LabelSubTitle

class FigureLabel(QWidget):
  """This class is a QLabel that will be used to display the statistics of the user.
  It is a QLabel that will contain the title of the statistic and its value.
  The value is a big number, associated with its meaning in a smaller font.
  """
  
  def __init__(self, number:str, text:str, parent=None):
    super().__init__(parent)
    
    self.mainLayout = QVBoxLayout()
    
    self.numberLabel = LabelSubTitle(number)
    self.mainLayout.addWidget(self.numberLabel)
    
    self.description = QLabel(text)
    self.description.setStyleSheet("color: grey;")
    self.mainLayout.addWidget(self.description)
    
    self.setLayout(self.mainLayout)