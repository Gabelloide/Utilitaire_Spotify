from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

class RightClickMenu(QMenu):
  
  
  def __init__(self, parent=None):
    super().__init__(parent)

    # Create actions
    action1 = QAction("Ajouter la musique aux tendances...", self)
    action2 = QAction("Voir les détails...", self)

    # Add actions to the menu
    self.addAction(action1)
    self.addAction(action2)
    
    # Get the parent widget, print its text (for example)
    print(parent.text_label.text())

    # Connect actions to slots
    action1.triggered.connect(lambda: print("Action 1 was triggered"))
    action2.triggered.connect(lambda: print("Action 2 was triggered"))

