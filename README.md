# GameLoop Smartkeys Reborn by Skuny

A lightweight Windows keyboard sequence tool designed for **GameLoop** and other Android emulators.

Press one trigger key and automatically send a configurable sequence of keyboard keys with an adjustable delay between each key.

---

## Features

* **F** trigger key
* Default sequence:
  **K → L → ; → ' → [ → ]**
* Adjustable delay between keys
* Add, remove, and reorder output keys
* Save settings automatically
* Settings persist between launches
* GameLoop/emulator focus detection
* F is intercepted only while the target emulator is focused
* F behaves normally when using other applications
* ARM / DISARM control
* **F12 emergency disarm**
* Always-on-top option
* Dark tactical-style interface
* Windows EXE build supported
* Inno Setup installer supported

---

# How It Works

When the application is armed and GameLoop is focused:

```text
F pressed
   ↓
K
   ↓
L
   ↓
;
   ↓
'
   ↓
[
   ↓
]
```

The default output sequence is:

```text
K → L → ; → ' → [ → ]
```

The delay between each output key can be changed in the application.

The default delay is:

```text
0.05 seconds
```

or:

```text
50 milliseconds
```

---

# Important Safety Feature

The application does **not** permanently block the F key.

When **Require GameLoop focus** is enabled:

```text
GameLoop focused
        ↓
F activates the sequence

Chrome / Discord / ChatGPT / Windows
        ↓
F behaves normally
```

This prevents the sequence from activating while you are using another application.

---

# Emergency Disarm

Press:

```text
F12
```

at any time to immediately disarm the application.

This stops the active sequence and removes the F-key hook.

---

# Installation

## Option 1 — Installer

Download the latest installer from the project's GitHub Releases page.

Run:

```text
GameLoop Smartkeys Reborn Setup.exe
```

Follow the installation wizard.

The installer creates Start Menu shortcuts and can optionally create a desktop shortcut.

---

## Option 2 — Run From Source

### Requirements

* Windows
* Python 3
* `keyboard`
* `psutil`

Install the required Python packages:

```bat
py -m pip install keyboard psutil
```

Then run:

```bat
py skr.py
```

---

# Using the Application

## 1. Start GameLoop

Launch GameLoop and open your desired Android game.

## 2. Start Smartkeys

Launch:

```text
GameLoop Smartkeys Reborn.exe
```

## 3. Configure the sequence

The default sequence is:

```text
01     K
02     L
03     ;
04     '
05     [
06     ]
```

You can:

* Add keys
* Remove keys
* Move keys up
* Move keys down

## 4. Set the delay

For example:

```text
0.05
```

means 50 milliseconds between output keys.

## 5. Press SAVE

Your configuration is stored locally and will be restored the next time the application starts.

## 6. Press ARM

The application becomes active.

When GameLoop is focused, the status changes to:

```text
ARMED • READY
```

Press:

```text
F
```

to start the sequence.

---

# Configuration

The application stores its configuration in:

```text
%APPDATA%\GameLoop Smartkeys Reborn\gameloop_keyboard_mapper.json
```

A typical default configuration looks like:

```json
{
    "keys": [
        "k",
        "l",
        ";",
        "'",
        "[",
        "]"
    ],
    "delay": 0.05,
    "always_on_top": false,
    "require_focus": true
}
```

## Configuration Options

### `keys`

The keyboard sequence that will be sent.

Default:

```json
"keys": [
    "k",
    "l",
    ";",
    "'",
    "[",
    "]"
]
```

This produces:

```text
K → L → ; → ' → [ → ]
```

### `delay`

Delay between output keys in seconds.

Example:

```json
"delay": 0.05
```

### `always_on_top`

Controls whether the application stays above other windows.

```json
"always_on_top": false
```

### `require_focus`

Controls whether GameLoop must be focused before the F trigger is active.

Recommended:

```json
"require_focus": true
```

---

# GameLoop Detection

The application checks the foreground Windows application and recognizes common GameLoop/emulator process names and window-title keywords.

Examples include:

```text
gameloopemulator.exe
androidemulator.exe
aow_exe.exe
qmemulatorservice.exe
gameloop.exe
emulator.exe
```

It also recognizes relevant emulator and game window titles.

The focus requirement can be disabled from the application settings if desired.

---

# Building the EXE

The project can be packaged into a standalone Windows executable using PyInstaller.

Install PyInstaller:

```bat
py -m pip install pyinstaller
```

From the project directory, build the EXE with:

```bat
py -m PyInstaller --noconfirm --clean --onefile --windowed --icon "smartkeys.ico" --name "GameLoop Smartkeys Reborn" skr.py
```

The resulting executable will be created in:

```text
dist\
```

The executable is:

``
