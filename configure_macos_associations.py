#!/usr/bin/env python3
"""
Configures Info.plist for MacPrint.app on macOS to associate it with
PDFs, Images, and Text files so it appears in Finder's 'Open With' menu.
"""
import sys
import os
import plistlib
import subprocess

DOCUMENT_TYPES = [
    {
        "CFBundleTypeName": "PDF Document",
        "CFBundleTypeRole": "Viewer",
        "LSHandlerRank": "Alternate",
        "LSItemContentTypes": ["com.adobe.pdf"],
        "CFBundleTypeExtensions": ["pdf"]
    },
    {
        "CFBundleTypeName": "Image Document",
        "CFBundleTypeRole": "Viewer",
        "LSHandlerRank": "Alternate",
        "LSItemContentTypes": [
            "public.image",
            "public.png",
            "public.jpeg",
            "public.tiff",
            "com.compuserve.gif",
            "org.webmproject.webp",
            "com.microsoft.bmp"
        ],
        "CFBundleTypeExtensions": [
            "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "gif"
        ]
    },
    {
        "CFBundleTypeName": "Text Document",
        "CFBundleTypeRole": "Viewer",
        "LSHandlerRank": "Alternate",
        "LSItemContentTypes": ["public.plain-text", "public.text"],
        "CFBundleTypeExtensions": ["txt", "log", "csv", "md", "json"]
    },
    {
        "CFBundleTypeName": "Microsoft Word Document",
        "CFBundleTypeRole": "Viewer",
        "LSHandlerRank": "Alternate",
        "LSItemContentTypes": [
            "org.openxmlformats.wordprocessingml.document",
            "com.microsoft.word.doc"
        ],
        "CFBundleTypeExtensions": ["docx", "doc"]
    },
    {
        "CFBundleTypeName": "Microsoft Excel Spreadsheet",
        "CFBundleTypeRole": "Viewer",
        "LSHandlerRank": "Alternate",
        "LSItemContentTypes": [
            "org.openxmlformats.spreadsheetml.sheet",
            "com.microsoft.excel.xls"
        ],
        "CFBundleTypeExtensions": ["xlsx", "xls"]
    },
    {
        "CFBundleTypeName": "Microsoft PowerPoint Presentation",
        "CFBundleTypeRole": "Viewer",
        "LSHandlerRank": "Alternate",
        "LSItemContentTypes": [
            "org.openxmlformats.presentationml.presentation",
            "com.microsoft.powerpoint.ppt"
        ],
        "CFBundleTypeExtensions": ["pptx", "ppt"]
    }
]


def update_plist(app_path: str):
    plist_path = os.path.join(app_path, "Contents", "Info.plist")
    if not os.path.exists(plist_path):
        print(f"[Error] Không tìm thấy Info.plist tại: {plist_path}")
        return False

    with open(plist_path, "rb") as f:
        pl = plistlib.load(f)

    # Inject document types
    pl["CFBundleDocumentTypes"] = DOCUMENT_TYPES
    pl["CFBundleName"] = "MacPrint"
    pl["CFBundleDisplayName"] = "MacPrint"
    pl["NSHighResolutionCapable"] = True
    pl["NSSupportsAutomaticGraphicsSwitching"] = True

    with open(plist_path, "wb") as f:
        plistlib.dump(pl, f)

    print(f"[OK] Đã cập nhật CFBundleDocumentTypes trong {plist_path}")

    # Register with macOS LaunchServices
    lsregister_path = "/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
    if os.path.exists(lsregister_path):
        try:
            subprocess.run([lsregister_path, "-f", app_path], check=True)
            print("[OK] Đã đăng ký MacPrint với macOS LaunchServices (Finder Open With).")
        except Exception as e:
            print(f"[Warning] Lỗi khi gọi lsregister: {e}")

    return True


if __name__ == "__main__":
    target_app = sys.argv[1] if len(sys.argv) > 1 else "dist/MacPrint.app"
    if os.path.exists(target_app):
        update_plist(target_app)
    else:
        print(f"Không tìm thấy file app tại {target_app}")
