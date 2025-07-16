import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from pathlib import Path

from youtube_handler import YoutubeHandler
from video_card import VideoItem, Icons

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class ProgressDialog(ctk.CTkToplevel):
    def __init__(self, parent, total_videos):
        super().__init__(parent)

        self.title("Baixando vídeos...")
        self.geometry("400x200")
        self.resizable(False, False)

        # Center the dialog
        self.transient(parent)
        self.grab_set()

        self.total_videos = total_videos
        self.current_video = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=f"Baixando {self.total_videos} vídeos...",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=20)

        self.overall_label = ctk.CTkLabel(
            self,
            text="Vídeo 0 de {self.total_videos}",
            font=("Arial", 12)
        )
        self.overall_label.pack(pady=5)

        self.overall_progress = ctk.CTkProgressBar(
            self,
            width=300,
        )
        self.overall_progress.pack(pady=10)
        self.overall_progress.set(0)

        # Actual video
        self.actual_label = ctk.CTkLabel(
            self,
            text="Aguardando...",
            font=("Arial", 11),
            text_color="gray70",
        )
        self.actual_label.pack(pady=5)

        # Cancel button
        self.cancel_button = ctk.CTkButton(
            self,
            text="Cancelar",
            command=self.cancel_download,
            fg_color="red",
            hover_color="darkred",
        )
        self.cancel_button.pack(pady=20)
        self.cancelled = False
        
    def update_progress(self, progress, current_video, video_num, total):
        self.overall_progress.set(progress/100)
        self.overall_label.configure(text=f"Vídeo {video_num} de {total}")

        if len(current_video) > 40:
            current_video = current_video[:37] + "..."

        self.actual_label.configure(text=f"Baixando: {current_video}")
    
    def cancel_download(self):
        self.cancelled = True
        self.destroy()
