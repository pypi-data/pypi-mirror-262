"""PenField provides a descriptor class for instances of QPen."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QPen
from vistutils.fields import unParseArgs, Wait

from vistside.core import parsePen


class PenWrap(QPen):
  """Subclass of QPen with a custom constructor enabling interaction
  with descriptors."""

  @classmethod
  def getDefault(cls, *args, **kwargs) -> PenWrap:
    """Returns the default value for the field."""
    return cls().apply((args, kwargs))

  def apply(self, value: Any) -> PenWrap:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    testPen = parsePen(*args, **kwargs)
    self.setStyle(testPen.style())
    self.setColor(testPen.color())
    self.setWidth(testPen.width())
    self.setCapStyle(testPen.capStyle())
    self.setJoinStyle(testPen.joinStyle())

    return self


class PenField(Wait):
  """The PenField class provides a descriptor for instances of QPen."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the PenField."""
    Wait.__init__(self, PenWrap, *args, **kwargs)
