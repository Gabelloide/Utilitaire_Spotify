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

            QScrollBar::handle:vertical {
                background: #363333;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #000000
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }"""