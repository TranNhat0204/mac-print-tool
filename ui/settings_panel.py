"""
Windows-style Print Settings Panel for macOS and Windows.
Matches Windows Print Preview dialog options with No-Scroll-Wheel Protection.
"""
from typing import List
from ui.qt_compat import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QRadioButton, QButtonGroup, QCheckBox, QLineEdit,
    QScrollArea, QFrame, Signal, Slot, Qt, QSizePolicy, QtCore,
    QGraphicsDropShadowEffect, QColor
)
from core.document_engine import PrintJobSettings
from core.universal_printer import UniversalPrinterManager, PrinterInfo


class NoScrollWheelFilter(QtCore.QObject):
    """
    Prevents mouse wheel from unintentionally changing combobox or spinbox values.
    Forwards the scroll event to the parent scroll area so the panel scrolls smoothly.
    """
    def __init__(self, scroll_widget=None, parent=None):
        super().__init__(parent)
        self.scroll_widget = scroll_widget

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.Wheel:
            if self.scroll_widget:
                # Forward to parent scroll area
                self.scroll_widget.wheelEvent(event)
            return True
        return super().eventFilter(obj, event)


def _add_drop_shadow(widget: QWidget, blur: int = 8, y_offset: int = 2, color_tuple=(190, 110, 50, 40)):
    """Applies a soft cross-platform drop shadow effect to a widget."""
    try:
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, y_offset)
        r, g, b, a = color_tuple
        shadow.setColor(QColor(r, g, b, a))
        widget.setGraphicsEffect(shadow)
    except Exception:
        pass


class SettingsPanel(QWidget):
    """Sidebar providing all standard Windows print options."""
    settings_changed = Signal()
    print_requested = Signal()
    cancel_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPanel")
        self.printers: List[PrinterInfo] = []
        self._block_signals = False

        self.init_ui()
        self.reload_printers()

    def init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Scroll Area for all settings
        scroll = QScrollArea(self)
        scroll.setObjectName("settingsScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Mouse wheel filter to protect inputs from accidental scroll changes
        self.no_wheel_filter = NoScrollWheelFilter(scroll, self)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header Title
        title_label = QLabel("Tùy chọn in ấn")
        title_label.setObjectName("dialogTitle")
        subtitle_label = QLabel("Xem trước và thiết lập thông số trang in")
        subtitle_label.setObjectName("dialogSubtitle")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(6)

        # 1. PRINTER SELECTION CARD
        layout.addWidget(self._create_section_label("MÁY IN (DESTINATION)"))
        p_card = QFrame()
        p_card.setProperty("class", "settingCard")
        p_layout = QVBoxLayout(p_card)
        p_layout.setContentsMargins(12, 12, 12, 12)
        p_layout.setSpacing(8)

        p_row = QHBoxLayout()
        p_row.setContentsMargins(0, 0, 0, 0)
        p_row.setSpacing(8)
        p_lbl = QLabel("Máy in đích:")
        p_lbl.setFixedWidth(110)
        p_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        p_lbl.setStyleSheet("font-weight: 600; color: #374151; font-size: 13px;")
        p_row.addWidget(p_lbl)

        self.printer_combo = QComboBox()
        self.printer_combo.currentIndexChanged.connect(self._on_printer_changed)
        p_row.addWidget(self.printer_combo, 1)

        self.refresh_printers_btn = QPushButton("⟳")
        self.refresh_printers_btn.setObjectName("refreshBtn")
        self.refresh_printers_btn.setToolTip("Làm mới danh sách máy in")
        self.refresh_printers_btn.setFixedSize(34, 32)
        self.refresh_printers_btn.clicked.connect(self.reload_printers)
        p_row.addWidget(self.refresh_printers_btn)
        p_layout.addLayout(p_row)

        self.printer_status_label = QLabel("Trạng thái: Sẵn sàng")
        self.printer_status_label.setStyleSheet("color: #C2410C; font-size: 11.5px; margin-left: 118px;")
        p_layout.addWidget(self.printer_status_label)
        layout.addWidget(p_card)

        # 2. COPIES CARD
        layout.addWidget(self._create_section_label("BẢN SAO (COPIES)"))
        c_card = QFrame()
        c_card.setProperty("class", "settingCard")
        c_layout = QVBoxLayout(c_card)
        c_layout.setContentsMargins(12, 12, 12, 12)
        c_layout.setSpacing(8)

        self.copies_spin = QSpinBox()
        self.copies_spin.setRange(1, 999)
        self.copies_spin.setValue(1)
        self.copies_spin.valueChanged.connect(self._on_change)
        c_layout.addLayout(self._create_form_row("Số lượng bản in:", self.copies_spin))

        self.collate_check = QCheckBox("In theo bộ (Collate: 1, 2, 3...)")
        self.collate_check.setChecked(True)
        self.collate_check.setStyleSheet("margin-left: 118px; font-size: 12.5px; color: #4B5563;")
        self.collate_check.stateChanged.connect(self._on_change)
        c_layout.addWidget(self.collate_check)
        layout.addWidget(c_card)

        # 3. PAGES RANGE CARD
        layout.addWidget(self._create_section_label("TRANG IN (PAGES)"))
        pg_card = QFrame()
        pg_card.setProperty("class", "settingCard")
        pg_layout = QVBoxLayout(pg_card)
        pg_layout.setContentsMargins(12, 12, 12, 12)
        pg_layout.setSpacing(8)

        self.range_btn_group = QButtonGroup(self)
        self.radio_all = QRadioButton("Tất cả các trang")
        self.radio_all.setChecked(True)
        self.range_btn_group.addButton(self.radio_all)
        pg_layout.addWidget(self.radio_all)

        self.radio_current = QRadioButton("Chỉ trang hiện tại")
        self.range_btn_group.addButton(self.radio_current)
        pg_layout.addWidget(self.radio_current)

        self.radio_custom = QRadioButton("Tùy chỉnh phạm vi trang")
        self.range_btn_group.addButton(self.radio_custom)
        pg_layout.addWidget(self.radio_custom)

        self.custom_range_edit = QLineEdit()
        self.custom_range_edit.setPlaceholderText("Ví dụ: 1-5, 8, 11-13")
        self.custom_range_edit.setEnabled(False)
        self.custom_range_edit.textChanged.connect(self._on_change)
        pg_layout.addLayout(self._create_form_row("Phạm vi trang:", self.custom_range_edit))

        self.radio_all.toggled.connect(self._on_range_mode_changed)
        self.radio_current.toggled.connect(self._on_range_mode_changed)
        self.radio_custom.toggled.connect(self._on_range_mode_changed)

        self.subset_combo = QComboBox()
        self.subset_combo.addItem("Tất cả các trang trong phạm vi", "all")
        self.subset_combo.addItem("Chỉ in trang lẻ (Odd pages)", "odd")
        self.subset_combo.addItem("Chỉ in trang chẵn (Even pages)", "even")
        self.subset_combo.currentIndexChanged.connect(self._on_change)
        pg_layout.addLayout(self._create_form_row("Tập hợp:", self.subset_combo))

        layout.addWidget(pg_card)

        # 4. COLOR MODE CARD
        layout.addWidget(self._create_section_label("CHẾ ĐỘ MÀU (COLOR)"))
        color_card = QFrame()
        color_card.setProperty("class", "settingCard")
        clr_layout = QVBoxLayout(color_card)
        clr_layout.setContentsMargins(12, 12, 12, 12)
        clr_layout.setSpacing(8)

        self.color_combo = QComboBox()
        self.color_combo.addItem("🌈 Màu sắc (Color)", "color")
        self.color_combo.addItem("⬛ Đen trắng / Mức xám (Grayscale / B&W)", "grayscale")
        self.color_combo.currentIndexChanged.connect(self._on_change)
        clr_layout.addLayout(self._create_form_row("Chế độ màu:", self.color_combo))

        layout.addWidget(color_card)

        # 5. ORIENTATION & PAPER SIZE CARD
        layout.addWidget(self._create_section_label("BỐ CỤC & KHỔ GIẤY (LAYOUT & PAPER)"))
        layout_card = QFrame()
        layout_card.setProperty("class", "settingCard")
        l_layout = QVBoxLayout(layout_card)
        l_layout.setContentsMargins(12, 12, 12, 12)
        l_layout.setSpacing(8)

        self.orient_combo = QComboBox()
        self.orient_combo.addItem("📄 Khổ dọc (Portrait)", "portrait")
        self.orient_combo.addItem("📑 Khổ ngang (Landscape)", "landscape")
        self.orient_combo.currentIndexChanged.connect(self._on_change)
        l_layout.addLayout(self._create_form_row("Hướng giấy:", self.orient_combo))

        self.paper_combo = QComboBox()
        self.paper_combo.addItem("A4 (210 x 297 mm)", "A4")
        self.paper_combo.addItem("Letter (8.5 x 11 inch)", "Letter")
        self.paper_combo.addItem("Legal (8.5 x 14 inch)", "Legal")
        self.paper_combo.addItem("A3 (297 x 420 mm)", "A3")
        self.paper_combo.addItem("A5 (148 x 210 mm)", "A5")
        self.paper_combo.addItem("B5 (176 x 250 mm)", "B5")
        self.paper_combo.addItem("4 x 6 Photo (Ảnh)", "4x6")
        self.paper_combo.currentIndexChanged.connect(self._on_change)
        l_layout.addLayout(self._create_form_row("Khổ giấy:", self.paper_combo))

        self.duplex_combo = QComboBox()
        self.duplex_combo.addItem("In một mặt (1-sided)", "one-sided")
        self.duplex_combo.addItem("In 2 mặt - Lật cạnh dài (Duplex long-edge)", "two-sided-long-edge")
        self.duplex_combo.addItem("In 2 mặt - Lật cạnh ngắn (Duplex short-edge)", "two-sided-short-edge")
        self.duplex_combo.currentIndexChanged.connect(self._on_change)
        l_layout.addLayout(self._create_form_row("In 2 mặt:", self.duplex_combo))

        layout.addWidget(layout_card)

        # 6. SCALE & N-UP CARD
        layout.addWidget(self._create_section_label("THU PHÓNG & BỐ CỤC N-UP"))
        scale_card = QFrame()
        scale_card.setProperty("class", "settingCard")
        s_layout = QVBoxLayout(scale_card)
        s_layout.setContentsMargins(12, 12, 12, 12)
        s_layout.setSpacing(8)

        self.scale_combo = QComboBox()
        self.scale_combo.addItem("Vừa khổ giấy (Fit to Paper)", "fit")
        self.scale_combo.addItem("Tràn toàn bộ mặt giấy (Fill Page)", "fill")
        self.scale_combo.addItem("Kích thước gốc 100% (Actual)", "actual")
        self.scale_combo.addItem("Tùy chỉnh tỉ lệ % (Custom)", "custom")
        self.scale_combo.currentIndexChanged.connect(self._on_scale_combo_changed)
        s_layout.addLayout(self._create_form_row("Thu phóng:", self.scale_combo))

        self.custom_scale_container = QWidget()
        custom_layout = QVBoxLayout(self.custom_scale_container)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        self.scale_percent_spin = QSpinBox()
        self.scale_percent_spin.setRange(20, 300)
        self.scale_percent_spin.setValue(100)
        self.scale_percent_spin.setSingleStep(5)
        self.scale_percent_spin.setSuffix(" %")
        self.scale_percent_spin.valueChanged.connect(self._on_change)
        custom_layout.addLayout(self._create_form_row("Tỉ lệ (%):", self.scale_percent_spin))
        self.custom_scale_container.setVisible(False)
        s_layout.addWidget(self.custom_scale_container)

        self.nup_combo = QComboBox()
        self.nup_combo.addItem("1 trang trên mỗi tờ", 1)
        self.nup_combo.addItem("2 trang trên mỗi tờ (2-up)", 2)
        self.nup_combo.addItem("4 trang trên mỗi tờ (4-up)", 4)
        self.nup_combo.addItem("6 trang trên mỗi tờ (6-up)", 6)
        self.nup_combo.addItem("9 trang trên mỗi tờ (9-up)", 9)
        self.nup_combo.addItem("16 trang trên mỗi tờ (16-up)", 16)
        self.nup_combo.currentIndexChanged.connect(self._on_change)
        s_layout.addLayout(self._create_form_row("Số trang / tờ:", self.nup_combo))

        self.margin_combo = QComboBox()
        self.margin_combo.addItem("Mặc định (Khớp 100% khổ giấy)", "default")
        self.margin_combo.addItem("Không lề (None)", "none")
        self.margin_combo.addItem("Tối thiểu (Minimum - 3mm)", "minimum")
        self.margin_combo.currentIndexChanged.connect(self._on_change)
        s_layout.addLayout(self._create_form_row("Lề trang:", self.margin_combo))

        layout.addWidget(scale_card)

        # APPLY DROP SHADOWS FOR FLOATING CARDS & TACTILE BUTTONS
        for card in [p_card, c_card, pg_card, color_card, layout_card, scale_card]:
            _add_drop_shadow(card, blur=10, y_offset=2, color_tuple=(219, 39, 119, 35))

        # INSTALL NO-WHEEL FILTER ON ALL CONTROLS & CONFIGURE AUTO-ELIDE
        # Prevents wheel scroll from accidentally changing values
        for widget in [
            self.printer_combo, self.copies_spin, self.subset_combo,
            self.color_combo, self.orient_combo, self.paper_combo,
            self.duplex_combo, self.scale_combo, self.scale_percent_spin,
            self.nup_combo, self.margin_combo
        ]:
            widget.installEventFilter(self.no_wheel_filter)
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            if isinstance(widget, QComboBox):
                widget.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
                widget.setMinimumContentsLength(8)

        layout.addStretch()
        scroll.setWidget(content)
        root_layout.addWidget(scroll, 1)

        # BOTTOM ACTION BAR
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("background-color: #FFF0F4; border-top: 1px solid #FCE7F0;")
        b_layout = QHBoxLayout(bottom_bar)
        b_layout.setContentsMargins(16, 12, 16, 12)
        b_layout.setSpacing(12)

        self.cancel_btn = QPushButton("Hủy bỏ")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)
        b_layout.addWidget(self.cancel_btn)

        b_layout.addStretch()

        self.print_btn = QPushButton("🖨  IN (PRINT)")
        self.print_btn.setObjectName("primaryPrintBtn")
        self.print_btn.setDefault(True)
        self.print_btn.clicked.connect(self.print_requested.emit)
        b_layout.addWidget(self.print_btn)

        # Drop shadows on action buttons
        _add_drop_shadow(self.cancel_btn, blur=8, y_offset=2, color_tuple=(180, 100, 140, 45))
        _add_drop_shadow(self.print_btn, blur=14, y_offset=3, color_tuple=(219, 39, 119, 100))
        _add_drop_shadow(self.refresh_printers_btn, blur=6, y_offset=2, color_tuple=(180, 100, 140, 45))

        root_layout.addWidget(bottom_bar)

    def _create_form_row(self, label_text: str, widget: QWidget) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        lbl = QLabel(label_text)
        lbl.setFixedWidth(110)
        lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        lbl.setStyleSheet("font-weight: 600; color: #374151; font-size: 13px;")
        row.addWidget(lbl)
        row.addWidget(widget, 1)
        return row

    def _create_section_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sectionTitle")
        return lbl

    def reload_printers(self):
        self._block_signals = True
        self.printer_combo.clear()
        self.printers = UniversalPrinterManager.get_printers()

        selected_idx = 0
        for i, p in enumerate(self.printers):
            disp_text = p.name
            if p.is_default:
                disp_text += " [Mặc định]"
            self.printer_combo.addItem(disp_text, p.name)
            if p.is_default:
                selected_idx = i

        if self.printers:
            self.printer_combo.setCurrentIndex(selected_idx)
            self._update_printer_status(self.printers[selected_idx])

        self._block_signals = False
        self._on_change()

    def _on_printer_changed(self, index: int):
        if index >= 0 and index < len(self.printers):
            self._update_printer_status(self.printers[index])
        self._on_change()

    def _update_printer_status(self, printer: PrinterInfo):
        self.printer_status_label.setText(f"Trạng thái: {printer.status}")
        if printer.is_virtual:
            self.print_btn.setText("💾  LƯU DƯỚI DẠNG PDF")
        else:
            self.print_btn.setText("🖨  IN (PRINT)")

    def _on_scale_combo_changed(self):
        is_custom = (self.scale_combo.currentData() == "custom")
        self.custom_scale_container.setVisible(is_custom)
        self._on_change()

    def sync_with_document(self, doc_engine):
        """
        Inspects the loaded document to auto-detect orientation and paper size,
        so preview immediately matches document geometry without manual switching.
        """
        if not doc_engine.is_loaded() or doc_engine.total_source_pages == 0:
            return

        try:
            first_page = doc_engine.doc[0]
            rect = first_page.rect
            w, h = rect.width, rect.height

            self._block_signals = True

            # 1. Detect orientation
            if w > h * 1.05:
                idx = self.orient_combo.findData("landscape")
                if idx >= 0:
                    self.orient_combo.setCurrentIndex(idx)
            else:
                idx = self.orient_combo.findData("portrait")
                if idx >= 0:
                    self.orient_combo.setCurrentIndex(idx)

            # 2. Paper size matching (pt = mm * 72 / 25.4)
            longer = max(w, h)
            shorter = min(w, h)

            matched_size = None
            if abs(shorter - 612) < 25 and abs(longer - 792) < 25:
                matched_size = "Letter"
            elif abs(shorter - 595) < 25 and abs(longer - 842) < 25:
                matched_size = "A4"
            elif abs(shorter - 612) < 25 and abs(longer - 1008) < 25:
                matched_size = "Legal"
            elif abs(shorter - 842) < 25 and abs(longer - 1191) < 25:
                matched_size = "A3"
            elif abs(shorter - 420) < 25 and abs(longer - 595) < 25:
                matched_size = "A5"

            if matched_size:
                idx = self.paper_combo.findData(matched_size)
                if idx >= 0:
                    self.paper_combo.setCurrentIndex(idx)

            self._block_signals = False
        except Exception:
            self._block_signals = False

    def _on_range_mode_changed(self):
        self.custom_range_edit.setEnabled(self.radio_custom.isChecked())
        if self.radio_custom.isChecked():
            self.custom_range_edit.setFocus()
        self._on_change()

    def _on_change(self):
        if not self._block_signals:
            self.settings_changed.emit()

    def get_settings(self) -> PrintJobSettings:
        s = PrintJobSettings()
        # Printer
        cur_idx = self.printer_combo.currentIndex()
        if 0 <= cur_idx < len(self.printers):
            s.printer_name = self.printers[cur_idx].name
        else:
            s.printer_name = UniversalPrinterManager.SAVE_AS_PDF_NAME

        # Copies & Collate
        s.copies = self.copies_spin.value()
        s.collate = self.collate_check.isChecked()

        # Page range
        if self.radio_current.isChecked():
            s.range_mode = "current"
        elif self.radio_custom.isChecked():
            s.range_mode = "custom"
            s.custom_range_text = self.custom_range_edit.text().strip()
        else:
            s.range_mode = "all"

        s.subset_filter = self.subset_combo.currentData() or "all"

        # Color mode
        s.color_mode = self.color_combo.currentData() or "color"

        # Orientation & Paper & Duplex
        s.orientation = self.orient_combo.currentData() or "portrait"
        s.paper_size = self.paper_combo.currentData() or "A4"
        s.duplex_mode = self.duplex_combo.currentData() or "one-sided"

        # Scale
        s.scale_mode = self.scale_combo.currentData() or "fit"
        s.custom_scale_percent = self.scale_percent_spin.value()

        # N-up & Margins
        s.pages_per_sheet = self.nup_combo.currentData() or 1
        s.margin_mode = self.margin_combo.currentData() or "default"

        return s
