import customtkinter as ctk
import tkinter as tk
from core.state_manager import StateManager

class FloatingWidget(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.state_manager = StateManager()
        
        # Window Setup
        self.overrideredirect(True) # Remove title bar
        self.attributes('-topmost', True) # Always on top
        self.attributes('-alpha', 0.85) # Semi-transparent
        
        # Dimensions and Position
        self.geometry("220x60+100+100")
        
        # Dragging logic
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        self.x = 0
        self.y = 0
        
        # UI Elements
        self.frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a1a", border_width=1, border_color="#333333")
        self.frame.pack(expand=True, fill="both", padx=0, pady=0)
        
        self.status_label = ctk.CTkLabel(self.frame, text="Inactive", font=("Segoe UI", 12, "bold"), text_color="gray")
        self.status_label.pack(pady=(5, 0))
        
        self.preview_label = ctk.CTkLabel(self.frame, text="...", font=("Consolas", 10), text_color="#aaaaaa")
        self.preview_label.pack(pady=(0, 5))
        
        # Start update loop
        self.update_widget()

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def stop_move(self, event):
        self.offset_x = None
        self.offset_y = None

    def do_move(self, event):
        if self.offset_x is None or self.offset_y is None:
            return
        x = self.winfo_pointerx() - self.offset_x
        y = self.winfo_pointery() - self.offset_y
        self.geometry(f"+{x}+{y}")

    def update_widget(self):
        status = self.state_manager.status
        stealth = self.state_manager.stealth_mode
        
        # Update visibility
        if status == StateManager.STATUS_INACTIVE or stealth:
             if self.state() != "withdrawn":
                 self.withdraw()
        else:
             if self.state() == "withdrawn":
                 self.deiconify()
        
        # Update Content
        if status != StateManager.STATUS_INACTIVE:
            # Status Color
            if status == StateManager.STATUS_ACTIVE:
                self.status_label.configure(text="ACTIVE", text_color="#2cc985") # Emerald
            elif status == StateManager.STATUS_PAUSED:
                self.status_label.configure(text="PAUSED", text_color="#f2a900") # Amber
            elif status == StateManager.STATUS_DONE:
                self.status_label.configure(text="DONE", text_color="#3b8ed0") # Blue
            
            # Progress / Preview
            preview = self.state_manager.peek_next_chars(15)
            preview = preview.replace("\n", "↵").replace("\t", "→")
            
            # Show progress in label
            # current / total is hard because total is sum of all texts.
            # Just show status and preview for now, maybe add "Text 1/3" later.
            self.preview_label.configure(text=f"Next: {preview}")

        self.after(100, self.update_widget)
