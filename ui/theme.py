"""
Visual Theme and Styling for PrintMaster.
Boxy, modern Pastel Pink theme with optimized Vietnamese typography and high contrast.
"""

STYLESHEET = """
/* Global Window Style - Optimized for macOS SF Pro and Windows Segoe UI */
QMainWindow {
    background-color: #FFF7F9;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", "Segoe UI", "Tahoma", "Arial", sans-serif;
    font-size: 13px;
    color: #1F2937;
}

/* Menu Bar */
QMenuBar {
    background-color: #FFF0F4;
    color: #4B5563;
    border-bottom: 1px solid #FCE7F0;
    padding: 2px 6px;
    font-weight: 500;
}

QMenuBar::item:selected {
    background-color: #FCE7F3;
    color: #881337;
    border-radius: 2px;
}

QMenu {
    background-color: #FFFFFF;
    color: #1F2937;
    border: 1px solid #FBCFE8;
    border-radius: 2px;
    padding: 4px;
}

QMenu::item:selected {
    background-color: #FCE7F3;
    color: #881337;
}

/* Canvas / Preview Container - Clean Boxy Look */
#previewArea {
    background-color: #2D2430;
    border: none;
}

#previewScroll {
    background-color: #2D2430;
    border: none;
}

/* Settings Sidebar Container */
#settingsPanel {
    background-color: #FFFFFF;
    border-left: 1px solid #FCE7F0;
}

#settingsScroll {
    background-color: #FFFFFF;
    border: none;
}

/* Headings and Section Labels */
QLabel#dialogTitle {
    font-size: 17px;
    font-weight: 700;
    color: #881337;
    padding-bottom: 2px;
}

QLabel#dialogSubtitle {
    font-size: 12px;
    color: #6B7280;
}

QLabel#sectionTitle {
    font-size: 12px;
    font-weight: 700;
    color: #9F1239;
    margin-top: 6px;
    margin-bottom: 3px;
    letter-spacing: 0.3px;
}

/* Group Cards - Raised Card with 3D Bevel & Floating Surface */
QFrame.settingCard {
    background-color: #FFFFFF;
    border: 1px solid #F3D2E2;
    border-top: 1px solid #FCE7F0;
    border-bottom: 2.5px solid #E8B4CB;
    border-radius: 6px;
    padding: 12px 12px;
    margin: 2px 2px 8px 2px;
}

/* Base Buttons - Tactile Raised 3D Look */
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FDF2F7);
    border: 1px solid #DFB5CA;
    border-top: 1px solid #F2DCE7;
    border-bottom: 2.5px solid #C4799C;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 600;
    color: #1F2937;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #FFF0F4;
    border-color: #F472B6;
    border-bottom: 2.5px solid #DB2777;
    color: #881337;
}

QPushButton:pressed {
    background-color: #FCE7F3;
    border: 1px solid #DB2777;
    border-top: 2.5px solid #9D174D;
    border-bottom: 1px solid #F472B6;
    padding-top: 8px;
    padding-bottom: 4px;
}

/* Primary Action Button (In / Print) - Prominent Raised 3D with Black Text */
QPushButton#primaryPrintBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F687B3, stop:0.4 #F472B6, stop:1 #EC4899);
    color: #000000;
    border: 1px solid #DB2777;
    border-top: 1px solid #F9A8D4;
    border-bottom: 3.5px solid #BE185D;
    font-weight: 700;
    font-size: 14px;
    border-radius: 4px;
    padding: 10px 24px;
    min-height: 42px;
}

QPushButton#primaryPrintBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F472B6, stop:1 #DB2777);
    border-color: #BE185D;
    border-bottom: 3.5px solid #9D174D;
    color: #000000;
}

QPushButton#primaryPrintBtn:pressed {
    background-color: #BE185D;
    border-color: #9D174D;
    border-top: 3.5px solid #831843;
    border-bottom: 1px solid #BE185D;
    padding-top: 13px;
    padding-bottom: 7px;
    color: #000000;
}

QPushButton#primaryPrintBtn:disabled {
    background-color: #E5E7EB;
    border: 1px solid #D1D5DB;
    border-bottom: 2px solid #9CA3AF;
    color: #9CA3AF;
}

/* Cancel Button */
QPushButton#cancelBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FDF2F7);
    border: 1px solid #DFB5CA;
    border-top: 1px solid #F0D7E4;
    border-bottom: 2.5px solid #C4799C;
    color: #4B5563;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 42px;
}

QPushButton#cancelBtn:hover {
    background-color: #FFF0F4;
    color: #1F2937;
    border-color: #F472B6;
    border-bottom: 2.5px solid #DB2777;
}

QPushButton#cancelBtn:pressed {
    background-color: #FCE7F3;
    border: 1px solid #DB2777;
    border-top: 2.5px solid #9D174D;
    border-bottom: 1px solid #F472B6;
    padding-top: 12px;
    padding-bottom: 8px;
}

/* Refresh Button */
QPushButton#refreshBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FDF2F7);
    border: 1px solid #DFB5CA;
    border-top: 1px solid #F0D7E4;
    border-bottom: 2.5px solid #C4799C;
    border-radius: 4px;
    font-weight: 700;
    font-size: 15px;
    color: #9D174D;
    min-height: 32px;
    max-height: 32px;
    min-width: 34px;
    max-width: 34px;
}

QPushButton#refreshBtn:hover {
    background-color: #FFF0F4;
    border-color: #F472B6;
    border-bottom: 2.5px solid #DB2777;
}

QPushButton#refreshBtn:pressed {
    background-color: #FCE7F3;
    border: 1px solid #DB2777;
    border-top: 2.5px solid #9D174D;
    border-bottom: 1px solid #F472B6;
    padding-top: 4px;
}

/* Uniform Input Controls - Raised 3D Bevel with Crisp Dimensions (32px) */
QComboBox {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.8 #FFFFFF, stop:1 #FFF0F5);
    border: 1px solid #DFB5CA;
    border-top: 1px solid #EED1DF;
    border-bottom: 2.5px solid #C4799C;
    border-radius: 4px;
    padding: 0px 10px;
    color: #1F2937;
    min-height: 32px;
    max-height: 32px;
    font-size: 13px;
}

QComboBox:hover {
    border-color: #F472B6;
    border-bottom: 2.5px solid #DB2777;
    background-color: #FFFFFF;
}

QComboBox:focus {
    border: 1.5px solid #EC4899;
    border-bottom: 2.5px solid #BE185D;
    background-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid #F3D2E2;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FCE7F0);
}

QComboBox::drop-down:hover {
    background-color: #FCE7F3;
}

QComboBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #9D174D;
    margin-right: 2px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #F472B6;
    selection-background-color: #FCE7F3;
    selection-color: #881337;
    border-radius: 4px;
    padding: 4px;
}

QSpinBox {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.8 #FFFFFF, stop:1 #FFF0F5);
    border: 1px solid #DFB5CA;
    border-top: 1px solid #EED1DF;
    border-bottom: 2.5px solid #C4799C;
    border-radius: 4px;
    padding: 0px 8px;
    color: #1F2937;
    min-height: 32px;
    max-height: 32px;
    font-size: 13px;
}

QSpinBox:hover {
    border-color: #F472B6;
    border-bottom: 2.5px solid #DB2777;
    background-color: #FFFFFF;
}

QSpinBox:focus {
    border: 1.5px solid #EC4899;
    border-bottom: 2.5px solid #BE185D;
    background-color: #FFFFFF;
}

QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    height: 16px;
    border-left: 1px solid #F3D2E2;
    border-bottom: 1px solid #F3D2E2;
    border-top-right-radius: 4px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FCE7F0);
}

QSpinBox::up-button:hover {
    background-color: #FCE7F3;
}

QSpinBox::up-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-bottom: 4px solid #9D174D;
}

QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    height: 16px;
    border-left: 1px solid #F3D2E2;
    border-bottom-right-radius: 4px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FCE7F0);
}

QSpinBox::down-button:hover {
    background-color: #FCE7F3;
}

QSpinBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-top: 4px solid #9D174D;
}

QLineEdit {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.8 #FFFFFF, stop:1 #FFF0F5);
    border: 1px solid #DFB5CA;
    border-top: 1px solid #EED1DF;
    border-bottom: 2.5px solid #C4799C;
    border-radius: 4px;
    padding: 0px 10px;
    color: #1F2937;
    min-height: 32px;
    max-height: 32px;
    font-size: 13px;
}

QLineEdit:hover {
    border-color: #F472B6;
    border-bottom: 2.5px solid #DB2777;
    background-color: #FFFFFF;
}

QLineEdit:focus {
    border: 1.5px solid #EC4899;
    border-bottom: 2.5px solid #BE185D;
    background-color: #FFFFFF;
}

QLineEdit:disabled {
    border: 1px solid #E5E7EB;
    border-bottom: 1.5px solid #D1D5DB;
    background-color: #F9FAFB;
    color: #9CA3AF;
}

QRadioButton {
    spacing: 8px;
    color: #1F2937;
    font-size: 13px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox {
    spacing: 8px;
    color: #1F2937;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 2px;
}

/* Preview Toolbar Header Controls - Raised 3D Look */
QFrame#previewToolbar {
    background-color: #241B26;
    border-bottom: 1px solid #433347;
    border-radius: 0px;
    padding: 6px 12px;
}

QFrame#previewToolbar QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3D2F43, stop:1 #2E2233);
    border: 1px solid #4D3A55;
    border-top: 1px solid #5C4666;
    border-bottom: 2px solid #1C1520;
    color: #FCE7F3;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 500;
    min-height: 28px;
}

QFrame#previewToolbar QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F472B6, stop:1 #EC4899);
    border-color: #EC4899;
    border-bottom: 2px solid #BE185D;
    color: #FFFFFF;
}

QFrame#previewToolbar QPushButton:pressed {
    background-color: #BE185D;
    border-top: 2px solid #831843;
    border-bottom: 1px solid #BE185D;
    padding-top: 5px;
    padding-bottom: 3px;
}

QFrame#previewToolbar QPushButton:disabled {
    background-color: #241B26;
    border: 1px solid #332737;
    border-bottom: 1px solid #231926;
    color: #635068;
}

QFrame#previewToolbar QLabel {
    color: #FCE7F3;
    font-size: 12px;
    font-weight: 600;
}

/* Status Bar */
QStatusBar {
    background-color: #FFF0F4;
    color: #6B7280;
    border-top: 1px solid #FCE7F0;
    font-size: 12px;
}

/* Splitter Handle - Flat line */
QSplitter::handle {
    background-color: #FCE7F0;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #F472B6;
}

/* Drag and Drop Zone - Boxy Modern */
#dropZone {
    background-color: #FFF7F9;
    border: 2px dashed #F472B6;
    border-radius: 4px;
    margin: 40px;
}

#dropZone:hover {
    background-color: #FFF0F4;
    border-color: #EC4899;
}
"""
