from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon


class ImageLabelSlider(QWidget):
    def __init__(self, ImageLabelList, visible_count=8):
        super().__init__()
        
        self.visible_count = visible_count
        self.widget_index = 0
        self.widgets = ImageLabelList

        self.layout = QHBoxLayout(self)

        self.widget_container = QWidget()
        self.widget_layout = QHBoxLayout(self.widget_container)

        self.update_widgets()
        
        # Create the previous button with a left arrow icon
        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon('Assets/icons/left.png'))
        self.prev_button.clicked.connect(self.show_prev_widgets)
        self.layout.addWidget(self.prev_button)
        
        self.layout.addWidget(self.widget_container)
        
        # Create the next button with a right arrow icon
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon('Assets/icons/right.png'))
        self.next_button.clicked.connect(self.show_next_widgets)
        self.layout.addWidget(self.next_button)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        
    def show_prev_widgets(self):
        self.widget_index = (self.widget_index - 1) % len(self.widgets)
        self.update_widgets()
    
    def show_next_widgets(self):
        self.widget_index = (self.widget_index + 1) % len(self.widgets)
        self.update_widgets()
        
    def update_widgets(self):
        # Clear the layout
        for i in reversed(range(self.widget_layout.count())): 
            widget_to_remove = self.widget_layout.itemAt(i).widget()
            self.widget_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Add visible widgets
        for i in range(self.visible_count):
            widget_index = (self.widget_index + i) % len(self.widgets)
            self.widget_layout.addWidget(self.widgets[widget_index])

    def show_prev_widgets(self):
        self.widget_index = (self.widget_index - 1) % len(self.widgets)
        self.update_widgets()

    def show_next_widgets(self):
        self.widget_index = (self.widget_index + 1) % len(self.widgets)
        self.update_widgets()