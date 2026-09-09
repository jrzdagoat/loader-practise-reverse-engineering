"""
Login App
---------
Reads keys.json (produced by keygen.py) and validates a username + key
pair. On success, shows a "Login Successful" screen with a Close button.

Run with:  python login.py
"""

import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# See the matching comment in keygen.py: when frozen into a --onefile .exe,
# __file__ points at a temp extraction folder, not the real .exe location.
# Use sys.executable instead so both exes look next to themselves for
# keys.json and actually share the same file.
if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

KEYS_FILE = os.path.join(APP_DIR, "keys.json")


def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    try:
        with open(KEYS_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

    # Support old-format keys.json where values were plain strings
    # (no active/deactivated concept yet) - treat those as active.
    for username, value in data.items():
        if isinstance(value, str):
            data[username] = {"key": value, "active": True}
    return data


class LoginApp:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        root.geometry("380x320")
        root.resizable(False, False)

        self.login_frame = tk.Frame(root)
        self.success_frame = tk.Frame(root)

        self.build_login_frame()
        self.build_success_frame()

        self.login_frame.pack(expand=True, fill="both")

    def build_login_frame(self):
        f = self.login_frame
        tk.Label(f, text="Sign In", font=("Segoe UI", 16, "bold")).pack(pady=(25, 15))

        form = tk.Frame(f)
        form.pack()

        tk.Label(form, text="Username:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=6)
        self.username_entry = tk.Entry(form, font=("Segoe UI", 11), width=22)
        self.username_entry.grid(row=0, column=1, padx=5, pady=6)

        tk.Label(form, text="Key:", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=6)
        self.key_entry = tk.Entry(form, font=("Segoe UI", 11), width=22, show="*")
        self.key_entry.grid(row=1, column=1, padx=5, pady=6)

        self.error_var = tk.StringVar(value="")
        tk.Label(f, textvariable=self.error_var, fg="#c0392b", font=("Segoe UI", 10)).pack(pady=(5, 0))

        tk.Button(
            f, text="Login", font=("Segoe UI", 11, "bold"),
            bg="#2d6cdf", fg="white", activebackground="#245bb5",
            padx=10, pady=6, command=self.attempt_login
        ).pack(pady=15)

        # Shows exactly which keys.json this app is reading -
        # if keygen.py shows a different path, that's why login fails.
        tk.Label(
            f, text=f"keys.json location:\n{KEYS_FILE}",
            font=("Segoe UI", 8), fg="#666666", justify="center"
        ).pack(pady=(0, 5))

    def build_success_frame(self):
        f = self.success_frame
        tk.Label(f, text="✅", font=("Segoe UI", 32)).pack(pady=(30, 5))
        tk.Label(f, text="Login Successful", font=("Segoe UI", 16, "bold"), fg="#1a7f37").pack(pady=(0, 25))
        tk.Button(
            f, text="Close", font=("Segoe UI", 11, "bold"),
            bg="#c0392b", fg="white", activebackground="#a5311f",
            padx=20, pady=6, command=self.root.destroy
        ).pack()

    def attempt_login(self):
        username = self.username_entry.get().strip()
        key = self.key_entry.get().strip()

        if not username or not key:
            self.error_var.set("Enter both a username and a key.")
            return

        keys = load_keys()
        entry = keys.get(username)

        if entry is None or entry.get("key") != key:
            self.error_var.set("Invalid username or key.")
        elif not entry.get("active", True):
            self.error_var.set("This key has been deactivated.")
        else:
            self.login_frame.pack_forget()
            self.success_frame.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
