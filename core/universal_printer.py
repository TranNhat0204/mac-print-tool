"""
Universal Cross-Platform Printer Interface for Windows and macOS.
Handles printer discovery, CUPS integration (macOS), and Qt Spooler integration (Windows).
"""
import sys
import os
import subprocess
import shutil
from typing import List, Tuple, Optional
import pymupdf as fitz

from ui.qt_compat import (
    QPrinter, QPrinterInfo, QPrintDialog, QPainter, QImage,
    QPageSize, QPageLayout, QRectF, QWidget
)


class PrinterInfo:
    def __init__(self, name: str, is_default: bool = False, status: str = "Sẵn sàng", is_virtual: bool = False):
        self.name = name
        self.is_default = is_default
        self.status = status
        self.is_virtual = is_virtual

    def __repr__(self):
        return f"<Printer: {self.name} (default={self.is_default}, status='{self.status}')>"


class UniversalPrinterManager:
    """Manages printers seamlessly on Windows, macOS, and Linux."""

    SAVE_AS_PDF_NAME = "Lưu dưới dạng PDF (Save as PDF)"

    @classmethod
    def is_macos(cls) -> bool:
        return sys.platform == "darwin"

    @classmethod
    def is_windows(cls) -> bool:
        return sys.platform == "win32"

    @classmethod
    def get_printers(cls) -> List[PrinterInfo]:
        """
        Enumerates all available printers on the operating system.
        """
        printers: List[PrinterInfo] = []

        try:
            qt_printers = QPrinterInfo.availablePrinters()
            default_name = QPrinterInfo.defaultPrinterName()

            # Rich CUPS status map if on macOS
            cups_status_map = {}
            if cls.is_macos() and shutil.which("lpstat"):
                try:
                    res = subprocess.run(["lpstat", "-p"], capture_output=True, text=True, timeout=4)
                    if res.returncode == 0:
                        for line in res.stdout.strip().splitlines():
                            line = line.strip()
                            if line.startswith("printer "):
                                parts = line.split()
                                if len(parts) >= 2:
                                    pname = parts[1]
                                    st = "Sẵn sàng"
                                    if "idle" in line:
                                        st = "Sẵn sàng (Idle)"
                                    elif "printing" in line:
                                        st = "Đang in (Printing)"
                                    elif "disabled" in line:
                                        st = "Tạm dừng (Disabled)"
                                    cups_status_map[pname] = st
                except Exception:
                    pass

            for qp in qt_printers:
                p_name = qp.printerName()
                is_def = (p_name == default_name or qp.isDefault())

                status = cups_status_map.get(p_name, "Sẵn sàng")
                printers.append(PrinterInfo(
                    name=p_name,
                    is_default=is_def,
                    status=status,
                    is_virtual=False
                ))
        except Exception as e:
            print(f"[UniversalPrinterManager] Lỗi lấy danh sách máy in: {e}")

        # Fallback if no printer found
        if not printers:
            if cls.is_windows():
                printers.append(PrinterInfo("Microsoft Print to PDF", is_default=True, status="Sẵn sàng"))
            elif cls.is_macos():
                printers.append(PrinterInfo("Canon LBP2900 (Mô phỏng)", is_default=True, status="Sẵn sàng"))

        # Always prepend 'Save as PDF'
        has_real_default = any(p.is_default for p in printers)
        pdf_printer = PrinterInfo(
            name=cls.SAVE_AS_PDF_NAME,
            is_default=not has_real_default,
            status="Sẵn sàng (Xuất tệp PDF)",
            is_virtual=True
        )

        return [pdf_printer] + printers

    @classmethod
    def print_file(
        cls,
        file_path: str,
        printer_name: str,
        copies: int = 1,
        paper_size: str = "A4",
        duplex_mode: str = "one-sided",
        orientation: str = "portrait",
        collate: bool = True,
        color_mode: str = "color"
    ) -> Tuple[bool, str]:
        """
        Prints the prepared file across macOS and Windows.
        """
        if printer_name == cls.SAVE_AS_PDF_NAME:
            return True, "File đã được xử lý lưu dưới dạng PDF."

        if not os.path.exists(file_path):
            return False, f"Không tìm thấy tệp in: {file_path}"

        # On macOS with CUPS
        if cls.is_macos() and shutil.which("lp") is not None:
            return cls._print_macos_cups(
                file_path=file_path,
                printer_name=printer_name,
                copies=copies,
                paper_size=paper_size,
                duplex_mode=duplex_mode,
                orientation=orientation,
                collate=collate
            )

        # On Windows or cross-platform fallback: use Qt Native Spooler
        return cls._print_via_qt(
            file_path=file_path,
            printer_name=printer_name,
            copies=copies,
            paper_size=paper_size,
            duplex_mode=duplex_mode,
            orientation=orientation,
            collate=collate,
            color_mode=color_mode
        )

    @classmethod
    def _print_macos_cups(
        cls,
        file_path: str,
        printer_name: str,
        copies: int,
        paper_size: str,
        duplex_mode: str,
        orientation: str,
        collate: bool
    ) -> Tuple[bool, str]:
        media_map = {
            "A4": "A4",
            "Letter": "Letter",
            "Legal": "Legal",
            "A3": "A3",
            "A5": "A5",
            "B5": "B5",
            "4x6": "Postcard"
        }
        cups_media = media_map.get(paper_size, "A4")
        orient_val = "4" if orientation == "landscape" else "3"

        cmd = [
            "lp",
            "-d", printer_name,
            "-n", str(max(1, copies)),
            "-o", f"media={cups_media}",
            "-o", f"orientation-requested={orient_val}",
            "-o", "fit-to-page"
        ]

        if duplex_mode in ("two-sided-long-edge", "two-sided-short-edge"):
            cmd.extend(["-o", f"sides={duplex_mode}"])
        else:
            cmd.extend(["-o", "sides=one-sided"])

        if collate:
            cmd.extend(["-o", "Collate=True"])

        cmd.append(file_path)

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                return True, f"Lệnh in đã được gửi thành công tới '{printer_name}'!\n{res.stdout.strip()}"
            else:
                return False, f"Lỗi CUPS: {res.stderr.strip() or res.stdout.strip()}"
        except Exception as e:
            return False, f"Lỗi thực thi lệnh in macOS: {str(e)}"

    @classmethod
    def _print_via_qt(
        cls,
        file_path: str,
        printer_name: str,
        copies: int,
        paper_size: str,
        duplex_mode: str,
        orientation: str,
        collate: bool,
        color_mode: str
    ) -> Tuple[bool, str]:
        """
        Prints using Qt QPrinter and QPainter for native Windows spooling.
        Renders each page of the prepared PDF at 300 DPI directly to printer DC.
        """
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setPrinterName(printer_name)

            if not printer.isValid():
                return False, f"Máy in '{printer_name}' không hợp lệ hoặc không phản hồi."

            printer.setCopyCount(max(1, copies))
            printer.setCollateCopies(collate)

            # Paper Size mapping
            size_map = {
                "A4": QPageSize.PageSizeId.A4,
                "Letter": QPageSize.PageSizeId.Letter,
                "Legal": QPageSize.PageSizeId.Legal,
                "A3": QPageSize.PageSizeId.A3,
                "A5": QPageSize.PageSizeId.A5,
                "B5": QPageSize.PageSizeId.B5,
            }
            target_size = size_map.get(paper_size, QPageSize.PageSizeId.A4)
            printer.setPageSize(QPageSize(target_size))

            # Orientation
            if orientation == "landscape":
                printer.setPageOrientation(QPageLayout.Orientation.Landscape)
            else:
                printer.setPageOrientation(QPageLayout.Orientation.Portrait)

            # Duplex
            if duplex_mode == "two-sided-long-edge":
                printer.setDuplex(QPrinter.DuplexMode.DuplexLongSide)
            elif duplex_mode == "two-sided-short-edge":
                printer.setDuplex(QPrinter.DuplexMode.DuplexShortSide)
            else:
                printer.setDuplex(QPrinter.DuplexMode.DuplexNone)

            # Color Mode
            if color_mode == "grayscale":
                printer.setColorMode(QPrinter.ColorMode.GrayScale)
            else:
                printer.setColorMode(QPrinter.ColorMode.Color)

            # Open the prepared PDF to print its pages
            pdf_doc = fitz.open(file_path)
            num_pages = len(pdf_doc)

            painter = QPainter(printer)
            if not painter.isActive():
                pdf_doc.close()
                return False, f"Không thể khởi tạo phiên in tới '{printer_name}'."

            # Printable rectangle in pixels at printer resolution
            paint_rect = printer.pageLayout().paintRectPixels(printer.resolution())
            cs = fitz.csGRAY if color_mode == "grayscale" else fitz.csRGB

            for i in range(num_pages):
                if i > 0:
                    printer.newPage()

                page = pdf_doc[i]
                # High DPI rasterization for crisp print
                # 300 DPI matrix
                mat = fitz.Matrix(300 / 72.0, 300 / 72.0)
                pix = page.get_pixmap(matrix=mat, colorspace=cs, alpha=False)

                if color_mode == "grayscale":
                    qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_Grayscale8)
                else:
                    qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)

                # Scale to fit printable rectangle with aspect ratio
                draw_w = paint_rect.width()
                draw_h = paint_rect.height()
                scale_ratio = min(draw_w / pix.width, draw_h / pix.height)

                dest_w = pix.width * scale_ratio
                dest_h = pix.height * scale_ratio
                dest_x = paint_rect.x() + (draw_w - dest_w) / 2
                dest_y = paint_rect.y() + (draw_h - dest_h) / 2

                target_rect = QRectF(dest_x, dest_y, dest_w, dest_h)
                painter.drawImage(target_rect, qimg)

            painter.end()
            pdf_doc.close()

            return True, f"Đã gửi thành công {copies} bản in tới máy in '{printer_name}'!"
        except Exception as e:
            return False, f"Lỗi in qua Windows Spooler: {str(e)}"

    @classmethod
    def open_system_print_dialog(cls, file_path: str, parent: Optional[QWidget] = None) -> Tuple[bool, str]:
        """
        Opens the native system print dialog (Windows or macOS).
        """
        if cls.is_windows():
            try:
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                dialog = QPrintDialog(printer, parent)
                if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                    # User confirmed in native Windows Print dialog
                    return cls._print_via_qt(
                        file_path=file_path,
                        printer_name=printer.printerName(),
                        copies=printer.copyCount(),
                        paper_size="A4",
                        duplex_mode="one-sided",
                        orientation="portrait",
                        collate=printer.collateCopies(),
                        color_mode="color"
                    )
                return True, "Đã đóng hộp thoại in hệ thống."
            except Exception as e:
                return False, f"Lỗi mở hộp thoại in Windows: {str(e)}"

        elif cls.is_macos():
            try:
                subprocess.Popen(["open", "-a", "Preview", file_path])
                return True, "Đã mở tệp trong Preview của macOS (Nhấn Command+P để in)."
            except Exception as e:
                return False, f"Lỗi mở Preview trên macOS: {str(e)}"

        return False, "Không hỗ trợ hộp thoại in trên nền tảng này."
