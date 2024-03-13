"""BrushField provides a descriptor class for instances of QBrush."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QBrush
from vistutils.fields import CoreDescriptor, Wait, unParseArgs

from vistside.core import parseBrush


class Brush(QBrush):
  """Subclass of QBrush with a custom constructor enabling interaction
  with descriptors."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Brush."""
    QBrush.__init__(self, *args, **kwargs)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Brush:
    """Returns the default value for the field."""
    defVal = cls()
    defVal.apply((args, kwargs))
    return defVal

  def apply(self, value: Any) -> Brush:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    testBrush = parseBrush(*args, **kwargs)
    self.setStyle(testBrush.style())
    self.setColor(testBrush.color())

    return self


class BrushField(Wait):
  """The BrushField class provides a descriptor for instances of QBrush."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the BrushField."""
    Wait.__init__(self, Brush, *args, **kwargs)
