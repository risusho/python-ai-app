---
name: run-app
description: Start this Streamlit app correctly on this machine (venv, .env check, headless launch, health check). Use when the user asks to run, start, restart, or verify the app is working.
---

1. Confirm dependencies are installed in `.venv`: `.venv/Scripts/python.exe -c "import streamlit, google.genai, dotenv"`. If this fails, run `.venv/Scripts/python.exe -m pip install -r requirements.txt` first.
2. Check `.env` exists and has a non-placeholder `GEMINI_API_KEY`. If missing, warn the user — the app will still start but show a warning banner and generation will fail.
3. If a Streamlit process is already running on port 8501 and `.env` was changed since it started, kill and restart it — env vars are loaded once at process start (`load_dotenv()` in `utils/gemini_client.py`), so edits to `.env` require a restart to take effect.
4. Launch in the background: `.venv/Scripts/python.exe -m streamlit run app.py --server.headless true --server.port 8501`
5. Verify it's up: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` should return `200`.

Known noise to ignore, not fix:
- Console output may show mojibake (garbled Japanese) for non-ASCII text — this is a Windows console codepage display issue, not a real encoding bug in the app. If verifying generated Japanese text, write it to a file with `encoding="utf-8"` and read that back instead of trusting terminal output.
- `FutureWarning: You are using a Python version 3.9 past its end of life` from `google-auth` on every run — expected given the installed Python 3.9, not an app bug.

---

## 日本語版

1. `.venv`に依存関係がインストール済みか確認する: `.venv/Scripts/python.exe -c "import streamlit, google.genai, dotenv"`。失敗する場合は先に`.venv/Scripts/python.exe -m pip install -r requirements.txt`を実行する。
2. `.env`が存在し、プレースホルダーでない`GEMINI_API_KEY`が設定されているか確認する。未設定の場合はユーザーに警告する — アプリ自体は起動するが警告バナーが表示され、生成は失敗する。
3. すでにポート8501でStreamlitが起動しており、その起動後に`.env`が変更されている場合はプロセスを停止して再起動する — 環境変数はプロセス起動時に一度だけ読み込まれる(`utils/gemini_client.py`内の`load_dotenv()`)ため、`.env`の変更を反映するには再起動が必要。
4. バックグラウンドで起動する: `.venv/Scripts/python.exe -m streamlit run app.py --server.headless true --server.port 8501`
5. 起動確認: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` が `200` を返せばOK。

無視してよい(修正不要な)ノイズ:
- コンソール出力で日本語が文字化けして表示されることがある — これはWindowsのコンソールコードページの表示上の問題であり、アプリ自体のエンコーディングバグではない。生成された日本語テキストを検証する場合は、`encoding="utf-8"`でファイルに書き出してから読み直すこと(ターミナル表示を信用しない)。
- 毎回出る`google-auth`の`FutureWarning: You are using a Python version 3.9 past its end of life` — インストールされているPythonが3.9であることによる想定内の警告で、アプリのバグではない。
