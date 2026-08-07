# vlc-delete-tool

[English README is here](README.en.md)

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

## License

MIT
