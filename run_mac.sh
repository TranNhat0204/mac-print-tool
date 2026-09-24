#!/usr/bin/env bash
# ==============================================================================
# MacPrint - Script chạy nhanh ứng dụng in ấn trên macOS
# ==============================================================================

set -e

# Chuyển về thư mục chứa script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "    PrintMaster - Trình xem trước & In ấn cho Mac "
echo "=================================================="

# Kiểm tra Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Không tìm thấy python3 trên máy của bạn."
    echo "Vui lòng cài đặt Python từ https://www.python.org hoặc qua Homebrew: brew install python"
    exit 1
fi

# Thiết lập Virtual Environment nếu chưa có
if [ ! -d ".venv" ]; then
    echo "📦 Đang khởi tạo môi trường ảo Python (.venv)..."
    python3 -m venv .venv
fi

# Kích hoạt virtualenv
source .venv/bin/activate

# Cài đặt hoặc cập nhật thư viện
echo "🔍 Đang kiểm tra thư viện (PyQt6, pymupdf, Pillow)..."
python3 -m pip install -q -r requirements.txt

# Khởi chạy ứng dụng
echo "🚀 Đang khởi chạy MacPrint..."
python3 main.py "$@"
