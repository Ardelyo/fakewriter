try:
    from core.state_manager import StateManager
    from core.character_injector import send_unicode_char
    from core.app_detector import AppDetector
    from core.keyboard_hook import KeyboardHook
    # GUI imports might fail if no display, but let's try importing classes
    from gui.floating_widget import FloatingWidget
    from gui.main_window import MainWindow
    print("Imports successful.")
except Exception as e:
    print(f"Import failed: {e}")
