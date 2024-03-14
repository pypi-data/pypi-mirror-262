import argparse
import os
import signal
from pathlib import Path
from typing import Dict, Tuple

os.environ["PYQTGRAPH_QT_LIB"] = "PyQt6"
from importlib.resources import files
from importlib.resources import path as resource_path

import pyvisa
import qdarktheme
from PyQt6.QtCore import QLocale
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget

from sonaris.frontend.header import (
    MONITOR_FILE,
    OSCILLOSCOPE_BUFFER_SIZE,
    TIMEKEEPER_JOBS_FILE,
    DeviceName,
)
from sonaris.frontend.managers.dg4202 import DG4202Manager
from sonaris.frontend.managers.edux1002a import EDUX1002AManager
from sonaris.frontend.managers.state_manager import StateManager
from sonaris.frontend.pages import factory
from sonaris.frontend.pages.general import GeneralPage
from sonaris.frontend.pages.monitor import MonitorPage
from sonaris.frontend.pages.scheduler import SchedulerPage
from sonaris.frontend.pages.settings import SettingsPage
from sonaris.frontend.tasks.tasks import get_tasks
from sonaris.frontend.widgets.menu import MainMenuBar
from sonaris.frontend.widgets.sidebar import Sidebar
from sonaris.frontend.widgets.templates import ModularMainWindow
from sonaris.scheduler import registry
from sonaris.scheduler.timekeeper import Timekeeper
from sonaris.scheduler.worker import Worker
from sonaris.utils.logging import get_logger

logger = get_logger()

# Before creating your application instance
QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))


def signal_handler(signum, frame):
    logger.info("Exit signal detected.")
    QApplication.quit()
    factory.worker.stop_worker()
    # Invoke the default SIGINT handler to exit the application
    signal.signal(signum, signal.SIG_DFL)
    os.kill(os.getpid(), signum)


def init_objects(args_dict: dict):
    factory.resource_manager = pyvisa.ResourceManager()
    factory.state_manager = StateManager()
    factory.edux1002a_manager = EDUX1002AManager(
        state_manager=factory.state_manager,
        args_dict=args_dict,
        resource_manager=factory.resource_manager,
        buffer_size=OSCILLOSCOPE_BUFFER_SIZE,
    )
    factory.dg4202_manager = DG4202Manager(
        factory.state_manager,
        args_dict=args_dict,
        resource_manager=factory.resource_manager,
    )
    factory.worker = Worker(
        function_map=registry.function_map,
        logger=logger,
    )
    factory.timekeeper = Timekeeper(
        persistence_file=TIMEKEEPER_JOBS_FILE,
        worker_instance=factory.worker,
        logger=logger,
    )

    for task_name, func_pointer in get_tasks(flatten=True).items():
        factory.worker.register_task(func_pointer, task_name)

    factory.worker.start_worker()


class MainWindow(ModularMainWindow):
    def __init__(self, args_dict: dict) -> None:
        super().__init__()
        menu_bar = MainMenuBar(self)
        self.setWindowTitle("Sonaris")
        self.setMenuBar(menu_bar)
        self.last_page = ""
        # ---------------------------------------------------------------------- #
        # ---------------------------SIDEBAR SETUP------------------------------ #
        self.sidebar = Sidebar(self)
        device_managers = {
            DeviceName.DG4202.value: factory.dg4202_manager,
            DeviceName.EDUX1002A.value: factory.edux1002a_manager,
        }
        self.sidebar.sizePolicy()
        self.sidebar_dict: Dict[str, QWidget] = {
            GeneralPage.PAGE_NAME: GeneralPage(
                dg4202_manager=factory.dg4202_manager,
                edux1002a_manager=factory.edux1002a_manager,
                parent=self,
                args_dict=args_dict,
                root_callback=self.root_callback,
            ),
            SchedulerPage.PAGE_NAME: SchedulerPage(
                timekeeper=factory.timekeeper,
                parent=self,
                args_dict=args_dict,
                root_callback=self.root_callback,
            ),
            MonitorPage.PAGE_NAME: MonitorPage(
                device_managers=device_managers,
                parent=self,
                args_dict=args_dict,
                monitor_logs=MONITOR_FILE,
                root_callback=self.root_callback,
            ),
            SettingsPage.PAGE_NAME: SettingsPage(
                device_managers=device_managers,
                parent=self,
                args_dict=args_dict,
                root_callback=self.root_callback,
            ),
        }
        self.sidebar.addItems(self.sidebar_dict.keys())  # Add strings to sidebar items
        self.sidebar_content = QStackedWidget(self)
        list(
            map(self.sidebar_content.addWidget, self.sidebar_dict.values())
        )  # Adds all child widgets to content widgets

        # --------------------------------------------------------------------- #
        # ---------------------------LAYOUT SETUP------------------------------ #
        # --------------------------------------------------------------------- #

        self.add_widget_to_left(self.sidebar)
        self.add_widget_to_middle(
            self.sidebar_content
        )  # Use the method from ModularMainWindow
        # Connect the Sidebar's custom signal to the MainWindow's slot
        self.sidebar.pageSelected.connect(self.loadPage)

    def loadPage(self, page_name: str) -> None:
        page_widget: QWidget = self.sidebar_dict.get(page_name)
        if page_widget and self.last_page != page_name:
            self.sidebar_content.setCurrentWidget(page_widget)
            # logger.info(f"[Sidebar] Switch event to {page_name}")
            page_widget.update()
            self.last_page = page_name

    def root_callback(self):
        """tells pages the pages to call update method."""
        for _, page_obj in self.sidebar_dict.items():
            page_obj.update()

    def closeEvent(self, event):
        logger.info("main x exit button was clicked")
        factory.worker.stop_worker()
        super().closeEvent(event)

    def showEvent(self, event):
        primaryScreen = QGuiApplication.primaryScreen()
        screenGeometry = primaryScreen.availableGeometry()
        centerPoint = screenGeometry.center()
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())
        super().showEvent(event)


def create_app(args_dict: dict) -> Tuple[QApplication, MainWindow]:
    init_objects(args_dict=args_dict)

    app = QApplication([])
    window = MainWindow(args_dict)

    qdarktheme.setup_theme()

    # Assuming 'sonaris.assets' is a valid package path
    favicon_path = files("sonaris.assets").joinpath("favicon.ico")
    app_icon = QIcon(str(favicon_path))

    app.setWindowIcon(app_icon)
    window.setWindowIcon(app_icon)

    window.setWindowTitle("sonaris")
    window.resize(640, 400)
    logger.info(f"Window size after resize: {window.size()} ")
    return app, window


def run_application(args_dict):
    logger.info(args_dict)
    app, window = create_app(args_dict)
    window.show()
    app.exec()


if __name__ == "__main__":
    # Not recommended anymore to run this way. (sonaris/__main__.py controls the argument parsing using click)
    # Do python -m sonaris run --hardware-mock to run the app in hardware mock mode instead ( or poetry run python -m sonaris run --hardware-mock)
    # You can do packaged runs as well by doing 'pip install .'
    parser = argparse.ArgumentParser(description="Run the sonaris application.")
    parser.add_argument(
        "--hardware-mock",
        action="store_true",
        help="Run the app in hardware mock mode.",
    )
    args = parser.parse_args()
    args_dict = vars(args)
    run_application(args_dict)
