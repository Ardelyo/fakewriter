import ctypes
import psutil
from .state_manager import StateManager

# Windows API
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def get_foreground_process_name():
    """
    Returns the process name (e.g., 'notepad.exe') of the foreground window.
    """
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None

    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    
    if pid.value == 0:
        return None

    try:
        process = psutil.Process(pid.value)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

class AppDetector:
    def __init__(self):
        self.state_manager = StateManager()

    def should_intercept(self):
        """
        Determines if FakeWriter should intercept keystrokes based on the active window.
        """
        # First check generic enabled state
        if self.state_manager.status == StateManager.STATUS_INACTIVE:
            return False
            
        # If paused, we still might want to intercept to block keys? 
        # No, if paused, we usually let keys through or block?
        # Plan says: "Active / Paused / Done / Inactive"
        # If Paused, we probably shouldn't be typing, but should we BLOCK?
        # Usually "Pause" means "Stop acting". So we should probably NOT intercept (allow pass-through).
        if self.state_manager.status != StateManager.STATUS_ACTIVE:
            return False

        mode = self.state_manager.target_app_mode
        target_apps = self.state_manager.target_apps

        if mode == "All":
            return True
        
        process_name = get_foreground_process_name()
        if not process_name:
            # If we can't identify, maybe default to False to be safe, or True?
            # Safer to False.
            return False

        # normalize to lowercase for comparison
        process_name = process_name.lower()
        target_apps = [app.lower() for app in target_apps]

        if mode == "Whitelist":
            return process_name in target_apps
        
        if mode == "Blacklist":
            return process_name not in target_apps
        
        return True
