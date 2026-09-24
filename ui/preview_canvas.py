"""
Interactive Preview Canvas widget with Zoom, Pan, High-DPI support,
mouse-wheel page scrolling, and boxy crisp paper rendering.
"""
from typing import Optional
from ui.qt_compat import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider,
    QScrollArea, QFrame, QPixmap, QPainter, QColor, QRect, QPoint,
    Qt, Signal, Slot, QSizePolicy
)
from core.document_engine import DocumentEngine, PrintJobSettings


class SheetDisplayWidget(QWidget):
    """Inner widget that paints the paper sheet with sharp rectangular shadow."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap: Optional[QPixmap] = None
        self.logical_w: int = 0
        self.logical_h: int = 0
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)

    def set_sheet(self, pixmap: Optional[QPixmap], logical_w: int, logical_h: int):
        self.pixmap = pixmap
        self.logical_w = logical_w
        self.logical_h = logical_h
        if pixmap and logical_w > 0 and logical_h > 0:
            self.setFixedSize(logical_w + 40, logical_h + 40)
        else:
            self.setFixedSize(400, 500)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Fill neutral boxy canvas background
        painter.fillRect(self.rect(), QColor("#2D2430"))

        if self.pixmap is None or self.pixmap.isNull() or self.logical_w <= 0:
            painter.setPen(QColor("#FBCFE8"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Không có nội dung xem trước")
            return

        # Center sheet on canvas with padding
        x = (self.width() - self.logical_w) // 2
        y = (self.height() - self.logical_h) // 2

        # Draw crisp, boxy drop shadow
        shadow_rect = QRect(x + 4, y + 4, self.logical_w, self.logical_h)
        painter.fillRect(shadow_rect, QColor(10, 8, 12, 170))

        # Smooth high-definition downscaling of the high-res pixmap to the logical paper rect
        target_rect = QRect(x, y, self.logical_w, self.logical_h)
        painter.drawPixmap(target_rect, self.pixmap)


class PreviewScrollArea(QScrollArea):
    """
    Scroll area providing smooth vertical mouse-wheel scrolling,
    page flip when scrolling past sheet boundary, and Ctrl+Wheel zooming.
    """
    def __init__(self, preview_canvas, parent=None):
        super().__init__(parent)
        self.preview_canvas = preview_canvas
        self._wheel_accum = 0

    def wheelEvent(self, event):
        # 1. Ctrl (Win) or Cmd (Mac) + Wheel/Trackpad => Zoom in / out
        is_zoom_mod = bool(event.modifiers() & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier))
        delta = event.pixelDelta().y() if not event.pixelDelta().isNull() else event.angleDelta().y()

        if is_zoom_mod:
            if delta > 0:
                self.preview_canvas.zoom_in()
            elif delta < 0:
                self.preview_canvas.zoom_out()
            event.accept()
            return

        vbar = self.verticalScrollBar()

        # If scrollable vertically (e.g. zoomed in or page taller than viewport)
        can_scroll_down = vbar.value() < vbar.maximum()
        can_scroll_up = vbar.value() > vbar.minimum()

        if delta < 0 and can_scroll_down:
            super().wheelEvent(event)
            self._wheel_accum = 0
            return
        elif delta > 0 and can_scroll_up:
            super().wheelEvent(event)
            self._wheel_accum = 0
            return

        # If entire page fits or reached boundary, wheel/trackpad flips page
        self._wheel_accum += delta
        threshold = 60 if not event.pixelDelta().isNull() else 80
        if self._wheel_accum <= -threshold:
            self._wheel_accum = 0
            if self.preview_canvas.current_sheet < self.preview_canvas.total_sheets - 1:
                self.preview_canvas.go_next()
                vbar.setValue(vbar.minimum())
        elif self._wheel_accum >= threshold:
            self._wheel_accum = 0
            if self.preview_canvas.current_sheet > 0:
                self.preview_canvas.go_prev()
                vbar.setValue(vbar.maximum())

        event.accept()


class PreviewCanvas(QWidget):
    """Preview container with clean boxy layout, zoom and header navigation."""
    page_changed = Signal(int)

    def __init__(self, doc_engine: DocumentEngine, parent=None):
        super().__init__(parent)
        self.doc_engine = doc_engine
        self.current_sheet: int = 0
        self.total_sheets: int = 0
        self.zoom_factor: float = 1.0
        self.fit_mode: str = "fit_page"  # "fit_page", "fit_width", "manual"
        self._current_settings: Optional[PrintJobSettings] = None

        self.init_ui()

    def init_ui(self):
        self.setObjectName("previewArea")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Zoom & Navigation Header Toolbar
        self.top_toolbar = QFrame(self)
        self.top_toolbar.setObjectName("previewToolbar")
        tb_layout = QHBoxLayout(self.top_toolbar)
        tb_layout.setContentsMargins(12, 6, 12, 6)
        tb_layout.setSpacing(8)

        self.fit_page_btn = QPushButton("⊡ Vừa trang")
        self.fit_page_btn.setToolTip("Thu phóng vừa toàn bộ trang")
        self.fit_page_btn.clicked.connect(self.set_fit_page)
        tb_layout.addWidget(self.fit_page_btn)

        self.fit_width_btn = QPushButton("↔ Vừa chiều rộng")
        self.fit_width_btn.setToolTip("Thu phóng vừa chiều rộng khung xem")
        self.fit_width_btn.clicked.connect(self.set_fit_width)
        tb_layout.addWidget(self.fit_width_btn)

        tb_layout.addSpacing(12)

        self.zoom_out_btn = QPushButton("－")
        self.zoom_out_btn.setToolTip("Thu nhỏ (Ctrl -)")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        tb_layout.addWidget(self.zoom_out_btn)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet("color: #FCE7F3; font-weight: 600; min-width: 45px;")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tb_layout.addWidget(self.zoom_label)

        self.zoom_in_btn = QPushButton("＋")
        self.zoom_in_btn.setToolTip("Phóng to (Ctrl +)")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        tb_layout.addWidget(self.zoom_in_btn)

        tb_layout.addStretch()

        # Sheet Navigation kept in header toolbar
        self.first_btn = QPushButton("|<")
        self.first_btn.setToolTip("Tờ đầu tiên")
        self.first_btn.clicked.connect(self.go_first)
        tb_layout.addWidget(self.first_btn)

        self.prev_btn = QPushButton(" < ")
        self.prev_btn.setToolTip("Tờ trước (hoặc cuộn chuột lên)")
        self.prev_btn.clicked.connect(self.go_prev)
        tb_layout.addWidget(self.prev_btn)

        self.page_indicator = QLabel("Tờ 1 / 1")
        self.page_indicator.setStyleSheet("color: #FCE7F3; font-weight: 600; margin: 0 8px;")
        tb_layout.addWidget(self.page_indicator)

        self.next_btn = QPushButton(" > ")
        self.next_btn.setToolTip("Tờ tiếp theo (hoặc cuộn chuột xuống)")
        self.next_btn.clicked.connect(self.go_next)
        tb_layout.addWidget(self.next_btn)

        self.last_btn = QPushButton(">|")
        self.last_btn.setToolTip("Tờ cuối cùng")
        self.last_btn.clicked.connect(self.go_last)
        tb_layout.addWidget(self.last_btn)

        main_layout.addWidget(self.top_toolbar)

        # Scroll Area for Sheet Rendering with Mouse Wheel Support
        self.scroll_area = PreviewScrollArea(self, self)
        self.scroll_area.setObjectName("previewScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sheet_display = SheetDisplayWidget(self.scroll_area)
        self.scroll_area.setWidget(self.sheet_display)

        main_layout.addWidget(self.scroll_area)

    def update_view(self, settings: PrintJobSettings):
        self._current_settings = settings
        if not self.doc_engine.is_loaded():
            self.sheet_display.set_sheet(None, 0, 0)
            self.page_indicator.setText("Tờ 0 / 0")
            return

        self.total_sheets = self.doc_engine.get_sheet_count(settings, self.current_sheet + 1)
        if self.total_sheets == 0:
            self.sheet_display.set_sheet(None, 0, 0)
            self.page_indicator.setText("Tờ 0 / 0")
            return

        if self.current_sheet >= self.total_sheets:
            self.current_sheet = max(0, self.total_sheets - 1)

        self._apply_auto_zoom_if_needed()
        self.render_current_sheet()
        self._update_navigation_buttons()

    def _apply_auto_zoom_if_needed(self):
        if not self._current_settings or not self.doc_engine.is_loaded():
            return

        paper_sizes = {
            "A4": (595.0, 842.0),
            "Letter": (612.0, 792.0),
            "Legal": (612.0, 1008.0),
            "A3": (842.0, 1191.0),
            "A5": (420.0, 595.0),
            "B5": (499.0, 709.0),
            "4x6": (288.0, 432.0),
        }
        base_w, base_h = paper_sizes.get(self._current_settings.paper_size, (595.0, 842.0))
        if self._current_settings.orientation == "landscape":
            sheet_w, sheet_h = max(base_w, base_h), min(base_w, base_h)
        else:
            sheet_w, sheet_h = min(base_w, base_h), max(base_w, base_h)

        vp_w = max(200, self.scroll_area.viewport().width() - 40)
        vp_h = max(200, self.scroll_area.viewport().height() - 40)

        if self.fit_mode == "fit_page":
            scale_w = vp_w / sheet_w
            scale_h = vp_h / sheet_h
            self.zoom_factor = round(min(scale_w, scale_h), 2)
        elif self.fit_mode == "fit_width":
            self.zoom_factor = round(vp_w / sheet_w, 2)

        self.zoom_factor = max(0.2, min(4.0, self.zoom_factor))
        self.zoom_label.setText(f"{int(self.zoom_factor * 100)}%")

    def render_current_sheet(self):
        if not self._current_settings or not self.doc_engine.is_loaded():
            return

        pixmap, logical_w, logical_h = self.doc_engine.render_preview_sheet(
            sheet_index=self.current_sheet,
            settings=self._current_settings,
            zoom=self.zoom_factor,
            current_view_page=self.current_sheet + 1
        )
        self.sheet_display.set_sheet(pixmap, logical_w, logical_h)
        self.page_indicator.setText(f"Tờ {self.current_sheet + 1} / {max(1, self.total_sheets)}")

    def _update_navigation_buttons(self):
        has_multiple = self.total_sheets > 1
        self.first_btn.setEnabled(has_multiple and self.current_sheet > 0)
        self.prev_btn.setEnabled(has_multiple and self.current_sheet > 0)
        self.next_btn.setEnabled(has_multiple and self.current_sheet < self.total_sheets - 1)
        self.last_btn.setEnabled(has_multiple and self.current_sheet < self.total_sheets - 1)

    def go_first(self):
        if self.current_sheet != 0:
            self.current_sheet = 0
            self.render_current_sheet()
            self._update_navigation_buttons()
            self.page_changed.emit(self.current_sheet + 1)

    def go_prev(self):
        if self.current_sheet > 0:
            self.current_sheet -= 1
            self.render_current_sheet()
            self._update_navigation_buttons()
            self.page_changed.emit(self.current_sheet + 1)

    def go_next(self):
        if self.current_sheet < self.total_sheets - 1:
            self.current_sheet += 1
            self.render_current_sheet()
            self._update_navigation_buttons()
            self.page_changed.emit(self.current_sheet + 1)

    def go_last(self):
        if self.current_sheet < self.total_sheets - 1:
            self.current_sheet = self.total_sheets - 1
            self.render_current_sheet()
            self._update_navigation_buttons()
            self.page_changed.emit(self.current_sheet + 1)

    def zoom_in(self):
        self.fit_mode = "manual"
        self.zoom_factor = min(4.0, round(self.zoom_factor + 0.15, 2))
        self.zoom_label.setText(f"{int(self.zoom_factor * 100)}%")
        self.render_current_sheet()

    def zoom_out(self):
        self.fit_mode = "manual"
        self.zoom_factor = max(0.2, round(self.zoom_factor - 0.15, 2))
        self.zoom_label.setText(f"{int(self.zoom_factor * 100)}%")
        self.render_current_sheet()

    def set_fit_page(self):
        self.fit_mode = "fit_page"
        self._apply_auto_zoom_if_needed()
        self.render_current_sheet()

    def set_fit_width(self):
        self.fit_mode = "fit_width"
        self._apply_auto_zoom_if_needed()
        self.render_current_sheet()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.fit_mode in ("fit_page", "fit_width"):
            self._apply_auto_zoom_if_needed()
            self.render_current_sheet()
