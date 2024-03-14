"""LayoutWindow subclasses the BaseWindow and provides the visual layouts."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistside.widgets import LabelField
from vistside.windows import BaseWindow


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses the BaseWindow and provides the visual
  layouts."""

  welcomeBanner = LabelField('Dynamic Plot Widget!', 36)

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)

  def show(self) -> None:
    """Shows the window. The base window class already provides the base
    widget and base layout. This method should add widgets to the base
    layout and then call the parent show method."""
    self.baseLayout.addWidget(self.welcomeBanner)
    BaseWindow.show(self)

  def connectActions(self, ) -> None:
    """Connects the actions to the window."""
    BaseWindow.connectActions(self)
