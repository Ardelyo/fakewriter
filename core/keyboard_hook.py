import keyboard
import threading
import time
from .state_manager import StateManager
from .app_detector import AppDetector
from .character_injector import send_unicode_char, send_backspace

class KeyboardHook:
    def __init__(self):
        self.state_manager = StateManager()
        self.app_detector = AppDetector()
        self._running = False
        self._hook_id = None
        self._intercepted_keys = set()

    def start(self):
        if self._running:
            return
        self._running = True
        
        # keyboard.on_press/on_release with suppress is generally reliable.
        # It's better than keyboard.hook in some cases.
        keyboard.on_press(self._on_press, suppress=True)
        keyboard.on_release(self._on_release, suppress=True)
        print("Keyboard library hook (press/release) started.")

    def stop(self):
        self._running = False
        keyboard.unhook_all()
        print("Keyboard library hook stopped.")

    def _on_press(self, event):
        # 1. Hotkey Handling: F12 Toggle
        if event.name == 'f12':
            self.state_manager.toggle_active()
            print(f"F12 pressed. Status: {self.state_manager.status}")
            return False # Block F12

        # 2. Check Active Status
        if self.state_manager.status != StateManager.STATUS_ACTIVE:
            keyboard.press(event.name) # Pass through
            return

        # 3. Modifiers Check
        if keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt') or keyboard.is_pressed('windows'):
            keyboard.press(event.name) # Pass through
            return

        # 4. Target App Check
        if not self.app_detector.should_intercept():
            keyboard.press(event.name) # Pass through
            return

        # 5. Interception and Injection
        
        # Line Sync Mode logic
        is_newline = self.state_manager.next_char_is_newline()
        if self.state_manager.line_sync:
            # If next is newline, ONLY 'enter' can trigger it
            if is_newline:
                if event.name != 'enter':
                    return False # Block other keys
            # If physical key is 'enter', ONLY trigger if next is newline
            elif event.name == 'enter':
                # Optional: Block enter if next isn't newline to prevent accidental skips
                return False

        # a. Typo Correction
        correction = self.state_manager.get_correction()
        if correction:
            send_backspace()
            send_unicode_char(correction)

        # b. Next Char
        char = self.state_manager.get_next_char()
        if char:
            send_unicode_char(char)
            # Mark this scan code as intercepted so we block the release too
            self._intercepted_keys.add(event.scan_code)
            return False # Suppressed
        else:
            # Done, just let it pass
            keyboard.press(event.name)

    def _on_release(self, event):
        # Always block F12 release to keep it clean
        if event.name == 'f12':
            return False
            
        if event.scan_code in self._intercepted_keys:
            self._intercepted_keys.remove(event.scan_code)
            return False # Suppress release of intercepted key
            
        # For everything else, pass release through
        keyboard.release(event.name)

