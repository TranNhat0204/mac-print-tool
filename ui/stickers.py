"""
Animated Sticker Manager for PrintMaster.
Provides cute animated mascot GIF stickers using PyQt6/PySide6 QMovie.
"""
import os
import sys
from ui.qt_compat import QLabel, QMovie, QSize, Qt


def get_asset_path(relative_path: str) -> str:
    """Returns absolute path to asset file, compatible with PyInstaller bundles."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)


def create_sticker_label(sticker_filename: str, width: int = 80, height: int = 80, parent=None) -> QLabel:
    """
    Creates a transparent QLabel playing an animated GIF sticker.
    Stores a reference to the QMovie on the label to prevent premature garbage collection.
    """
    label = QLabel(parent)
    label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    label.setStyleSheet("background: transparent; border: none;")

    gif_path = get_asset_path(os.path.join("assets", "stickers", sticker_filename))
    if os.path.exists(gif_path):
        movie = QMovie(gif_path)
        movie.setScaledSize(QSize(width, height))
        label.setMovie(movie)
        label.setFixedSize(width, height)
        label._movie = movie
        movie.start()

    return label
