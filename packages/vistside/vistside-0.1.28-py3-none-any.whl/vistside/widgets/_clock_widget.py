"""ClockWidget provides a clock widget for the main application window"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime
from typing import Any

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLCDNumber
from vistutils.fields import IntField, Wait, unParseArgs

from vistside.core import TimerField, Precise
from vistside.widgets import BaseWidget, LCDField, BaseLayoutField


class ClockWidget(BaseWidget):
  """ClockWidget provides a clock widget for the main application window"""

  quartz = TimerField(100, Precise, singleShot=True)
  baseLayout = BaseLayoutField('horizontal')
  sevenSegment = LCDField(8, )
  prevTime = IntField(0, )

  @staticmethod
  def timeDict() -> dict[str, int]:
    """Returns a dictionary with the current time"""
    return {
      "hours"  : datetime.now().hour,
      "minutes": datetime.now().minute,
      "seconds": datetime.now().second,
    }

  @Slot()
  def showTime(self, ) -> None:
    """Shows the current time"""
    timeDict = self.timeDict()
    h, m, s = timeDict['hours'], timeDict['minutes'], timeDict['seconds']
    if self.prevTime - s:
      self.sevenSegment.display('%02d:%02d:%02d' % (h, m, s))
      self.prevTime = s

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the ClockWidget"""
    BaseWidget.__init__(self, *args, **kwargs)
    self.quartz.timeout.connect(self.showTime)
    self.quartz.start()
    self.showTime()

  def initUI(self, ) -> None:
    """Initializes the UI"""
    self.baseLayout.setContentsMargins(0, 0, 0, 0)
    self.sevenSegment.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
    self.setStyleSheet("""
    QLCDNumber {
      color: black;
      background: rgba(255, 255, 255, 0.2); 
      border: 1px solid black;
      border-radius: 4px;
      padding: 0px;
      margin: 0px;
    }
    """)
    self.baseLayout.addWidget(self.sevenSegment)
    self.setLayout(self.baseLayout)

  def connectActions(self, ) -> None:
    """Connects the actions"""
    self.quartz.timeout.connect(self.showTime)

  @classmethod
  def getDefault(cls, *args, **kwargs) -> ClockWidget:
    """Returns the default ClockWidget"""
    clockWidget = cls()
    clockWidget.apply((args, kwargs))
    return clockWidget

  def apply(self, value: Any) -> ClockWidget:
    """Applies the value to the field"""
    args, kwargs = unParseArgs(value)
    return self


class ClockField(Wait):
  """ClockField provides a widget showing the time"""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor"""
    Wait.__init__(self, ClockWidget, *args, **kwargs)
