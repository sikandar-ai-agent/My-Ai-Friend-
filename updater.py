import os
import sys
import subprocess
import threading
import requests
import json
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ForcefulUpdater:
    def __init__(self, current_version="1.0.0", update_check_url=""):
        self.current_version = current_version
        self.update_check_url = update_check_url  # Yahan apni raw JSON file ka URL dein (e.g., GitHub raw link)
        self.is_updating = False

    def check_for_updates_forcefully(self):
        """Background thread mein system ko majboor karta hai ke update check kare"""
        if not self.update_check_url:
            return
        try:
            response = requests.get(self.update_check_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("version", self.current_version)
                apk_url = data.get("apk_url", "")
                force_update = data.get("force_update", True) # Forceful flag

                if latest_version != self.current_version and apk_url:
                    print(f"[UPDATER] New version {latest_version} detected. Forcing update...")
                    if force_update:
                        # Main UI thread par forced popup ya download shuru karein
                        Clock.schedule_once(lambda dt: self.trigger_forced_download(apk_url), 0)
        except Exception as e:
            print(f"[UPDATER] Update check failed: {e}")

    def trigger_forced_download(self, apk_url):
        """Sistem ko majboor karta hai ke app ke chalte hue update download kare"""
        if self.is_updating:
            return
        self.is_updating = True

        # UI par forceful warning dikhana taake user bypass na kar sakay
        content = Label(text="System Update Required!\nDownloading latest patch forcefully...", halign="center")
        popup = Popup(title="Critical System Update", content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        popup.open()

        # Background thread mein APK download aur install trigger karna
        def download_and_install():
            try:
                download_path = os.path.join(os.path.expanduser("~"), "downloaded_update.apk")
                print(f"[UPDATER] Downloading from {apk_url}...")
                
                req = requests.get(apk_url, stream=True)
                with open(download_path, "wb") as f:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                print("[UPDATER] Download complete. Forcing Android package installer...")
                popup.dismiss()

                # Android system ko majboor karna ke wo APK installer khol de
                if platform.platform() == 'android' or 'android' in sys.platform:
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Intent = autoclass('android.content.Intent')
                    Uri = autoclass('net.sf.androlua.Uri') # ya standard Uri
                    File = autoclass('java.io.File')
                    
                    # Android intent to install APK
                    # (Yeh background execution ko force karta hai)
                    os.system(f"am start -a android.intent.action.VIEW -d file://{download_path} -t application/vnd.android.package-archive")
            except Exception as e:
                print(f"[UPDATER] Forceful installation failed: {e}")
                self.is_updating = False

        threading.Thread(target=download_and_install, daemon=True).start()

    def start_background_guardian(self):
        """System run ke doran lagataar guardian thread chalata hai"""
        def guardian_loop():
            while True:
                self.check_for_updates_forcefully()
                # Har 10 minute baad system forcefully check karega
                threading.Event().wait(600)

        t = threading.Thread(target=guardian_loop, daemon=True)
        t.start()
