"""ArrayField class for storing and manipulating arrays of data."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import Any

import numpy as np
from vistutils.fields import Wait, MutableDescriptor, IntField
from vistutils.text import stringList, monoSpace
from vistutils.waitaminute import typeMsg


class ArrayField(MutableDescriptor):
  """ArrayField class for storing and manipulating arrays of data."""

  __fallback_num_data__ = 128

  numData = IntField()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the field."""
    numKeys = stringList("""numData, numDataPoints, numDataPoints, n, num""")
    for key in numKeys:
      if key in kwargs:
        val = kwargs.get(key)
        if isinstance(val, int):
          self.numData = val
          break
        e = typeMsg(key, val, int)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, int):
          self.numData = arg
          break
      else:
        self.numData = self.__fallback_num_data__
    MutableDescriptor.__init__(self, np.ndarray, *args, **kwargs)
    self._setFieldType(np.ndarray)

  def _instantiate(self, instance: object) -> None:
    """Instantiates the field."""
    n = getattr(instance, 'arrayLength', self.__fallback_num_data__)
    pvtName = self._getPrivateName()
    array = np.full((n,), np.nan, dtype=complex)
    setattr(instance, self._getPrivateName(), array)

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Returns the value of the field."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._instantiate(instance)
      return self.__get__(instance, owner, _recursion=True)
    return getattr(instance, self._getPrivateName())

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the value of the field."""
    e = """This subclass of MutableDescriptor does not implement a setter 
    operation. """
    raise TypeError(monoSpace(e))

  def __delete__(self, instance: object, ) -> None:
    """Deletes the value of the field."""
    e = """Instances of MutableDescriptor cannot be deleted."""
    raise TypeError(monoSpace(e))
