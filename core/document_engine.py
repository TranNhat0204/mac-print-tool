"""
Document engine using PyMuPDF (fitz) and Pillow.
Handles loading PDFs/Images/Text, live page rendering, caching,
page range filtering, grayscale transformation, and N-up sheet composition.
"""
import os
import math
import tempfile
from typing import List, Tuple, Optional, Dict
from PIL import Image
try:
    import pymupdf as fitz
except ImportError:
    import fitz

from ui.qt_compat import QImage, QPixmap
from core.office_converter import is_office_file, convert_office_to_pdf


class PrintJobSettings:
    """Stores all user-selected print options."""
    def __init__(self):
        self.printer_name: str = ""
        self.copies: int = 1
        self.collate: bool = True
        
        # Page range settings
        self.range_mode: str = "all"  # "all", "current", "custom"
        self.custom_range_text: str = ""
        self.subset_filter: str = "all"  # "all", "odd", "even"
        
        # Color mode
        self.color_mode: str = "color"  # "color", "grayscale"
        
        # Orientation
        self.orientation: str = "portrait"  # "portrait", "landscape", "auto"
        
        # Paper size
        self.paper_size: str = "A4"  # A4, Letter, Legal, A3, A5, etc.
        
        # Duplex
        self.duplex_mode: str = "one-sided"  # "one-sided", "two-sided-long-edge", "two-sided-short-edge"
        
        # Scale
        self.scale_mode: str = "fit"  # "fit", "paper_fit", "actual", "custom"
        self.custom_scale_percent: int = 100
        
        # Pages per sheet (N-up)
        self.pages_per_sheet: int = 1  # 1, 2, 4, 6, 9, 16
        
        # Margins
        self.margin_mode: str = "default"  # "default", "none", "minimum"


class DocumentEngine:
    def __init__(self):
        self.original_path: Optional[str] = None
        self.doc: Optional[fitz.Document] = None
        self.temp_pdf_path: Optional[str] = None
        self.total_source_pages: int = 0
        self._pixmap_cache: Dict[str, QPixmap] = {}
        
        # Enable maximum font and vector anti-aliasing
        try:
            fitz.TOOLS.set_aa_level(8)
        except Exception:
            pass

    def is_loaded(self) -> bool:
        return self.doc is not None and not self.doc.is_closed

    def load_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Loads a PDF or converts image/text to an in-memory PDF.
        """
        self.close()
        if not os.path.exists(file_path):
            return False, f"Tệp không tồn tại: {file_path}"

        self.original_path = file_path
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == ".pdf":
                self.doc = fitz.open(file_path)
            elif is_office_file(file_path):
                ok, temp_pdf, msg = convert_office_to_pdf(file_path)
                if not ok or not temp_pdf or not os.path.exists(temp_pdf):
                    self.close()
                    return False, msg
                self.temp_pdf_path = temp_pdf
                self.doc = fitz.open(temp_pdf)
            elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".tif", ".gif"]:
                self.doc = self._convert_image_to_pdf(file_path)
            elif ext in [".txt", ".log", ".csv", ".py", ".md", ".json", ".ini", ".conf"]:
                self.doc = self._convert_text_to_pdf(file_path)
            else:
                # Try opening with fitz as generic document
                try:
                    self.doc = fitz.open(file_path)
                except Exception:
                    return False, f"Định dạng tệp không được hỗ trợ: {ext}"

            self.total_source_pages = len(self.doc)
            self._pixmap_cache.clear()
            return True, f"Đã mở tệp thành công ({self.total_source_pages} trang)"
        except Exception as e:
            self.close()
            return False, f"Lỗi đọc tệp: {str(e)}"

    def close(self):
        if self.doc:
            try:
                self.doc.close()
            except Exception:
                pass
            self.doc = None
        self._pixmap_cache.clear()
        self.total_source_pages = 0
        if self.temp_pdf_path and os.path.exists(self.temp_pdf_path):
            try:
                os.remove(self.temp_pdf_path)
            except Exception:
                pass
            self.temp_pdf_path = None

    def _convert_image_to_pdf(self, image_path: str) -> fitz.Document:
        """Converts an image file into a single-page PDF document."""
        with Image.open(image_path) as img:
            # Handle image orientation from EXIF if needed
            w_px, h_px = img.size
            # Convert px to points (assuming 72 or 150 dpi standard)
            # Default to standard A4 or image aspect ratio
            img_doc = fitz.open()
            rect = fitz.Rect(0, 0, w_px, h_px)
            page = img_doc.new_page(width=w_px, height=h_px)
            page.insert_image(rect, filename=image_path)
            return img_doc

    def _convert_text_to_pdf(self, text_path: str) -> fitz.Document:
        """Converts a text file into a paginated PDF document."""
        doc = fitz.open()
        with open(text_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        # A4 standard size: 595 x 842 points
        page_w, page_h = 595.0, 842.0
        margin_x, margin_y = 50.0, 50.0
        line_height = 14.0
        lines_per_page = int((page_h - 2 * margin_y) / line_height)

        curr_page = None
        for i, line in enumerate(lines):
            line_idx_on_page = i % lines_per_page
            if line_idx_on_page == 0:
                curr_page = doc.new_page(width=page_w, height=page_h)
            
            y_pos = margin_y + line_idx_on_page * line_height
            curr_page.insert_text(
                fitz.Point(margin_x, y_pos),
                line.rstrip("\r\n"),
                fontsize=10,
                fontname="helv"
            )

        if len(doc) == 0:
            doc.new_page(width=page_w, height=page_h)

        return doc

    def parse_page_range(self, settings: PrintJobSettings, current_view_page: int = 1) -> List[int]:
        """
        Calculates 1-based page numbers selected for printing/preview based on settings.
        """
        if not self.is_loaded() or self.total_source_pages <= 0:
            return []

        all_pages = list(range(1, self.total_source_pages + 1))

        if settings.range_mode == "current":
            pages = [max(1, min(current_view_page, self.total_source_pages))]
        elif settings.range_mode == "custom" and settings.custom_range_text.strip():
            pages = []
            tokens = settings.custom_range_text.replace(";", ",").split(",")
            for tok in tokens:
                tok = tok.strip()
                if not tok:
                    continue
                if "-" in tok:
                    parts = tok.split("-")
                    if len(parts) == 2:
                        try:
                            start = int(parts[0].strip())
                            end = int(parts[1].strip())
                            if start <= end:
                                for p in range(start, end + 1):
                                    if 1 <= p <= self.total_source_pages and p not in pages:
                                        pages.append(p)
                        except ValueError:
                            pass
                else:
                    try:
                        p = int(tok)
                        if 1 <= p <= self.total_source_pages and p not in pages:
                            pages.append(p)
                    except ValueError:
                        pass
            if not pages:
                pages = all_pages
        else:
            pages = all_pages

        # Apply subset filter: all, odd, even
        if settings.subset_filter == "odd":
            pages = [p for p in pages if p % 2 != 0]
        elif settings.subset_filter == "even":
            pages = [p for p in pages if p % 2 == 0]

        return pages

    def get_sheet_count(self, settings: PrintJobSettings, current_view_page: int = 1) -> int:
        """
        Returns the number of printed sheets after applying N-up (pages per sheet).
        """
        selected_pages = self.parse_page_range(settings, current_view_page)
        n_up = max(1, settings.pages_per_sheet)
        if not selected_pages:
            return 0
        return math.ceil(len(selected_pages) / n_up)

    def render_preview_sheet(
        self,
        sheet_index: int,
        settings: PrintJobSettings,
        zoom: float = 1.0,
        current_view_page: int = 1
    ) -> Tuple[Optional[QPixmap], int, int]:
        """
        Renders a composite preview sheet (0-indexed) with Ultra-HD Super-Sampling
        for razor-sharp vector clarity on Retina and High-DPI screens.
        Returns: (pixmap, logical_w, logical_h)
        """
        if not self.is_loaded():
            return None, 0, 0

        selected_pages = self.parse_page_range(settings, current_view_page)
        if not selected_pages:
            return None, 0, 0

        n_up = max(1, settings.pages_per_sheet)
        start_idx = sheet_index * n_up
        sheet_pages = selected_pages[start_idx : start_idx + n_up]
        if not sheet_pages:
            return None, 0, 0

        # Sheet dimensions based on paper size
        paper_sizes = {
            "A4": (595.0, 842.0),
            "Letter": (612.0, 792.0),
            "Legal": (612.0, 1008.0),
            "A3": (842.0, 1191.0),
            "A5": (420.0, 595.0),
            "B5": (499.0, 709.0),
            "4x6": (288.0, 432.0),
        }
        base_w, base_h = paper_sizes.get(settings.paper_size, (595.0, 842.0))

        if settings.orientation == "landscape":
            sheet_w, sheet_h = max(base_w, base_h), min(base_w, base_h)
        else:
            sheet_w, sheet_h = min(base_w, base_h), max(base_w, base_h)

        # Logical display dimensions on canvas
        logical_w = max(100, int(sheet_w * zoom))
        logical_h = max(100, int(sheet_h * zoom))

        # Ultra-HD Super-Sampling factor:
        # At small zooms, keep at least 2.5x (180 DPI) so tiny text is super sharp.
        # At larger zooms, scale up to 3.5x - 4.0x.
        render_scale = max(2.5, min(4.0, zoom * 2.0))
        img_w = int(sheet_w * render_scale)
        img_h = int(sheet_h * render_scale)

        cache_key = f"s_{sheet_index}_{n_up}_{settings.color_mode}_{settings.orientation}_{settings.paper_size}_{settings.margin_mode}_{settings.scale_mode}_{settings.custom_scale_percent}_{render_scale}_{'-'.join(map(str, sheet_pages))}"
        if cache_key in self._pixmap_cache:
            return self._pixmap_cache[cache_key], logical_w, logical_h

        # Create QImage canvas for the sheet
        canvas = QImage(img_w, img_h, QImage.Format.Format_ARGB32)
        canvas.fill(0xFFFFFFFF)  # Pure white paper

        from ui.qt_compat import QPainter, QRectF, QPen, QColor

        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Grid layout for N-up
        cols, rows = self._get_nup_grid(n_up)
        cell_w = img_w / cols
        cell_h = img_h / rows

        # Margin ratio:
        # For 1-up: default is 0.0 (fit 100% to paper edge without artificial borders).
        # For N-up > 1: small margin so pages don't merge together.
        if n_up == 1:
            if settings.margin_mode == "minimum":
                margin_ratio = 0.015
            else:
                margin_ratio = 0.00
        else:
            if settings.margin_mode == "none":
                margin_ratio = 0.00
            elif settings.margin_mode == "minimum":
                margin_ratio = 0.015
            else:
                margin_ratio = 0.03

        colorspace = fitz.csGRAY if settings.color_mode == "grayscale" else fitz.csRGB

        for i, page_num in enumerate(sheet_pages):
            if page_num < 1 or page_num > self.total_source_pages:
                continue

            page = self.doc[page_num - 1]
            c = i % cols
            r = i // cols

            box_x = c * cell_w + cell_w * margin_ratio
            box_y = r * cell_h + cell_h * margin_ratio
            box_w = cell_w * (1.0 - 2 * margin_ratio)
            box_h = cell_h * (1.0 - 2 * margin_ratio)

            # Render source page pixmap with crisp vector resolution
            p_rect = page.rect
            base_scale_x = box_w / p_rect.width
            base_scale_y = box_h / p_rect.height

            # Determine scale factor based on scale_mode
            if settings.scale_mode == "fill":
                # Fill page (scale to cover entire cell box, no white borders)
                cell_scale = max(base_scale_x, base_scale_y)
            elif settings.scale_mode == "actual":
                # 100% actual size
                cell_scale = render_scale
            elif settings.scale_mode == "custom":
                # User defined percent (e.g. 100, 110, 85)
                pct = max(20, min(300, settings.custom_scale_percent)) / 100.0
                cell_scale = min(base_scale_x, base_scale_y) * pct
            else:
                # "fit" (Fit to paper) - default
                cell_scale = min(base_scale_x, base_scale_y)

            mat = fitz.Matrix(cell_scale, cell_scale)
            pix = page.get_pixmap(matrix=mat, colorspace=colorspace, alpha=False)

            # Convert fitz pixmap to QImage
            if settings.color_mode == "grayscale":
                qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_Grayscale8)
            else:
                qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)

            # Center page inside cell box
            draw_x = box_x + (box_w - pix.width) / 2
            draw_y = box_y + (box_h - pix.height) / 2

            painter.save()
            painter.setClipRect(QRectF(box_x, box_y, box_w, box_h))
            painter.drawImage(int(round(draw_x)), int(round(draw_y)), qimg)
            painter.restore()

            # Draw subtle page border if N-up > 1
            if n_up > 1:
                painter.setPen(QPen(QColor(210, 215, 220), 2))
                painter.drawRect(QRectF(draw_x - 1, draw_y - 1, pix.width + 2, pix.height + 2))

        painter.end()

        pixmap = QPixmap.fromImage(canvas)
        self._pixmap_cache[cache_key] = pixmap
        return pixmap, logical_w, logical_h

    def _get_nup_grid(self, n_up: int) -> Tuple[int, int]:
        """Returns (columns, rows) for given N-up layout."""
        if n_up <= 1:
            return 1, 1
        elif n_up == 2:
            return 2, 1
        elif n_up <= 4:
            return 2, 2
        elif n_up <= 6:
            return 3, 2
        elif n_up <= 9:
            return 3, 3
        else:
            return 4, 4

    def generate_prepared_pdf(self, settings: PrintJobSettings, output_pdf_path: str) -> Tuple[bool, str]:
        """
        Creates a new PDF on disk with the exact pages, N-up arrangement,
        grayscale transformation, and orientation specified in settings.
        This ensures 100% WYSIWYG printing via CUPS lp!
        """
        if not self.is_loaded():
            return False, "Chưa tải tài liệu."

        selected_pages = self.parse_page_range(settings)
        if not selected_pages:
            return False, "Không có trang nào được chọn để in."

        try:
            out_doc = fitz.open()

            paper_sizes = {
                "A4": (595.0, 842.0),
                "Letter": (612.0, 792.0),
                "Legal": (612.0, 1008.0),
                "A3": (842.0, 1191.0),
                "A5": (420.0, 595.0),
                "B5": (499.0, 709.0),
                "4x6": (288.0, 432.0),
            }
            base_w, base_h = paper_sizes.get(settings.paper_size, (595.0, 842.0))
            if settings.orientation == "landscape":
                sheet_w, sheet_h = max(base_w, base_h), min(base_w, base_h)
            else:
                sheet_w, sheet_h = min(base_w, base_h), max(base_w, base_h)

            n_up = max(1, settings.pages_per_sheet)
            cols, rows = self._get_nup_grid(n_up)
            cell_w = sheet_w / cols
            cell_h = sheet_h / rows

            if n_up == 1:
                if settings.margin_mode == "minimum":
                    margin_ratio = 0.015
                else:
                    margin_ratio = 0.00
            else:
                if settings.margin_mode == "none":
                    margin_ratio = 0.00
                elif settings.margin_mode == "minimum":
                    margin_ratio = 0.015
                else:
                    margin_ratio = 0.03

            colorspace = fitz.csGRAY if settings.color_mode == "grayscale" else fitz.csRGB

            total_sheets = math.ceil(len(selected_pages) / n_up)

            for s in range(total_sheets):
                sheet_page = out_doc.new_page(width=sheet_w, height=sheet_h)
                batch = selected_pages[s * n_up : (s + 1) * n_up]

                for i, p_num in enumerate(batch):
                    src_page = self.doc[p_num - 1]
                    c = i % cols
                    r = i // cols

                    box_x = c * cell_w + cell_w * margin_ratio
                    box_y = r * cell_h + cell_h * margin_ratio
                    box_w = cell_w * (1.0 - 2 * margin_ratio)
                    box_h = cell_h * (1.0 - 2 * margin_ratio)

                    p_rect = src_page.rect
                    base_scale_x = box_w / p_rect.width
                    base_scale_y = box_h / p_rect.height

                    if settings.scale_mode == "fill":
                        scale = max(base_scale_x, base_scale_y)
                    elif settings.scale_mode == "actual":
                        scale = 1.0
                    elif settings.scale_mode == "custom":
                        pct = max(20, min(300, settings.custom_scale_percent)) / 100.0
                        scale = min(base_scale_x, base_scale_y) * pct
                    else:
                        # "fit" (Fit to paper) - default
                        scale = min(base_scale_x, base_scale_y)

                    target_w = p_rect.width * scale
                    target_h = p_rect.height * scale
                    target_x = box_x + (box_w - target_w) / 2
                    target_y = box_y + (box_h - target_h) / 2
                    target_rect = fitz.Rect(target_x, target_y, target_x + target_w, target_y + target_h)
                    clip_rect = fitz.Rect(box_x, box_y, box_x + box_w, box_y + box_h)

                    # Vector embedding for color mode (lossless crisp text at any printer DPI)
                    if settings.color_mode == "color":
                        sheet_page.show_pdf_page(target_rect, self.doc, p_num - 1, clip=clip_rect)
                    else:
                        # High-resolution rasterization (300 DPI for print quality)
                        dpi_mat = fitz.Matrix(300 / 72.0, 300 / 72.0)
                        pix = src_page.get_pixmap(matrix=dpi_mat, colorspace=colorspace, alpha=False)
                        img_bytes = pix.tobytes("png")
                        sheet_page.insert_image(target_rect, stream=img_bytes)

            out_doc.save(output_pdf_path)
            out_doc.close()
            return True, output_pdf_path
        except Exception as e:
            return False, f"Lỗi tạo tệp in chuẩn hóa: {str(e)}"
