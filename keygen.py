"""
Key Generator
-------------
A standalone tool for generating login keys tied to a username.
Generated keys are saved to keys.json, which the Login app reads
to validate sign-ins.

Run with:  python keygen.py
"""

import json
import os
import secrets
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


def save_keys(data):
    with open(KEYS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_key():
    # 16 hex-char key, grouped for readability: XXXX-XXXX-XXXX-XXXX
    raw = secrets.token_hex(8).upper()
    return "-".join(raw[i:i + 4] for i in range(0, len(raw), 4))


class KeyGenApp:
    def __init__(self, root):
        self.root = root
        root.title("Key Generator")
        root.geometry("420x260")
        root.resizable(False, False)

        tk.Label(root, text="Key Generator", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))

        form = tk.Frame(root)
        form.pack(pady=5)

        tk.Label(form, text="Username:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.username_entry = tk.Entry(form, font=("Segoe UI", 11), width=24)
        self.username_entry.grid(row=0, column=1, padx=5, pady=8)

        tk.Button(
            root, text="Generate Key", font=("Segoe UI", 11, "bold"),
            bg="#2d6cdf", fg="white", activebackground="#245bb5",
            padx=10, pady=6, command=self.on_generate
        ).pack(pady=10)

        self.result_var = tk.StringVar(value="")
        self.result_label = tk.Label(
            root, textvariable=self.result_var, font=("Consolas", 13, "bold"),
            fg="#1a7f37"
        )
        self.result_label.pack(pady=(5, 0))

        tk.Button(root, text="Copy Key", command=self.copy_key).pack(pady=8)

        self.current_key = None

    def on_generate(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Missing username", "Please enter a username first.")
            return

        keys = load_keys()
        new_key = generate_key()
        keys[username] = new_key
        save_keys(keys)

        self.current_key = new_key
        self.result_var.set(f"{username} -> {new_key}")
        messagebox.showinfo("Key generated", f"Key created for '{username}'.\nSaved to keys.json.")

    def copy_key(self):
        if not self.current_key:
            messagebox.showwarning("Nothing to copy", "Generate a key first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_key)
        messagebox.showinfo("Copied", "Key copied to clipboard.")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyGenApp(root)
    root.mainloop()
