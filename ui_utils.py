import os
from PyQt6.QtGui import QFont, QFontDatabase
from matplotlib import font_manager

def getFont(taille):
    font_id = QFontDatabase.addApplicationFont("Assets/fonts/HelveticaNeueMedium.otf")
    if font_id == -1:
        print("Failed to load the custom font")
        return

    font_families = QFontDatabase.applicationFontFamilies(font_id)
    custom_font = font_families[0]
    return QFont(custom_font, taille)

def getFontmapltolib():
    custom_font_path = "Assets/fonts/HelveticaNeueMedium.ttf"
    custom_font = font_manager.FontProperties(fname=custom_font_path)
    return custom_font