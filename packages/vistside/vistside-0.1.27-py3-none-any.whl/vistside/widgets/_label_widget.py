"""LabelWidget provides a widget for displaying labels. This is intended
for short names or descriptions rather than longer text."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self
from warnings import warn

from PySide6.QtCore import QRect, QPoint, QMargins, QSize, Qt
from PySide6.QtGui import (QColor, QPaintEvent, QPainter, QFontMetrics,
                           QFont, \
                           QFontDatabase)
from vistutils.parse import maybe
from vistutils.text import monoSpace, stringList
from vistutils.fields import TextField, Wait, unParseArgs
from vistutils.waitaminute import typeMsg

from vistside.core import FontField, PenField, SolidLine, parseFont
from vistside.core import resolveFontFamily, NoWrap
from vistside.core import BrushField, SolidFill, White
from vistside.widgets import BaseWidget


class LabelWidget(BaseWidget):
  """LabelWidget provides a widget for displaying labels. This is intended
  for short names or descriptions rather than longer text."""

  fillBrush = BrushField(QColor(144, 255, 63, 255), SolidFill)
  borderPen = PenField(White, 2, SolidLine)
  textFillBrush = BrushField(QColor(255, 255, 0, 31), SolidFill)
  textBorderPen = PenField(White, 1, SolidLine)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the widget."""
    BaseWidget.__init__(self, *args, **kwargs)
    self.innerText = [*[i for i in args if isinstance(i, str)], 'Label'][0]
    self.textFont = QFont()
    self.textFont.setFamily('Montserrat')
    self.textFont.setPointSize(18)
    self.hAlign = 'center'
    self.vAlign = 'center'

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paints the widget."""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    b = self.borderPen.width() * 2
    borderMargins = QMargins(b, b, b, b)
    borderRect = viewRect.marginsRemoved(borderMargins)
    borderRect.moveCenter(viewRect.center())
    b = self.textBorderPen.width() * 4
    textBorderMargins = QMargins(b, b, b, b)
    textSpace = borderRect.marginsRemoved(textBorderMargins)
    painter.setRenderHint(QPainter.Antialiasing)
    # # # # # # # # # # # # # # # # #
    #  fill background
    painter.setPen(self.emptyPen)
    painter.setBrush(self.fillBrush)
    painter.drawRect(viewRect)
    # # # # # # # # # # # # # # # # #
    #  draw border
    painter.setPen(self.borderPen)
    painter.setBrush(self.emptyBrush)
    painter.drawRect(borderRect)
    # # # # # # # # # # # # # # # # #
    #  Calculate required size for text
    painter.setFont(self.textFont)
    painter.setPen(self.textPen)
    textRect = painter.boundingRect(textSpace, NoWrap, self.innerText)
    textSize = (textRect + QMargins(8, 1, 8, 1)).size()
    # # # # # # # # # # # # # # # # #
    #  Align text rectangle
    if self.hAlign.lower() == 'center':
      left = textSpace.center().x() - textSize.width() / 2
    elif self.hAlign.lower() == 'right':
      left = textSpace.right() - textSize.width()
    elif self.hAlign.lower() == 'left':
      left = textSpace.left()
    else:
      e = """Invalid horizontal alignment! Expected one of: 'center', 
      'right', 'left', but received: '%s'!""" % self.hAlign
      raise ValueError(monoSpace(e))
    if self.vAlign.lower() == 'center':
      top = textSpace.center().y() - textSize.height() / 2
    elif self.vAlign.lower() == 'bottom':
      top = textSpace.bottom() - textSize.height()
    elif self.vAlign.lower() == 'top':
      top = textSpace.top()
    else:
      e = """Invalid vertical alignment! Expected one of: 'center', 'bottom',
      'top', but received: '%s'!""" % self.vAlign
      raise ValueError(monoSpace(e))
    textTopLeft = QPoint(left, top)
    textRect = QRect(textTopLeft, textSize)
    textRect.moveCenter(viewRect.center())
    # # # # # # # # # # # # # # # # #
    #  Fill text background
    painter.setPen(self.emptyPen)
    painter.setBrush(self.textFillBrush)
    painter.drawRect(textRect)
    # # # # # # # # # # # # # # # # #
    #  Draw text border
    painter.setPen(self.textBorderPen)
    painter.setBrush(self.emptyBrush)
    painter.drawRect(textRect)
    # # # # # # # # # # # # # # # # #
    #  Print text
    painter.setPen(self.textPen)
    flags = NoWrap | Qt.AlignmentFlag.AlignHCenter
    painter.drawText(textRect, flags, self.innerText)
    painter.end()

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Self:
    """Creates default"""
    return cls(*args, **kwargs)


class LabelField(Wait):
  """LabelField is a field for a LabelWidget."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor"""
    Wait.__init__(self, LabelWidget, *args, **kwargs)
