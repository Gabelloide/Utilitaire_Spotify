from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QSize
import ui_utils as iu_utils

class TrendingPage(QWidget):

  genreChangedSignal = pyqtSignal(str)
  def __init__(self, parentView) -> None:
    super().__init__()

    self.parentView = parentView
    
    self.mainLayout = QVBoxLayout()
    
    self.containerTitle = QHBoxLayout()
    self.labelTitle = QLabel("Tendances")
    
    spacerItem_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_left)
    self.containerTitle.addWidget(self.labelTitle)

    # CSS
    with open("Assets/style.css", "r") as file:
      stylesheet = file.read()
    #font
   
    self.labelTitle.setStyleSheet(stylesheet)
    
    self.mainLayout.addLayout(self.containerTitle)
    self.setLayout(self.mainLayout)


    self.refreshButton = QPushButton()
    self.refreshButton.setIcon(QIcon("Assets/icons/refresh.png"))
    self.refreshButton.setStyleSheet("""
          QPushButton {
              border: 0px;
              background-color: #211f1f;
              border-radius: 10px;
          }
          QPushButton:hover {
              background-color: #333333;
          }
        """)
    self.refreshButton.setFixedSize(64, 64)
    self.refreshButton.setIconSize(QSize(64, 64))
    self.containerTitle.addWidget(self.refreshButton)
    
    spacerItem_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    self.containerTitle.addItem(spacerItem_right)
    

    self.genreFilterLayout = QHBoxLayout()
    self.labelFilter = QLabel("Filtrer par genre:")
    self.labelFilter.setStyleSheet("""
      color: white;
    """)
    self.labelFilter.setFont(iu_utils.getFont(14))
    self.genreFilterLayout.addWidget(self.labelFilter)
    self.genreFilter = QComboBox(self)
    self.genreFilter.addItem("Tous les genres")

    self.genreFilter.currentTextChanged.connect(self.genreChanged)

    self.genreFilter.setFont(iu_utils.getFont(13))
    self.genreFilter.setStyleSheet("""
    QComboBox {
        color: white; 
        border-radius: 10px; 
        border: 2px solid #FFFFFF;
        padding: 10px 10px 10px 10px;
    }
    QComboBox::drop-down {
        border-radius: 10px;
        color: white;
        image: url("Assets/icons/comboBoxDropDown.png");
        width: 25px;
        height: 25px;
        subcontrol-position: center right;
        subcontrol-origin: padding;
        padding-right: 10px;
    }
    QComboBox QAbstractItemView {
        color: white;
    }
    """)
    self.genreFilter.setFixedHeight(50)
    self.genreFilter.setFixedWidth(180)
    self.genreFilterLayout.addWidget(self.genreFilter)

    self.mainLayout.addLayout(self.genreFilterLayout)

    self.containerTrends = QVBoxLayout()
    self.mainLayout.addLayout(self.containerTrends)

  def genreChanged(self, genre):
    self.genreChangedSignal.emit(genre)

  def clearComboBox(self):
    self.genreFilter.disconnect()
    self.genreFilter.clear()
  
  def connectComboBox(self):
    self.genreFilter.currentTextChanged.connect(self.genreChanged)

  