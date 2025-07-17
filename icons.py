import tkinter as tk
from PIL import Image, ImageTk
import os

class Icons:
    _icon_chars = {
        "search": "🔍",
        "folder": "📁",
        "download": "⬇",
        "trash": "🗑",
        "music": "🎵",
        "play": "▶",
        "list": "📋",
        "check": "✓",
        "error": "✗",
        "info": "ℹ",
        "loading": "⟳"
    }

    @staticmethod
    def get(icon_name):
        return Icons._icon_chars.get(icon_name, "?") 