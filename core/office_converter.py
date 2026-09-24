"""
Office Document Converter for MacPrint / PrintMaster.
Converts Microsoft Word (.docx, .doc), Excel (.xlsx, .xls), and
PowerPoint (.pptx, .ppt) documents into temporary PDF files for preview and printing.

Supports:
- Windows: Microsoft Office COM automation (PowerShell) and LibreOffice (soffice).
- macOS: Apple iWork (Pages, Numbers, Keynote), Microsoft Office for Mac (AppleScript), and LibreOffice (soffice).
"""
import os
import sys
import shutil
import tempfile
import subprocess
from typing import Tuple, Optional

OFFICE_WORD_EXTENSIONS = {".docx", ".doc"}
OFFICE_EXCEL_EXTENSIONS = {".xlsx", ".xls"}
OFFICE_PPT_EXTENSIONS = {".pptx", ".ppt"}
OFFICE_EXTENSIONS = OFFICE_WORD_EXTENSIONS | OFFICE_EXCEL_EXTENSIONS | OFFICE_PPT_EXTENSIONS


def is_office_file(file_path: str) -> bool:
    """Checks if the given file path has an Office extension."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext in OFFICE_EXTENSIONS


def convert_office_to_pdf(input_path: str) -> Tuple[bool, Optional[str], str]:
    """
    Converts an Office document (.docx, .doc, .xlsx, .xls, .pptx, .ppt) to a temporary PDF.
    Returns:
        (success: bool, pdf_path: Optional[str], message: str)
    """
    if not os.path.exists(input_path):
        return False, None, f"Tệp không tồn tại: {input_path}"

    ext = os.path.splitext(input_path)[1].lower()
    if ext not in OFFICE_EXTENSIONS:
        return False, None, f"Định dạng không phải là tài liệu Office: {ext}"

    abs_input = os.path.abspath(input_path)
    base_name = os.path.splitext(os.path.basename(abs_input))[0]
    fd, temp_pdf = tempfile.mkstemp(prefix=f"macprint_{base_name}_", suffix=".pdf")
    os.close(fd)

    # 1. Try LibreOffice if installed on any OS
    soffice_path = _find_soffice()
    if soffice_path:
        success, msg = _convert_via_libreoffice(soffice_path, abs_input, temp_pdf)
        if success and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
            return True, temp_pdf, "Chuyển đổi thành công qua LibreOffice"

    # 2. Windows: Native Office COM via PowerShell
    if sys.platform == "win32":
        success, msg = _convert_windows_office(abs_input, temp_pdf, ext)
        if success and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
            return True, temp_pdf, "Chuyển đổi thành công qua Microsoft Office (Windows)"
        else:
            _cleanup_temp_file(temp_pdf)
            return False, None, _build_fallback_guidance(input_path, msg)

    # 3. macOS: Native textutil or AppleScript (Pages/Numbers/Keynote/Office)
    elif sys.platform == "darwin":
        # Strategy A: For Word documents (.docx, .doc), use native macOS /usr/bin/textutil + QTextDocument
        # textutil is built into 100% of Macs, converts in 0.1s, and bypasses Apple Event -1743!
        if ext in OFFICE_WORD_EXTENSIONS:
            ok, t_msg = _convert_macos_textutil(abs_input, temp_pdf)
            if ok and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
                return True, temp_pdf, "Chuyển đổi thành công qua macOS textutil"

        # Strategy B: AppleScript via Pages / Numbers / Keynote / MS Office
        success, msg = _convert_macos_applescript(abs_input, temp_pdf, ext)
        if success and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
            return True, temp_pdf, "Chuyển đổi thành công qua Apple iWork / MS Office (macOS)"
        else:
            _cleanup_temp_file(temp_pdf)
            return False, None, _build_fallback_guidance(input_path, msg)

    # 4. Other OS / Unsupported
    _cleanup_temp_file(temp_pdf)
    return False, None, _build_fallback_guidance(input_path, "Hệ điều hành chưa hỗ trợ công cụ chuyển đổi tự động.")


def _cleanup_temp_file(path: Optional[str]):
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


def _find_soffice() -> Optional[str]:
    """Locates LibreOffice soffice binary across platforms."""
    # Check PATH
    found = shutil.which("soffice")
    if found:
        return found

    if sys.platform == "win32":
        candidates = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        for c in candidates:
            if os.path.exists(c):
                return c

    elif sys.platform == "darwin":
        candidates = [
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            os.path.expanduser("~/Applications/LibreOffice.app/Contents/MacOS/soffice"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c

    return None


def _convert_via_libreoffice(soffice_bin: str, input_path: str, output_pdf_path: str) -> Tuple[bool, str]:
    """Uses headless LibreOffice to convert input document to PDF."""
    try:
        out_dir = os.path.dirname(output_pdf_path)
        cmd = [
            soffice_bin,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", out_dir,
            input_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        
        # LibreOffice outputs <base_name>.pdf in out_dir
        expected_name = os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        actual_output = os.path.join(out_dir, expected_name)
        
        if os.path.exists(actual_output) and os.path.getsize(actual_output) > 0:
            if actual_output != output_pdf_path:
                shutil.move(actual_output, output_pdf_path)
            return True, "Thành công"
        return False, f"LibreOffice không tạo ra tệp PDF: {res.stderr}"
    except Exception as e:
        return False, f"Lỗi chạy LibreOffice: {str(e)}"


def _convert_windows_office(input_path: str, output_pdf_path: str, ext: str) -> Tuple[bool, str]:
    """Uses PowerShell to automate Microsoft Word, Excel, or PowerPoint COM on Windows."""
    if ext in OFFICE_WORD_EXTENSIONS:
        ps_code = """
param([string]$inPath, [string]$outPath)
$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($inPath, $false, $true)
    $doc.SaveAs([ref]$outPath, [ref]17)
    $doc.Close([ref]0)
    Write-Output "SUCCESS"
} catch {
    Write-Output ("ERROR: " + $_.Exception.Message)
} finally {
    if ($word -ne $null) {
        $word.Quit([ref]0)
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
}
"""
    elif ext in OFFICE_EXCEL_EXTENSIONS:
        ps_code = """
param([string]$inPath, [string]$outPath)
$excel = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $wb = $excel.Workbooks.Open($inPath, $false, $true)
    $wb.ExportAsFixedFormat(0, $outPath)
    $wb.Close($false)
    Write-Output "SUCCESS"
} catch {
    Write-Output ("ERROR: " + $_.Exception.Message)
} finally {
    if ($excel -ne $null) {
        $excel.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
}
"""
    elif ext in OFFICE_PPT_EXTENSIONS:
        ps_code = """
param([string]$inPath, [string]$outPath)
$ppt = $null
try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($inPath, -1, 0, 0)
    $pres.SaveAs($outPath, 32)
    $pres.Close()
    Write-Output "SUCCESS"
} catch {
    Write-Output ("ERROR: " + $_.Exception.Message)
} finally {
    if ($ppt -ne $null) {
        $ppt.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
    }
}
"""
    else:
        return False, f"Định dạng không được hỗ trợ: {ext}"

    ps_file = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8") as f:
            f.write(ps_code)
            ps_file = f.name

        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-File", ps_file,
            input_path,
            output_pdf_path
        ]

        # Use startupinfo to hide PowerShell console window completely
        startupinfo = None
        if hasattr(subprocess, "STARTUPINFO"):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            startupinfo=startupinfo
        )

        stdout = res.stdout.strip()
        if "SUCCESS" in stdout and os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
            return True, "Thành công"
        return False, stdout or res.stderr or "Không thể chuyển đổi qua Microsoft Office COM"
    except Exception as e:
        return False, f"Lỗi COM Windows: {str(e)}"
    finally:
        if ps_file and os.path.exists(ps_file):
            try:
                os.remove(ps_file)
            except Exception:
                pass


def _convert_macos_applescript(input_path: str, output_pdf_path: str, ext: str) -> Tuple[bool, str]:
    """Uses AppleScript to convert Office documents using Pages/Numbers/Keynote or MS Office for Mac."""
    scripts = []

    if ext in OFFICE_WORD_EXTENSIONS:
        # Try MS Word first, then Apple Pages
        scripts.append(("""
on run argv
    set inPath to POSIX file (item 1 of argv)
    set outPath to POSIX file (item 2 of argv)
    tell application "Microsoft Word"
        set theDoc to open inPath
        save as theDoc file name (item 2 of argv) file format format PDF
        close theDoc saving no
    end tell
end run
""", "Microsoft Word"))
        scripts.append(("""
on run argv
    set inPath to POSIX file (item 1 of argv)
    set outPath to POSIX file (item 2 of argv)
    tell application "Pages"
        set theDoc to open inPath
        export theDoc to outPath as PDF
        close theDoc saving no
    end tell
end run
""", "Apple Pages"))

    elif ext in OFFICE_EXCEL_EXTENSIONS:
        # Try MS Excel first, then Apple Numbers
        scripts.append(("""
on run argv
    set inPath to POSIX file (item 1 of argv)
    set outPath to item 2 of argv
    tell application "Microsoft Excel"
        open workbook workbook file name (item 1 of argv)
        save active workbook in filename outPath as PDF file format
        close active workbook saving no
    end tell
end run
""", "Microsoft Excel"))
        scripts.append(("""
on run argv
    set inPath to POSIX file (item 1 of argv)
    set outPath to POSIX file (item 2 of argv)
    tell application "Numbers"
        set theDoc to open inPath
        export theDoc to outPath as PDF
        close theDoc saving no
    end tell
end run
""", "Apple Numbers"))

    elif ext in OFFICE_PPT_EXTENSIONS:
        # Try MS PowerPoint first, then Apple Keynote
        scripts.append(("""
on run argv
    set inPath to POSIX file (item 1 of argv)
    set outPath to item 2 of argv
    tell application "Microsoft PowerPoint"
        open inPath
        save active presentation in outPath as save as PDF
        close active presentation saving no
    end tell
end run
""", "Microsoft PowerPoint"))
        scripts.append(("""
on run argv
    set inPath to POSIX file (item 1 of argv)
    set outPath to POSIX file (item 2 of argv)
    tell application "Keynote"
        set theDoc to open inPath
        export theDoc to outPath as PDF
        close theDoc saving no
    end tell
end run
""", "Apple Keynote"))

    last_error = ""
    for script_text, app_name in scripts:
        try:
            cmd = ["osascript", "-e", script_text, input_path, output_pdf_path]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if res.returncode == 0 and os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
                return True, f"Chuyển đổi thành công qua {app_name}"
            last_error = res.stderr.strip() or f"Không thể xuất PDF từ {app_name}"
        except Exception as e:
            last_error = str(e)

    return False, last_error


def _convert_macos_textutil(input_path: str, output_pdf_path: str) -> Tuple[bool, str]:
    """
    Converts Word (.docx, .doc) to PDF using macOS built-in /usr/bin/textutil
    combined with PyQt6 QTextDocument & QPrinter.
    Runs 100% locally on macOS without needing Pages, MS Word, or Apple Event permissions (-1743).
    """
    textutil_bin = "/usr/bin/textutil"
    if not os.path.exists(textutil_bin):
        return False, "Không tìm thấy textutil trên macOS"

    fd, temp_html = tempfile.mkstemp(prefix="macprint_txtutil_", suffix=".html")
    os.close(fd)

    try:
        cmd = [textutil_bin, "-convert", "html", "-output", temp_html, input_path]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode != 0 or not os.path.exists(temp_html) or os.path.getsize(temp_html) == 0:
            return False, f"Lỗi textutil: {res.stderr.strip()}"

        with open(temp_html, "r", encoding="utf-8", errors="replace") as f:
            html_text = f.read()

        from ui.qt_compat import QTextDocument, QPrinter, QPageSize
        doc = QTextDocument()
        doc.setHtml(html_text)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_pdf_path)
        if hasattr(QPageSize, "PageSizeId"):
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        doc.print(printer)

        if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
            return True, "Thành công qua textutil"
        return False, "Không thể xuất PDF từ HTML"
    except Exception as e:
        return False, f"Lỗi chuyển đổi textutil: {str(e)}"
    finally:
        if os.path.exists(temp_html):
            try:
                os.remove(temp_html)
            except Exception:
                pass


def _build_fallback_guidance(input_path: str, raw_err: str) -> str:
    """Builds a clear, polite, and actionable guidance message in Vietnamese."""
    fname = os.path.basename(input_path)

    # Specific guidance for macOS Automation / Apple Event -1743 error
    if "-1743" in raw_err or "Không được phép gửi" in raw_err or "Not authorized to send Apple events" in raw_err:
        return (
            f"macOS đang chặn quyền gửi lệnh tự động của MacPrint đến Pages/Office (Lỗi -1743).\n\n"
            f"🔓 ĐỂ BẬT QUYỀN TỰ ĐỘNG CHUYỂN ĐỔI:\n"
            f"1. Vào Cài đặt hệ thống (System Settings) trên Mac.\n"
            f"2. Vào 'Quyền riêng tư & Bảo mật' (Privacy & Security) -> chọn 'Tự động hóa' (Automation).\n"
            f"3. Dưới mục 'MacPrint' (hoặc 'Terminal'), gạt BẬT quyền cho 'Pages' / 'Numbers' / 'Keynote'.\n\n"
            f"💡 HOẶC MẸO XỬ LÝ NHANH TRONG 3 GIÂY:\n"
            f"1. Mở tệp '{fname}' trong Word, Pages, Excel hoặc PPT.\n"
            f"2. Bấm Cmd+P -> Chọn 'Lưu dưới dạng PDF' (Save as PDF).\n"
            f"3. Kéo tệp PDF vừa tạo vào MacPrint để in ấn với đầy đủ tùy chọn!"
        )

    return (
        f"Không thể mở trực tiếp tài liệu Office '{fname}'.\n"
        f"Chi tiết: {raw_err}\n\n"
        f"💡 HƯỚNG DẪN XỬ LÝ NHANH:\n"
        f"1. Mở tệp '{fname}' trong Word, Excel hoặc PowerPoint.\n"
        f"2. Bấm Ctrl+P (hoặc Cmd+P trên Mac) -> Chọn 'Lưu dưới dạng PDF' (Print to PDF).\n"
        f"3. Kéo thả tệp PDF vừa lưu vào MacPrint để in ấn với đầy đủ tùy chọn (N-up, 2 mặt, tỷ lệ, màu sắc)!"
    )
