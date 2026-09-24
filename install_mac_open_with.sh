#!/usr/bin/env bash
# ==============================================================================
# Đăng ký MacPrint vào menu chuột phải "Open With" trên macOS
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
chmod +x "$DIR"/*.sh "$DIR"/*.command 2>/dev/null || true
APP_NAME="MacPrint.app"
SRC_APP="$DIR/dist/$APP_NAME"
DEST_APP="/Applications/$APP_NAME"

echo "=================================================="
echo "    Đăng ký MacPrint vào menu chuột phải Finder   "
echo "=================================================="

# 1. Kiểm tra xem đã build MacPrint.app chưa
if [ ! -d "$SRC_APP" ]; then
    echo "⚙️ Chưa tìm thấy bản build. Đang tiến hành build MacPrint.app..."
    bash "$DIR/build_mac_app.sh"
fi

# 2. Cài đặt vào /Applications
echo "📦 Đang cài đặt MacPrint vào thư mục /Applications..."
rm -rf "$DEST_APP"
cp -R "$SRC_APP" "/Applications/"

# 3. Chạy cập nhật liên kết tệp tin
python3 "$DIR/configure_macos_associations.py" "$DEST_APP"

# 4. Ép macOS LaunchServices quét lại ứng dụng
echo "🔄 Đang làm mới cơ sở dữ liệu LaunchServices của macOS..."
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
if [ -f "$LSREGISTER" ]; then
    "$LSREGISTER" -kill -r -domain local -domain system -domain user
    "$LSREGISTER" -f "$DEST_APP"
fi

# 5. Khởi động lại Finder để cập nhật menu chuột phải ngay tức thì
killall Finder 2>/dev/null || true

echo "=================================================="
echo "🎉 THÀNH CÔNG!"
echo "MacPrint đã được cài đặt vào /Applications/MacPrint.app"
echo ""
echo "Bây giờ bạn chỉ cần:"
echo "1. Chuột phải vào bất kỳ file PDF, PNG, JPG, TXT nào."
echo "2. Chọn 'Open With' (Mở bằng) -> chọn 'MacPrint'!"
echo "=================================================="
