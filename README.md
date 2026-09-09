# Username + Key Login System

Two small desktop apps (Python + tkinter) that work together:

## Files
- **keygen.py** — generates a key for a username, saved to `keys.json`.
  Also lists every existing username/key and lets you **Deactivate** or
  **Reactivate** them.
- **login.py** — asks for a username + key, checks them against
  `keys.json`. On a valid, active match it shows a **"Login Successful"**
  screen with a **Close** button. A deactivated key is rejected with
  "This key has been deactivated."
- **keys.json** — created automatically the first time you generate a key.
  Both apps must live in the same folder so they share this file.

## Running from source

1. Make sure Python 3 is installed (tkinter ships with it on Windows/macOS;
   on Linux you may need `sudo apt install python3-tk`).
2. Run the key generator:
   ```
   python keygen.py
   ```
   Enter a username, click **Generate Key**, and note the key shown
   (or click **Copy Key**).
3. Run the login app:
   ```
   python login.py
   ```
   Enter the same username and key, click **Login**. On success you'll see
   **"Login Successful"** with a **Close** button.

## Deactivating a key

Open `keygen.py` — every username you've generated a key for shows up in
the **Existing Keys** list along with its status (`ACTIVE` or
`DEACTIVATED`). Click a row to select it, then:
- **Deactivate** — the key stops working for login, but stays in
  `keys.json` so you can turn it back on later.
- **Reactivate** — turns a deactivated key back on.
- **Refresh** — reloads the list (useful if `keys.json` changed on disk).

Deactivating doesn't delete anything — it just flips a flag, so nothing
is lost if you deactivate the wrong user by mistake.

## Turning it into .exe files via GitHub

This repo includes a GitHub Actions workflow (`.github/workflows/build.yml`)
that automatically builds `keygen.exe` and `login.exe` for Windows using
PyInstaller — you don't need Windows or PyInstaller installed locally.

### 1. Push this folder to a new GitHub repo

```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2. Let the workflow build the EXEs

As soon as you push to `main`, GitHub Actions will run automatically.
To watch it:
1. Go to your repo on GitHub.
2. Click the **Actions** tab.
3. Open the latest **Build Windows EXEs** run.

You can also trigger it manually any time from Actions -> **Build Windows
EXEs** -> **Run workflow**.

### 3. Download the .exe files

When the run finishes (green check), scroll to the bottom of that run's
page to **Artifacts** and download `auth-app-windows-exes.zip` — it
contains `keygen.exe` and `login.exe`.

### 4. (Optional) Get them attached to a Release automatically

If you push a version tag, the workflow also creates a GitHub Release with
the .exe files attached as downloads:

```
git tag v1.0.0
git push origin v1.0.0
```

Then check the **Releases** section of your repo — `keygen.exe` and
`login.exe` will be attached there for anyone to download directly.

## Notes / things you could extend later
- Keys are currently stored in plain text in `keys.json` for simplicity —
  fine for a local demo, but if this is ever exposed to other people you'd
  want to hash the keys (e.g. with `hashlib.sha256`) before saving/comparing.
- Right now generating a new key for a username overwrites their old one.
- You could add key expiry, one-time-use keys, or multiple keys per user
  by extending the JSON structure.
- Both `keygen.exe` and `login.exe` will look for `keys.json` next to
  wherever the .exe is run from, so keep them in the same folder (or
  point both at a shared network/cloud-synced folder) if you want the
  generator and the login app on different machines to share keys.
