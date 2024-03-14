"""The widgets module provides widget classes for the GUI framework."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._base_widget import BaseWidget
from ._base_layout_field import BaseLayoutField
from ._fill_widget import FillWidget
from ._label_widget import LabelWidget, LabelField
from ._lcd_field import LCDField
from ._clock_widget import ClockWidget, ClockField
from ._abstract_dialog_field import AbstractDialogField
from ._confirm_dialog import ConfirmDialog
from ._plot_widget import PlotWidget
from ._dynamic_plot_widget import DynamicPlotWidget
