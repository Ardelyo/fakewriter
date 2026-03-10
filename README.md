# FakeWriter

FakeWriter is a Windows desktop tool that intercepts physical keystrokes and replaces them with characters from a pre-loaded text buffer. It uses a low-level keyboard hook to suppress real input and injects substituted characters through the Windows `SendInput` API. The typing output is deliberately paced and randomized to resemble natural human composition.

Built with Python and CustomTkinter. Requires administrative privileges.

---

## How It Works

When active, FakeWriter installs a global `WH_KEYBOARD_LL` hook that captures every physical keypress before it reaches the target application. Each captured key is silently discarded and replaced with the next character from your prepared text. The injection timing is varied per-character to avoid the mechanical uniformity of pasted or scripted text.

The result: it looks like you are typing the prepared text naturally, in real time, keystroke by keystroke.

```
Physical input:    a  s  d  f  g  h  j  k  l  ...
Injected output:   T  h  e     q  u  i  c  k  ...
```

---

## Features

**Keystroke Interception**
Global low-level keyboard hook captures and suppresses physical input across all applications. Replacement characters are injected via the Win32 `SendInput` API with full Unicode support, including non-Latin scripts and emoji.

**Variable Typing Speed**
Base speed is adjustable from 20 to 200 words per minute. Each character delay is randomized by ±30% around the base interval to break up rhythmic patterns.

**Natural Pauses**
The engine introduces longer pauses after periods, commas, paragraph breaks, and other punctuation to mimic the cadence of someone composing text rather than copying it.

**Typo Simulation**
When enabled, the auto-typo system occasionally injects an incorrect character chosen from physically adjacent keys on a QWERTY layout. After a brief delay, it sends backspace events and retypes the correct character. The frequency is configurable.

**Backspace Handling**
Two modes are available:
- *Natural* — Physical backspace rewinds the internal pointer by one position, so you can "undo" the last injected character and re-trigger it on the next keypress.
- *Strict* — Backspace is intercepted and discarded. The buffer only moves forward.

**Application Targeting**
Restrict operation to specific processes (whitelist mode) or exclude specific processes and run everywhere else (blacklist mode). Process matching is done by executable name using `psutil`.

**Stealth Mode**
Hides the floating status indicator and all visible UI elements. The application continues running in the background and responds to the global hotkey.

**Global Hotkey**
Press `F12` at any time to toggle the faker between active and paused states without switching windows.

---

## Requirements

- Windows 10 or later
- Python 3.10+
- Administrative privileges (required for global keyboard hooks and cross-process input injection)

### Dependencies

| Package | Purpose |
|---|---|
| [customtkinter](https://github.com/TomSchimansky/CustomTkinter) | GUI framework |
| [keyboard](https://github.com/boppreh/keyboard) | Low-level keyboard hooking |
| [psutil](https://github.com/giampaolo/psutil) | Process enumeration for app targeting |

All dependencies are listed in `requirements.txt`.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/fakewriter.git
cd fakewriter
pip install -r requirements.txt
```

Optionally, generate the application icon:

```bash
python create_icon.py
```

---

## Usage

**1. Launch as Administrator**

```bash
python main.py
```

Right-click your terminal or IDE and select "Run as administrator," or launch from an elevated command prompt. Without admin privileges, the keyboard hook will not function in most applications.

**2. Load your text**

Paste or type the text you want to output into the main text area.

**3. Configure settings**

Set your desired WPM, backspace mode, typo frequency, and application targeting rules.

**4. Start the engine**

Click **Start**. The engine is now armed but paused.

**5. Activate**

Switch to your target application and press `F12`. The status indicator will show that the faker is active.

**6. Type**

Press any keys on your keyboard. Each keypress will produce the next character from your loaded text instead of the key you pressed.

Press `F12` again to pause. Click **Stop** in the main window to fully disengage the hook.

---

## Configuration

| Option | Description | Default |
|---|---|---|
| WPM Speed | Base typing speed in words per minute. Range: 20–200. | 80 |
| Human Variance | Randomization applied to each character delay (±%). | 30% |
| Backspace Mode | `Natural` (rewinds pointer) or `Strict` (blocks backspace). | Natural |
| Auto-Typo | Enable proximity-based typo injection with automatic correction. | Off |
| Typo Frequency | Approximate percentage of characters that trigger a typo. | 3% |
| Target Mode | `All Apps`, `Whitelist`, or `Blacklist`. | All Apps |
| Target Processes | Comma-separated list of executable names (e.g., `notepad.exe, chrome.exe`). | — |
| Stealth Mode | Hide the floating status widget. | Off |

---

## Project Structure

```
fakewriter/
├── main.py              # Entry point
├── core/
│   ├── hook.py           # Keyboard hook installation and management
│   ├── injector.py       # SendInput wrapper for character injection
│   ├── engine.py         # Typing engine (timing, pauses, typo logic)
│   └── process.py        # Application targeting and process detection
├── gui/
│   ├── app.py            # Main application window
│   └── status.py         # Floating status indicator widget
├── assets/
│   └── icon.ico          # Application icon
├── create_icon.py        # Icon generation script
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Known Limitations

- **Windows only.** The application depends on Win32 APIs (`SetWindowsHookEx`, `SendInput`) and will not function on macOS or Linux.
- **Admin required.** Without elevated privileges, the low-level hook cannot intercept input directed at higher-integrity processes.
- **Gaming / anti-cheat software** may conflict with or block the keyboard hook.
- **Remote desktop sessions** may not forward low-level hooks correctly depending on the client configuration.
- **Some applications** with their own low-level input handling (certain game engines, VM software) may not receive injected input reliably.

---

## Disclaimer

FakeWriter is a technical demonstration of low-level input handling on Windows. It is provided as-is for educational and personal use. The authors do not endorse using this tool to misrepresent authorship, circumvent proctoring systems, or violate any applicable policies or laws. You are solely responsible for how you use this software.

---

## License

Released under the [MIT License](LICENSE).