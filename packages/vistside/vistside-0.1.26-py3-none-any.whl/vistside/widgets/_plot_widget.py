"""PlotWidget draws a static plot"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any

import numpy as np
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QVBoxLayout)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from vistutils.fields import unParseArgs

from vistside.core import generateWhiteNoise, interpolateWhiteNoise
from vistside.widgets import BaseWidget


class PlotWidget(BaseWidget):
  """Displays a static plot using QChart."""

  def __init__(self, x_data: list, y_data: list):
    """
    Initializes the widget.

    Args:
        x_data: List of x-values for the plot.
        y_data: List of y-values for the plot.
    """
    super().__init__()

    self.chart = QChart()
    self.series = QLineSeries()
    self.chart.addSeries(self.series)

    self.set_data(x_data, y_data)

    # Customize axes (optional)
    axisX = QValueAxis()
    axisY = QValueAxis()
    self.chart.setAxisX(axisX, self.series)
    self.chart.setAxisY(axisY, self.series)

    # Customize appearance (optional)
    self.chart.legend().hide()

    self.chart_view = QChartView(self.chart)
    self.chart_view.setRenderHint(QPainter.Antialiasing)

    layout = QVBoxLayout()
    layout.addWidget(self.chart_view)
    self.setLayout(layout)

  def set_data(self, x_data: list, y_data: list) -> None:
    """Sets the data to be plotted."""
    self.series.clear()  # Clear existing data
    for x, y in zip(x_data, y_data):
      self.series.append(x, y)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Self:
    """Creates a default instance"""
    t = np.linspace(0, 2 * np.pi, 100)
    x = np.sin(t)
    return cls(t.tolist(), x.tolist())

  def apply(self, val: Any) -> Self:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(val)
    x, y = None, None
    for arg in args:
      if isinstance(arg, np.ndarray):
        if x is None:
          x = arg
        elif y is None:
          y = arg
          break
    if x is None or y is None:
      return self
    self.series.appendNP(x, y)
    return self
