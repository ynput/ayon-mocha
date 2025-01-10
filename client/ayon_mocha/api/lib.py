"""Library functions for the Ayon Mocha API."""
from __future__ import annotations
from typing import TYPE_CHECKING
from mocha import ui
from qtpy.QtWidgets import QApplication

if TYPE_CHECKING:
    from qtpy import QtWidgets


def get_main_window() -> QtWidgets.QWidget:
    """Get the main window of the application.

    Returns:
        QWidget: Main window of the application.
    """
    return ui.get_widgets()["MainWindow"]

def update_UI():
    """Update the UI."""
    QApplication.processEvents()
