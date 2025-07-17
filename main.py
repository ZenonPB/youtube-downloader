#!/usr/bin/env python3
"""
DadTunes - Downloader de Música do YouTube
Arquivo principal para executar a aplicação
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    required_packages = [
        'customtkinter',
        'yt-dlp',
        'pillow',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'pillow':
                import PIL
            elif package == 'customtkinter':
                import customtkinter
            elif package == 'yt-dlp':
                import yt_dlp
            elif package == 'requests':
                import requests
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    print("Instalando dependências...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} instalado com sucesso")
        except subprocess.CalledProcessError:
            print(f"✗ Erro ao instalar {package}")
            return False
    return True

def check_required_files():
    required_files = [
        'youtube_handler.py',
        'video_card.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def main():
    print("=" * 50)
    print("DadTunes - Downloader de Música do YouTube")
    print("=" * 50)
    
    # Check required files
    missing_files = check_required_files()
    if missing_files:
        print("❌ Arquivos em falta:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nCertifique-se de que todos os arquivos estão na mesma pasta.")
        input("Pressione Enter para sair...")
        return
    
    # Check dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        print("❌ Dependências em falta:")
        for package in missing_packages:
            print(f"   - {package}")
        
        response = input("\nDeseja instalar as dependências automaticamente? (s/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            if install_dependencies(missing_packages):
                print("✅ Todas as dependências foram instaladas!")
            else:
                print("❌ Erro ao instalar dependências. Instale manualmente:")
                print("pip install customtkinter yt-dlp pillow requests")
                input("Pressione Enter para sair...")
                return
        else:
            print("Instale as dependências manualmente:")
            print("pip install customtkinter yt-dlp pillow requests")
            input("Pressione Enter para sair...")
            return
    
    # Verify FFmpeg (necessary for audio conversion)
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg encontrado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg não encontrado!")
        print("Para converter vídeos para MP3, instale o FFmpeg:")
        print("- Windows: Baixe de https://ffmpeg.org/download.html")
        print("- Linux: sudo apt install ffmpeg")
        print("- macOS: brew install ffmpeg")
        print("\nA aplicação funcionará, mas sem conversão para MP3.")
        input("Pressione Enter para continuar...")
    
    print("\n🚀 Iniciando DadTunes...")
    
    try:
        # Import and run the main application
        from gui import DadTunes
        
        app = DadTunes()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro ao importar a aplicação: {e}")
        print("Certifique-se de que o arquivo 'dadtunes_app.py' está presente.")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()