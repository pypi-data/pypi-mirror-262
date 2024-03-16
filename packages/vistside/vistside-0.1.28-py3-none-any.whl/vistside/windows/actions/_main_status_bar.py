"""MainStatusBar provides the status bar for the main application window. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QStatusBar, QMainWindow, QLabel
from icecream import ic
from vistutils.fields import unParseArgs

from vistside.core import parseParent
from vistside.widgets import ClockField


class MainStatusBar(QStatusBar):
  """MainStatusBar provides the status bar for the main application
  window. """

  clock = ClockField()

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QStatusBar.__init__(self, parent)
    self.setStyleSheet("""
    QStatusBar {
        margin: 0px;
        padding: 0px;
        background: rgba(255, 255, 255, 0.5);
        color: black;
        font-family: "Courier", sans-serif; 
        font-size: 14px;

    }""")

  def show(self) -> None:
    """Hook to print to stdout"""
    ic(self)
    QStatusBar.show(self, )

  @classmethod
  def getDefault(cls, *args, **kwargs) -> MainStatusBar:
    """Returns the default MainStatusBar"""
    mainWindow = parseParent(*args)
    statusBar = cls(mainWindow)
    statusBar.clock.initUI()
    statusBar.clock.connectActions()
    statusBar.addPermanentWidget(statusBar.clock)
    statusBar.apply((args, kwargs))
    return statusBar

  def apply(self, value: Any) -> MainStatusBar:
    """Applies the value to the field."""
    args, kwargs = unParseArgs(value)
    for arg in args:
      if isinstance(arg, str):
        self.showMessage(arg)
    return self
