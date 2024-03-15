"""LCDField provides a descriptor for QLCDNumber objects."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self

from PySide6.QtWidgets import QLCDNumber
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from vistutils.fields import Wait, unParseArgs


class LCDNumber(QLCDNumber):
  """LCDNumber provides a QLCDNumber object."""

  def __init__(self, *args, **kwargs) -> None:
    QLCDNumber.__init__(self, *args, **kwargs)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Any:
    """Returns the default value for the field."""
    defVal = cls()
    defVal.apply((args, kwargs))
    return defVal

  def apply(self, value: Any) -> Self:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    numDigs = None
    digitsKey = stringList("""digits, numDigits, num, number, n""")
    for key in digitsKey:
      if key in kwargs and numDigs is None:
        val = kwargs.get(key)
        if isinstance(key, int):
          numDigs = val
          break
        e = typeMsg(key, val, int)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, int) and numDigs is None:
          numDigs = arg
          break
    if isinstance(numDigs, int):
      self.setDigitCount(numDigs)
      return self


class LCDField(Wait):
  """LCDField provides a descriptor for QLCDNumber objects."""

  def __init__(self, *args, **kwargs) -> None:
    Wait.__init__(self, LCDNumber, *args, **kwargs)
