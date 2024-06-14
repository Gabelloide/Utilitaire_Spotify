# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from matplotlib import font_manager
# import ui_utils



# class PieGenre(FigureCanvas):
#     def __init__(self, parent=None, width=4, height=3, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
        
#         super(PieGenre, self).__init__(fig)

#     def plot_pie_chart(self, labels, sizes, colors, title="Genres écoutés récemment"):
#         self.figure.set_facecolor('#211f1f')
        
#         self.axes.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
#         self.axes.axis('equal')  # Assure que le camembert est un cercle

#         for text in self.axes.texts:
#             text.set_color('white') 
#             text.set_fontproperties(ui_utils.getFontmapltolib())
#             text.set_fontsize(10)
#         self.draw()

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
import ui_utils

class PieChartGenre(QChart):
  def __init__(self, datas, parent=None):
    super().__init__(parent)
    
    self.datas = datas
    
    self.series = QPieSeries()
    
    colors = ["#1DB954", "#00A573", "#008F84", "#007784", "#005F74", "#2F4858", "#00A0AE", "#008DC9", "#0077CD", "#0F5CB9"]
    for i, (genre, count) in enumerate(datas):
      slice = QPieSlice(f"{genre} ({count})", count)
      
      slice.setLabel(f"{genre} ({count / sum(dict(datas).values()) * 100:.1f}%)")
      slice.setLabelColor(QColor("white"))
      slice.setLabelFont(ui_utils.getFont(10))
      
      slice.setColor(QColor(colors[i % len(colors)]))
      
      slice.hovered.connect(lambda state, s=slice: self.sliceHovered(state, s))
      self.series.append(slice)
      
    self.series.setLabelsVisible(True)
    self.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
    self.series.setLabelsPosition(QPieSlice.LabelPosition.LabelOutside)

    self.legend().setVisible(False)
    self.setBackgroundVisible(False)
    self.setMinimumSize(600, 300)

    self.addSeries(self.series)
    
    
  def generateView(self):
    """Returns a QChartView object with the chart inside."""
    chartView = QChartView(self)
    chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
    chartView.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    chartView.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    return chartView


  def sliceHovered(self, state, slice):
    """Fonction appelée lorsque la souris entre ou sort d'une tranche."""
    slice.setExploded(state)