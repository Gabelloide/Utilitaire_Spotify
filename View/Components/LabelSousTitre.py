from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt
import ui_utils

class LabelSousTitre(QLabel):
    def __init__(self,text:str,parent=None):
        super().__init__(parent)

        font = ui_utils.getFont(14)
        self.setFont(font)
        self.setText(text)
        self.setStyleSheet("""
            color: white;                    
        """)

