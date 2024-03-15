"""FillWidget provides a widget with a fill color"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QPainter

from vistside.core import BrushField
from vistside.widgets import BaseWidget


class FillWidget(BaseWidget):
  """FillWidget provides a widget with a fill color"""

  fillBrush = BrushField()

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self.fillBrush = 144, 0, 255, 255

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paints the widget."""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(painter.Antialiasing)
    painter.setPen(self.emptyPen)
    painter.setBrush(self.fillBrush)
    painter.drawRect(painter.viewport())
    painter.end()
