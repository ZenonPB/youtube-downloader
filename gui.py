import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from pathlib import Path

from youtube_handler import YoutubeHandler
from video_card import VideoItem
from icons import Icons

# Configuração do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Configurar fonte que suporte emojis
try:
    # Tentar usar uma fonte que suporte emojis
    ctk.FontManager.load_font("C:/Windows/Fonts/seguiemj.ttf")
except:
    try:
        ctk.FontManager.load_font("C:/Windows/Fonts/arial.ttf")
    except:
        pass

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

class DadTunes(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DadTunes V1.0")
        self.geometry("900x700")
        self.resizable(False, False)

        self.youtube_handler = YoutubeHandler()

        self.destination_folder = tk.StringVar(value="Selecione uma pasta")
        self.video_list = []
        self.video_items = []

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, height=120, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)

        input_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=15)
        input_frame.grid_columnconfigure(0, weight=1)

        # URL input
        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Cole aqui a URL do youtube aqui (ex: https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
            height=40,
            font=("Arial", 12)
        )
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.url_entry.bind("<Return>", lambda event: self.search_video())

        # Search button
        self.search_button = ctk.CTkButton(
            input_frame,
            text=Icons.get("search"),
            width=50,
            height=40,
            command=self.search_video,
            font=("Arial", 16)
        )
        self.search_button.grid(row=0, column=1, padx=(0, 10))

        # Destination folder
        self.destination_button = ctk.CTkButton(
            input_frame,
            text=Icons.get("folder"),
            width=50,
            height=40,
            command=self.select_destination,
            font=("Arial", 16)
        )
        self.destination_button.grid(row=0, column=2)

        # Destination label
        self.destination_label = ctk.CTkLabel(
            input_frame,
            textvariable=self.destination_folder,
            font=("Arial", 11),
            text_color="gray70"
        )
        self.destination_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        title_container = ctk.CTkFrame(self, fg_color="transparent")
        title_container.pack(fill="x", padx=20, pady=(0, 10))
        title_container.grid_columnconfigure(0, weight=1)

        # Setlist title
        self.title_label = ctk.CTkLabel(
            title_container,
            text="Sua Setlist",
            font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Video counter
        self.video_counter_label = ctk.CTkLabel(
            title_container,
            text="0 vídeos",
            font=("Arial", 12),
            text_color="gray60"
        )
        self.video_counter_label.grid(row=0, column=1, sticky="e")

        self.setup_scrollable_frame()

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=20)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # Clear setlist button
        self.clear_button = ctk.CTkButton(
            bottom_frame,
            text=f"{Icons.get('trash')} Limpar Setlist",
            height=50,
            font=("Arial", 16),
            command=self.clear_setlist,
            fg_color="orange",
            hover_color="darkorange",
        )
        self.clear_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Download button
        self.download_button = ctk.CTkButton(
            bottom_frame,
            text=f"{Icons.get('download')} Baixar Todas",
            height=50,
            font=("Arial", 16, "bold"),
            command=self.download_all,
            fg_color="green",
            hover_color="darkgreen",
        )
        self.download_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        self.update_ui_state()
    
    def setup_scrollable_frame(self):
        container = ctk.CTkFrame(self, corner_radius=15)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            container,
            corner_radius=10,
            scrollbar_button_color="gray30",
            scrollbar_button_hover_color="gray20"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.empty_label = ctk.CTkLabel(
            container,
            text="Nenhuma música adicionada ainda.\nCole uma URL do YouTube acima e clique em 🔍",
            font=("Arial", 14),
            text_color="gray60",
        )
        self.empty_label.pack(pady=50)

    def update_ui_state(self):
        has_videos = len(self.video_list) > 0
        has_destination = self.destination_folder.get() != "Selecione uma pasta"

        count_text = f"{len(self.video_list)} vídeo(s)" if has_videos else ""
        self.video_counter_label.configure(text=count_text)
        
        self.clear_button.configure(state="normal" if has_videos else "disabled")
        self.download_button.configure(state="normal" if has_videos and has_destination else "disabled")

        if has_videos:
            self.empty_label.pack_forget()
        else:
            self.empty_label.pack(pady=50)
    
    def select_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder.set(folder)
            self.update_ui_state()
    
    def clear_setlist(self):
        if self.video_list:
            result = messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar toda a setlist?")
            if result:
                for item in self.video_items:
                    item.destroy()
                self.video_items.clear()
                self.video_list.clear()
                self.update_ui_state()
    
    def search_video(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Atenção", "Por favor, insira uma URL válida do YouTube")
            return
        
        if not self.youtube_handler.is_valid_url(url):
            messagebox.showwarning("Atenção", "URL inválida. Por favor, insira uma URL válida do YouTube")
            return

        for video in self.video_list:
            if video["url"] == url:
                messagebox.showwarning("Atenção", "Esta música já está na setlist")
                return
            
        self.search_button.configure(state="disabled", text=Icons.get("loading"))
        self.url_entry.configure(state="disabled")
        
        # Start search thread
        threading.Thread(target=self.search_thread, args=(url,), daemon=True).start()

    def search_thread(self, url):
        try:
            self.youtube_handler.set_url(url)
            video_info = self.youtube_handler.get_info()

            if video_info:
                self.after(0, lambda: self.add_video_to_setlist(video_info))
            else:
                self.after(0, lambda: self.on_search_error("Não foi possível obter informações do vídeo"))
        except Exception as e:
            self.after(0, lambda: self.on_search_error(f"Erro ao buscar vídeo: {str(e)}"))
        finally:
            self.after(0, self.reset_search_button)

    def on_search_error(self, message):
        messagebox.showerror("Erro", message)
        self.reset_search_button()

    def reset_search_button(self):
        self.search_button.configure(state="normal", text=Icons.get("search"))
        self.url_entry.configure(state="normal")
    
    def add_video_to_setlist(self, video_info):
        self.video_list.append(video_info)

        video_item = VideoItem(
            self.scrollable_frame,
            video_info,
            on_remove = self.remove_video_item,
            on_download = self.download_single_video,
        )
        video_item.grid(row=len(self.video_items), column=0, pady=5, padx=10, sticky="ew")
        self.video_items.append(video_item)

        self.url_entry.delete(0, tk.END)
        self.update_ui_state()

        messagebox.showinfo("Sucesso", f"Música adicionada com sucesso! {video_info['title']}")

    def remove_video_item(self, video_item):
        if video_item in self.video_items:
            video_info = video_item.video_info
            if video_info in self.video_list:
                self.video_list.remove(video_info)

            video_item.destroy()
            self.video_items.remove(video_item)

            for i, item in enumerate(self.video_items):
                item.grid(row=i, column=0, pady=5, padx=10, sticky="ew")

            self.update_ui_state()

    def download_single_video(self, video_info, progress_callback=None, complete_callback=None):
        if self.destination_folder.get() == "Selecione uma pasta":
            messagebox.showwarning("Atenção", "Por favor, selecione uma pasta de destino antes de baixar")
            if complete_callback:
                complete_callback(False, "Destino não selecionado")
            return

        def download_thread():
            try:
                self.youtube_handler.set_destination(self.destination_folder.get())
                self.youtube_handler.set_url(video_info["url"])

                def progress_hook(progress):
                    if progress_callback is not None:
                        self.after(0, lambda: progress_callback(progress) if progress_callback else None)
                    
                success, message = self.youtube_handler.download(progress_hook)

                if complete_callback is not None:
                    self.after(0, lambda: complete_callback(success, message) if complete_callback else None)
            
            except Exception as e:
                if complete_callback is not None:
                    self.after(0, lambda: complete_callback(False, f"Erro ao baixar: {str(e)}") if complete_callback else None)

        threading.Thread(target=download_thread, daemon=True).start()

    def download_all(self):
        if not self.video_list:
            messagebox.showwarning("Atenção", "Nenhuma música na setlist para baixar")
            return
            
        if self.destination_folder.get() == "Selecione uma pasta":
            messagebox.showwarning("Atenção", "Por favor, selecione uma pasta de destino antes de baixar")
            return
            
        progress_dialog = ProgressDialog(self, len(self.video_list))

        self.download_button.configure(state="disabled", text=Icons.get("loading"))
        self.clear_button.configure(state="disabled")

        def download_all_thread():
            try:
                self.youtube_handler.set_destination(self.destination_folder.get())

                def progress_hook(progress, current_video, video_num, total):
                    if hasattr(progress_dialog, "cancelled") and progress_dialog.cancelled:
                        return False
                        
                    self.after(0, lambda: progress_dialog.update_progress(progress, current_video, video_num, total))
                    return True
                    
                # Simular download múltiplo já que o método não existe
                successful_downloads = 0
                failed_downloads = []
                
                for i, video in enumerate(self.video_list):
                    try:
                        self.youtube_handler.set_url(video["url"])
                        success, message = self.youtube_handler.download(lambda p: progress_hook(p, video["title"], i+1, len(self.video_list)))
                        if success:
                            successful_downloads += 1
                        else:
                            failed_downloads.append({"title": video["title"], "error": message})
                    except Exception as e:
                        failed_downloads.append({"title": video["title"], "error": str(e)})

                self.after(0, lambda: progress_dialog.destroy() if hasattr(progress_dialog, 'winfo_exists') and progress_dialog.winfo_exists() else None)
                if successful_downloads == len(self.video_list):
                    self.after(0, lambda: messagebox.showinfo("Sucesso", "Todas as músicas foram baixadas com sucesso!"))

                elif successful_downloads > 0:
                    failed_list = "\n".join([f"• {item['title']}: {item['error']}" for item in failed_downloads])
                    self.after(0, lambda: messagebox.showwarning("Atenção", f"Algumas músicas não foram baixadas:\n\n{failed_list}"))
                    
                else:
                    failed_list = "\n".join([f"• {item['title']}: {item['error']}" for item in failed_downloads])
                    self.after(0, lambda: messagebox.showerror("Erro", f"Nenhuma música foi baixada:\n\n{failed_list}"))

            except Exception as e:
                self.after(0, lambda: progress_dialog.destroy() if hasattr(progress_dialog, 'winfo_exists') and progress_dialog.winfo_exists() else None)
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro ao baixar: {str(e)}"))
            finally:
                self.after(0, lambda: self.download_button.configure(state="normal", text=f"{Icons.get('download')} Baixar Todas"))
                self.after(0, lambda: self.clear_button.configure(state="normal"))

        threading.Thread(target=download_all_thread, daemon=True).start()

if __name__ == "__main__":
    app = DadTunes()
    app.mainloop()