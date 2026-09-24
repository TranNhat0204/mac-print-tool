#!/usr/bin/env bash
# ==============================================================================
# MacPrint - Double-click để chạy nhanh trên macOS (tương đương .bat trên Windows)
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "    PrintMaster - Trình xem trước & In ấn cho Mac "
echo "=================================================="

# Kiểm tra Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Chưa tìm thấy Python 3 trên máy của bạn."
    echo "👉 Hãy mở trang web: https://www.python.org/downloads/ để tải và cài đặt Python 3."
    echo "Hoặc cài qua Homebrew: brew install python"
    echo ""
    read -p "Nhấn phím Enter để đóng..."
    exit 1
fi

# Tạo môi trường ảo nếu chưa có
if [ ! -d ".venv" ]; then
    echo "📦 Đang khởi tạo môi trường Python độc lập (.venv)..."
    python3 -m venv .venv
fi

# Kích hoạt môi trường
source .venv/bin/activate

# Cài đặt thư viện nếu thiếu
echo "🔍 Đang kiểm tra và cài đặt thư viện cần thiết..."
python3 -m pip install -q -r requirements.txt

# Khởi chạy ứng dụng
echo "🚀 Đang mở giao diện PrintMaster..."
python3 main.py "$@"
