import os
import subprocess
import sys

def run_cmd(command):
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error executing {command}")
        sys.exit(result.returncode)

def fix_android_environment():
    android_home = os.path.expanduser("~/.android/sdk")
    os.environ["ANDROID_HOME"] = android_home
    
    # 1. Check and Setup Command-line Tools if missing
    cmdline_tools_path = os.path.join(android_home, "cmdline-tools", "latest", "bin", "sdkmanager")
    if not os.path.exists(cmdline_tools_path):
        print("SDK Manager missing! Auto-fixing and downloading command-line tools...")
        os.makedirs(os.path.join(android_home, "cmdline-tools"), exist_ok=True)
        run_cmd(f"cd {android_home}/cmdline-tools && curl -O https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip")
        run_cmd(f"cd {android_home}/cmdline-tools && unzip -o commandlinetools-linux-11076708_latest.zip && mv -f cmdline-tools latest")
    
    # 2. Auto-inject Licenses to prevent blockades
    licenses_dir = os.path.join(android_home, "licenses")
    os.makedirs(licenses_dir, exist_ok=True)
    with open(os.path.join(licenses_dir, "android-sdk-license"), "w") as f:
        f.write("24333f1a43ef661ef218c0130af61e545e1ebd1d\nd56f5187479451eabf01fb78af6dfcb131a6481e")
    with open(os.path.join(licenses_dir, "android-sdk-preview-license"), "w") as f:
        f.write("84831b9409646a918e30573bab4c9c91346d8abd")
    
    print("Environment auto-fixed successfully!")

if __name__ == "__main__":
    fix_android_environment()
    # Run buildozer with automatic self-healing environment
    run_cmd("buildozer -v android debug")
