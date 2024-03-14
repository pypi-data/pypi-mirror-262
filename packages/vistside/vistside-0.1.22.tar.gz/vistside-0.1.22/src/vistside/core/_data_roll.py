"""The DataEcho class provides a way to echo data from one object to
another."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any

import numpy as np
from icecream import ic
from vistutils.fields import unParseArgs, Wait, IntField
from vistutils.waitaminute import typeMsg

from vistside.core import ArrayField, RightNowField


class _Im:
  """Retrieves the imaginary part of the series."""

  def __get__(self, instance: DataRoll, owner: type) -> np.ndarray:
    """Returns the imaginary part of the last value."""
    return instance.toArray().imag


class _Re:
  """Retrieves the real part of the series."""

  def __get__(self, instance: DataRoll, owner: type) -> np.ndarray:
    """Returns the real part of the last value."""
    return instance.toArray().real


class DataRoll:
  """The DataEcho class provides a way to echo data from one object to
  another."""

  __callback_functions__ = None
  __zero_index__ = None

  imag = _Im()
  real = _Re()
  rightNow = RightNowField()
  array = ArrayField(16)
  arrayLength = IntField(64)

  def __init__(self, *args, **kwargs) -> None:
    self.__callback_functions__ = []
    self.__zero_index__ = 0

  def appendCallback(self, callMeMaybe: Callable) -> Callable:
    """Notify the DataEcho object when a value is appended."""
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    self.__callback_functions__.append(callMeMaybe)
    return callMeMaybe

  def CALL(self, callMeMaybe: Callable) -> Callable:
    """Call the callback functions."""
    return self.appendCallback(callMeMaybe)

  def notifyCallbacks(self, val: complex) -> None:
    """Notify the callback functions."""
    for func in self.__callback_functions__:
      func()

  def append(self, value: float = None) -> None:
    """Append a value to the DataEcho object."""
    if not value == value:
      return
    if isinstance(value, int):
      value = float(value) + 0j
    if isinstance(value, complex):
      value = value.imag
    self.array[self.__zero_index__] = self.rightNow + value * 1j
    entry = None
    try:
      entry = self.array[self.__zero_index__]
      self.notifyCallbacks(entry.item())
    except ValueError as valueError:
      ic(entry)
      ic(self.__zero_index__)
      raise valueError
    self.__zero_index__ = (self.__zero_index__ + 1) % len(self.array)

  def __str__(self, ) -> str:
    line = []
    lines = []
    for val in self.toArray():
      this = '(%.3f + %.3fI)' % (val.real, val.imag)
      if sum([len(x) for x in line]) + len(this) + 2 * len(line) + 1 > 77:
        lines.append(', '.join(line))
        line = []
      line.append(this)
    if line:
      lines.append(', '.join(line))
    return '\n'.join(lines)

  def __len__(self, ) -> int:
    """Returns the length of the array  ."""
    return self.array.shape[0]

  def toArray(self, ) -> np.ndarray:
    """Returns the array."""
    arr = np.roll(self.array, -self.__zero_index__)
    return arr[~np.isnan(arr)]

  @classmethod
  def getDefault(cls, *args, **kwargs) -> DataRoll:
    """Returns the default value for the field."""
    dataRoll = DataRoll()
    return dataRoll.apply((args, kwargs))

  def apply(self, value: Any) -> DataRoll:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    for arg in args:
      if isinstance(arg, int):
        self.arrayLength = arg
    return self


class DataRollField(Wait):
  """Wraps the DataRoll in a mutable descriptor class"""

  def __init__(self, *args, **kwargs) -> None:
    Wait.__init__(self, DataRoll, *args, **kwargs)
