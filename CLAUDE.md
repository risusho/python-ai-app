# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A Streamlit + Gemini API personal writing tool (Japanese UI). `app.py` is the home page; each feature is a separate page under `pages/` (blog article generation, email reply drafting, text summarization, proofreading/rewriting, title/catchcopy generation). Shared logic lives in `utils/`:
- `gemini_client.py` — Gemini client, `generate_text()`, model list
- `history.py` — reads/writes `data/history.json` (auto-created, gitignored)
- `ui.py` — shared sidebar (model selector, API key warning)

## Setup and running

- Dependencies: `pip install -r requirements.txt` (plain pip, no lockfile) into `.venv`
- Requires a `.env` file with `GEMINI_API_KEY=...` (see `.env.example`); without it the app shows a warning banner instead of failing
- Run with `streamlit run app.py`

## Adding a new writing tool

New features are added as a new file in `pages/`, following the existing pages' pattern: `render_common_sidebar()` for the model selector, build a prompt string, call `generate_text(prompt, model=model)`, store the result in `st.session_state`, and call `add_history(category, input_summary, result)`. Use the `new-tool-page` skill to scaffold this.

## Linting and tests

- `ruff check .` (config in `ruff.toml`, line-length 160 to accommodate long Japanese prompt strings). Install with `pip install -r requirements-dev.txt`. A `PostToolUse` hook in `.claude/settings.json` also runs `py_compile` on every edited `.py` file to catch syntax errors immediately.
- `pytest` runs the tests under `tests/` (currently covers `utils/history.py`). A root-level `conftest.py` exists solely so `utils` is importable from test modules — don't remove it.

## Known quirks

- `AVAILABLE_MODELS` in `utils/gemini_client.py` includes `"gemini-3.5-flash"`, which is not a real Gemini model name (likely a typo/placeholder). Don't "fix" this without checking with the user first — flag it if it comes up.
- Python is 3.9 (soon EOL) — the `google-auth` `FutureWarning` about this on every run is expected noise, not a bug.

## Windows environment notes

- `jq` is not installed in this environment's Bash tool. When writing hook commands or scripts that need to parse JSON from stdin, use `python -X utf8 -c "..."` instead.
- Filenames/content containing Japanese text or emoji (e.g. the `pages/` filenames) can get mangled when piped through commands without forcing UTF-8 — always run Python with `-X utf8` (or set `PYTHONUTF8=1`) when it touches such paths or JSON payloads.
- `/tmp/...` paths don't resolve for the Windows-native Python interpreter even though Git Bash accepts them — use a relative path inside the repo (or a real Windows path) for any file a Python subprocess needs to read/write.
- Terminal output showing garbled Japanese text is usually a console codepage display issue, not an actual encoding bug — verify by writing the text to a UTF-8 file and reading that back instead of trusting the terminal.

---

# CLAUDE.md(日本語版)

このファイルは、このリポジトリのコードを扱う際にClaude Code(claude.ai/code)へガイダンスを提供するものです。

## プロジェクト概要

Streamlit + Gemini APIを使った個人用ライティングツール(日本語UI)。`app.py`がホームページで、各機能は`pages/`配下の個別ファイルになっている(ブログ記事生成、メール返信作成、文章要約、校正・リライト、タイトル・キャッチコピー生成)。共通ロジックは`utils/`にある:
- `gemini_client.py` — Geminiクライアント、`generate_text()`、モデル一覧
- `history.py` — `data/history.json`の読み書き(自動生成、gitignore対象)
- `ui.py` — 共通サイドバー(モデル選択、APIキー未設定警告)

## セットアップと起動

- 依存関係: `pip install -r requirements.txt`(プレーンなpip、ロックファイルなし)を`.venv`にインストール
- `.env`ファイルに`GEMINI_API_KEY=...`が必要(`.env.example`参照)。未設定でもエラーにはならず、アプリ上に警告バナーが表示される
- `streamlit run app.py`で起動

## 新しいライティング機能の追加

新機能は`pages/`配下に新しいファイルとして追加し、既存ページと同じパターンに従う: `render_common_sidebar()`でモデル選択、プロンプト文字列を組み立て、`generate_text(prompt, model=model)`を呼び出し、結果を`st.session_state`に保存し、`add_history(category, input_summary, result)`を呼ぶ。スキャフォールドには`new-tool-page`スキルを使うこと。

## Lintとテスト

- `ruff check .`(設定は`ruff.toml`、日本語プロンプト文字列が長いため行長160)。`pip install -r requirements-dev.txt`でインストール。`.claude/settings.json`の`PostToolUse`フックが、編集された`.py`ファイルに対して毎回`py_compile`を実行し、構文エラーを即座に検出する。
- `pytest`で`tests/`配下のテストを実行(現状`utils/history.py`をカバー)。ルート直下の`conftest.py`は`utils`をテストモジュールからインポート可能にするためだけに存在するので削除しないこと。

## 既知の癖

- `utils/gemini_client.py`の`AVAILABLE_MODELS`に`"gemini-3.5-flash"`が含まれているが、これは実在しないGeminiのモデル名(おそらくタイポ/プレースホルダー)。ユーザーに確認せずに「修正」しないこと — 話題に出たら指摘する。
- Pythonは3.9(まもなくEOL) — 毎回出る`google-auth`の`FutureWarning`は想定内のノイズであり、バグではない。

## Windows環境に関する注意

- この環境のBashツールには`jq`がインストールされていない。stdinからJSONをパースする必要があるフックコマンドやスクリプトを書く場合は、代わりに`python -X utf8 -c "..."`を使うこと。
- 日本語や絵文字を含むファイル名・コンテンツ(例: `pages/`配下のファイル名)は、UTF-8を強制しないままコマンドにパイプすると文字化けすることがある — そのようなパスやJSONペイロードを扱う際は必ず`-X utf8`付きでPythonを実行する(または`PYTHONUTF8=1`を設定する)。
- `/tmp/...`のパスは、Git Bashでは受け付けられてもWindowsネイティブのPythonインタプリタでは解決できない — Pythonのサブプロセスが読み書きするファイルには、リポジトリ内の相対パスか実際のWindows形式のパスを使うこと。
- ターミナル出力で日本語が文字化けして見える場合、たいていはコンソールのコードページ表示上の問題であり、実際のエンコーディングバグではない — ターミナルの表示を信用せず、テキストをUTF-8ファイルに書き出して読み直して確認すること。
