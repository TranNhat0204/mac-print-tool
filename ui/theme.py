"""
Visual Theme and Styling for PrintMaster.
Boxy, modern Pastel Orange theme with optimized Vietnamese typography and high contrast tactile 3D controls.
"""

STYLESHEET = """
/* Global Window Style - Optimized for macOS SF Pro and Windows Segoe UI */
QMainWindow {
    background-color: #FFFBF7;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", "Segoe UI", "Tahoma", "Arial", sans-serif;
    font-size: 13px;
    color: #1F2937;
}

/* Menu Bar */
QMenuBar {
    background-color: #FFF5EB;
    color: #4B5563;
    border-bottom: 1px solid #FED7AA;
    padding: 2px 6px;
    font-weight: 500;
}

QMenuBar::item:selected {
    background-color: #FFEDD5;
    color: #9A3412;
    border-radius: 2px;
}

QMenu {
    background-color: #FFFFFF;
    color: #1F2937;
    border: 1px solid #FED7AA;
    border-radius: 2px;
    padding: 4px;
}

QMenu::item:selected {
    background-color: #FFEDD5;
    color: #9A3412;
}

/* Canvas / Preview Container - Clean Boxy Warm Charcoal Look */
#previewArea {
    background-color: #292524;
    border: none;
}

#previewScroll {
    background-color: #292524;
    border: none;
}

/* Settings Sidebar Container */
#settingsPanel {
    background-color: #FFFFFF;
    border-left: 1px solid #FED7AA;
}

#settingsScroll {
    background-color: #FFFFFF;
    border: none;
}

/* Headings and Section Labels */
QLabel#dialogTitle {
    font-size: 17px;
    font-weight: 700;
    color: #9A3412;
    padding-bottom: 2px;
}

QLabel#dialogSubtitle {
    font-size: 12px;
    color: #78716C;
}

QLabel#sectionTitle {
    font-size: 12px;
    font-weight: 700;
    color: #C2410C;
    margin-top: 6px;
    margin-bottom: 3px;
    letter-spacing: 0.3px;
}

/* Group Cards - Raised Card with 3D Bevel & Floating Surface */
QFrame.settingCard {
    background-color: #FFFFFF;
    border: 1px solid #FCD3B0;
    border-top: 1px solid #FFEDD5;
    border-bottom: 2.5px solid #FDBA74;
    border-radius: 6px;
    padding: 12px 12px;
    margin: 2px 2px 8px 2px;
}

/* Base Buttons - Tactile Raised 3D Look */
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFF7ED);
    border: 1px solid #FDBA74;
    border-top: 1px solid #FFE4CD;
    border-bottom: 2.5px solid #FB923C;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 600;
    color: #1F2937;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #FFF5EB;
    border-color: #FB923C;
    border-bottom: 2.5px solid #F97316;
    color: #9A3412;
}

QPushButton:pressed {
    background-color: #FFEDD5;
    border: 1px solid #EA580C;
    border-top: 2.5px solid #C2410C;
    border-bottom: 1px solid #FB923C;
    padding-top: 8px;
    padding-bottom: 4px;
}

/* Primary Action Button (In / Print) - Prominent Raised 3D with Black Text */
QPushButton#primaryPrintBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FDBA74, stop:0.4 #FB923C, stop:1 #F97316);
    color: #000000;
    border: 1px solid #EA580C;
    border-top: 1px solid #FED7AA;
    border-bottom: 3.5px solid #C2410C;
    font-weight: 700;
    font-size: 14px;
    border-radius: 4px;
    padding: 10px 24px;
    min-height: 42px;
}

QPushButton#primaryPrintBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FB923C, stop:1 #EA580C);
    border-color: #C2410C;
    border-bottom: 3.5px solid #9A3412;
    color: #000000;
}

QPushButton#primaryPrintBtn:pressed {
    background-color: #EA580C;
    border-color: #9A3412;
    border-top: 3.5px solid #7C2D12;
    border-bottom: 1px solid #EA580C;
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
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFF7ED);
    border: 1px solid #FDBA74;
    border-top: 1px solid #FFE4CD;
    border-bottom: 2.5px solid #FB923C;
    color: #4B5563;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 42px;
}

QPushButton#cancelBtn:hover {
    background-color: #FFF5EB;
    color: #1F2937;
    border-color: #FB923C;
    border-bottom: 2.5px solid #F97316;
}

QPushButton#cancelBtn:pressed {
    background-color: #FFEDD5;
    border: 1px solid #EA580C;
    border-top: 2.5px solid #C2410C;
    border-bottom: 1px solid #FB923C;
    padding-top: 12px;
    padding-bottom: 8px;
}

/* Refresh Button */
QPushButton#refreshBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFF7ED);
    border: 1px solid #FDBA74;
    border-top: 1px solid #FFE4CD;
    border-bottom: 2.5px solid #FB923C;
    border-radius: 4px;
    font-weight: 700;
    font-size: 15px;
    color: #C2410C;
    min-height: 32px;
    max-height: 32px;
    min-width: 34px;
    max-width: 34px;
}

QPushButton#refreshBtn:hover {
    background-color: #FFF5EB;
    border-color: #FB923C;
    border-bottom: 2.5px solid #F97316;
}

QPushButton#refreshBtn:pressed {
    background-color: #FFEDD5;
    border: 1px solid #EA580C;
    border-top: 2.5px solid #C2410C;
    border-bottom: 1px solid #FB923C;
    padding-top: 4px;
}

/* Uniform Input Controls - Raised 3D Bevel with Crisp Dimensions (32px) */
QComboBox {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.8 #FFFFFF, stop:1 #FFF7ED);
    border: 1px solid #FDBA74;
    border-top: 1px solid #FFE4CD;
    border-bottom: 2.5px solid #FB923C;
    border-radius: 4px;
    padding: 0px 10px;
    color: #1F2937;
    min-height: 32px;
    max-height: 32px;
    font-size: 13px;
}

QComboBox:hover {
    border-color: #FB923C;
    border-bottom: 2.5px solid #F97316;
    background-color: #FFFFFF;
}

QComboBox:focus {
    border: 1.5px solid #F97316;
    border-bottom: 2.5px solid #C2410C;
    background-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid #FCD3B0;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFEDD5);
}

QComboBox::drop-down:hover {
    background-color: #FFEDD5;
}

QComboBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #C2410C;
    margin-right: 2px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #FB923C;
    selection-background-color: #FFEDD5;
    selection-color: #9A3412;
    border-radius: 4px;
    padding: 4px;
}

QSpinBox {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.8 #FFFFFF, stop:1 #FFF7ED);
    border: 1px solid #FDBA74;
    border-top: 1px solid #FFE4CD;
    border-bottom: 2.5px solid #FB923C;
    border-radius: 4px;
    padding: 0px 8px;
    color: #1F2937;
    min-height: 32px;
    max-height: 32px;
    font-size: 13px;
}

QSpinBox:hover {
    border-color: #FB923C;
    border-bottom: 2.5px solid #F97316;
    background-color: #FFFFFF;
}

QSpinBox:focus {
    border: 1.5px solid #F97316;
    border-bottom: 2.5px solid #C2410C;
    background-color: #FFFFFF;
}

QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    height: 16px;
    border-left: 1px solid #FCD3B0;
    border-bottom: 1px solid #FCD3B0;
    border-top-right-radius: 4px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFEDD5);
}

QSpinBox::up-button:hover {
    background-color: #FFEDD5;
}

QSpinBox::up-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-bottom: 4px solid #C2410C;
}

QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    height: 16px;
    border-left: 1px solid #FCD3B0;
    border-bottom-right-radius: 4px;
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFEDD5);
}

QSpinBox::down-button:hover {
    background-color: #FFEDD5;
}

QSpinBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-top: 4px solid #C2410C;
}

QLineEdit {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.8 #FFFFFF, stop:1 #FFF7ED);
    border: 1px solid #FDBA74;
    border-top: 1px solid #FFE4CD;
    border-bottom: 2.5px solid #FB923C;
    border-radius: 4px;
    padding: 0px 10px;
    color: #1F2937;
    min-height: 32px;
    max-height: 32px;
    font-size: 13px;
}

QLineEdit:hover {
    border-color: #FB923C;
    border-bottom: 2.5px solid #F97316;
    background-color: #FFFFFF;
}

QLineEdit:focus {
    border: 1.5px solid #F97316;
    border-bottom: 2.5px solid #C2410C;
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
    background-color: #24201D;
    border-bottom: 1px solid #3E352F;
    border-radius: 0px;
    padding: 6px 12px;
}

QFrame#previewToolbar QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #38312C, stop:1 #27221E);
    border: 1px solid #443B35;
    border-top: 1px solid #544942;
    border-bottom: 2px solid #181513;
    color: #FFEDD5;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 500;
    min-height: 28px;
}

QFrame#previewToolbar QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FB923C, stop:1 #F97316);
    border-color: #F97316;
    border-bottom: 2px solid #C2410C;
    color: #000000;
    font-weight: 700;
}

QFrame#previewToolbar QPushButton:pressed {
    background-color: #EA580C;
    border-top: 2px solid #7C2D12;
    border-bottom: 1px solid #EA580C;
    padding-top: 5px;
    padding-bottom: 3px;
    color: #000000;
}

QFrame#previewToolbar QPushButton:disabled {
    background-color: #24201D;
    border: 1px solid #332B26;
    border-bottom: 1px solid #1F1B18;
    color: #78716C;
}

QFrame#previewToolbar QLabel {
    color: #FFEDD5;
    font-size: 12px;
    font-weight: 600;
}

/* Status Bar */
QStatusBar {
    background-color: #FFF5EB;
    color: #78716C;
    border-top: 1px solid #FED7AA;
    font-size: 12px;
}

/* Splitter Handle - Flat line */
QSplitter::handle {
    background-color: #FED7AA;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #FB923C;
}

/* Drag and Drop Zone - Boxy Modern */
#dropZone {
    background-color: #FFFBF7;
    border: 2px dashed #FB923C;
    border-radius: 4px;
    margin: 40px;
}

#dropZone:hover {
    background-color: #FFF5EB;
    border-color: #F97316;
}
"""
