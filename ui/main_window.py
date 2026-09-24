"""
Main Application Window for MacPrint.
Provides Drag & Drop file opening, Splitter layout, status bar, and printing workflows.
"""
import os
import tempfile
import shutil
from typing import Optional

from ui.qt_compat import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QSplitter, QFileDialog, QMessageBox, QStatusBar,
    QProgressBar, QAction, QKeySequence, Qt, Signal, Slot
)
from ui.theme import STYLESHEET
from ui.preview_canvas import PreviewCanvas
from ui.settings_panel import SettingsPanel
from core.document_engine import DocumentEngine, PrintJobSettings
from core.universal_printer import UniversalPrinterManager
from core.office_converter import is_office_file


class DropZoneWidget(QWidget):
    """Initial landing page with Drag & Drop support."""
    file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QWidget()
        frame.setObjectName("dropZone")
        f_layout = QVBoxLayout(frame)
        f_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.setContentsMargins(40, 60, 40, 60)
        f_layout.setSpacing(16)

        icon_label = QLabel("🖨️")
        icon_label.setStyleSheet("font-size: 56px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(icon_label)

        title = QLabel("Kéo và thả tệp vào đây để in")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #831843;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(title)

        subtitle = QLabel("Hỗ trợ PDF, Word, Excel, PowerPoint, hình ảnh (PNG, JPG, WEBP, TIFF, BMP), văn bản (TXT, CSV, MD...)")
        subtitle.setStyleSheet("font-size: 13px; color: #9D174D;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(subtitle)

        f_layout.addSpacing(12)

        self.choose_btn = QPushButton("📂  Chọn tệp từ máy...")
        self.choose_btn.setStyleSheet("""
            QPushButton {
                background-color: #F472B6; color: #FFFFFF; font-weight: 600;
                padding: 10px 24px; border-radius: 8px; font-size: 14px;
                border: 1px solid #F472B6;
            }
            QPushButton:hover {
                background-color: #EC4899;
                border-color: #EC4899;
            }
            QPushButton:pressed {
                background-color: #DB2777;
            }
        """)
        self.choose_btn.clicked.connect(self._browse_file)
        f_layout.addWidget(self.choose_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(frame)

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn tệp cần in",
            "",
            "Tất cả tệp hỗ trợ (*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt *.png *.jpg *.jpeg *.webp *.bmp *.tiff *.txt *.log *.csv *.md);;Tài liệu Office (*.docx *.doc *.xlsx *.xls *.pptx *.ppt);;PDF (*.pdf);;Hình ảnh (*.png *.jpg *.jpeg *.webp *.bmp *.tiff);;Văn bản (*.txt *.log *.csv *.md);;Tất cả (*.*)"
        )
        if file_path:
            self.file_selected.emit(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.exists(path):
                self.file_selected.emit(path)


class MainWindow(QMainWindow):
    def __init__(self, initial_file: Optional[str] = None):
        super().__init__()
        self.setWindowTitle("PrintMaster - Xem trước & In ấn chuyên nghiệp (Windows & Mac)")
        self.resize(1150, 800)
        self.setMinimumSize(850, 600)
        self.setStyleSheet(STYLESHEET)

        self.doc_engine = DocumentEngine()
        self.current_file_path: Optional[str] = None

        self.init_ui()
        self.init_menu()

        if initial_file and os.path.exists(initial_file):
            self.open_file(initial_file)

    def init_ui(self):
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 0. Welcome / Drop Zone
        self.drop_zone = DropZoneWidget(self)
        self.drop_zone.file_selected.connect(self.open_file)
        self.stack.addWidget(self.drop_zone)

        # 1. Preview & Settings Splitter View
        preview_container = QWidget()
        pc_layout = QVBoxLayout(preview_container)
        pc_layout.setContentsMargins(0, 0, 0, 0)
        pc_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: Preview Canvas
        self.preview_canvas = PreviewCanvas(self.doc_engine, self)
        self.splitter.addWidget(self.preview_canvas)

        # Right: Settings Panel
        self.settings_panel = SettingsPanel(self)
        self.settings_panel.setMinimumWidth(320)
        self.settings_panel.settings_changed.connect(self._on_settings_changed)
        self.settings_panel.print_requested.connect(self._on_print_requested)
        self.settings_panel.cancel_requested.connect(self._on_cancel)
        self.splitter.addWidget(self.settings_panel)

        # Set ratio: 6:4 (60% preview, 40% settings)
        self.splitter.setStretchFactor(0, 6)
        self.splitter.setStretchFactor(1, 4)
        self.splitter.setSizes([690, 460])

        pc_layout.addWidget(self.splitter)
        self.stack.addWidget(preview_container)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sẵn sàng. Kéo thả tệp hoặc bấm 'Chọn tệp' để bắt đầu.")

    def init_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("Tệp (File)")
        
        open_action = QAction("Mở tệp khác...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._browse_open_file)
        file_menu.addAction(open_action)

        save_pdf_action = QAction("Lưu dưới dạng PDF...", self)
        save_pdf_action.setShortcut(QKeySequence.StandardKey.Save)
        save_pdf_action.triggered.connect(self._save_as_pdf)
        file_menu.addAction(save_pdf_action)

        file_menu.addSeparator()

        print_action = QAction("In ấn (Print)", self)
        print_action.setShortcut(QKeySequence.StandardKey.Print)
        print_action.triggered.connect(self._on_print_requested)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        quit_action = QAction("Thoát", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # View Menu
        view_menu = menubar.addMenu("Xem (View)")
        
        fit_page_act = QAction("Vừa toàn bộ trang", self)
        fit_page_act.triggered.connect(self.preview_canvas.set_fit_page)
        view_menu.addAction(fit_page_act)

        fit_width_act = QAction("Vừa chiều rộng", self)
        fit_width_act.triggered.connect(self.preview_canvas.set_fit_width)
        view_menu.addAction(fit_width_act)

        view_menu.addSeparator()

        zoom_in_act = QAction("Phóng to (+)", self)
        zoom_in_act.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_act.triggered.connect(self.preview_canvas.zoom_in)
        view_menu.addAction(zoom_in_act)

        zoom_out_act = QAction("Thu nhỏ (-)", self)
        zoom_out_act.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_act.triggered.connect(self.preview_canvas.zoom_out)
        view_menu.addAction(zoom_out_act)

    def _browse_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn tệp cần in",
            "",
            "Tất cả tệp hỗ trợ (*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt *.png *.jpg *.jpeg *.webp *.bmp *.tiff *.txt *.log *.csv *.md);;Tài liệu Office (*.docx *.doc *.xlsx *.xls *.pptx *.ppt);;PDF (*.pdf);;Hình ảnh (*.png *.jpg *.jpeg *.webp *.bmp *.tiff);;Văn bản (*.txt *.log *.csv *.md);;Tất cả (*.*)"
        )
        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path: str):
        is_office = is_office_file(file_path)
        if is_office:
            self.status_bar.showMessage("Đang chuẩn bị và chuyển đổi tài liệu Office sang định dạng in...")
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            QApplication.processEvents()

        try:
            success, msg = self.doc_engine.load_file(file_path)
        finally:
            if is_office:
                QApplication.restoreOverrideCursor()

        if not success:
            QMessageBox.critical(self, "Lỗi mở tệp", msg)
            self.status_bar.showMessage("Lỗi mở tệp.")
            return

        self.current_file_path = file_path
        file_name = os.path.basename(file_path)
        self.setWindowTitle(f"PrintMaster - {file_name}")

        self.stack.setCurrentIndex(1)
        self.status_bar.showMessage(f"Đã mở: {file_name} ({self.doc_engine.total_source_pages} trang)")

        # Automatically match document orientation and standard paper size
        self.settings_panel.sync_with_document(self.doc_engine)

        # Ensure exact 6:4 ratio when opening a document
        self._apply_splitter_ratio()

        # Trigger initial preview render
        self._on_settings_changed()

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_splitter_ratio()

    def _apply_splitter_ratio(self):
        total_w = self.splitter.width()
        if total_w > 100:
            w_preview = int(total_w * 0.6)
            w_settings = total_w - w_preview
            self.splitter.setSizes([w_preview, w_settings])

    def _on_settings_changed(self):
        settings = self.settings_panel.get_settings()
        self.preview_canvas.update_view(settings)

    def _on_print_requested(self):
        if not self.doc_engine.is_loaded():
            QMessageBox.warning(self, "Chưa chọn tệp", "Vui lòng mở một tệp trước khi in.")
            return

        settings = self.settings_panel.get_settings()

        if settings.printer_name == UniversalPrinterManager.SAVE_AS_PDF_NAME:
            self._save_as_pdf()
            return

        # Prepare print output
        self.status_bar.showMessage(f"Đang chuẩn bị trang in cho '{settings.printer_name}'...")

        # Create temporary prepared PDF
        with tempfile.NamedTemporaryFile(suffix="_print_job.pdf", delete=False) as tmp_file:
            temp_pdf_path = tmp_file.name

        try:
            ok, gen_msg = self.doc_engine.generate_prepared_pdf(settings, temp_pdf_path)
            if not ok:
                QMessageBox.critical(self, "Lỗi chuẩn bị tệp in", gen_msg)
                return

            # Send to printer via UniversalPrinterManager (CUPS on Mac, Qt Spooler on Windows)
            success, print_msg = UniversalPrinterManager.print_file(
                file_path=temp_pdf_path,
                printer_name=settings.printer_name,
                copies=settings.copies,
                paper_size=settings.paper_size,
                duplex_mode=settings.duplex_mode,
                orientation=settings.orientation,
                collate=settings.collate,
                color_mode=settings.color_mode
            )

            if success:
                self.status_bar.showMessage(f"In thành công: {settings.printer_name}")
                QMessageBox.information(
                    self,
                    "Lệnh in thành công",
                    f"Đã gửi lệnh in thành công tới máy in:\n\n{settings.printer_name}\n\nSố bản sao: {settings.copies}"
                )
            else:
                self.status_bar.showMessage("Lỗi gửi lệnh in.")
                QMessageBox.critical(self, "Lỗi khi in", print_msg)
        finally:
            if os.path.exists(temp_pdf_path):
                try:
                    os.remove(temp_pdf_path)
                except Exception:
                    pass

    def _save_as_pdf(self):
        if not self.doc_engine.is_loaded():
            QMessageBox.warning(self, "Chưa chọn tệp", "Vui lòng mở một tệp trước khi lưu.")
            return

        default_name = "TaiLieuIn.pdf"
        if self.current_file_path:
            base = os.path.splitext(os.path.basename(self.current_file_path))[0]
            default_name = f"{base}_printed.pdf"

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu tệp PDF",
            default_name,
            "Tài liệu PDF (*.pdf)"
        )

        if not save_path:
            return

        settings = self.settings_panel.get_settings()
        self.status_bar.showMessage("Đang xuất tệp PDF...")

        ok, msg = self.doc_engine.generate_prepared_pdf(settings, save_path)
        if ok:
            self.status_bar.showMessage(f"Đã lưu tệp PDF: {save_path}")
            QMessageBox.information(self, "Lưu thành công", f"Tệp PDF đã được tạo thành công tại:\n{save_path}")
        else:
            self.status_bar.showMessage("Lỗi xuất tệp PDF.")
            QMessageBox.critical(self, "Lỗi lưu PDF", msg)

    def _on_cancel(self):
        # Return to drop zone or close
        if self.doc_engine.is_loaded():
            res = QMessageBox.question(
                self,
                "Đóng tệp hiện tại",
                "Bạn có muốn đóng tệp hiện tại và chọn tệp khác không?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if res == QMessageBox.StandardButton.Yes:
                self.doc_engine.close()
                self.current_file_path = None
                self.stack.setCurrentIndex(0)
                self.setWindowTitle("PrintMaster - Xem trước & In ấn chuyên nghiệp (Windows & Mac)")
                self.status_bar.showMessage("Sẵn sàng. Kéo thả tệp hoặc bấm 'Chọn tệp' để bắt đầu.")
        else:
            self.close()

    def closeEvent(self, event):
        self.doc_engine.close()
        event.accept()
