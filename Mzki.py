import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pyperclip
import os
import sys

# Attempt to load VelocityAPI using PythonNet
try:
    import clr
    # We will assume VelocityAPI.dll is in the same directory or adjust the path.
    # For now, this is just the UI skeleton with pink x blue theme.
    velocity_loaded = False
except ImportError:
    velocity_loaded = False

# --- Theme Configuration (Pink x Blue) ---
# We will use a custom theme by setting colors directly or overriding ctk defaults.
ctk.set_appearance_mode("Dark")

BG_COLOR = "#0b0f19"         # Deep dark blue background
CARD_BG = "#131a2a"          # Slightly lighter blue for cards
ACCENT_PINK = "#ec4899"      # Vibrant pink
ACCENT_BLUE = "#3b82f6"      # Bright blue
TEXT_COLOR = "#f8fafc"
TEXT_DIM = "#94a3b8"

class MzkiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Mzki - Powered by Strivon Labs")
        self.geometry("1100x700")
        self.configure(fg_color=BG_COLOR)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Build UI
        self.build_sidebar()
        self.build_main_area()
        
    def build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=CARD_BG)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Logo Area
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🌸 MZKI ⚡", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=ACCENT_PINK
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5), sticky="w")
        
        self.sub_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Velocity Injector • Strivon Labs", 
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal"),
            text_color=ACCENT_BLUE
        )
        self.sub_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        
        # Controls
        self.attach_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🔗 Attach (Velocity)",
            font=ctk.CTkFont(weight="bold"),
            fg_color=ACCENT_BLUE,
            hover_color="#2563eb",
            height=40,
            command=self.attach_event
        )
        self.attach_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.execute_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="▶ Execute Script",
            font=ctk.CTkFont(weight="bold"),
            fg_color=ACCENT_PINK,
            hover_color="#db2777",
            height=40,
            command=self.execute_event
        )
        self.execute_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Status Label inside Sidebar at the bottom
        self.status_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Status: Not Attached", 
            text_color=TEXT_DIM,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=5, column=0, padx=20, pady=20, sticky="sw")

    def build_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame,
            text="Script Editor",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Textbox Editor with Pink Border
        self.editor = ctk.CTkTextbox(
            self.main_frame,
            fg_color=CARD_BG,
            text_color=TEXT_COLOR,
            border_color=ACCENT_PINK,
            border_width=2,
            font=ctk.CTkFont(family="Consolas", size=14)
        )
        self.editor.grid(row=1, column=0, sticky="nsew")
        self.editor.insert("0.0", "-- Welcome to Mzki\n-- Powered by Velocity erto Injector\n\nprint('Mzki Loaded!')\n")
        
        # Additional Tools Frame
        self.tools_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tools_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        self.clear_btn = ctk.CTkButton(
            self.tools_frame, text="Clear", width=80, 
            fg_color="transparent", border_width=1, text_color=TEXT_COLOR,
            command=lambda: self.editor.delete("0.0", "end")
        )
        self.clear_btn.pack(side="left", padx=(0, 10))

        self.copy_btn = ctk.CTkButton(
            self.tools_frame, text="Copy URL/Script", width=120, 
            fg_color="transparent", border_width=1, text_color=TEXT_COLOR, border_color=ACCENT_BLUE,
            command=self.copy_script
        )
        self.copy_btn.pack(side="left")

    def attach_event(self):
        self.status_label.configure(text="Status: Attaching...", text_color=ACCENT_BLUE)
        # Logic to call VelAPI.Attach() will go here
        self.after(1500, lambda: self.status_label.configure(text="Status: Attached ✅", text_color="#4ade80"))

    def execute_event(self):
        # Logic to call VelAPI.Execute() will go here
        code = self.editor.get("0.0", "end")
        print("Executing code:", code)
        self.status_label.configure(text="Status: Executed Script", text_color=ACCENT_PINK)

    def copy_script(self):
        code = self.editor.get("0.0", "end")
        pyperclip.copy(code)
        messagebox.showinfo("Copied", "Script copied to clipboard.")

if __name__ == "__main__":
    app = MzkiApp()
    app.mainloop()
