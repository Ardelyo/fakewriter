# FakeWriter 🖊️

**FakeWriter** is a sophisticated Windows desktop application that intercepts physical keystrokes and replaces them with pre-defined text in real-time. It simulates natural human typing patterns, making it appear as if you are naturally composing the prepared text.

## 🚀 Features

- **OS-Level Interception**: Intercepts and blocks physical keystrokes globally using a low-level Windows hook.
- **Smart Typing Engine**: 
    - **Variable Speed**: Adjust typing speed from 20 to 200 WPM.
    - **Natural Pauses**: Automatically adds realistic pauses after punctuation and sentence ends.
    - **Human Variance**: Randomizes delay between characters by ±30% to mimic human rhythm.
- **Advanced Typo Simulation**:
    - **QWERTY Proximity**: In "Auto-Typo" mode, mistakes are made using keys physically adjacent to the target key.
    - **Natural Correction**: Automatically backspaces and "fixes" the typo after a short delay.
- **Stealth Mode**: Hide all UI elements (including the floating status widget) for undetectable operation.
- **App Targeting**: 
    - **Whitelist**: Only active in specific applications (e.g., `notepad.exe`).
    - **Blacklist**: Active everywhere *except* specific applications.
- **Unicode Support**: Inject any character, including emojis and non-Latin scripts, using `SendInput`.
- **Global Hotkey**: Toggle the faker on/off instantly with `F12`.

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern Dark Theme)
- **Hooks**: `keyboard` library (Win32 `WH_KEYBOARD_LL`)
- **Injection**: Windows `SendInput` API via `ctypes`
- **Process Detection**: `psutil`

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/fakewriter.git
   cd fakewriter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Assets** (Optional):
   ```bash
   python create_icon.py
   ```

## 🖥️ Usage

> [!IMPORTANT]
> **Run as Administrator**: FakeWriter must be run with administrative privileges to intercept and inject keystrokes into other applications.

1. Launch the application:
   ```bash
   python main.py
   ```
2. Enter the text you want to "fake type" into the main text area.
3. Configure your **WPM Speed**, **Backspace Mode**, and **Target Apps**.
4. Click **START**.
5. Switch to your target application (e.g., Notepad, Word, Browser).
6. Press **F12** to toggle the faker **ACTIVE**.
7. Start typing on your physical keyboard. Each keypress will now output a character from your pre-defined text.

## ⚙️ Configuration

- **Natural Backspace**: Allows you to physically backspace and rewinds the internal text pointer.
- **Strict Backspace**: Blocks the backspace key entirely while active.
- **Auto-Typo**: Randomly generates a realistic mistake and corrects it.
- **Stealth Mode**: Hides the floating status widget.

## ⚠️ Disclaimer

This tool is for educational and productivity purposes only. Use it responsibly and ensure you have permission to use such tools in your environment.

## 📄 License

MIT License. See `LICENSE` for details.
