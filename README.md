# PrintMaster - Trình xem trước & In ấn phong cách Windows (Hỗ trợ cả Windows & macOS)

**PrintMaster** là công cụ in ấn đa nền tảng (Cross-Platform) hoạt động mượt mà trên cả **Windows** và **macOS (MacBook)**. Công cụ mang lại trải nghiệm **Print Preview trực quan và đầy đủ mọi tùy chọn cấu hình in ấn theo chuẩn giao diện Windows** quen thuộc.

---

## 🌟 Tính năng nổi bật

### 1. Khung xem trước trực quan thời gian thực (Live Preview)
- **Mô phỏng tờ in chân thực**: Tờ in hiển thị rõ nét trên nền canvas tối với hiệu ứng bóng đổ (Drop Shadow), chất lượng hiển thị sắc nét (hỗ trợ màn hình Retina trên MacBook và màn hình độ phân giải cao High-DPI trên Windows).
- **Cập nhật tức thời (WYSIWYG)**: Khi đổi sang *Đen trắng*, xoay *Khổ ngang*, đổi *Khổ giấy*, hoặc chọn ghép nhiều trang trên 1 tờ (*N-up*), màn hình xem trước sẽ cập nhật giao diện ngay lập tức.
- **Bộ điều khiển thu phóng & điều hướng**:
  - `⊡ Vừa trang (Fit Page)`: Thu phóng vừa vặn toàn bộ trang vào màn hình.
  - `↔ Vừa chiều rộng (Fit Width)`: Tối ưu theo chiều ngang để đọc rõ văn bản.
  - Phóng to (`+`), thu nhỏ (`-`), tỉ lệ phần trăm %.
  - Nút chuyển trang nhanh: Tờ đầu `|<`, tờ trước `<`, tờ tiếp `>`, tờ cuối `>|` và chỉ báo `Tờ X / Y`.

### 2. Bảng tùy chọn in ấn phong cách Windows (Print Options)
- **Máy in (Destination / Printer)**:
  - Tự động nhận diện và liệt kê tất cả các máy in thực tế trên cả Windows (qua Windows Spooler) và macOS (qua CUPS).
  - Đánh dấu máy in mặc định và hiển thị trạng thái hiện tại (*Sẵn sàng*, *Đang in*...).
  - Nút **⟳ Làm mới** danh sách máy in ngay tức thì.
  - Tích hợp sẵn máy in ảo **"Lưu dưới dạng PDF (Save as PDF)"**.
- **Số bản in (Copies) & Ghép bộ (Collate)**:
  - Tùy chỉnh số lượng bản in (1 - 999 bản).
  - Tùy chọn in theo bộ (*Collate: 1-2-3, 1-2-3* thay vì in dồn *1-1, 2-2, 3-3*).
- **Phạm vi trang in (Pages)**:
  - *Tất cả các trang (All)*.
  - *Chỉ trang hiện tại (Current Page)*.
  - *Tùy chỉnh phạm vi (Custom)*: Hỗ trợ dải trang linh hoạt (vd: `1-5, 8, 11-13`).
  - Bộ lọc: *Tất cả*, *Chỉ in trang lẻ (Odd)*, *Chỉ in trang chẵn (Even)*.
- **Chế độ màu (Color Mode)**:
  - 🌈 Màu sắc (Color).
  - ⬛ Đen trắng / Mức xám (Grayscale / B&W).
- **Bố cục & Hướng giấy (Layout & Orientation)**:
  - 📄 Khổ dọc (Portrait) hoặc 📑 Khổ ngang (Landscape).
- **Khổ giấy (Paper size)**:
  - Đầy đủ các khổ phổ biến: A4, Letter, Legal, A3, A5, B5, Ảnh 4x6...
- **In hai mặt (Duplex Printing)**:
  - In một mặt (1-sided).
  - In 2 mặt - Lật cạnh dài (Duplex Long-edge).
  - In 2 mặt - Lật cạnh ngắn (Duplex Short-edge).
- **Bố cục nhiều trang trên một tờ (Pages per sheet / N-up)**:
  - Hỗ trợ in 1, 2, 4 (2x2), 6, 9 hoặc 16 trang trên cùng một tờ giấy in.
- **Lề trang (Margins)**:
  - Mặc định (Default), Tối thiểu (Minimum), Không lề (None / Tràn viền).
- **Khóa cuộn chuột thông minh**:
  - Không lo vô tình lăn chuột đổi giá trị combobox/spinbox. Người dùng nhấp để chọn giá trị.
- **Cuộn chuột xem tài liệu mượt mà**:
  - Lăn chuột xuống để lật sang trang sau, lăn chuột lên để về trang trước. Giữ `Ctrl` (hoặc `Cmd` trên Mac) + lăn chuột để phóng to/thu nhỏ.

### 3. Định dạng tệp tin hỗ trợ phong phú
- **Tài liệu PDF** (`.pdf`).
- **Tài liệu Microsoft Office** (tự động chuyển đổi & xem trước chân thực):
  - 📄 **Word**: `.docx`, `.doc`
  - 📊 **Excel**: `.xlsx`, `.xls`
  - 📽️ **PowerPoint**: `.pptx`, `.ppt`
  - *Tự động tận dụng engine Microsoft Office (Windows/macOS), Apple iWork (Pages, Numbers, Keynote trên Mac), hoặc LibreOffice để kết xuất tài liệu sắc nét chuẩn vector.*
- **Hình ảnh**: `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.gif` (tự động căn vừa khổ giấy).
- **Tệp văn bản**: `.txt`, `.log`, `.csv`, `.md`, `.json`... (tự động phân trang và hiển thị phông chữ rõ nét).
- Hỗ trợ **Kéo & Thả (Drag & Drop)** tệp trực tiếp vào cửa sổ ứng dụng.

---

## 💻 Hướng dẫn sử dụng trên WINDOWS

### Cách 1: Chạy nhanh bằng 1 click (Khuyên dùng)
1. Chỉ cần **click đúp chuột** vào tệp **`run_win.bat`**.
2. Script sẽ tự động kiểm tra Python, tạo môi trường ảo `.venv` và bật giao diện PrintMaster lên.
3. Bạn cũng có thể **kéo thả trực tiếp file PDF hoặc ảnh thả đè lên file `run_win.bat`** để mở ngay file đó!

### Cách 2: Đóng gói thành file chạy `PrintMaster.exe` độc lập
Nếu muốn tạo một file `.exe` duy nhất để chạy trên bất kỳ máy Windows nào mà không cần cài đặt Python:
1. Click đúp vào file **`build_win_exe.bat`**.
2. Sau khi đóng gói xong, file thực thi sẽ nằm tại:
   `dist\PrintMaster\PrintMaster.exe`

---

## 🍏 Hướng dẫn sử dụng trên MACBOOK (macOS)

### Cách 1: Chạy nhanh bằng Terminal
1. Mở **Terminal** và điều hướng tới thư mục:
   ```bash
   cd /duong_dan_toi/mac-print-tool
   ```
2. Cấp quyền và chạy:
   ```bash
   chmod +x run_mac.sh
   ./run_mac.sh
   ```
   *(Script sẽ tự động tạo virtualenv, cài thư viện và khởi chạy).*

3. Hoặc mở kèm tệp:
   ```bash
   ./run_mac.sh /Users/ten_ban/Documents/baocao.pdf
   ```

### Cách 2: Đóng gói thành ứng dụng `PrintMaster.app`
1. Chạy lệnh:
   ```bash
   chmod +x build_mac_app.sh
   ./build_mac_app.sh
   ```
2. Kéo thư mục **`dist/PrintMaster.app`** vào thư mục **`/Applications`** trên MacBook để dùng như ứng dụng Mac thông thường.

---

## 📁 Cấu trúc mã nguồn

```
mac-print-tool/
├── assets/
│   ├── app_icon.png            # Icon định dạng PNG (cho Mac & Linux)
│   └── app_icon.ico            # Icon định dạng ICO (cho Windows)
├── core/
│   ├── document_engine.py      # Xử lý PDF/ảnh, phân trang, lọc dải trang, N-up, Grayscale
│   ├── universal_printer.py    # Quản lý máy in đa nền tảng (CUPS trên Mac, Spooler trên Windows)
│   └── mac_printer.py          # Module alias tương thích ngược
├── ui/
│   ├── qt_compat.py            # Tương thích mượt mà giữa PyQt6 và PySide6
│   ├── theme.py                # Giao diện hiện đại phong cách Windows Print Dialog
│   ├── preview_canvas.py       # Khung xem trước zoom, pan, hiển thị trang & bóng đổ
│   ├── settings_panel.py       # Bảng tùy chọn in ấn Windows-style
│   └── main_window.py          # Cửa sổ chính, Drag & Drop, Menu bar, thanh trạng thái
├── main.py                     # Entry point khởi chạy ứng dụng
├── requirements.txt            # Danh sách thư viện (PyQt6, pymupdf, Pillow)
├── run_win.bat                 # Script chạy nhanh 1-click trên Windows
├── build_win_exe.bat           # Script đóng gói thành PrintMaster.exe trên Windows
├── run_mac.sh                  # Script chạy nhanh 1-click trên macOS
├── build_mac_app.sh            # Script đóng gói thành PrintMaster.app trên macOS
└── README.md                   # Tài liệu hướng dẫn sử dụng chi tiết
```
