import os
import json
import requests

class AgentCore:
    def __init__(self, memory_file="agent_memory.json"):
        self.memory_file = memory_file
        self.memory = self.load_memory()

    def load_memory(self):
        """فون کی لوکل اسٹوریج سے میموری لوڈ کرنا"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_memory(self):
        """میموری کو لوکل فائل میں محفوظ کرنا"""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Memory save error: {e}")

    def read_local_file(self, file_path):
        """فون کی کوئی بھی فائل ریڈ کرنے کے لیے"""
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            return "File nahi mili!"
        except Exception as e:
            return f"Error reading file: {e}"

    def chat_with_server(self, prompt, server_url="https://api.example.com/v1/chat"):
        """بغیر گوگل API کے کسٹم یا لوکل سرور سے بات چیت کرنے کا فنکشن"""
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"prompt": prompt, "memory": self.memory}
            
            response = requests.post(server_url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "Server se sahi jawab nahi mila.")
            else:
                return f"Server Error: {response.status_code}"
        except Exception as e:
            return f"[Offline Mode Active] انٹرنیٹ کنکشن دستیاب نہیں ہے یا سرور آف ہے۔ (Error: {e})"
