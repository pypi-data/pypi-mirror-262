"""FontField provides a field for selecting a font."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QFont
from vistutils.fields import CoreDescriptor, unParseArgs, Wait
from vistutils.text import stringList, monoSpace

from vistside.core import parseFont, resolveFontFamily


class Font(QFont):
  """Wrapper for QFont enabling use with descriptor."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the font."""
    QFont.__init__(self)
    self.apply((args, kwargs))

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Font:
    """Creates a default instance"""
    return cls().apply((args, kwargs))

  def apply(self, value: Any) -> Font:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    famKeys = stringList("""family, fontFamily, fontFam""")
    sizeKeys = stringList("""size, pointSize, fontSize, fontPointSize""")
    weightKeys = stringList("""weight, fontWeight, fontWeight""")
    names = stringList('family, size, weight')
    types = [str, int, QFont.Weight]
    Keys = [famKeys, sizeKeys, weightKeys]
    parsedKwargs = {key: None for key in names}
    for (name, keys, type_) in zip(names, Keys, types):
      for key in keys:
        if key in kwargs and parsedKwargs[key] is None:
          val = kwargs.get(key)
          if isinstance(val, type_):
            parsedKwargs[name] = val
            break
          e = """Tried setting font to a string, but the string: '%s' was 
          not recognized as a valid font family name!"""
          raise ValueError(monoSpace(e % val))
    fontFamily = parsedKwargs.get('family', self.family())
    fontSize = parsedKwargs.get('size', self.pointSize())
    fontWeight = parsedKwargs.get('weight', self.weight())
    self.setFamily(fontFamily)
    self.setPointSize(fontSize)
    self.setWeight(fontWeight)
    return self


class FontField(Wait):
  """The FontField class provides a field for selecting a font."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the font field."""
    Wait.__init__(self, Font, *args, **kwargs)
