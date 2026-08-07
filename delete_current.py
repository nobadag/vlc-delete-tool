"""
VLC now-playing file deleter
Ctrl+Alt+D (default) を押すと、VLCで再生中のローカルファイルを
次の曲へスキップしたうえでゴミ箱に移動します。

事前準備:
  1. VLC の 設定(すべて表示) > インターフェース > メインインターフェース で「Web」を有効化
  2. 同 > メインインターフェース > Lua でパスワードを設定
  3. config.ini を作成し、[vlc] password = 設定したパスワード を記入
     (config.example.ini をコピーして使ってください)
"""

import configparser
import os
import time
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname

import keyboard
import requests
from send2trash import send2trash

CONFIG_PATH = Path(__file__).with_name("config.ini")


def load_config():
    config = configparser.ConfigParser()
    if CONFIG_PATH.exists():
        config.read(CONFIG_PATH, encoding="utf-8")

    password = os.environ.get("VLC_PASSWORD") or config.get(
        "vlc", "password", fallback=""
    )
    host = os.environ.get("VLC_HOST") or config.get(
        "vlc", "host", fallback="127.0.0.1"
    )
    port = os.environ.get("VLC_PORT") or config.get("vlc", "port", fallback="8080")
    hotkey = os.environ.get("VLC_HOTKEY") or config.get(
        "vlc", "hotkey", fallback="ctrl+alt+d"
    )

    if not password:
        raise RuntimeError(
            "VLCのWebインターフェース用パスワードが設定されていません。"
            "config.ini か環境変数 VLC_PASSWORD を設定してください。"
        )

    return host, int(port), password, hotkey


VLC_HOST, VLC_PORT, VLC_PASSWORD, HOTKEY = load_config()
AUTH = ("", VLC_PASSWORD)


def find_current(node):
    if node.get("current") == "current":
        return node
    for child in node.get("children", []):
        result = find_current(child)
        if result:
            return result
    return None


def uri_to_path(uri):
    return url2pathname(unquote(urlparse(uri).path))


def delete_current_file():
    try:
        r = requests.get(
            f"http://{VLC_HOST}:{VLC_PORT}/requests/playlist.json",
            auth=AUTH,
            timeout=3,
        )
        r.raise_for_status()
        current = find_current(r.json())

        if not current or not current.get("uri", "").startswith("file://"):
            print("再生中のローカルファイルが見つかりません")
            return

        path = uri_to_path(current["uri"])

        # 次の曲へ進めてファイルロックを解除
        requests.get(
            f"http://{VLC_HOST}:{VLC_PORT}/requests/status.json",
            params={"command": "pl_next"},
            auth=AUTH,
            timeout=3,
        )
        time.sleep(0.3)

        send2trash(path)
        print("ゴミ箱に移動しました:", path)
    except requests.exceptions.RequestException as e:
        print("VLCに接続できませんでした(VLCが起動しているか確認してください):", e)
    except Exception as e:
        print("エラー:", e)


def main():
    keyboard.add_hotkey(HOTKEY, delete_current_file)
    print(f"待機中... {HOTKEY} で再生中ファイルを削除します")
    keyboard.wait()


if __name__ == "__main__":
    main()
