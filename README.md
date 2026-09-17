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
py src\skr.py
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

```text
GameLoop Smartkeys Reborn.exe
```

---

# Building the Installer

The project uses **Inno Setup** to create the Windows installer.

The installer script is:

```text
GameLoop Smartkeys Reborn.iss
```

The installer packages:

```text
GameLoop Smartkeys Reborn.exe
```

and creates the Start Menu and optional desktop shortcuts.

The final installer is:

```text
GameLoop Smartkeys Reborn Setup.exe
```

---

# Project Structure

The source repository is organized around the application source, artwork, and installer configuration.

```text
GameLoop-Smartkeys-Reborn/
│
├── README.md
│
├── src/
│   └── skr.py
│
├── assets/
│   └── smartkeys.ico
│
└── installer/
    └── GameLoop Smartkeys Reborn.iss
```

Build-generated files such as the PyInstaller `build` and `dist` directories do not need to be stored in the source repository.

---

# Troubleshooting

## F does nothing

Check:

1. The application is **ARMED**.
2. GameLoop is the focused window.
3. **Require GameLoop focus** is enabled if you want focus protection.
4. The output sequence contains at least one key.
5. Try pressing F12 and then ARM again.

---

## F works in another application

Make sure:

```text
Require GameLoop focus
```

is enabled.

When enabled, the F hook is installed only while the recognized GameLoop/emulator window is focused.

---

## The application does not start

If running from source, make sure the required modules are installed:

```bat
py -m pip install keyboard psutil
```

Then try:

```bat
py skr.py
```

---

## Emergency stop

Press:

```text
F12
```

The application should change to:

```text
DISARMED
```

---

# Source Code

The main application source is:

```text
src/skr.py
```

The application is written in Python using:

* Tkinter
* ctypes
* keyboard
* psutil

---

# Scope

GameLoop Smartkeys Reborn is designed specifically for keyboard-to-keyboard automation.

It does not use:

* ADB commands
* Mouse coordinates
* Touch coordinates
* Screen-coordinate clicking
* Screen-coordinate automation
* Background mouse or touch control

The application sends keyboard keys through the Windows keyboard input mechanism.

## Security & Software Scope

GameLoop Smartkeys Reborn does **not** contain or intentionally use:

* Malware
* Viruses
* Spyware
* Keyloggers
* Credential-stealing functionality
* Remote-control functionality
* Harmful payloads

The application is intended to provide a simple keyboard automation tool for the community.

---

# Community Build

Version **1.0** is a community-requested build created in response to requests for a lightweight keyboard sequence tool for GameLoop.

The project is provided **free to use**.

### Version 1.0

```text
GameLoop Smartkeys Reborn
Version 1.0
Free to use
Community-requested build
Created by Skuny
```

Users are encouraged to review the source code and build the application themselves if they prefer.

---

# Credits

Created by:

**Skuny**

Big shoutout to **KryptonPsycho** for assisting me in making this project.

Project:

**GameLoop Smartkeys Reborn**

---

# Version

Current version:

```text
1.0
```

Application name:

```text
GameLoop Smartkeys Reborn by Skuny
```

---

# License

License information will be added to this repository separately.

---

# Disclaimer

GameLoop Smartkeys Reborn is a keyboard automation utility and does not modify, inject into, or alter game data or game files.

The application does not directly modify gameplay data, game memory, game files, or game assets. It operates by sending keyboard input through the Windows keyboard input mechanism.

We hope this project will not be blocked or flagged by **TAC or other anti-cheat systems**, as Version 1.0 does not intentionally interact with or modify the game's internal data.

However, anti-cheat systems and game policies may change at any time. No guarantee is made that the application will be permitted by any particular game, emulator, or anti-cheat system.

Use this software responsibly and make sure its use complies with the rules and terms of the games, emulators, and services with which you use it.

---

# Final Note

Hi everyone,

Thanks for taking the time to read all of this.

I was honestly at my breaking point when I was trying to fix the keymaps in the GameLoop CODM Beta versions **1.0.56 and 1.0.57**. I spent a lot of time trying to figure out why things weren't working properly, and I got pretty frustrated.

I started digging deeper into how everything worked. I reverse-engineered parts of `config.db`, looked into `gameloopemulator.exe`, ADB, and various Android sub-files, and used **Ghidra** to inspect and understand the data and structures I was dealing with.

Just when I was about to give up, the idea came to me to build a tool that could handle the key sequences myself.

That eventually became **GameLoop Smartkeys Reborn**.

This is **Version 1.0**, so it is intentionally simple. There is no complicated preset system or massive collection of pre-made configurations. You can adjust the key sequence yourself depending on your keymap and the game mode you're using.

The hierarchy is simple: **the buttons at the top run first, followed by the buttons underneath them**. You can add, remove, and reorder them however you want.

I'm also including my **BR.txt** keymap as a reference for my CODM Battle Royale 3rd-person setup.

I don't work for **GameLoop, Tencent, or TAC**. I'm just a small creator trying to build something useful for the community, just like many of you.

I hope I can get some feedback, suggestions, and support from the community as the project develops.

I also hope GameLoop/TAC can eventually bring the emulator back to its former stability and continue improving it. While working on this project, I came across a lot of broken, inconsistent, or messy parts of the emulator, and I really hope the developers continue improving them.

Most importantly, I hope this project can remain useful for **open GameLoop use** and that the community can continue building and experimenting with tools like this.

Have a great day, everyone.

**STAY FROSTY!** 🥶
