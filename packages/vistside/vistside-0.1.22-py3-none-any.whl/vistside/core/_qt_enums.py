"""Common names from Qt."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QSizePolicy

__all__ = []

from vistutils.text import stringList

#  Timer types
TimerType = Qt.TimerType
Precise = Qt.TimerType.PreciseTimer
Coarse = Qt.TimerType.CoarseTimer
VeryCoarse = Qt.TimerType.VeryCoarseTimer
__all__ += stringList("""TimerType, Precise, Coarse, VeryCoarse""")
#  Text flags
TextFlag = Qt.TextFlag
WordWrap = Qt.TextFlag.TextWordWrap
CharWrap = Qt.TextFlag.TextWrapAnywhere
NoWrap = Qt.TextFlag.TextSingleLine
__all__ += stringList("""TextFlag, WordWrap, CharWrap, NoWrap""")
#  Alignments
Left = Qt.AlignmentFlag.AlignLeft
Right = Qt.AlignmentFlag.AlignRight
Top = Qt.AlignmentFlag.AlignTop
Bottom = Qt.AlignmentFlag.AlignBottom
Center = Qt.AlignmentFlag.AlignCenter
HCenter = Qt.AlignmentFlag.AlignHCenter
VCenter = Qt.AlignmentFlag.AlignVCenter
__all__ += stringList(
  """Left, Right, Top, Bottom, Center, HCenter, VCenter""")
#  Pen styles
SolidLine = Qt.PenStyle.SolidLine
DashLine = Qt.PenStyle.DashLine
DotLine = Qt.PenStyle.DotLine
DashDotLine = Qt.PenStyle.DashDotLine
DashDotDotLine = Qt.PenStyle.DashDotDotLine
EmptyLine = Qt.PenStyle.NoPen
RoundCap = Qt.PenCapStyle.RoundCap
FlatCap = Qt.PenCapStyle.FlatCap
SquareCap = Qt.PenCapStyle.SquareCap
__all__ += stringList(
  """SolidLine, DashLine, DotLine, DashDotLine, DashDotDotLine, EmptyLine,
  RoundCap, FlatCap, SquareCap""")
#  Brush styles
SolidFill = Qt.BrushStyle.SolidPattern
__all__ += stringList("""SolidFill""")
#  Size policy
Spread = QSizePolicy.Policy.MinimumExpanding
Fixed = QSizePolicy.Policy.Fixed
Tight = QSizePolicy.Policy.Maximum
__all__ += stringList("""Spread, Fixed, Tight""")
#  Mouse buttons
MouseBtn = Qt.MouseButton
NoBtn = Qt.MouseButton.NoButton
LeftBtn = Qt.MouseButton.LeftButton
RightBtn = Qt.MouseButton.RightButton
MiddleBtn = Qt.MouseButton.MiddleButton
NextBtn = Qt.MouseButton.ForwardButton
BackBtn = Qt.MouseButton.BackButton
__all__ += stringList(
  """NoBtn, MouseBtn, LeftBtn, RightBtn, MiddleBtn, NextBtn, BackBtn""")
#  Mouse events
Mouse = QMouseEvent
BtnDown = QEvent.Type.MouseButtonPress
BtnUp = QEvent.Type.MouseButtonRelease
MouseMove = QEvent.Type.MouseMove
__all__ += stringList("""Mouse, BtnDown, BtnUp, MouseMove""")
