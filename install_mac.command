#!/usr/bin/env bash
# ==============================================================================
# Tự động đóng gói & Cài đặt MacPrint vào /Applications
# Cấu hình chuột phải Open With cho Finder
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "    CÀI ĐẶT MACPRINT VÀO ỨNG DỤNG MACBOOK        "
echo "=================================================="

# 1. Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Chưa tìm thấy Python 3 trên máy của bạn."
    echo "👉 Hãy tải Python tại: https://www.python.org/downloads/"
    read -p "Nhấn phím Enter để đóng..."
    exit 1
fi

# 2. Chạy script cài đặt
bash "$DIR/install_mac_open_with.sh"

echo ""
echo "=================================================="
echo "✨ ĐÃ CÀI ĐẶT THÀNH CÔNG!"
echo "Bạn có thể tìm thấy 'MacPrint' trong thư mục Applications (Ứng dụng)."
echo "Chuột phải vào file PDF/ảnh bất kỳ -> Open With -> MacPrint."
echo "=================================================="
echo ""
read -p "Nhấn phím Enter để hoàn tất..."
