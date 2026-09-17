import json
import time
import threading
import ctypes
import sys
from ctypes import wintypes
from pathlib import Path

import tkinter as tk
from tkinter import messagebox

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    psutil = None
    HAS_PSUTIL = False

try:
    import keyboard
except ImportError:
    keyboard = None


# ============================================================
# GAMELOOP SMARTKEYS REBORN
# ============================================================

APP_NAME = "GameLoop Smartkeys Reborn by Skuny"


# ============================================================
# GAMELOOP DETECTION
# ============================================================

TARGET_NAMES = {
    "gameloopemulator.exe",
    "androidemulator.exe",
    "aow_exe.exe",
    "qmemulatorservice.exe",
    "gameloop.exe",
    "tencentdl.exe",
    "androidemulatoren.exe",
    "emulator.exe",
}

TITLE_KEYWORDS = [
    "gameloop",
    "android",
    "aow",
    "call of duty",
    "cod",
    "warzone",
    "pubg",
    "freefire",
    "free fire",
    "bgmi",
    "mobile",
    "emulator",
]


# ============================================================
# COLORS
# ============================================================

BG = "#101214"
PANEL = "#171A1D"
PANEL2 = "#1D2125"
BORDER = "#30363B"

TEXT = "#E7E9EA"
MUTED = "#8E969D"

GREEN = "#7CFF6B"
RED = "#FF5C5C"
RED_DARK = "#522525"

ORANGE = "#F2A900"
ORANGE_LIGHT = "#FFC84A"

BLACK = "#080A0B"


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CONFIG = {
    "keys": [
        "k",
        "l",
        "j",
        "o",
        "p",
        "i"
    ],
    "delay": 0.05,
    "always_on_top": False,
    "require_focus": True,
}


# ============================================================
# CONFIG LOCATION
# ============================================================

def get_config_file():

    appdata = (
        Path.home()
        / "AppData"
        / "Roaming"
        / "GameLoop Smartkeys Reborn"
    )

    try:
        appdata.mkdir(
            parents=True,
            exist_ok=True
        )

    except Exception:

        if getattr(sys, "frozen", False):

            return (
                Path(sys.executable)
                .resolve()
                .with_name(
                    "gameloop_keyboard_mapper.json"
                )
            )

        return (
            Path(__file__)
            .resolve()
            .with_name(
                "gameloop_keyboard_mapper.json"
            )
        )

    return (
        appdata
        / "gameloop_keyboard_mapper.json"
    )


CONFIG_FILE = get_config_file()


# ============================================================
# WINDOWS API
# ============================================================

user32 = ctypes.windll.user32

VK_F12 = 0x7B


# ============================================================
# WINDOW TITLE
# ============================================================

def get_window_title(hwnd):

    if not hwnd:
        return ""

    length = user32.GetWindowTextLengthW(hwnd)

    if length <= 0:
        return ""

    buffer = ctypes.create_unicode_buffer(
        length + 1
    )

    user32.GetWindowTextW(
        hwnd,
        buffer,
        length + 1
    )

    return buffer.value


# ============================================================
# FOREGROUND WINDOW INFO
# ============================================================

def get_foreground_info():

    hwnd = user32.GetForegroundWindow()

    if not hwnd:
        return None, None, ""

    pid = wintypes.DWORD()

    user32.GetWindowThreadProcessId(
        hwnd,
        ctypes.byref(pid)
    )

    title = get_window_title(hwnd)

    name = None

    if pid.value and HAS_PSUTIL:

        try:

            name = (
                psutil.Process(
                    pid.value
                ).name()
                or ""
            ).lower()

        except Exception:

            name = None

    return (
        name,
        pid.value if pid.value else None,
        title
    )


# ============================================================
# CHECK TARGET RUNNING
# ============================================================

def is_any_target_running():

    if not HAS_PSUTIL:
        return True

    for proc in psutil.process_iter(["name"]):

        try:

            process_name = (
                proc.info["name"]
                or ""
            ).lower()

            if process_name in TARGET_NAMES:
                return True

        except Exception:

            continue

    return False


# ============================================================
# CHECK TARGET FOCUSED
# ============================================================

def is_target_focused():

    name, _, title = get_foreground_info()

    t = (
        title or ""
    ).lower()

    if name and name in TARGET_NAMES:
        return True

    for kw in TITLE_KEYWORDS:

        if kw in t:
            return True

    if (
        is_any_target_running()
        and t
        and name not in (
            "python.exe",
            "pythonw.exe"
        )
    ):

        if name is None and t:
            return True

    return False


# ============================================================
# MAIN APPLICATION
# ============================================================

class GameLoopSmartkeys:

    def __init__(self, root):

        self.root = root

        self.root.title(
            APP_NAME
        )

        self.root.geometry(
            "650x700"
        )

        self.root.minsize(
            600,
            650
        )

        self.root.configure(
            bg=BG
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_application
        )

        # ----------------------------------------------------
        # RUNTIME STATE
        # ----------------------------------------------------

        self.armed = False

        self.sequence_running = False

        self.f_hooked = False

        # ----------------------------------------------------
        # SETTINGS
        # ----------------------------------------------------

        self.keys = []

        self.delay = DEFAULT_CONFIG["delay"]

        self.always_on_top = DEFAULT_CONFIG[
            "always_on_top"
        ]

        self.require_focus = DEFAULT_CONFIG[
            "require_focus"
        ]

        # ----------------------------------------------------
        # LOAD
        # ----------------------------------------------------

        self.load_config()

        # ----------------------------------------------------
        # GUI
        # ----------------------------------------------------

        self.build_gui()

        # ----------------------------------------------------
        # LOOPS
        # ----------------------------------------------------

        self.update_status_loop()

        self.f12_loop()


    # ========================================================
    # LOAD CONFIG
    # ========================================================

    def load_config(self):

        config = DEFAULT_CONFIG.copy()

        try:

            if CONFIG_FILE.exists():

                with open(
                    CONFIG_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    saved = json.load(f)

                if isinstance(saved, dict):

                    config.update(saved)

        except Exception:

            pass

        keys = config.get("keys")

        if (
            not isinstance(keys, list)
            or not keys
        ):

            keys = DEFAULT_CONFIG["keys"].copy()

        cleaned_keys = []

        for key in keys:

            if not isinstance(key, str):
                continue

            key = key.strip().lower()

            if key:
                cleaned_keys.append(key)

        if not cleaned_keys:

            cleaned_keys = DEFAULT_CONFIG[
                "keys"
            ].copy()

        self.keys = cleaned_keys

        try:

            self.delay = float(
                config.get(
                    "delay",
                    DEFAULT_CONFIG["delay"]
                )
            )

        except Exception:

            self.delay = DEFAULT_CONFIG["delay"]

        if self.delay < 0.001:

            self.delay = 0.001

        self.always_on_top = bool(
            config.get(
                "always_on_top",
                False
            )
        )

        self.require_focus = bool(
            config.get(
                "require_focus",
                True
            )
        )


    # ========================================================
    # SAVE CONFIG
    # ========================================================

    def save_config(self, show_message=True):

        if hasattr(self, "key_list"):

            self.read_keys_from_list()

        if hasattr(self, "delay_entry"):

            try:

                self.delay = float(
                    self.delay_entry.get()
                )

                if self.delay < 0.001:
                    self.delay = 0.001

            except Exception:

                self.delay = 0.05

        if hasattr(self, "always_on_top_var"):

            self.always_on_top = bool(
                self.always_on_top_var.get()
            )

        if hasattr(self, "require_focus_var"):

            self.require_focus = bool(
                self.require_focus_var.get()
            )

        config = {
            "keys": self.keys,
            "delay": self.delay,
            "always_on_top": self.always_on_top,
            "require_focus": self.require_focus
        }

        try:

            CONFIG_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                CONFIG_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    config,
                    f,
                    indent=4
                )

            if show_message:

                self.set_message(
                    "SETTINGS SAVED",
                    GREEN
                )

        except Exception as e:

            if show_message:

                messagebox.showerror(
                    "Save Error",
                    f"Could not save settings:\n\n{e}"
                )


    # ========================================================
    # BUILD GUI
    # ========================================================

    def build_gui(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.root,
            bg=BLACK,
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="GAMELOOP SMARTKEYS",
            bg=BLACK,
            fg=ORANGE_LIGHT,
            font=(
                "Segoe UI",
                19,
                "bold"
            )
        )

        title.pack(
            pady=(10, 0)
        )

        subtitle = tk.Label(
            header,
            text="REBORN BY SKUNY",
            bg=BLACK,
            fg=MUTED,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        )

        subtitle.pack()


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status_panel = tk.Frame(
            self.root,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        status_panel.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            status_panel,
            text="SYSTEM STATUS",
            bg=PANEL,
            fg=TEXT,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 3)
        )

        self.status_label = tk.Label(
            status_panel,
            text="DISARMED",
            bg=PANEL,
            fg=RED,
            font=(
                "Segoe UI",
                18,
                "bold"
            )
        )

        self.status_label.pack(
            anchor="w",
            padx=15
        )

        self.target_label = tk.Label(
            status_panel,
            text="GameLoop: NOT FOCUSED",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                10
            )
        )

        self.target_label.pack(
            anchor="w",
            padx=15,
            pady=(2, 12)
        )


        # ----------------------------------------------------
        # SEQUENCE PANEL
        # ----------------------------------------------------

        sequence_panel = tk.Frame(
            self.root,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        sequence_panel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        tk.Label(
            sequence_panel,
            text="OUTPUT KEY SEQUENCE",
            bg=PANEL,
            fg=TEXT,
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        tk.Label(
            sequence_panel,
            text="Press F → keys are sent in order",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 8)
        )


        # ----------------------------------------------------
        # LIST
        # ----------------------------------------------------

        list_frame = tk.Frame(
            sequence_panel,
            bg=PANEL
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=15
        )

        scrollbar = tk.Scrollbar(
            list_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.key_list = tk.Listbox(
            list_frame,
            bg=BLACK,
            fg=TEXT,
            selectbackground=ORANGE,
            selectforeground=BLACK,
            font=(
                "Consolas",
                13,
                "bold"
            ),
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            yscrollcommand=scrollbar.set
        )

        self.key_list.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.key_list.yview
        )

        self.refresh_key_list()


        # ----------------------------------------------------
        # KEY CONTROLS
        # ----------------------------------------------------

        key_input_frame = tk.Frame(
            sequence_panel,
            bg=PANEL
        )

        key_input_frame.pack(
            fill="x",
            padx=15,
            pady=12
        )

        tk.Label(
            key_input_frame,
            text="KEY:",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            side="left"
        )

        self.key_entry = tk.Entry(
            key_input_frame,
            bg=BLACK,
            fg=TEXT,
            insertbackground=ORANGE,
            relief="flat",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            width=12
        )

        self.key_entry.pack(
            side="left",
            padx=8
        )

        self.key_entry.bind(
            "<Return>",
            lambda event: self.add_key()
        )

        self.make_button(
            key_input_frame,
            "ADD",
            self.add_key,
            ORANGE
        ).pack(
            side="left",
            padx=3
        )

        self.make_button(
            key_input_frame,
            "REMOVE",
            self.remove_key,
            RED
        ).pack(
            side="left",
            padx=3
        )

        self.make_button(
            key_input_frame,
            "UP",
            self.move_key_up,
            MUTED
        ).pack(
            side="left",
            padx=3
        )

        self.make_button(
            key_input_frame,
            "DOWN",
            self.move_key_down,
            MUTED
        ).pack(
            side="left",
            padx=3
        )


        # ----------------------------------------------------
        # DELAY
        # ----------------------------------------------------

        delay_frame = tk.Frame(
            sequence_panel,
            bg=PANEL
        )

        delay_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        tk.Label(
            delay_frame,
            text="DELAY BETWEEN KEYS:",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            side="left"
        )

        self.delay_entry = tk.Entry(
            delay_frame,
            bg=BLACK,
            fg=TEXT,
            insertbackground=ORANGE,
            relief="flat",
            width=10,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

        self.delay_entry.pack(
            side="left",
            padx=8
        )

        self.delay_entry.insert(
            0,
            str(self.delay)
        )

        tk.Label(
            delay_frame,
            text="seconds",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            side="left"
        )


        # ----------------------------------------------------
        # OPTIONS
        # ----------------------------------------------------

        options_frame = tk.Frame(
            sequence_panel,
            bg=PANEL
        )

        options_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        self.always_on_top_var = tk.BooleanVar(
            value=self.always_on_top
        )

        self.require_focus_var = tk.BooleanVar(
            value=self.require_focus
        )

        tk.Checkbutton(
            options_frame,
            text="Always on top",
            variable=self.always_on_top_var,
            command=self.update_window_options,
            bg=PANEL,
            fg=TEXT,
            activebackground=PANEL,
            activeforeground=TEXT,
            selectcolor=BLACK,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            side="left"
        )

        tk.Checkbutton(
            options_frame,
            text="Require GameLoop focus",
            variable=self.require_focus_var,
            bg=PANEL,
            fg=TEXT,
            activebackground=PANEL,
            activeforeground=TEXT,
            selectcolor=BLACK,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            side="left",
            padx=20
        )


        # ----------------------------------------------------
        # MAIN CONTROL BUTTONS
        # ----------------------------------------------------

        control_frame = tk.Frame(
            self.root,
            bg=BG
        )

        control_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        # IMPORTANT:
        # Starts with command=self.arm.
        # arm() changes it to command=self.disarm.
        self.arm_button = tk.Button(
            control_frame,
            text="ARM",
            command=self.arm,
            bg=GREEN,
            fg=BLACK,
            activebackground=GREEN,
            activeforeground=BLACK,
            font=(
                "Segoe UI",
                13,
                "bold"
            ),
            relief="flat",
            bd=0,
            height=2,
            cursor="hand2"
        )

        self.arm_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.save_button = tk.Button(
            control_frame,
            text="SAVE",
            command=self.save_config,
            bg=ORANGE,
            fg=BLACK,
            activebackground=ORANGE_LIGHT,
            activeforeground=BLACK,
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            relief="flat",
            bd=0,
            height=2,
            cursor="hand2"
        )

        self.save_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.exit_button = tk.Button(
            control_frame,
            text="EXIT",
            command=self.exit_application,
            bg=RED_DARK,
            fg=TEXT,
            activebackground=RED,
            activeforeground=TEXT,
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            relief="flat",
            bd=0,
            height=2,
            cursor="hand2"
        )

        self.exit_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )


        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        tk.Label(
            self.root,
            text="TRIGGER: F    |    EMERGENCY DISARM: F12",
            bg=BG,
            fg=MUTED,
            font=(
                "Segoe UI",
                8,
                "bold"
            )
        ).pack(
            pady=(0, 8)
        )

        self.update_window_options()


    # ========================================================
    # BUTTON HELPER
    # ========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        color
    ):

        if color in (
            ORANGE,
            ORANGE_LIGHT,
            GREEN
        ):

            fg = BLACK

        else:

            fg = TEXT

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=color,
            activeforeground=fg,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )


    # ========================================================
    # KEY LIST
    # ========================================================

    def refresh_key_list(self):

        self.key_list.delete(
            0,
            tk.END
        )

        for index, key in enumerate(
            self.keys,
            start=1
        ):

            self.key_list.insert(
                tk.END,
                f"{index:02d}     {key.upper()}"
            )


    def read_keys_from_list(self):

        new_keys = []

        for item in self.key_list.get(
            0,
            tk.END
        ):

            text = str(item).strip()

            if not text:
                continue

            parts = text.split()

            if len(parts) >= 2:

                key = parts[-1].lower()

            else:

                key = text.lower()

            if key:
                new_keys.append(key)

        self.keys = new_keys


    def add_key(self):

        value = (
            self.key_entry
            .get()
            .strip()
            .lower()
        )

        if not value:
            return

        if " " in value:
            value = value.split()[0]

        self.keys.append(
            value
        )

        self.refresh_key_list()

        self.key_entry.delete(
            0,
            tk.END
        )

        self.key_entry.focus_set()


    def remove_key(self):

        selection = (
            self.key_list
            .curselection()
        )

        if not selection:
            return

        index = selection[0]

        if 0 <= index < len(
            self.keys
        ):

            del self.keys[index]

            self.refresh_key_list()


    def move_key_up(self):

        selection = (
            self.key_list
            .curselection()
        )

        if not selection:
            return

        index = selection[0]

        if index <= 0:
            return

        self.keys[
            index - 1
        ], self.keys[
            index
        ] = (
            self.keys[index],
            self.keys[index - 1]
        )

        self.refresh_key_list()

        self.key_list.selection_set(
            index - 1
        )

        self.key_list.activate(
            index - 1
        )


    def move_key_down(self):

        selection = (
            self.key_list
            .curselection()
        )

        if not selection:
            return

        index = selection[0]

        if index >= len(self.keys) - 1:
            return

        self.keys[
            index + 1
        ], self.keys[
            index
        ] = (
            self.keys[index],
            self.keys[index + 1]
        )

        self.refresh_key_list()

        self.key_list.selection_set(
            index + 1
        )

        self.key_list.activate(
            index + 1
        )


    # ========================================================
    # WINDOW OPTIONS
    # ========================================================

    def update_window_options(self):

        if not hasattr(
            self,
            "always_on_top_var"
        ):
            return

        self.always_on_top = bool(
            self.always_on_top_var.get()
        )

        self.require_focus = bool(
            self.require_focus_var.get()
        )

        self.root.attributes(
            "-topmost",
            self.always_on_top
        )


    # ========================================================
    # ARM
    # ========================================================

    def arm(self):

        if keyboard is None:

            messagebox.showerror(
                "Missing module",
                "The 'keyboard' module is not installed."
            )

            return

        self.read_keys_from_list()

        if not self.keys:

            messagebox.showwarning(
                "No keys",
                "Add at least one output key."
            )

            return

        try:

            self.delay = float(
                self.delay_entry.get()
            )

            if self.delay < 0.001:
                self.delay = 0.001

        except Exception:

            messagebox.showwarning(
                "Invalid delay",
                "Please enter a valid delay such as 0.05."
            )

            return

        self.armed = True

        # ====================================================
        # CRITICAL FIX:
        # Change the BUTTON COMMAND from ARM to DISARM.
        # ====================================================

        self.arm_button.config(
            text="DISARM",
            command=self.disarm,
            bg=RED,
            fg=BLACK,
            activebackground=RED,
            activeforeground=BLACK
        )

        self.set_message(
            "ARMED - WAITING FOR GAMELOOP",
            GREEN
        )

        self.update_hook()


    # ========================================================
    # DISARM
    # ========================================================

    def disarm(self):

        # Stop armed state first
        self.armed = False

        # Stop sequence
        self.sequence_running = False

        # Remove F hook immediately
        self.remove_f_hook()

        # ====================================================
        # CRITICAL FIX:
        # Change the BUTTON COMMAND back to ARM.
        # ====================================================

        self.arm_button.config(
            text="ARM",
            command=self.arm,
            bg=GREEN,
            fg=BLACK,
            activebackground=GREEN,
            activeforeground=BLACK
        )

        self.set_message(
            "DISARMED",
            RED
        )


    # ========================================================
    # INSTALL F HOOK
    # ========================================================

    def install_f_hook(self):

        if keyboard is None:
            return

        if self.f_hooked:
            return

        try:

            keyboard.hook_key(
                "f",
                self._f_event,
                suppress=True
            )

            self.f_hooked = True

        except Exception as e:

            self.f_hooked = False

            print(
                "Could not install F hook:",
                e
            )


    # ========================================================
    # REMOVE F HOOK
    # ========================================================

    def remove_f_hook(self):

        if keyboard is None:
            return

        if not self.f_hooked:
            return

        try:

            keyboard.unhook_key(
                "f"
            )

        except Exception as e:

            print(
                "Could not remove F hook:",
                e
            )

        finally:

            self.f_hooked = False


    # ========================================================
    # UPDATE HOOK
    # ========================================================

    def update_hook(self):

        # NEVER hook F while disarmed
        if not self.armed:

            self.remove_f_hook()

            return

        if self.require_focus:

            if is_target_focused():

                self.install_f_hook()

            else:

                self.remove_f_hook()

        else:

            self.install_f_hook()


    # ========================================================
    # F EVENT
    # ========================================================

    def _f_event(
        self,
        event
    ):

        if event.event_type != "down":
            return

        if not self.armed:
            return

        if self.require_focus:

            if not is_target_focused():
                return

        if self.sequence_running:
            return

        self.sequence_running = True

        worker = threading.Thread(
            target=self._run_sequence,
            daemon=True
        )

        worker.start()


    # ========================================================
    # RUN SEQUENCE
    # ========================================================

    def _run_sequence(self):

        try:

            for key in list(
                self.keys
            ):

                if not self.armed:
                    break

                if self.require_focus:

                    if not is_target_focused():
                        break

                try:

                    keyboard.press_and_release(
                        key
                    )

                except Exception as e:

                    print(
                        f"Could not send key {key}: {e}"
                    )

                if self.delay > 0:

                    time.sleep(
                        self.delay
                    )

        finally:

            self.sequence_running = False


    # ========================================================
    # F12 EMERGENCY DISARM
    # ========================================================

    def f12_loop(self):

        try:

            if (
                user32.GetAsyncKeyState(
                    VK_F12
                ) & 0x8000
            ):

                if self.armed:

                    self.disarm()

        except Exception:

            pass

        self.root.after(
            50,
            self.f12_loop
        )


    # ========================================================
    # STATUS
    # ========================================================

    def set_message(
        self,
        text,
        color
    ):

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.config(
                text=text,
                fg=color
            )


    def update_status_loop(self):

        focused = False

        try:

            focused = is_target_focused()

        except Exception:

            focused = False

        if focused:

            self.target_label.config(
                text="GameLoop: FOCUSED",
                fg=GREEN
            )

        else:

            self.target_label.config(
                text="GameLoop: NOT FOCUSED",
                fg=MUTED
            )

        # ----------------------------------------------------
        # ARMED
        # ----------------------------------------------------

        if self.armed:

            if focused:

                self.status_label.config(
                    text="ARMED • READY",
                    fg=GREEN
                )

            else:

                self.status_label.config(
                    text="ARMED • WAITING",
                    fg=ORANGE
                )

            self.update_hook()

        # ----------------------------------------------------
        # DISARMED
        # ----------------------------------------------------

        else:

            self.status_label.config(
                text="DISARMED",
                fg=RED
            )

            self.remove_f_hook()

        self.root.after(
            250,
            self.update_status_loop
        )


    # ========================================================
    # EXIT
    # ========================================================

    def exit_application(self):

        self.armed = False

        self.sequence_running = False

        self.remove_f_hook()

        try:

            self.save_config(
                show_message=False
            )

        except Exception:

            pass

        try:

            self.root.destroy()

        except Exception:

            pass


# ============================================================
# MAIN
# ============================================================

def main():

    if keyboard is None:

        print(
            "ERROR: keyboard module is not installed."
        )

        print(
            "Install it with:"
        )

        print(
            "py -m pip install keyboard"
        )

        return

    root = tk.Tk()

    GameLoopSmartkeys(
        root
    )

    root.mainloop()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
