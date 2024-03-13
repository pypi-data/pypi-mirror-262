"""FontField provides a field for selecting a font."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QFont
from vistutils.fields import CoreDescriptor

from vistside.core import parseFont, resolveFontFamily


class FontField(CoreDescriptor):
  """The FontField class provides a field for selecting a font."""

  def _instantiate(self, instance: object) -> None:
    """Instantiates the field."""
    font = parseFont(*self._getArgs(), **self._getKwargs())
    setattr(instance, self._getPrivateName(), font)

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the field."""
    pvtName = self._getPrivateName()
    owner = self._getFieldOwner()
    if isinstance(value, str):
      try:
        family = resolveFontFamily(value)
        existingFont = self.__get__(instance, owner)
        existingFont.setFamily(family)
        return setattr(instance, pvtName, existingFont)
      except NameError as nameError:
        e = """Tried setting font to a string, but the string was not 
        recognized as a valid font family name!"""
        raise ValueError(e) from nameError
    if isinstance(value, QFont):
      return setattr(instance, pvtName, value)
    if isinstance(value, int):
      existingFont = self.__get__(instance, owner)
      existingFont.setPointSize(value)
      return setattr(instance, pvtName, existingFont)
    if isinstance(value, QFont.Weight):
      existingFont = self.__get__(instance, owner)
      existingFont.setWeight(value)
      return setattr(instance, pvtName, existingFont)
    e = """The FontField supports setting the font family to a string, 
    the font size to an integer, the font weight to an enum value of 
    QFont.Weight, or the entire font to an instance of QFont. The value 
    received was of type %s.""" % type(value)
    raise TypeError(value)
