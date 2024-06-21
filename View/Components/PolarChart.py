from PyQt6.QtGui import QPainter
from PyQt6.QtCharts import QChart, QChartView, QPolarChart, QCategoryAxis, QValueAxis, QScatterSeries
from PyQt6.QtCore import QPointF
import sys
from math import pi, cos, sin
from PyQt6.QtWidgets import QApplication, QMainWindow

class PolarChart(QPolarChart):
    def __init__(self, values_dict):
        super().__init__()

        self.values_dict = values_dict
        categories = list(values_dict.keys())
        values = list(values_dict.values())

        for i in range(len(categories)):
            # Convert the index to an angle in radians
            angle = i * (2 * pi / len(categories))
            radius = values[i]
            x = radius * cos(angle)
            y = radius * sin(angle)
            point = QPointF(x, y)
            print("Category:", categories[i], "Angle:", angle, "Radius:", radius, "X:", x, "Y:", y)

            # Create a QScatterSeries for each point
            scatter_series = QScatterSeries()
            scatter_series.append(point)
            scatter_series.setName(categories[i])  # Set the name of the series to the category name
            scatter_series.setMarkerSize(10)  # Increase the size of the points

            self.addSeries(scatter_series)

        # Axis
        angle_axis = QCategoryAxis()
        angle_axis.setTickCount(len(categories))
        angle_axis.setLabelsPosition(QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue)

        for i, category in enumerate(categories):
            angle_axis.append(category, i * (360 / len(categories)))

        self.addAxis(angle_axis, QPolarChart.PolarOrientation.PolarOrientationAngular)

        for series in self.series():
            series.attachAxis(angle_axis)

        value_axis = QValueAxis()
        value_axis.setTickCount(10)
        value_axis.setLabelFormat("%0.1f")
        value_axis.setRange(0, 1)

        self.addAxis(value_axis, QPolarChart.PolarOrientation.PolarOrientationRadial)

        for series in self.series():
            series.attachAxis(value_axis)

        self.setMinimumSize(600, 350)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    values_dict = {
        'Danceability': 0.8,
        'Energy': 0.7,
        'Instrumentalness': 0.2,
        'Speechiness': 0.1,
        'Valence': 0.6
    }
    polar_chart = PolarChart(values_dict)
    chart_view = polar_chart.generateView()

    main_window = QMainWindow()
    main_window.setCentralWidget(chart_view)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
