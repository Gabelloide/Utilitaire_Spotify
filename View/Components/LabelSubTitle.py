from PyQt6.QtWidgets import QLabel
import ui_utils

class LabelSubTitle(QLabel):
    def __init__(self,text:str,parent=None):
        super().__init__(parent)

        font = ui_utils.getFont(14)
        self.setFont(font)
        self.setText(text)
        self.setStyleSheet("""
            color: white;
        """)