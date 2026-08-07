# vlc-delete-tool

[日本語版はこちら](README.md)

A small tool that lets you delete the file currently playing in VLC media player with a single hotkey.

It uses VLC's HTTP (Web) interface to find the path of the currently playing file, skips to the next track to release the file lock, then moves the file to the Recycle Bin using `send2trash`.

## Requirements

- Windows
- Python 3.9+
- VLC media player (with the Web/Lua interface enabled)

## Setup

### 1. Configure VLC

1. Open `Tools > Preferences` in VLC
2. Switch the settings view (bottom-left) to "All"
3. Under `Interface > Main interfaces`, check **Web**
4. Under `Interface > Main interfaces > Lua`, set a password
5. Restart VLC

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your config file

Copy `config.example.ini` to `config.ini` and fill in the password you set in VLC:

```bash
copy config.example.ini config.ini
```

`config.ini` is excluded via `.gitignore`, so it won't accidentally get committed with your password in it.
You can also supply the password via the `VLC_PASSWORD` environment variable instead.

### 4. Run

```bash
python delete_current.py
```

The default hotkey is `Ctrl+Alt+D` (configurable in `config.ini`).

## Running VLC with the script automatically

You can either create a small batch file that launches both VLC and the script together, or have the script use `psutil` to watch for the VLC process and register the hotkey once it starts. Adjust to whatever fits your setup.

## Notes

- Deletion is done via `send2trash`, i.e. files go to the Recycle Bin, not permanently deleted.
- Non-local content (e.g. network streams) is skipped and never deleted.
- Use at your own risk — the author is not responsible for accidental file deletion.

## License

MIT
