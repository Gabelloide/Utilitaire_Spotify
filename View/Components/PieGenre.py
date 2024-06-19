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
    self.setMinimumSize(600, 350)

    self.addSeries(self.series)
    
    
  def generateView(self):
    """Returns a QChartView object with the chart inside."""
    chartView = QChartView(self)
    chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
    chartView.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    chartView.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    chartView.setStyleSheet("""
      padding-top:10px;
    """)
    return chartView


  def sliceHovered(self, state, slice):
    """Fonction appelée lorsque la souris entre ou sort d'une tranche."""
    slice.setExploded(state)