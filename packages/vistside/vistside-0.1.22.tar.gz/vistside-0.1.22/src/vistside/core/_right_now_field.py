"""The RightNowField provides a StaticField return the epoch the moment
the __getter__ is invoked. If accessed on the owner class, the descriptor
returns itself, if accessed on any instance, it returns the time. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import Any

from vistutils.fields import StaticField
from vistutils.waitaminute import typeMsg


class RightNowField(StaticField):
  """The RightNowField provides a StaticField return the epoch the moment
    the __getter__ is invoked. If accessed on the owner class, the descriptor
    returns itself, if accessed on any instance, it returns the time. """

  def __init__(self, *args, **kwargs) -> None:
    StaticField.__init__(self, None)

  def __get__(self, instance: object, owner: type) -> Any:
    """Getter-function implementation."""
    if instance is None:
      return self
    if getattr(owner, '__zero_time__', None) is None:
      e = """The owner class does not have a __zero_time__ attribute!"""
      raise AttributeError(e)
    zeroTime = getattr(owner, '__zero_time__')
    if isinstance(zeroTime, float):
      return time.time() - zeroTime
    e = typeMsg('zeroTime', zeroTime, float)
    raise TypeError(e)

  def __set_name__(self, owner: type, name: str) -> None:
    """Invoked automatically when the owner class is created."""
    StaticField.__set_name__(self, owner, name)
    setattr(owner, '__zero_time__', time.time())
