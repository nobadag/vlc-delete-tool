# vlc-delete-tool

A small tool that lets you delete the file currently playing in VLC media player with a single hotkey.

日本語版は下にあります。([Jump to Japanese](#vlc-delete-tool-日本語))

It uses VLC's HTTP (Web) interface to find the path of the currently playing file, skips to the next track to release the file lock, then moves the file to the Recycle Bin using `send2trash`.

---

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

---

# vlc-delete-tool (日本語)

VLC media player で再生中のファイルを、ホットキー一発でゴミ箱に移動するツールです。

VLCのHTTP(Web)インターフェースを使って再生中ファイルのパスを取得し、
次の曲へスキップしてファイルロックを解除したうえで `send2trash` によりゴミ箱送りにします。

## 動作環境

- Windows
- Python 3.9+
- VLC media player (Web/Luaインターフェース利用)

## セットアップ

### 1. VLC側の設定

1. VLCの `ツール > 設定` を開く
2. 左下の表示設定を「すべて」に切り替える
3. `インターフェース > メインインターフェース` で **Web** にチェック
4. `インターフェース > メインインターフェース > Lua` でパスワードを設定
5. VLCを再起動

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 設定ファイルの作成

`config.example.ini` を `config.ini` にコピーし、VLCで設定したパスワードを記入してください。

```bash
copy config.example.ini config.ini
```

`config.ini` は `.gitignore` で除外されるため、誤ってパスワードをコミットする心配はありません。
環境変数 `VLC_PASSWORD` で渡すことも可能です。

### 4. 実行

```bash
python delete_current.py
```

デフォルトのホットキーは `Ctrl+Alt+D` です(`config.ini` で変更可能)。

## VLC起動時に自動実行したい場合

VLCとスクリプトをまとめて起動するバッチファイルを作成するか、
`psutil` でVLCプロセスの起動を監視してからホットキー登録する方式が使えます。

## 注意事項

- 削除は `send2trash` によるゴミ箱移動です。完全削除ではありません。
- ネットワークストリーム等、ローカルファイルでない再生中コンテンツは削除対象外です。
- 誤操作によるファイル削除について、作者は責任を負いません。自己責任でご利用ください。

## ライセンス

MIT
