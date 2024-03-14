"""TimerField provides QTimer typed descriptor class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QTimer
from icecream import ic
from vistutils.fields import Wait, unParseArgs
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from vistside.core import parseTimer, TimerType, Precise

ic.configureOutput(includeContext=True)


class Timer(QTimer):
  """Timer wraps the QTimer class allowing it to interact with the
  descriptor classes."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor"""
    QTimer.__init__(self, *args, **kwargs)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> Any:
    """Returns the default value for the field."""
    defVal = cls()
    defVal.apply((args, kwargs))
    return defVal

  def apply(self, value: Any) -> Timer:
    """Applies the arguments contained in value to the timer."""
    args, kwargs = unParseArgs(value)
    epoch = None
    epochKeys = stringList("""epoch, time, interval, length, duration, d""")
    timerType = None
    timerKeys = stringList("""timer, type, precision, accuracy, acc""")
    singleShot = None
    singleShotKeys = stringList("""single, shot, one, once, only""")
    names = stringList('epoch, timerType, singleShot')
    types = [int, TimerType, bool]
    Keys = [epochKeys, timerKeys, singleShotKeys]
    parsedKwargs = {key: None for key in names}
    for (name, keys, type_) in zip(names, Keys, types):
      for key in keys:
        if key in kwargs and parsedKwargs[key] is None:
          val = kwargs.get(key)
          if isinstance(val, type_):
            parsedKwargs[name] = val
            break
          e = typeMsg(key, val, type_)
          raise TypeError(e)
    parsedArgs = {key: None for key in names}
    for (name, type_) in zip(names, types):
      for arg in args:
        if isinstance(arg, type_) and parsedArgs[name] is None:
          parsedArgs[name] = arg
          break
    parsedDefaults = dict(epoch=1000, timerType=Precise, singleShot=False)
    values = {}
    P = [parsedKwargs, parsedArgs, parsedDefaults]
    epoch = maybe(*[p.get('epoch') for p in P])
    if not isinstance(epoch, int):
      e = typeMsg('epoch', epoch, int)
      raise TypeError(e)
    timerType = maybe(*[p.get('timerType') for p in P])
    if not isinstance(timerType, TimerType):
      e = typeMsg('timerType', timerType, TimerType)
      raise TypeError(e)
    singleShot = maybe(*[p.get('singleShot') for p in P])
    if not isinstance(singleShot, bool):
      e = typeMsg('singleShot', singleShot, bool)
      raise TypeError(e)
    self.setInterval(epoch)
    self.setTimerType(timerType)
    self.setSingleShot(singleShot)
    return self


class TimerField(Wait):
  """TimerField provides QTimer typed descriptor class"""

  def __init__(self, *args, **kwargs) -> None:
    Wait.__init__(self, Timer, *args, **kwargs)
