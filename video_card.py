import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import requests
import threading
from io import BytesIO
from icons import Icons

class VideoItem(ctk.CTkFrame):
    def __init__(self, parent, video_info, on_download=None, on_remove=None):
        super().__init__(parent)
        self.video_info = video_info
        self.on_download = on_download
        self.on_remove = on_remove
        self.thumbnail_image = None
        self._setup_ui()
        self._load_thumbnail_async()

    def _setup_ui(self):
        self.configure(height=100, corner_radius=10)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Thumbnail
        self.thumbnail_label = ctk.CTkLabel(
            self,
            text=Icons.get("music"),
            font=("Arial", 20),
            width=80,
            height=80,
            corner_radius=8
        )
        self.thumbnail_label.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")

        # Information frame
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_rowconfigure(0, weight=1)

        # Information container
        info_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_container.grid(row=0, column=0, sticky="nsew")
        info_container.grid_columnconfigure(0, weight=1)

        # Title
        title_text = self._truncate_text(self.video_info.get('title', ''), 60)
        self.title_label = ctk.CTkLabel(
            info_container,
            text=title_text,
            font=("Arial", 14, "bold"),
            anchor="w",
            justify="left"
        )
        self.title_label.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        # Uploader
        uploader_text = self._truncate_text(self.video_info.get('uploader', ''), 30)
        self.uploader_label = ctk.CTkLabel(
            info_container,
            text=f"Por: {uploader_text}",
            font=("Arial", 11),
            text_color="gray70",
            anchor="w",
            justify="left"
        )
        self.uploader_label.grid(row=1, column=0, pady=(0, 2), sticky="ew")

        # Upload date
        upload_date = self.video_info.get('upload_date')
        if upload_date:
            self.upload_date_label = ctk.CTkLabel(
                info_container,
                text=f"Publicado em: {upload_date}",
                font=("Arial", 11),
                text_color="gray70",
                anchor="w",
                justify="left"
            )
            self.upload_date_label.grid(row=2, column=0, pady=(0, 2), sticky="ew")

        # Duration
        duration = self.video_info.get('duration')
        if duration:
            self.duration_label = ctk.CTkLabel(
                info_container,
                text=f"Duração: {duration}",
                font=("Arial", 11),
                text_color="gray70",
                anchor="w",
                justify="left"
            )
            self.duration_label.grid(row=3, column=0, pady=(0, 2), sticky="ew")

        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            info_container,
            height=8,
            progress_color="green",
        )
        self.progress_bar.grid(row=3, column=0, pady=(5, 0), sticky="ew")
        self.progress_bar.grid_remove()

        # Status
        self.status_label = ctk.CTkLabel(
            info_container,
            text="",
            font=("Arial", 9),
            text_color="gray50",
            justify="left"
        )
        self.status_label.grid(row=4, column=0, pady=(0, 2), sticky="ew")
        self.status_label.grid_remove()

        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, padx=15, pady=10)

        # Download button
        self.download_button = ctk.CTkButton(
            buttons_frame,
            text=Icons.get("download"),
            font=("Arial", 16),
            width=45,
            height=35,
            command=self._on_download_clicked,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.download_button.grid(row=0, column=0, padx=(0, 5))

        # Remove button
        self.remove_button = ctk.CTkButton(
            buttons_frame,
            text=Icons.get("trash"),
            font=("Arial", 16),
            width=45,
            height=35,
            command=self._on_remove_clicked,
            fg_color="red",
            hover_color="darkred"
        )
        self.remove_button.grid(row=0, column=1)

    @staticmethod
    def _truncate_text(text, max_length):
        return text[:max_length] + "..." if len(text) > max_length else text

    def _load_thumbnail_async(self):
        url = self.video_info.get('thumbnail')
        if not url:
            return
        def load_image():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image = image.resize((80, 60), Image.Resampling.LANCZOS)
                    # Usar CTkImage para compatibilidade com HighDPI
                    photo = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
                    self.after(0, lambda: self._update_thumbnail(photo))
            except Exception as e:
                print(f"Erro ao carregar a thumbnail: {e}")
        threading.Thread(target=load_image, daemon=True).start()

    def _update_thumbnail(self, photo):
        self.thumbnail_image = photo
        self.thumbnail_label.configure(image=photo, text="")

    def _on_download_clicked(self):
        if self.on_download:
            self.set_downloading_state(True)
            self.on_download(self.video_info, self._on_download_progress, self._on_download_complete)

    def _on_remove_clicked(self):
        if self.on_remove:
            self.on_remove(self)

    def set_downloading_state(self, downloading):
        if downloading:
            self.download_button.configure(
                text=Icons.get("loading"),
                state="disabled",
            )
            self.remove_button.configure(state="disabled")
            self.progress_bar.grid()
            self.status_label.grid()
            self.status_label.configure(text="Baixando...")
        else:
            self.download_button.configure(
                text=Icons.get("download"),
                state="normal",
            )
            self.remove_button.configure(state="normal")
            self.progress_bar.grid_remove()
            self.status_label.grid_remove()

    def _on_download_progress(self, progress):
        self.progress_bar.set(progress / 100)
        self.status_label.configure(text=f"Baixando... {progress:.1f}%")

    def _on_download_complete(self, success, message):
        self.set_downloading_state(False)
        if success:
            self.status_label.configure(text=f"{Icons.get('check')} {message}", text_color="green")
            self.status_label.grid()
            self.after(3000, lambda: self.status_label.grid_remove())
        else:
            self.status_label.configure(text=f"{Icons.get('error')} {message}", text_color="red")
            self.status_label.grid()
            self.after(5000, lambda: self.status_label.grid_remove())