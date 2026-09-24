#!/usr/bin/env bash
# ==============================================================================
# Script đóng gói MacPrint thành ứng dụng macOS độc lập (.app)
# Tự động cấu hình 'Open With' trong menu chuột phải của Finder
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "    Đang đóng gói MacPrint thành file .app        "
echo "=================================================="

# 1. Khởi tạo và kích hoạt môi trường ảo Python
if [ ! -d ".venv" ]; then
    echo "📦 Đang khởi tạo môi trường ảo Python (.venv)..."
    python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Cài đặt PyInstaller nếu chưa có
echo "[1/4] Kiểm tra PyInstaller và các thư viện..."
python3 -m pip install -q pyinstaller -r requirements.txt

# 3. Dọn dẹp bản build cũ
rm -rf build dist

# 4. Đóng gói app bundle
echo "[2/4] Đang biên dịch bundle MacPrint.app với PyInstaller..."
python3 -m PyInstaller \
    --name "MacPrint" \
    --windowed \
    --noconfirm \
    --clean \
    --add-data "ui:ui" \
    --add-data "core:core" \
    --add-data "assets:assets" \
    --osx-bundle-identifier "com.antigravity.macprint" \
    main.py

# 5. Cấu hình liên kết tệp tin (File Associations) cho Finder Open With
echo "[3/4] Cấu hình menu chuột phải 'Open With -> MacPrint'..."
python3 configure_macos_associations.py "$DIR/dist/MacPrint.app"

# 6. Đăng ký với LaunchServices của macOS
echo "[4/4] Cập nhật macOS LaunchServices..."
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
if [ -f "$LSREGISTER" ]; then
    "$LSREGISTER" -f "$DIR/dist/MacPrint.app" || true
fi

echo "=================================================="
echo "✅ ĐÓNG GÓI HOÀN TẤT THÀNH CÔNG!"
echo ""
echo "Ứng dụng MacPrint đã được tạo tại:"
echo "📁 $DIR/dist/MacPrint.app"
echo ""
echo "👉 BƯỚC TIẾP THEO:"
echo "1. Mở Finder và kéo 'MacPrint.app' vào thư mục '/Applications'."
echo "2. Chuột phải vào bất kỳ file PDF hoặc ảnh -> chọn 'Open With' -> bạn sẽ thấy 'MacPrint'!"
echo "=================================================="
