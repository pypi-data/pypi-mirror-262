"""BaseWindow provides the menus and actions used by the main application
window. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import numpy as np
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QApplication, QStatusBar
from vistutils.fields import Wait

from vistside.core import generateWhiteNoise, TimerField, Precise
from vistside.widgets import PlotWidget, BaseLayoutField, BaseWidget, \
  DynamicPlotWidget
from vistside.windows.actions import FilesMenu, EditMenu, HelpMenu, \
  MainStatusBar
from vistside.windows.actions import DebugMenu


class BaseWindow(QMainWindow):
  """BaseWindow provides the menus and actions used by the main
  application window. """

  newAction: QAction
  openAction: QAction
  saveAction: QAction
  saveAsAction: QAction
  exitAction: QAction

  selectAllAction: QAction
  cutAction: QAction
  copyAction: QAction
  pasteAction: QAction
  undoAction: QAction
  redoAction: QAction

  aboutAction: QAction
  aboutQtAction: QAction
  aboutPythonAction: QAction

  debug01Action: QAction
  debug02Action: QAction
  debug03Action: QAction
  debug04Action: QAction
  debug05Action: QAction
  debug06Action: QAction
  debug07Action: QAction
  debug08Action: QAction
  debug09Action: QAction
  debug10Action: QAction

  __main_menu_bar__: QMenuBar = None
  __files_menu__: FilesMenu = None
  __edit_menu__: EditMenu = None
  __help_menu__: HelpMenu = None
  __debug_menu__: DebugMenu = None

  showSignal = Signal()

  mainStatusBar = Wait(MainStatusBar, )
  baseWidget = Wait(BaseWidget, )
  baseLayout = BaseLayoutField('vertical')
  paintTimer = TimerField(20, Precise, singleShot=False)

  def __init__(self, *args, **kwargs) -> None:
    QMainWindow.__init__(self)
    self.setMinimumSize(640, 480)
    self.setWindowTitle('Welcome to EZRos!')
    self.timePlot = None
    self.freqPlot = None
    self.__main_menu_bar__ = QMenuBar(self)
    self.__files_menu__ = FilesMenu(self, 'Files')
    self.__edit_menu__ = EditMenu(self, 'Edit')
    self.__help_menu__ = HelpMenu(self, 'Help')
    self.__debug_menu__ = DebugMenu(self, 'DEBUG')

  def show(self) -> None:
    """show displays the window."""
    self.setupMenus()
    self.connectActions()
    self.setStatusBar(self.mainStatusBar)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
    QMainWindow.show(self)
    self.showSignal.emit()

  def setupMenus(self, ) -> None:
    """Function responsible for setting up menus."""
    self.__main_menu_bar__.addMenu(self.__files_menu__)
    self.__main_menu_bar__.addMenu(self.__edit_menu__)
    self.__main_menu_bar__.addMenu(self.__help_menu__)
    self.__main_menu_bar__.addMenu(self.__debug_menu__)
    self.setMenuBar(self.__main_menu_bar__)
    self.__files_menu__.setupActions()
    self.__edit_menu__.setupActions()
    self.__help_menu__.setupActions()
    self.__debug_menu__.setupActions()

  def connectActions(self, ) -> None:
    """connectActions connects the actions to the status bar."""
    self.connectDebugActions()
    self.aboutQtAction.triggered.connect(QApplication.aboutQt)
    self.exitAction.triggered.connect(QApplication.quit)

  def connectDebugActions(self, ) -> None:
    """connectDebugActions connects the debug actions to the status bar."""
    self.debug01Action.triggered.connect(self.debug01Func)
    self.debug02Action.triggered.connect(self.debug02Func)
    self.debug03Action.triggered.connect(self.debug03Func)
    self.debug04Action.triggered.connect(self.debug04Func)
    self.debug05Action.triggered.connect(self.debug05Func)
    self.debug06Action.triggered.connect(self.debug06Func)
    self.debug07Action.triggered.connect(self.debug07Func)
    self.debug08Action.triggered.connect(self.debug08Func)
    self.debug09Action.triggered.connect(self.debug09Func)
    self.debug10Action.triggered.connect(self.debug10Func)

  def debug01Func(self, ) -> None:
    """debug01Func provides a debug function for the window."""
    print('Debug01 action triggered!')
    self.mainStatusBar.showMessage('Debug01 action triggered!')

  def debug02Func(self, ) -> None:
    """debug02Func provides a debug function for the window."""
    print('Debug02 action triggered!')

  def debug03Func(self, ) -> None:  # noqa
    """debug03Func provides a debug function for the window."""
    print('Debug03 action triggered!')

  def debug04Func(self, ) -> None:
    """debug04Func provides a debug function for the window."""
    print('Debug04 action triggered!')

  def debug05Func(self, ) -> None:
    """debug05Func provides a debug function for the window."""
    print('Debug05 action triggered!')

  def debug06Func(self, ) -> None:
    """debug06Func provides a debug function for the window."""
    print('Debug06 action triggered!')

  def debug07Func(self, ) -> None:
    """debug07Func provides a debug function for the window."""
    print('Debug07 action triggered!')

  def debug08Func(self, ) -> None:
    """debug08Func provides a debug function for the window."""
    print('Debug08 action triggered!')

  def debug09Func(self, ) -> None:
    """debug09Func provides a debug function for the window."""
    print('Debug09 action triggered!')

  def debug10Func(self, ) -> None:
    """debug10Func provides a debug function for the window."""
    print('Debug10 action triggered!')
