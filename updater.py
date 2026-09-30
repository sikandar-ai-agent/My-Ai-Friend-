import os
import requests

class SelfUpdater:
    def __init__(self, update_url="https://raw.githubusercontent.com/sikandar-ai-agent/my-ai-friend/main/agent_core.py", target_file="agent_core.py"):
        self.update_url = update_url
        self.target_file = target_file

    def check_and_update(self):
        """Server se latest script download kar ke khud ko update karna"""
        try:
            print("Checking for updates...")
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                new_code = response.text
                # Purani file ko naye code se replace kar dena
                with open(self.target_file, "w", encoding="utf-8") as f:
                    f.write(new_code)
                return True, "Agent successfully updated itself!"
            else:
                return False, f"Failed to fetch update, status: {response.status_code}"
        except Exception as e:
            return False, f"Update error: {e}"
