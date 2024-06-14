from turtle import title
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import font_manager
import ui_utils

class PieGenre(FigureCanvas):
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        
        super(PieGenre, self).__init__(fig)

    def plot_pie_chart(self, labels, sizes, colors, title="Genres écoutés récemment"):
        self.figure.set_facecolor('#211f1f')
        
        self.axes.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        self.axes.axis('equal')  # Assure que le camembert est un cercle

        for text in self.axes.texts:
            text.set_color('white') 
            text.set_fontproperties(ui_utils.getFontmapltolib())
            text.set_fontsize(10)
        self.draw()