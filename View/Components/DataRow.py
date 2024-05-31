from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from View.Components.FlowLayout import FlowLayout
from View.Components.LabelSubTitle import LabelSubTitle

class DataRow(QWidget):
  """This class is a custom widget that displays a row of data.
  The row consists of a QLabel for a title, and a QHBoxLayout for the data. (Horizontal layout).
  The label is positioned on top of the data, which is why the class inherits QVBoxLayout.
  """

  def __init__(self, title: str, parent=None):
    super().__init__(parent)

    self.mainLayout = QVBoxLayout()

    self.title_label = LabelSubTitle(title)
    self.mainLayout.addWidget(self.title_label)


    self.data_layout = FlowLayout()
    self.mainLayout.addLayout(self.data_layout)

    self.setLayout(self.mainLayout)

  def addComponent(self, component):
    """Adds a component to the data layout."""
    self.data_layout.addWidget(component)

  def setStyleSheet(self, styleSheet: str):
    self.title_label.setStyleSheet(styleSheet)