import os
import zipfile
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import keyboard  # Requires 'pip install keyboard'
import pygame    # Requires 'pip install pygame' for audio sync

# === CONFIGURATION ===
# Default keybinds for 4K Mania
KEYBINDS = ['d', 'f', 'j', 'k']
COLUMNS = 4
HIT_WINDOW = 0.005  # Tight tolerance for "Perfect" hits

class OsuManiaPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Strivon Labs | Osu! Mania PFC Tool")
        self.root.geometry("400x300")
        self.root.configure(bg="#0f172a")

        # UI Elements
        self.label = tk.Label(self.root, text="Strivon Osu! Mania Auto-Player", font=("Arial", 14, "bold"), fg="#f472b6", bg="#0f172a")
        self.label.pack(pady=20)

        self.btn_select = tk.Button(self.root, text="Select .osz File", command=self.load_osz, bg="#334155", fg="white", font=("Arial", 10), padx=20, pady=10)
        self.btn_select.pack(pady=10)

        self.status = tk.Label(self.root, text="Status: Ready", fg="#94a3b8", bg="#0f172a")
        self.status.pack(pady=20)

        self.objects = []
        self.audio_path = ""
        self.is_playing = False

        pygame.mixer.init()

    def load_osz(self):
        file_path = filedialog.askopenfilename(filetypes=[("Osu! Beatmap", "*.osz")])
        if not file_path:
            return

        self.status.config(text="Status: Extracting...")
        temp_dir = "temp_beatmap"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find .osu file (prefer highest difficulty)
        osu_files = [f for f in os.listdir(temp_dir) if f.endswith(".osu")]
        if not osu_files:
            messagebox.showerror("Error", "No .osu files found in package.")
            return

        # Simple heuristic: longest filename or last in list for difficulty
        osu_file = os.path.join(temp_dir, osu_files[-1])
        self.parse_osu(osu_file)
        self.status.config(text=f"Status: Loaded {osu_files[-1]}")

    def parse_osu(self, path):
        self.objects = []
        section = ""
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if line.startswith("["):
                    section = line
                    continue
                
                if section == "[General]":
                    if line.startswith("AudioFilename:"):
                        self.audio_path = os.path.join("temp_beatmap", line.split(":")[1].strip())
                
                if section == "[HitObjects]":
                    parts = line.split(",")
                    if len(parts) >= 3:
                        x = int(parts[0])
                        t = int(parts[2])
                        col = int(x * COLUMNS / 512)
                        if col >= COLUMNS: col = COLUMNS - 1
                        
                        # Check for slider (long note)
                        is_slider = ":" in parts[5] if len(parts) > 5 else False
                        end_t = t
                        if is_slider:
                            end_t = int(parts[5].split(":")[0])
                        
                        self.objects.append({'time': t, 'col': col, 'end_t': end_t})

        # Start playback thread
        threading.Thread(target=self.play_logic, daemon=True).start()

    def play_logic(self):
        if not os.path.exists(self.audio_path):
            messagebox.showerror("Error", "Audio file not found in package.")
            return

        self.status.config(text="Status: Starting in 3s... Focus Osu!")
        time.sleep(3)
        
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()
        start_time = time.time() * 1000

        self.is_playing = True
        idx = 0
        active_sliders = []

        while self.is_playing and idx < len(self.objects):
            curr_time = (time.time() * 1000) - start_time
            obj = self.objects[idx]

            # Handle hit
            if curr_time >= obj['time']:
                key = KEYBINDS[obj['col']]
                keyboard.press(key)
                
                if obj['end_t'] > obj['time']:
                    # Slider: Hold until end
                    active_sliders.append({'key': key, 'end_t': obj['end_t']})
                else:
                    # Circle: Quick release
                    time.sleep(0.01)
                    keyboard.release(key)
                
                idx += 1

            # Handle slider releases
            for slider in active_sliders[:]:
                if curr_time >= slider['end_t']:
                    keyboard.release(slider['key'])
                    active_sliders.remove(slider)
            
            time.sleep(0.001) # Poll fast

        self.status.config(text="Status: Finished")
        self.is_playing = False

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = OsuManiaPlayer()
    app.run()
