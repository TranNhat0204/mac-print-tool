#!/usr/bin/env python3
"""
PrintMaster (MacPrint) - Ứng dụng xem trước và in ấn chuyên nghiệp (Windows & macOS)
"""
import sys
import os

# Ensure current dir is in PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.qt_compat import QApplication, QtCore, Qt
from ui.main_window import MainWindow


class PrintApplication(QApplication):
    """
    Custom QApplication subclass to capture macOS 'Open With' and Drag-to-Dock
    FileOpen events (kAEOpenDocuments).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = None
        self.queued_file = None

    def event(self, event):
        if event.type() == QtCore.QEvent.Type.FileOpen:
            file_path = ""
            if hasattr(event, "file"):
                file_path = event.file()
            elif hasattr(event, "url"):
                file_path = event.url().toLocalFile()

            if file_path and os.path.exists(file_path):
                if self.main_window:
                    self.main_window.open_file(file_path)
                else:
                    self.queued_file = file_path
                return True

        return super().event(event)


def main():
    # Enable High DPI scaling for Retina displays
    if hasattr(QtCore.Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = PrintApplication(sys.argv)
    app.setApplicationName("MacPrint")
    app.setApplicationDisplayName("MacPrint - Xem trước & In ấn")
    app.setOrganizationName("MacPrint")

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "app_icon.png")
    if os.path.exists(icon_path):
        from ui.qt_compat import QIcon
        app.setWindowIcon(QIcon(icon_path))

    initial_file = None
    if len(sys.argv) > 1:
        arg_path = sys.argv[1]
        if os.path.exists(arg_path):
            initial_file = os.path.abspath(arg_path)

    window = MainWindow(initial_file=initial_file)
    app.main_window = window

    # If a file was received via macOS FileOpen event before window ready
    if app.queued_file and not initial_file:
        window.open_file(app.queued_file)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
