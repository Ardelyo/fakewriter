import customtkinter as ctk
import tkinter as tk
import time
import threading
from core.state_manager import StateManager
from gui.floating_widget import FloatingWidget

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.state_manager = StateManager()
        
        # Window Setup
        self.title("FakeWriter")
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Icon
        import os
        if os.path.exists("assets/icon.ico"):
            self.iconbitmap("assets/icon.ico")
        
        # Theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Text area
        self.grid_rowconfigure(1, weight=0) # Settings
        self.grid_rowconfigure(2, weight=0) # Smart Settings
        self.grid_rowconfigure(3, weight=0) # Controls
        self.grid_rowconfigure(4, weight=0) # Debug
        self.grid_rowconfigure(5, weight=0) # Status bar
        
        # --- TEXT INPUT AREA ---
        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        
        self.text_box = ctk.CTkTextbox(self.text_frame, font=("Consolas", 12))
        self.text_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.text_box.insert("0.0", "Enter text to type here...")
        
        # --- SETTINGS PANEL ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Backspace Mode
        self.bs_label = ctk.CTkLabel(self.settings_frame, text="Backspace Mode:", font=("Segoe UI", 12, "bold"))
        self.bs_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.bs_var = tk.StringVar(value=StateManager.MODE_BACKSPACE_NATURAL)
        self.bs_natural = ctk.CTkRadioButton(self.settings_frame, text="Natural", variable=self.bs_var, value=StateManager.MODE_BACKSPACE_NATURAL, command=self.update_settings)
        self.bs_strict = ctk.CTkRadioButton(self.settings_frame, text="Strict", variable=self.bs_var, value=StateManager.MODE_BACKSPACE_STRICT, command=self.update_settings)
        self.bs_autotypo = ctk.CTkRadioButton(self.settings_frame, text="Auto-Typo", variable=self.bs_var, value=StateManager.MODE_BACKSPACE_AUTOTYPO, command=self.update_settings)
        
        self.bs_natural.grid(row=0, column=1, padx=5, pady=5)
        self.bs_strict.grid(row=0, column=2, padx=5, pady=5)
        self.bs_autotypo.grid(row=0, column=3, padx=5, pady=5)
        
        # End Behavior
        self.end_label = ctk.CTkLabel(self.settings_frame, text="End Behavior:", font=("Segoe UI", 12, "bold"))
        self.end_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.end_var = tk.StringVar(value=StateManager.END_BEHAVIOR_STOP)
        self.end_stop = ctk.CTkRadioButton(self.settings_frame, text="Stop", variable=self.end_var, value=StateManager.END_BEHAVIOR_STOP, command=self.update_settings)
        self.end_loop = ctk.CTkRadioButton(self.settings_frame, text="Loop", variable=self.end_var, value=StateManager.END_BEHAVIOR_LOOP, command=self.update_settings)
        self.end_stop.grid(row=1, column=1, padx=5, pady=5)
        self.end_loop.grid(row=1, column=2, padx=5, pady=5)
        
        # Target App
        self.target_label = ctk.CTkLabel(self.settings_frame, text="Target App:", font=("Segoe UI", 12, "bold"))
        self.target_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.target_mode_var = tk.StringVar(value="All")
        self.target_mode_combo = ctk.CTkComboBox(self.settings_frame, values=["All", "Whitelist", "Blacklist"], variable=self.target_mode_var, command=self.update_settings)
        self.target_mode_combo.grid(row=2, column=1, padx=5, pady=5)
        
        self.target_apps_entry = ctk.CTkEntry(self.settings_frame, placeholder_text="notepad.exe, code.exe")
        self.target_apps_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        self.settings_frame.grid_columnconfigure(2, weight=1)
        self.target_apps_entry.bind("<FocusOut>", lambda e: self.update_settings())

        # --- SMART SETTINGS ---
        self.smart_frame = ctk.CTkFrame(self)
        self.smart_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.smart_frame.grid_columnconfigure(1, weight=1)

        self.stealth_var = tk.BooleanVar(value=False)
        self.stealth_switch = ctk.CTkSwitch(self.smart_frame, text="Stealth Mode", variable=self.stealth_var, command=self.update_settings)
        self.stealth_switch.grid(row=0, column=0, padx=10, pady=10)

        self.speed_label = ctk.CTkLabel(self.smart_frame, text="Speed: 60 WPM", font=("Segoe UI", 12))
        self.speed_label.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="e")
        
        self.speed_slider = ctk.CTkSlider(self.smart_frame, from_=20, to=200, number_of_steps=18, command=self.update_speed_label)
        self.speed_slider.set(60)
        self.speed_slider.grid(row=0, column=2, padx=10, pady=10)

        # --- CONTROLS ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        self.controls_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.btn_start = ctk.CTkButton(self.controls_frame, text="START (F12)", command=self.start_typing, fg_color="#2cc985", hover_color="#25a870")
        self.btn_start.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.btn_pause = ctk.CTkButton(self.controls_frame, text="PAUSE", command=self.pause_typing, fg_color="#f2a900", hover_color="#c98c00")
        self.btn_pause.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.btn_stop = ctk.CTkButton(self.controls_frame, text="STOP", command=self.stop_typing, fg_color="#cf3838", hover_color="#a82d2d")
        self.btn_stop.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # --- DEBUG ---
        self.btn_test = ctk.CTkButton(self, text="DEBUG: SELF TEST (2s delay)", command=self.run_self_test, fg_color="#555555")
        self.btn_test.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # --- STATUS BAR ---
        self.status_bar = ctk.CTkLabel(self, text="Ready | Hotkey: F12 to Toggle", anchor="w", padx=10)
        self.status_bar.grid(row=5, column=0, sticky="ew")

        # Floating Widget
        self.floating_widget = FloatingWidget(self)
        self.floating_widget.withdraw() # Start hidden
        
        # Periodic Update
        self.update_ui_state()

    def update_speed_label(self, value):
        self.speed_label.configure(text=f"Speed: {int(value)} WPM")
        self.update_settings()

    def update_settings(self, *args):
        self.state_manager.backspace_mode = self.bs_var.get()
        self.state_manager.end_behavior = self.end_var.get()
        self.state_manager.target_app_mode = self.target_mode_var.get()
        self.state_manager.stealth_mode = self.stealth_var.get()
        self.state_manager.typing_speed_wpm = int(self.speed_slider.get())
        
        apps_str = self.target_apps_entry.get()
        self.state_manager.target_apps = [s.strip() for s in apps_str.split(",") if s.strip()]

    def run_self_test(self):
        """Sends 'Test' to active window after 2 seconds."""
        def task():
            time.sleep(2)
            from core.character_injector import send_unicode_char
            for c in "Self Test Working!":
                send_unicode_char(c)
                time.sleep(0.01)
        
        threading.Thread(target=task, daemon=True).start()

    def start_typing(self):
        text = self.text_box.get("0.0", "end-1c")
        if not text.strip():
            return
            
        self.state_manager.set_text_queue([text])
        self.state_manager.set_active(True)
        self.update_settings()

    def pause_typing(self):
        self.state_manager.toggle_active()

    def stop_typing(self):
        self.state_manager.set_active(False)
        self.state_manager.reset_progress()

    def update_ui_state(self):
        status = self.state_manager.status
        self.status_bar.configure(text=f"Status: {status} | Hotkey: F12 to Toggle")
        
        if status == StateManager.STATUS_ACTIVE:
            self.btn_start.configure(state="disabled")
            self.btn_pause.configure(state="normal", text="PAUSE")
            self.btn_stop.configure(state="normal")
            if not self.state_manager.stealth_mode:
                self.floating_widget.deiconify()
        elif status == StateManager.STATUS_PAUSED:
            self.btn_start.configure(state="normal", text="RESUME")
            self.btn_pause.configure(state="normal", text="RESUME")
            self.btn_stop.configure(state="normal")
            if not self.state_manager.stealth_mode:
                self.floating_widget.deiconify()
        else: # Inactive or Done
            self.btn_start.configure(state="normal", text="START (F12)")
            self.btn_pause.configure(state="disabled", text="PAUSE")
            self.btn_stop.configure(state="disabled")
            self.floating_widget.withdraw()
            
        self.after(200, self.update_ui_state)
