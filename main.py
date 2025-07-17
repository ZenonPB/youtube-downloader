import sys
import os
import subprocess
import shutil
import zipfile
import urllib.request


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
    print("Installing dependencies...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Error installing {package}")
            return False
    return True


def ffmpeg_available():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except Exception:
        return False


def install_ffmpeg_windows(dest_dir="ffmpeg_bin"):

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(dest_dir, "ffmpeg.zip")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    print("Downloading FFmpeg...")
    urllib.request.urlretrieve(url, zip_path)

    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

    # Find the extracted ffmpeg folder
    bin_path = None
    for folder in os.listdir(dest_dir):
        if folder.startswith("ffmpeg") and os.path.isdir(os.path.join(dest_dir, folder)):
            bin_path = os.path.join(dest_dir, folder, "bin")
            break
    if not bin_path or not os.path.exists(bin_path):
        raise Exception("Could not locate FFmpeg bin folder after extraction.")

    # Add to PATH for this process
    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
    print(f"FFmpeg ready to use at: {bin_path}")

    # Clean up zip
    os.remove(zip_path)


def install_ffmpeg_if_needed():
    
    if ffmpeg_available():
        print("✅ FFmpeg found")
        return

    print("⚠️  FFmpeg not found!")
    print("Attempting automatic installation...")

    if sys.platform.startswith("win"):
        try:
            install_ffmpeg_windows()
            if ffmpeg_available():
                print("✅ FFmpeg installed and ready!")
            else:
                print("❌ FFmpeg installation failed. Please install manually.")
        except Exception as e:
            print(f"❌ Error installing FFmpeg: {e}")
            print("Please install FFmpeg manually from https://ffmpeg.org/download.html")
    elif sys.platform.startswith("linux"):
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"])
            if ffmpeg_available():
                print("✅ FFmpeg installed and ready!")
            else:
                print("❌ FFmpeg installation failed. Please install manually.")
        except Exception as e:
            print(f"❌ Error installing FFmpeg: {e}")
            print("Please install FFmpeg manually with: sudo apt install ffmpeg")
    elif sys.platform == "darwin":
        try:
            subprocess.run(["brew", "install", "ffmpeg"])
            if ffmpeg_available():
                print("✅ FFmpeg installed and ready!")
            else:
                print("❌ FFmpeg installation failed. Please install manually.")
        except Exception as e:
            print(f"❌ Error installing FFmpeg: {e}")
            print("Please install FFmpeg manually with: brew install ffmpeg")
    else:
        print("Automatic FFmpeg installation is not supported for this OS. Please install manually.")


def main():
    print("=" * 50)
    print("DadTunes - YouTube Music Downloader")
    print("=" * 50)


    # Check for dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        print("\u274c Missing dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        response = input("\nDo you want to install the dependencies automatically? (y/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            if install_dependencies(missing_packages):
                print("\u2705 All dependencies installed!")
            else:
                print("\u274c Error installing dependencies. Please install manually:")
                print("pip install customtkinter yt-dlp pillow requests")
                input("Press Enter to exit...")
                return
        else:
            print("Please install the dependencies manually:")
            print("pip install customtkinter yt-dlp pillow requests")
            input("Press Enter to exit...")
            return

    # Check and install FFmpeg if needed
    install_ffmpeg_if_needed()

    print("\n\ud83d\ude80 Starting DadTunes...")

    try:
        # Import and run the main application
        from gui import DadTunes
        app = DadTunes()
        app.mainloop()
    except ImportError as e:
        print(f"\u274c Error importing the application: {e}")
        print("Make sure the file 'gui.py' is present.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\u274c Unexpected error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()