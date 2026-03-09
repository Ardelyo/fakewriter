import customtkinter as ctk
import sys
import threading
import keyboard
from core.keyboard_hook import KeyboardHook
from gui.main_window import MainWindow

def main():
    # Initialize Hook
    hook = KeyboardHook()
    hook.start()
    
    # Initialize GUI
    app = MainWindow()
    
    # Run App
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        hook.stop()
        # keyboard library sometimes needs a cleanup
        keyboard.unhook_all()
        sys.exit(0)

if __name__ == "__main__":
    main()
