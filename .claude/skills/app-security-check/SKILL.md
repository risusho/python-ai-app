---
name: app-security-check
description: Perform a security check of this Streamlit + Gemini writing app. Covers app-specific risks - API key/secret leakage, prompt injection into Gemini prompts, Streamlit rendering risks (unsafe_allow_html/XSS), and dependency vulnerabilities - either across the whole codebase or limited to pending changes (git diff). Use whenever the user asks to security-check, audit, or scan this app for vulnerabilities, e.g. "このアプリをセキュリティチェックして", "脆弱性ないか確認して", "check this app for security issues".
---

Audit this repo for security issues. This app is a single-user Streamlit tool that calls the Gemini API, so the checklist below is scoped to what can actually go wrong here — not a generic OWASP checklist.

## 1. Pick a scope

- **Full scan** (default): walk `app.py`, `pages/*.py`, `utils/*.py`, and config files `.env.example`, `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `ruff.toml`.
- **Diff scan**: if the user's phrasing implies only recent/pending changes ("before I merge this", "diff", "変更点だけ", "レビュー"), run `git diff main...HEAD` (or `git diff` for uncommitted changes) and restrict the checklist below to the touched files/lines only.
- If it's genuinely unclear which the user wants, ask before starting — the results and effort differ a lot.

## 2. Check these four areas

### API key / secret leakage
- `utils/gemini_client.get_api_key()` reads `GEMINI_API_KEY` from the environment via `python-dotenv`. Confirm no code hardcodes a key literal, prints it, or includes it in an `st.error(...)` / logged exception message.
- Confirm `.gitignore` still excludes `.env`, `.streamlit/secrets.toml`, and `data/history.json` (history entries can contain arbitrary user text, so it must never be committed).
- If any new code persists request/response data (following the `history.py` pattern), check it doesn't also capture the API key or other credentials.

### Prompt injection
- Every page builds its Gemini prompt with an f-string that interpolates raw `st.text_input`/`st.text_area` values directly (see `pages/1_📝_ブログ記事作成.py` for the canonical pattern) with no delimiter or escaping. For a single-user personal tool this is an accepted, low-severity risk — don't flag the pattern itself.
- Do flag it as a real finding if you find a case where: Gemini's *output* is fed back into another prompt unreviewed (chained injection), or Gemini's output ends up controlling app behavior — used as a filename, shell/subprocess argument, `eval`'d, or used to build a file path. None of the current pages do this; call it out clearly if a new one does.

### Streamlit rendering risk
- Grep for `unsafe_allow_html=True` across `pages/` and `utils/`. As of now none of the pages use it. `st.markdown()` does not execute raw HTML/JS without that flag, so rendering Gemini's text output via `st.markdown()` (as every page does) is not itself an XSS risk — only flag it if `unsafe_allow_html=True` shows up anywhere near user- or model-controlled text.

### Dependency vulnerabilities
- Run `python .claude/skills/app-security-check/scripts/check_dependencies.py` from the repo root against `requirements.txt` and `requirements-dev.txt`. It uses `pip-audit` if available in the active environment, otherwise falls back to querying the OSV.dev API directly using the versions actually installed in `.venv`.
- Also note, as a Low/Info item, that this project targets Python 3.9, which is close to end-of-life — no security patches will be backported once it's EOL. This is a known, accepted quirk (see CLAUDE.md) — report it as an informational note, not a blocking finding.

## 3. Don't flag these as vulnerabilities

- `AVAILABLE_MODELS` in `utils/gemini_client.py` containing `"gemini-3.5-flash"` — this is a known naming quirk unrelated to security (see CLAUDE.md). Never "fix" it as part of a security check.
- The `google-auth` `FutureWarning` about Python 3.9 that prints on every run — expected noise, not a bug.

## 4. Report format

Write a Markdown report directly in the chat (no need to save it to a file) with this structure:

```markdown
# セキュリティチェック結果

**対象範囲:** <full scan | diff (base..head)>
**チェック日:** <date>

## サマリー
<1-3 sentence overview: how many findings, overall risk level>

## 🔴 Critical
## 🟠 High
## 🟡 Medium
## 🔵 Low / Info

各項目: `file:line` — 内容の説明 — 推奨対応
```

Omit severity sections that have no findings rather than writing "no findings" under each of them. If everything looks clean, say so briefly instead of forcing the template.

---

## 日本語版

このリポジトリのセキュリティをチェックする。このアプリはGemini APIを呼び出す個人向けStreamlitツールなので、以下のチェック項目は汎用的なOWASPチェックリストではなく、実際にこのアプリで起こりうるリスクに絞っている。

### 1. 範囲を選ぶ

- **フルスキャン(デフォルト)**: `app.py`、`pages/*.py`、`utils/*.py`、および設定ファイル(`.env.example`、`.gitignore`、`requirements.txt`、`requirements-dev.txt`、`ruff.toml`)を確認する。
- **差分スキャン**: ユーザーの言い回しが直近の変更点だけを指している場合(「マージ前に」「diffだけ」「変更点だけ」「レビューして」など)、`git diff main...HEAD`(またはコミット前の変更には`git diff`)を実行し、変更されたファイル・行のみに絞ってチェックする。
- どちらを求めているか本当に判断できない場合は、開始前にユーザーに確認する(範囲によって結果と工数が大きく変わるため)。

### 2. 4つの観点をチェックする

**APIキー・秘密情報の漏洩**
- `utils/gemini_client.get_api_key()`は`python-dotenv`経由で環境変数`GEMINI_API_KEY`を読む。キーをハードコードしたり、`print`したり、`st.error(...)`や例外メッセージに含めているコードがないか確認する。
- `.gitignore`が`.env`・`.streamlit/secrets.toml`・`data/history.json`を除外し続けているか確認する(履歴には任意のユーザーテキストが含まれうるため、コミットされてはならない)。
- `history.py`のパターンに倣ってリクエスト/レスポンスを永続化する新しいコードがあれば、APIキーなどの認証情報まで一緒に保存していないか確認する。

**プロンプトインジェクション**
- 各ページは`st.text_input`/`st.text_area`の値をそのままf-stringでプロンプトに埋め込んでいる(典型例は`pages/1_📝_ブログ記事作成.py`)。区切り文字やエスケープはない。個人用ツールとしてはこれは許容されている低リスクなパターンなので、これ自体を指摘しなくてよい。
- 一方で、Geminiの**出力**がレビューなしに別のプロンプトへ再投入されているケース(連鎖的なインジェクション)や、Geminiの出力がアプリの挙動を左右するケース(ファイル名・シェル/サブプロセス引数として使われる、`eval`される、パス生成に使われるなど)は実際の指摘事項として報告する。現状のページにはこのようなコードはないので、新規ページで見つかった場合は明確に指摘すること。

**Streamlit表示リスク**
- `pages/`と`utils/`全体で`unsafe_allow_html=True`をgrepする。現時点ではどのページも使用していない。`st.markdown()`はこのフラグなしでは生のHTML/JSを実行しないため、Geminiのテキスト出力を`st.markdown()`で表示すること自体(全ページ共通のパターン)はXSSリスクではない。ユーザー入力やモデル出力の近くで`unsafe_allow_html=True`が使われている場合のみ指摘する。

**依存パッケージの脆弱性**
- リポジトリのルートから`python .claude/skills/app-security-check/scripts/check_dependencies.py`を実行し、`requirements.txt`と`requirements-dev.txt`をチェックする。実行環境に`pip-audit`があればそれを使い、なければ`.venv`にインストールされている実際のバージョンを使ってOSV.dev APIに問い合わせる。
- また、このプロジェクトがPython 3.9を対象としており、EOL(サポート終了)が近いことをLow/Info項目として触れておく。EOL後はセキュリティパッチが提供されなくなる。これはCLAUDE.mdに記載済みの既知の事象なので、ブロッカーではなく情報提供として報告すること。

### 3. 脆弱性として指摘しないもの

- `utils/gemini_client.py`の`AVAILABLE_MODELS`に含まれる`"gemini-3.5-flash"` — CLAUDE.md記載の通り、セキュリティとは無関係な既知の命名の癖。セキュリティチェックの一環として「修正」しないこと。
- 毎回出力される`google-auth`のPython 3.9に関する`FutureWarning` — 想定内のノイズであり、バグではない。

### 4. レポート形式

チャット上に直接Markdownレポートを書く(ファイルへの保存は不要)。構成は以下の通り:

```markdown
# セキュリティチェック結果

**対象範囲:** <full scan | diff (base..head)>
**チェック日:** <date>

## サマリー
<1〜3文で概要: 指摘件数、全体的なリスクレベル>

## 🔴 Critical
## 🟠 High
## 🟡 Medium
## 🔵 Low / Info

各項目: `file:line` — 内容の説明 — 推奨対応
```

指摘のない重大度セクションは「該当なし」と書かず、省略する。全体的に問題がなければ、テンプレートに無理に当てはめず簡潔にその旨を伝える。
