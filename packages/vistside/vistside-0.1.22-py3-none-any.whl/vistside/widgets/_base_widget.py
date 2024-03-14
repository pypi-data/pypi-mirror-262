"""BaseWidget provides the lowest level of abstraction for a QWidget. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from vistutils.fields import unParseArgs

from vistside.core import TextPen, EmptyPen, EmptyBrush, parseParent


class BaseWidget(QWidget):
  """BaseWidget provides the lowest level of abstraction for a QWidget. """

  hover = Signal()
  leave = Signal()
  leftClick = Signal()
  rightClick = Signal()
  middleClick = Signal()
  forwardClick = Signal()
  backwardClick = Signal()
  doubleClick = Signal()
  leftPressHold = Signal()
  rightPressHold = Signal()

  textPen = TextPen()
  emptyPen = EmptyPen()
  emptyBrush = EmptyBrush()

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QWidget.__init__(self, parent)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Self:
    """Creates a default instance"""
    return BaseWidget()

  def apply(self, value: Any) -> Self:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    return self
