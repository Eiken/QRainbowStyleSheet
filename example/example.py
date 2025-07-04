#!python
# -*- coding: utf-8 -*-

"""Example of qrainbowstyle use for Python and Qt applications.

This module a main window with every item that could be created with
Qt Design (common ones) in the basic states (enabled/disabled), and
(checked/unchecked) for those who has this attribute.

Requirements:

    - Python 3
    - QtPy
    - PyQt5, PySide2 or PySide6
    - Qt.Py (if choosen)

To run this example using PyQt5, simple do

.. code-block:: python

    python example.py

or

.. code-block:: python

    python example.py  --qt_from=pyqt5

Other options for qt_from are: pyqt5, pyside2, pyside6, qtpy, and qt.py.
Also, you can run the example without dark theme (no_dark), to check for problems.

.. code-block:: python

    python example.py  --qt_from=pyqt5 --no_dark

Note:
    qrainbowstyle does not have to be installed to run the example.

"""

# Standard library imports

import argparse
import logging
import os
import sys
import platform
import time
import random

# Make the example runnable without the need to install and include ui
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..'))
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/ui'))

# Must be in this place, after setting path, to not need to install
import qrainbowstyle  # noqa: E402
import qrainbowstyle.windows  # noqa: E402
import qrainbowstyle.widgets  # noqa: E402

# Set log for debug
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

# Constants
SCREENSHOTS_PATH = qrainbowstyle.IMAGES_PATH


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--qt_from', default='qtpy', type=str,
                        choices=['pyqt5', 'pyside2', 'pyside6', 'qtpy', 'qt.py'],
                        help="Choose which binding and/or abstraction is to be used to run the example.")
    parser.add_argument('--style', type=str,
                        help="Use custom style.")
    parser.add_argument('--test', action='store_true',
                        help="Auto close window after 2s.")
    parser.add_argument('--reset', action='store_true',
                        help="Reset GUI settings (position, size) then opens.")
    parser.add_argument('--screenshots', action='store_true',
                        help="Generate screenshots on images folder.")

    # Parsing arguments from command line
    args = parser.parse_args()

    if args.test:
        for style in qrainbowstyle.getAvailableStyles():
            parser.set_defaults(style=style)
            _main(parser.parse_args())
    else:
        _main(args)


def _main(args):
    # To avoid problems when testing without screen
    if args.test or args.screenshots:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'

    # Set QT_API variable before importing QtPy
    if args.qt_from in ['pyqt5', 'pyside2', 'pyside6']:
        os.environ['QT_API'] = args.qt_from
    elif args.qt_from in ['qt.py', 'qt']:
        try:
            import Qt
        except ImportError:
            print('Could not import Qt (Qt.Py)')
        else:
            os.environ['QT_API'] = Qt.__binding__

    # QtPy imports
    from qtpy import API_NAME, QT_VERSION, PYQT_VERSION, PYSIDE_VERSION
    from qtpy import __version__ as QTPY_VERSION
    from qtpy.QtWidgets import (QApplication, QMainWindow, QDockWidget,
                                QStatusBar, QLabel, QMenu)
    from qtpy.QtCore import QTimer, Qt, QSettings

    # Set API_VERSION variable
    API_VERSION = ''

    if PYQT_VERSION:
        API_VERSION = PYQT_VERSION
    elif PYSIDE_VERSION:
        API_VERSION = PYSIDE_VERSION
    else:
        API_VERSION = 'Not found'

    # Import examples UI
    from mw_menus_ui import Ui_MainWindow as ui_main

    from dw_buttons_ui import Ui_DockWidget as ui_buttons
    from dw_displays_ui import Ui_DockWidget as ui_displays
    from dw_inputs_fields_ui import Ui_DockWidget as ui_inputs_fields
    from dw_inputs_no_fields_ui import Ui_DockWidget as ui_inputs_no_fields

    from dw_widgets_ui import Ui_DockWidget as ui_widgets
    from dw_views_ui import Ui_DockWidget as ui_views
    from dw_containers_tabs_ui import Ui_DockWidget as ui_containers_tabs
    from dw_containers_no_tabs_ui import Ui_DockWidget as ui_containers_no_tabs

    # qrainbowstyle.useDarwinButtons()

    # If using Qt5 enable for HighDPI support, in Qt6 HighDPI support is
    # enabled by default.
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    # create the application
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setOrganizationName('QRainbowStyle')
    app.setApplicationName('QRainbowStyle Example')

    styles = qrainbowstyle.getAvailableStyles()

    style = args.style
    if not args.style:
        style = styles[random.randint(0, len(styles)) - 1]

    app.setStyleSheet(qrainbowstyle.load_stylesheet(style=str(style)))

    # create main window
    window = qrainbowstyle.windows.FramelessWindow()
    window.setTitlebarHeight(30)

    widget = QMainWindow(window)
    widget.setWindowFlags(Qt.Widget)
    widget.setObjectName('mainwindow')
    ui = ui_main()
    ui.setupUi(widget)

    window.addContentWidget(widget)

    title = ("QRainbowStyle Example - "
             + "(QRainbowStyle=v" + qrainbowstyle.__version__
             + ", QtPy=v" + QTPY_VERSION
             + ", " + API_NAME + "=v" + API_VERSION
             + ", Qt=v" + QT_VERSION
             + ", Python=v" + platform.python_version() + ")")

    _logger.info(title)

    window.setWindowTitle(title)

    # Create docks for buttons
    dw_buttons = QDockWidget()
    dw_buttons.setObjectName('buttons')
    ui_buttons = ui_buttons()
    ui_buttons.setupUi(dw_buttons)
    widget.addDockWidget(Qt.RightDockWidgetArea, dw_buttons)

    # Add actions on popup toolbuttons
    menu = QMenu()

    for action in ['Action A', 'Action B', 'Action C']:
        menu.addAction(action)

    ui_buttons.toolButtonDelayedPopup.setMenu(menu)
    ui_buttons.toolButtonInstantPopup.setMenu(menu)
    ui_buttons.toolButtonMenuButtonPopup.setMenu(menu)

    # Create docks for buttons
    dw_displays = QDockWidget()
    dw_displays.setObjectName('displays')
    ui_displays = ui_displays()
    ui_displays.setupUi(dw_displays)
    widget.addDockWidget(Qt.RightDockWidgetArea, dw_displays)

    # Create docks for inputs - no fields
    dw_inputs_no_fields = QDockWidget()
    dw_inputs_no_fields.setObjectName('inputs_no_fields')
    ui_inputs_no_fields = ui_inputs_no_fields()
    ui_inputs_no_fields.setupUi(dw_inputs_no_fields)
    widget.addDockWidget(Qt.RightDockWidgetArea, dw_inputs_no_fields)

    # Create docks for inputs - fields
    dw_inputs_fields = QDockWidget()
    dw_inputs_fields.setObjectName('inputs_fields')
    ui_inputs_fields = ui_inputs_fields()
    ui_inputs_fields.setupUi(dw_inputs_fields)
    widget.addDockWidget(Qt.RightDockWidgetArea, dw_inputs_fields)

    # Create docks for widgets
    dw_widgets = QDockWidget()
    dw_widgets.setObjectName('widgets')
    ui_widgets = ui_widgets()
    ui_widgets.setupUi(dw_widgets)
    widget.addDockWidget(Qt.LeftDockWidgetArea, dw_widgets)

    # Create docks for views
    dw_views = QDockWidget()
    dw_views.setObjectName('views')
    ui_views = ui_views()
    ui_views.setupUi(dw_views)
    widget.addDockWidget(Qt.LeftDockWidgetArea, dw_views)

    # Create docks for containers - no tabs
    dw_containers_no_tabs = QDockWidget()
    dw_containers_no_tabs.setObjectName('containers_no_tabs')
    ui_containers_no_tabs = ui_containers_no_tabs()
    ui_containers_no_tabs.setupUi(dw_containers_no_tabs)
    widget.addDockWidget(Qt.LeftDockWidgetArea, dw_containers_no_tabs)

    # Create docks for containters - tabs
    dw_containers_tabs = QDockWidget()
    dw_containers_tabs.setObjectName('containers_tabs')
    ui_containers_tabs = ui_containers_tabs()
    ui_containers_tabs.setupUi(dw_containers_tabs)
    widget.addDockWidget(Qt.LeftDockWidgetArea, dw_containers_tabs)

    # Tabify right docks
    widget.tabifyDockWidget(dw_buttons, dw_displays)
    widget.tabifyDockWidget(dw_displays, dw_inputs_fields)
    widget.tabifyDockWidget(dw_inputs_fields, dw_inputs_no_fields)

    # Tabify left docks
    widget.tabifyDockWidget(dw_containers_no_tabs, dw_containers_tabs)
    widget.tabifyDockWidget(dw_containers_tabs, dw_widgets)
    widget.tabifyDockWidget(dw_widgets, dw_views)

    # Issues #9120, #9121 on Spyder
    qstatusbar = QStatusBar()
    qstatusbar.addWidget(QLabel('Style'))
    qstatusbarbutton = qrainbowstyle.widgets.StylePickerHorizontal()
    qstatusbar.addWidget(qstatusbarbutton)
    qstatusbar.setSizeGripEnabled(False)

    # Add info also in status bar for screenshots get it
    qstatusbar.addWidget(QLabel('INFO: ' + title))
    widget.setStatusBar(qstatusbar)

    # Todo: add report info and other info in HELP graphical

    # Auto quit after 2s when in test mode
    if args.test:
        QTimer.singleShot(2000, app.exit)

    _read_settings(widget, args.reset, QSettings)
    window.show()
    # window.showMaximized()

    app.exec_()
    _write_settings(widget, QSettings)


def _write_settings(window, QSettings):
    """Get window settings and write it into a file."""
    settings = QSettings('QRainbowStyle', 'QRainbowStyle Example')
    settings.setValue('pos', window.pos())
    settings.setValue('size', window.size())
    settings.setValue('state', window.saveState())


def _read_settings(window, reset, QSettings):
    """Read and set window settings from a file."""
    settings = QSettings('QRainbowStyle', 'QRainbowStyle Example')

    try:
        pos = settings.value('pos', window.pos())
        size = settings.value('size', window.size())
        state = settings.value('state', window.saveState())
    except Exception:
        pos = settings.value('pos', window.pos(), type='QPoint')
        size = settings.value('size', window.size(), type='QSize')
        state = settings.value('state', window.saveState(), type='QByteArray')

    if not reset:
        window.restoreState(state)
        window.resize(size)
        window.move(pos)


if __name__ == "__main__":
    sys.exit(main())
