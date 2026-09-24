"""
Qt Compatibility layer supporting both PyQt6 and PySide6.
Defaults to PyQt6, falls back to PySide6.
"""
import sys

QT_API = None

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtCore import Qt, QSize, QPoint, QRect, QRectF, pyqtSignal as Signal, pyqtSlot as Slot, QTimer
    from PyQt6.QtGui import (
        QPixmap, QImage, QPainter, QColor, QFont, QPen, QBrush, QIcon, QKeySequence, QAction,
        QPageSize, QPageLayout, QTextDocument, QMovie
    )
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
        QLabel, QPushButton, QComboBox, QSpinBox, QRadioButton, QButtonGroup,
        QCheckBox, QLineEdit, QSlider, QScrollArea, QFrame, QSplitter,
        QFileDialog, QMessageBox, QStatusBar, QProgressBar, QSizePolicy, QToolButton,
        QStackedWidget, QGroupBox, QGraphicsDropShadowEffect
    )
    from PyQt6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog
    QT_API = "PyQt6"
except ImportError:
    try:
        from PySide6 import QtCore, QtGui, QtWidgets
        from PySide6.QtCore import Qt, QSize, QPoint, QRect, QRectF, Signal, Slot, QTimer
        from PySide6.QtGui import (
            QPixmap, QImage, QPainter, QColor, QFont, QPen, QBrush, QIcon, QKeySequence, QAction,
            QPageSize, QPageLayout, QTextDocument, QMovie
        )
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
            QLabel, QPushButton, QComboBox, QSpinBox, QRadioButton, QButtonGroup,
            QCheckBox, QLineEdit, QSlider, QScrollArea, QFrame, QSplitter,
            QFileDialog, QMessageBox, QStatusBar, QProgressBar, QSizePolicy, QToolButton,
            QStackedWidget, QGroupBox, QGraphicsDropShadowEffect
        )
        from PySide6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog
        QT_API = "PySide6"
    except ImportError as e:
        raise ImportError("Cần cài đặt PyQt6 hoặc PySide6. Hãy chạy: pip install PyQt6 pymupdf Pillow") from e

__all__ = [
    'QT_API', 'QtCore', 'QtGui', 'QtWidgets', 'Qt', 'QSize', 'QPoint', 'QRect', 'QRectF',
    'Signal', 'Slot', 'QTimer', 'QPixmap', 'QImage', 'QPainter', 'QColor', 'QFont',
    'QPen', 'QBrush', 'QIcon', 'QKeySequence', 'QAction', 'QApplication', 'QMainWindow',
    'QWidget', 'QVBoxLayout', 'QHBoxLayout', 'QGridLayout', 'QLabel', 'QPushButton',
    'QComboBox', 'QSpinBox', 'QRadioButton', 'QButtonGroup', 'QCheckBox', 'QLineEdit',
    'QSlider', 'QScrollArea', 'QFrame', 'QSplitter', 'QFileDialog', 'QMessageBox',
    'QStatusBar', 'QProgressBar', 'QSizePolicy', 'QToolButton', 'QStackedWidget', 'QGroupBox',
    'QGraphicsDropShadowEffect',
    'QPrinter', 'QPrinterInfo', 'QPrintDialog', 'QPageSize', 'QPageLayout', 'QTextDocument',
    'QMovie'
]
