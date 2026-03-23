import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import pyperclip
import os
import sys
import subprocess
import base64

try:
    import psutil
except ImportError:
    psutil = None

# --- Premium Theme Configuration (Strivon Navy x Purple) ---
ctk.set_appearance_mode("Dark")

BG_COLOR = "#05070a"         # Strivon darkest navy
CARD_BG = "#0f1420"          # Card navy
ACCENT_PRIMARY = "#a855f7"   # Strivon Purple (Accent)
ACCENT_HOVER = "#9333ea"     # Darker purple for hover
ACCENT_SECONDARY = "#3b82f6" # Strivon Blue
TEXT_COLOR = "#f8fafc"
TEXT_DIM = "#94a3b8"

PIPE_NAME = r"\\.\pipe\uoQcySKXSUxxJNpVQyatpHQwYoGfhcbh"

class MzkiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Mzki - Strivon Engine")
        self.geometry("1100x700")
        self.configure(fg_color=BG_COLOR)
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.attached_pid = None
        self.editors = {} # tab_name -> textbox

        # Build UI
        self.build_sidebar()
        self.build_main_area()
        
    def build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=CARD_BG, border_width=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        # Logo Area
        self.logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="ew")
        
        self.logo_icon = ctk.CTkLabel(
            self.logo_frame,
            text="S",
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
            text_color="#ffffff",
            fg_color=ACCENT_PRIMARY,
            corner_radius=8,
            width=40, height=40
        )
        self.logo_icon.pack(side="left")
        
        self.logo_text = ctk.CTkLabel(
            self.logo_frame, 
            text="MZKI V4", 
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.logo_text.pack(side="left", padx=(10, 0))
        
        self.sub_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Native C++ Execution Layer", 
            font=ctk.CTkFont(family="Inter", size=11, weight="normal"),
            text_color=ACCENT_SECONDARY
        )
        self.sub_label.grid(row=1, column=0, padx=20, pady=(0, 30), sticky="w")
        
        # Controls
        self.attach_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🔗 Attach Engine",
            font=ctk.CTkFont(family="Inter", weight="bold", size=14),
            fg_color=ACCENT_SECONDARY,
            hover_color="#2563eb",
            height=45,
            corner_radius=10,
            command=self.attach_event
        )
        self.attach_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.execute_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="▶ Execute Payload",
            font=ctk.CTkFont(family="Inter", weight="bold", size=14),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            height=45,
            corner_radius=10,
            command=self.execute_event
        )
        self.execute_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Tools Separator
        self.sep = ctk.CTkFrame(self.sidebar_frame, height=1, fg_color="#1e293b")
        self.sep.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        # Utility Buttons
        self.save_btn = ctk.CTkButton(
            self.sidebar_frame, text="💾 Save to File", fg_color="transparent", 
            border_width=1, border_color="#1e293b", text_color=TEXT_COLOR,
            hover_color="#1e293b", height=35, command=self.save_script
        )
        self.save_btn.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        self.open_btn = ctk.CTkButton(
            self.sidebar_frame, text="📁 Open File", fg_color="transparent", 
            border_width=1, border_color="#1e293b", text_color=TEXT_COLOR,
            hover_color="#1e293b", height=35, command=self.open_script
        )
        self.open_btn.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        # Status Label inside Sidebar at the bottom
        self.status_container = ctk.CTkFrame(self.sidebar_frame, fg_color="#1e293b", corner_radius=8)
        self.status_container.grid(row=8, column=0, padx=20, pady=20, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_container, 
            text="Status: Idle", 
            text_color=TEXT_DIM,
            font=ctk.CTkFont(family="Inter", size=12, weight="bold")
        )
        self.status_label.pack(padx=15, pady=10, anchor="w")

    def build_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Script Editor",
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.header_label.pack(side="left")

        self.new_tab_btn = ctk.CTkButton(
            self.header_frame, text="+ New Tab", width=100, height=30,
            fg_color="transparent", border_width=1, text_color=ACCENT_PRIMARY, border_color=ACCENT_PRIMARY,
            hover_color="rgba(168, 85, 247, 0.1)",
            command=lambda: self.add_tab(f"Script {len(self.editors)+1}")
        )
        self.new_tab_btn.pack(side="right")
        
        self.clear_btn = ctk.CTkButton(
            self.header_frame, text="Clear", width=80, height=30,
            fg_color="transparent", text_color=TEXT_DIM, hover_color="#1e293b",
            command=self.clear_script
        )
        self.clear_btn.pack(side="right", padx=10)
        
        # Tab View for Multiple Scripts
        self.tab_view = ctk.CTkTabview(
            self.main_frame,
            fg_color=CARD_BG,
            segmented_button_selected_color=ACCENT_PRIMARY,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            segmented_button_unselected_color=BG_COLOR,
            text_color=TEXT_COLOR,
            corner_radius=12
        )
        self.tab_view.grid(row=1, column=0, sticky="nsew")
        
        self.add_tab("Script 1")

    def add_tab(self, name):
        tab = self.tab_view.add(name)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        editor = ctk.CTkTextbox(
            tab,
            fg_color=BG_COLOR,
            text_color="#c3e88d", # Syntax-like color
            font=ctk.CTkFont(family="JetBrains Mono", size=14), # Better font for code
            border_spacing=10
        )
        editor.grid(row=0, column=0, sticky="nsew")
        if name == "Script 1":
            editor.insert("0.0", "-- Welcome to Mzki v4\n-- Strivon Labs Engine Active\n\nprint('Injecting into process...')\n")
        
        self.editors[name] = editor
        self.tab_view.set(name)

    def get_current_editor(self):
        current_tab = self.tab_view.get()
        return self.editors.get(current_tab)

    def attach_event(self):
        if not psutil:
            messagebox.showerror("Error", "psutil module is missing.")
            return

        self.status_label.configure(text="Status: Searching for Roblox...", text_color=ACCENT_SECONDARY)
        self.status_container.configure(fg_color="rgba(59, 130, 246, 0.1)")
        self.update()

        target_pid = None
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] == 'RobloxPlayerBeta.exe':
                    target_pid = proc.info['pid']
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if not target_pid:
            self.status_label.configure(text="Status: Target Not Found", text_color="#ef4444")
            self.status_container.configure(fg_color="rgba(239, 68, 68, 0.1)")
            messagebox.showwarning("Not Found", "Please open Roblox before attaching.")
            return

        self.status_label.configure(text=f"Status: Attaching to {target_pid}...", text_color=ACCENT_SECONDARY)
        self.update()

        # Check for Bin folder (we copy it alongside the program)
        bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        injector_path = os.path.join(bundle_dir, "Bin", "erto3e4rortoergn.exe")
        
        # Fallback to current working directory in case it's placed outside _MEIPASS
        if not os.path.exists(injector_path):
            injector_path = os.path.join(os.getcwd(), "Bin", "erto3e4rortoergn.exe")

        if not os.path.exists(injector_path):
            self.status_label.configure(text="Status: Dependency missing", text_color="#ef4444")
            self.status_container.configure(fg_color="rgba(239, 68, 68, 0.1)")
            messagebox.showerror("File Not Found", f"Could not find injector at:\n{injector_path}\nPlease make sure the Bin folder is next to Mzki.")
            return

        try:
            # Run silently
            subprocess.run(
                [injector_path, str(target_pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=0x08000000  # CREATE_NO_WINDOW
            )
            self.attached_pid = target_pid
            self.status_label.configure(text=f"Status: Attached ✅ ({self.attached_pid})", text_color="#10b981")
            self.status_container.configure(fg_color="rgba(16, 185, 129, 0.1)")
        except Exception as e:
            self.status_label.configure(text="Status: Attach Failed", text_color="#ef4444")
            self.status_container.configure(fg_color="rgba(239, 68, 68, 0.1)")
            messagebox.showerror("Error", f"Failed to run injector:\n{e}")

    def execute_event(self):
        editor = self.get_current_editor()
        if not editor: return
        
        code = editor.get("0.0", "end-1c")
        if not code.strip():
            return
            
        if not self.attached_pid:
            messagebox.showwarning("Not Attached", "Please attach to the target process first.")
            return
            
        pipe_path = f"{PIPE_NAME}_{self.attached_pid}"
        
        try:
            # Base64 encode script
            encoded_script = base64.b64encode(code.encode('utf-8')).decode('utf-8')
            
            with open(pipe_path, 'w') as pipe:
                pipe.write(encoded_script)
                
            self.status_label.configure(text="Status: Payload Executed", text_color=ACCENT_PRIMARY)
            self.status_container.configure(fg_color="rgba(168, 85, 247, 0.1)")
        except FileNotFoundError:
            self.status_label.configure(text="Status: Pipe Not Found", text_color="#ef4444")
            self.status_container.configure(fg_color="rgba(239, 68, 68, 0.1)")
            messagebox.showerror("Error", "Velocity named pipe not found. Are you still attached?")
        except Exception as e:
            self.status_label.configure(text="Status: Execution Error", text_color="#ef4444")
            self.status_container.configure(fg_color="rgba(239, 68, 68, 0.1)")
            messagebox.showerror("Error", f"Failed to execute script:\n{e}")

    def clear_script(self):
        editor = self.get_current_editor()
        if editor:
            editor.delete("0.0", "end")

    def open_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("Lua Scripts", "*.lua"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                editor = self.get_current_editor()
                if editor:
                    editor.delete("0.0", "end")
                    editor.insert("0.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file:\n{e}")

    def save_script(self):
        editor = self.get_current_editor()
        if not editor: return
        content = editor.get("0.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".lua", filetypes=[("Lua Scripts", "*.lua"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

if __name__ == "__main__":
    app = MzkiApp()
    app.mainloop()
