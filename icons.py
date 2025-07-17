import tkinter as tk
from PIL import Image, ImageTk
import os

class Icons:
    @staticmethod
    def get(icon_name):
        icon_chars = {
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
        return icon_chars.get(icon_name, "?") 