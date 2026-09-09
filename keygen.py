"""
Key Generator
-------------
A standalone tool for generating login keys tied to a username, and for
deactivating/reactivating keys later without deleting them.

Keys are saved to keys.json, which the Login app reads to validate
sign-ins. Each entry looks like:

    {"username": {"key": "XXXX-XXXX-XXXX-XXXX", "active": true}}

Run with:  python keygen.py
"""

import json
import os
import sys
import secrets
import tkinter as tk
from tkinter import messagebox

# When PyInstaller bundles this into a --onefile .exe, __file__ points at a
# temporary extraction folder that's deleted after the app closes - not the
# actual .exe location. sys.executable is the real .exe path in that case,
# so keys.json ends up saved next to the .exe itself and both apps can find it.
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

    # Upgrade any old-format entries (plain string keys) to the new
    # {"key": ..., "active": true} shape so old keys.json files still work.
    changed = False
    for username, value in list(data.items()):
        if isinstance(value, str):
            data[username] = {"key": value, "active": True}
            changed = True
    if changed:
        save_keys(data)
    return data


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
        root.geometry("480x520")
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
        ).pack(pady=8)

        self.result_var = tk.StringVar(value="")
        tk.Label(
            root, textvariable=self.result_var, font=("Consolas", 12, "bold"), fg="#1a7f37"
        ).pack(pady=(0, 4))

        tk.Button(root, text="Copy Key", command=self.copy_key).pack(pady=(0, 15))

        # --- Existing keys list ---
        tk.Label(root, text="Existing Keys", font=("Segoe UI", 12, "bold")).pack(pady=(0, 5))

        list_frame = tk.Frame(root)
        list_frame.pack(fill="both", expand=True, padx=20)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame, font=("Consolas", 10), height=8,
            yscrollcommand=scrollbar.set, selectmode="single"
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        btn_row = tk.Frame(root)
        btn_row.pack(pady=10)

        tk.Button(
            btn_row, text="Deactivate", bg="#c0392b", fg="white",
            activebackground="#a5311f", padx=10, pady=4,
            command=self.deactivate_selected
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_row, text="Reactivate", bg="#1a7f37", fg="white",
            activebackground="#166a2e", padx=10, pady=4,
            command=self.reactivate_selected
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_row, text="Refresh", padx=10, pady=4,
            command=self.refresh_list
        ).grid(row=0, column=2, padx=5)

        # Shows exactly which keys.json this app is reading/writing -
        # if login.py shows a different path, that's why keys don't match.
        tk.Label(
            root, text=f"keys.json location:\n{KEYS_FILE}",
            font=("Segoe UI", 8), fg="#666666", justify="center"
        ).pack(pady=(5, 10))

        self.current_key = None
        self.list_entries = []  # parallel list of usernames matching listbox rows
        self.refresh_list()

    def on_generate(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Missing username", "Please enter a username first.")
            return

        keys = load_keys()
        new_key = generate_key()
        keys[username] = {"key": new_key, "active": True}
        save_keys(keys)

        self.current_key = new_key
        self.result_var.set(f"{username} -> {new_key}")
        messagebox.showinfo("Key generated", f"Key created for '{username}'.\nSaved to keys.json.")
        self.refresh_list()

    def copy_key(self):
        if not self.current_key:
            messagebox.showwarning("Nothing to copy", "Generate a key first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_key)
        messagebox.showinfo("Copied", "Key copied to clipboard.")

    def refresh_list(self):
        keys = load_keys()
        self.listbox.delete(0, "end")
        self.list_entries = []
        for username in sorted(keys.keys()):
            entry = keys[username]
            status = "ACTIVE" if entry.get("active", True) else "DEACTIVATED"
            self.listbox.insert("end", f"{username:<15} {entry.get('key', ''):<20} [{status}]")
            self.list_entries.append(username)

    def get_selected_username(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Select a user from the list first.")
            return None
        return self.list_entries[selection[0]]

    def deactivate_selected(self):
        username = self.get_selected_username()
        if not username:
            return
        keys = load_keys()
        keys[username]["active"] = False
        save_keys(keys)
        messagebox.showinfo("Deactivated", f"Key for '{username}' has been deactivated.")
        self.refresh_list()

    def reactivate_selected(self):
        username = self.get_selected_username()
        if not username:
            return
        keys = load_keys()
        keys[username]["active"] = True
        save_keys(keys)
        messagebox.showinfo("Reactivated", f"Key for '{username}' has been reactivated.")
        self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyGenApp(root)
    root.mainloop()
