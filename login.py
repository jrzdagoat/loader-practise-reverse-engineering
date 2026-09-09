"""
Login App
---------
Reads keys.json (produced by keygen.py) and validates a username + key
pair. On success, shows a "Login Successful" screen with a Close button.

Run with:  python login.py
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

KEYS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys.json")


def load_keys():
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


class LoginApp:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        root.geometry("380x260")
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
        expected = keys.get(username)

        if expected is not None and expected == key:
            self.login_frame.pack_forget()
            self.success_frame.pack(expand=True, fill="both")
        else:
            self.error_var.set("Invalid username or key.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
