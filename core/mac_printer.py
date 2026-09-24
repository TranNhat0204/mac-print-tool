"""
Compatibility alias for UniversalPrinterManager.
"""
from core.universal_printer import UniversalPrinterManager, PrinterInfo

# Alias for backward compatibility
MacPrinterManager = UniversalPrinterManager

__all__ = ["UniversalPrinterManager", "MacPrinterManager", "PrinterInfo"]
