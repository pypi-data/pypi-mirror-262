"""BaseLayout wraps the basic layout."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QLayout
from vistutils.fields import Wait
from vistutils.text import stringList


class BaseGrid(QGridLayout):
  """The BaseLayout class is a layout of widgets."""

  def __init__(self, *args, **kwargs) -> None:
    """Create a new BaseLayout."""
    QGridLayout.__init__(self, *args, **kwargs)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> BaseGrid:
    """Returns the default value for the field."""
    return cls()


class BaseHBox(QHBoxLayout):
  """The BaseLayout class is a layout of widgets."""

  def __init__(self, *args, **kwargs) -> None:
    """Create a new BaseLayout."""
    QHBoxLayout.__init__(self, *args, **kwargs)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> BaseHBox:
    """Returns the default value for the field."""
    return cls()


class BaseVBox(QVBoxLayout):
  """The BaseLayout class is a layout of widgets."""

  def __init__(self, *args, **kwargs) -> None:
    """Create a new BaseLayout."""
    QVBoxLayout.__init__(self, *args, **kwargs)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> BaseVBox:
    """Returns the default value for the field."""
    return cls()


class BaseLayoutField(Wait):
  """BaseLayoutField is a field for a BaseLayout."""

  def __init__(self, *args, **kwargs) -> None:
    layoutType = BaseGrid
    layoutKeys = stringList("""layout, layoutType, layoutMode""")
    gridKeys = stringList("""grid, gridLayout, gridMode""")
    hBoxKeys = stringList("""horizontal, hBox, hBoxLayout, hBoxMode""")
    vBoxKeys = stringList("""vertical, vBox, vBoxLayout, vBoxMode""")
    for key in layoutKeys:
      if key in kwargs:
        val = kwargs.get(key)
        if isinstance(val, str):
          if val.lower() in gridKeys:
            layoutType = BaseGrid
          elif val.lower() in hBoxKeys:
            layoutType = BaseHBox
          elif val.lower() in vBoxKeys:
            layoutType = BaseVBox
          else:
            continue
          break
        elif isinstance(val, type):
          if issubclass(val, QLayout):
            layoutType = val
            break
    else:
      for arg in args:
        if isinstance(arg, type):
          if issubclass(arg, QLayout):
            layoutType = arg
            break
      else:
        layoutType = BaseGrid
    Wait.__init__(self, layoutType, *args, **kwargs)
