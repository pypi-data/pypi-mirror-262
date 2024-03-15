"""DynamicPlotWidget provides a widget for plotting dynamic data."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time

import numpy as np
from PySide6.QtGui import QPainter
from vistutils.fields import IntField, Wait

from vistside.core import parseParent, ArrayField, DataRollField
from vistside.widgets import BaseWidget
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QTimer, QObject, QThread, Signal, Slot


class DynamicPlotWidget(BaseWidget):
  """DynamicPlotWidget provides a widget for plotting dynamic data."""

  dataRoll = DataRollField(128)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the widget."""
    BaseWidget.__init__(self, *args, **kwargs)
    self.current_index = 0

    # Chart setup
    self.chart = QChart()
    self.series = QLineSeries()
    self.chart.addSeries(self.series)

    axis_x = QValueAxis()  # For the time axis
    axis_y = QValueAxis()  # For the value axis
    self.chart.setAxisX(axis_x, self.series)
    self.chart.setAxisY(axis_y, self.series)

    # Customize axes, titles, etc. as needed (add your code here)

    self.chart_view = QChartView(self.chart)
    self.chart_view.setRenderHint(QPainter.Antialiasing)

    layout = QVBoxLayout()
    layout.addWidget(self.chart_view)
    self.setLayout(layout)

  @Slot(float)
  def callback(self, value) -> None:
    """Appends new data (value, timestamp)."""
    self.dataRoll.append(value)

  @Slot()
  def updateSlot(self) -> None:
    """Updates the plot visualization."""
    self.series.clear()
    self.series.appendNp(self.dataRoll.real, self.dataRoll.imag)
    # self.chart.update()
    self.update()
