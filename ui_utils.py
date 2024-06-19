import os
from PyQt6.QtGui import QFont, QFontDatabase

def getFont(taille):
    font_id = QFontDatabase.addApplicationFont("Assets/fonts/HelveticaNeueMedium.otf")
    if font_id == -1:
        print("Failed to load the custom font")
        return

    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    return QFont(custom_font, taille)


def getScrollBarStyle():
  return """
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 10px;
    margin: 0px 0px 0px 0px;
}"""