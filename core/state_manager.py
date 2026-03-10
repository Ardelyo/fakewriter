import threading
import time
import random

class StateManager:
    _instance = None
    _lock = threading.Lock()

    # Constants
    STATUS_INACTIVE = "Inactive"
    STATUS_ACTIVE = "Active"
    STATUS_PAUSED = "Paused"
    STATUS_DONE = "Done"

    MODE_BACKSPACE_STRICT = "Strict"
    MODE_BACKSPACE_NATURAL = "Natural"
    MODE_BACKSPACE_AUTOTYPO = "AutoTypo"

    END_BEHAVIOR_STOP = "Stop"
    END_BEHAVIOR_LOOP = "Loop"

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(StateManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # State
        self.status = self.STATUS_INACTIVE
        self.text_queue = [] 
        self.current_text_index = 0
        self.current_char_index = 0
        
        # Configuration
        self.backspace_mode = self.MODE_BACKSPACE_NATURAL
        self.end_behavior = self.END_BEHAVIOR_STOP
        self.target_app_mode = "All"
        self.target_apps = []
        
        # Smart Typing Settings
        self.stealth_mode = False
        self.typing_speed_wpm = 60 # Words per minute (approx)
        self.variance = 0.3 # 30% speed variance
        self.typo_chance = 0.03 # 3% chance
        self.line_sync = False # New feature!
        
        # Auto-Typo State
        self.typo_pending = False
        self.typo_char = None
        
        # QWERTY Proximity Map for "Smart" Typos
        self.proximity_map = {
            'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'erfcx', 'e': 'rdsw', 'f': 'rtgvcd',
            'g': 'tyhbvf', 'h': 'yujnbg', 'i': 'ujko', 'j': 'uikmnh', 'k': 'iolmj', 'l': 'opk',
            'm': 'njk', 'n': 'bhjm', 'o': 'ipkl', 'p': 'ol', 'q': 'wa', 'r': 'tfde',
            's': 'wedxz', 't': 'ygfr', 'u': 'yhji', 'v': 'cfgb', 'w': 'qesa', 'x': 'zsdc',
            'y': 'tghu', 'z': 'asx'
        }

    def set_text_queue(self, texts):
        with self._lock:
            self.text_queue = texts
            self.current_text_index = 0
            self.current_char_index = 0
            self.status = self.STATUS_INACTIVE

    def toggle_active(self):
        with self._lock:
            if self.status == self.STATUS_ACTIVE:
                self.status = self.STATUS_PAUSED
            else:
                if self.status == self.STATUS_DONE:
                    self.reset_progress()
                self.status = self.STATUS_ACTIVE

    def set_active(self, active: bool):
        with self._lock:
            if active:
                if self.status == self.STATUS_DONE:
                    self.reset_progress()
                self.status = self.STATUS_ACTIVE
            else:
                self.status = self.STATUS_PAUSED

    def reset_progress(self):
        self.current_text_index = 0
        self.current_char_index = 0
        self.status = self.STATUS_INACTIVE

    def get_next_char(self):
        with self._lock:
            if self.status != self.STATUS_ACTIVE:
                return None

            if not self.text_queue:
                return None

            current_text = self.text_queue[self.current_text_index]
            
            if self.current_char_index >= len(current_text):
                self.current_text_index += 1
                self.current_char_index = 0
                
                if self.current_text_index >= len(self.text_queue):
                    if self.end_behavior == self.END_BEHAVIOR_LOOP:
                        self.current_text_index = 0
                    else:
                        self.status = self.STATUS_DONE
                        return None
                
                current_text = self.text_queue[self.current_text_index]

            # Smart Typo Logic
            if self.backspace_mode == self.MODE_BACKSPACE_AUTOTYPO and not self.typo_pending:
                 if random.random() < self.typo_chance:
                      self.typo_pending = True
                      self.typo_char = current_text[self.current_char_index]
                      orig_char = self.typo_char.lower()
                      if orig_char in self.proximity_map:
                          return random.choice(self.proximity_map[orig_char])
                      return random.choice("abcdefghijklmnopqrstuvwxyz")

            char = current_text[self.current_char_index]
            self.current_char_index += 1
            return char

    def next_char_is_newline(self):
        with self._lock:
            if not self.text_queue:
                return False
            
            temp_text_idx = self.current_text_index
            temp_char_idx = self.current_char_index
            
            if temp_text_idx >= len(self.text_queue):
                return False
                
            current_text = self.text_queue[temp_text_idx]
            if temp_char_idx >= len(current_text):
                # We're at the end of a string in the queue, normally next is \n if we treat strings as lines
                # But in this app, the input is usually one big string from a Textbox
                return False
            
            return current_text[temp_char_idx] == '\n'

    def get_correction(self):
        with self._lock:
            if self.typo_pending:
                char = self.typo_char
                self.typo_pending = False
                self.typo_char = None
                self.current_char_index += 1
                return char
            return None

    def get_delay(self, char):
        """Calculates a smart delay based on WPM and character type."""
        # Base delay: 60 sec / (WPM * 5 chars per word)
        base_delay = 60.0 / (self.typing_speed_wpm * 5.0)
        
        # Add variance
        delay = base_delay * (1.0 + random.uniform(-self.variance, self.variance))
        
        # Smart pauses
        if char in ".!?":
            delay += random.uniform(0.3, 0.7) # Sentence end
        elif char in ",;:":
            delay += random.uniform(0.1, 0.3) # Punctuation pause
        elif char == " ":
            delay += random.uniform(0.02, 0.1) # Word end
            
        return delay

    def peek_next_chars(self, count=5):
        with self._lock:
            if not self.text_queue:
                return ""
            result = ""
            temp_text_idx = self.current_text_index
            temp_char_idx = self.current_char_index
            for _ in range(count):
                if temp_text_idx >= len(self.text_queue):
                    if self.end_behavior == self.END_BEHAVIOR_LOOP:
                        temp_text_idx = 0; temp_char_idx = 0
                    else: break
                current_text = self.text_queue[temp_text_idx]
                if temp_char_idx >= len(current_text):
                    temp_text_idx += 1; temp_char_idx = 0
                    continue
                result += current_text[temp_char_idx]
                temp_char_idx += 1
            return result

    def handle_backspace(self):
        with self._lock:
            if self.backspace_mode == self.MODE_BACKSPACE_STRICT:
                return False
            if self.backspace_mode == self.MODE_BACKSPACE_NATURAL:
                if self.current_char_index > 0:
                    self.current_char_index -= 1
                elif self.current_text_index > 0:
                     self.current_text_index -= 1
                     self.current_char_index = len(self.text_queue[self.current_text_index]) - 1
                return True
            return False
