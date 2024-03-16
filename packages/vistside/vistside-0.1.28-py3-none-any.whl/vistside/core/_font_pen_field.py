"""FontPenField provides a static descriptor class for QPen instances for
rendering text. Static means that they are not sensitive to which instance
calls for them, but only whether the field was accessed through and
instance or through the owner. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtGui import QPen
from vistutils.fields import StaticField
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from vistside.core import SolidLine, parsePen


class FontPenField(StaticField):
  """The FontPenField class provides a descriptor for instances of QPen for
  rendering text. """

  __font_pen__ = None

  @staticmethod
  def _getFallbackPen() -> QPen:
    """Returns a fallback pen."""
    pen = QPen()
    pen.setColor("black")
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    return pen

  @staticmethod
  def _parseKwargs(**kwargs) -> Optional[QPen]:
    """Parses the keyword arguments."""
    penKeys = stringList("""pen, fontPen, font_pen, fontLine, line""")
    for key in penKeys:
      if key in kwargs:
        val = kwargs.get(key)
        if isinstance(val, QPen):
          return val
        e = typeMsg(key, val, QPen)
        raise TypeError(e)

  @staticmethod
  def _parseArgs(*args, ) -> Optional[QPen]:
    """Parses the positional arguments."""
    for arg in args:
      if isinstance(arg, QPen):
        return arg

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor."""
    penKwarg = self._parseKwargs(**kwargs)
    penArg = self._parseArgs(*args)
    penDefault = self._getFallbackPen()
    fontPen = maybe(penKwarg, penArg, penDefault)
    if isinstance(fontPen, QPen):
      self.__font_pen__ = fontPen
      StaticField.__init__(self, fontPen, )
