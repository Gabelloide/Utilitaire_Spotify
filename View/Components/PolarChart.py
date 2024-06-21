import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import QSize

class PolarChart(FigureCanvas):
    def __init__(self, values_dict, parent=None):
        categories = list(values_dict.keys())
        values = list(values_dict.values())
        
        # Number of variables to split the circle
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        #Creating a closed loop
        values += values[:1]
        angles += angles[:1]
        
        # Figure creation
        screen_dpi = QApplication.primaryScreen().logicalDotsPerInch()
        width = 450 / screen_dpi
        height = 350 / screen_dpi
        fig, ax = plt.subplots(figsize=(width, height), subplot_kw=dict(polar=True))
        
        fig.set_facecolor("none")
        ax.set_facecolor("none")
        
        # Axis configuration
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        plt.xticks(angles[:-1], categories, color="white")
        
        ax.plot(angles, values, linewidth=1, linestyle='solid', color="#1ED760")
        ax.fill(angles, values, '#143921', alpha=1)
        ax.spines['polar'].set_color('grey')
        ax.grid(color='grey', linestyle='-', linewidth=0.5)
        
        plt.yticks([0.2, 0.4, 0.6, 0.8], ['0.2', '0.4', '0.6', '0.8'], color="grey", size=7)
        plt.ylim(0, 1)
        
        super().__init__(fig)
        self.setFixedSize(QSize(450, 350))