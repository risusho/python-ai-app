---
name: new-tool-page
description: Scaffold a new AI writing feature as a page under pages/, following the existing pattern (sidebar model selector, prompt template, generate_text call, history logging, session-state result display). Use when the user wants to add a new writing tool/feature to this app.
---

Create a new file in `pages/` named `N_<emoji>_<機能名>.py` where `N` is the next number after the existing pages (currently 1-5). Follow this structure, modeled on `pages/1_📝_ブログ記事作成.py`:

```python
import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="<ページ名>", page_icon="<絵文字>")
model = render_common_sidebar()

st.title("<絵文字> <ページ名>")
st.caption("<説明>")

# Input widgets (st.text_input / st.text_area / st.selectbox / st.select_slider as needed)

if st.button("<実行ボタン名>", type="primary", disabled=not <required_input>):
    prompt = f"""<プロンプトテンプレート>"""
    with st.spinner("処理中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["<page>_result"] = result
            add_history("<カテゴリ名>", <input_summary>, result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "<page>_result" in st.session_state:
    st.markdown("### 結果")
    st.markdown(st.session_state["<page>_result"])
    st.text_area("コピー用テキスト", st.session_state["<page>_result"], height=250)
```

Rules to follow:
- Session state key and history category must be unique per page (don't collide with existing pages' keys).
- `add_history()`'s second argument is a short input summary string (truncate long text inputs, e.g. `source_text[:50]`).
- Wrap the `generate_text` call in `st.spinner` + `try/except` exactly like the existing pages, so API errors surface as `st.error` instead of crashing the page.
- After scaffolding, verify the new file compiles: `.venv/Scripts/python.exe -m py_compile pages/<new_file>.py`.

---

## 日本語版

`pages/`配下に新規ファイルを作成する。ファイル名は`N_<絵文字>_<機能名>.py`とし、`N`は既存ページの続き番号(現在1〜6)。`pages/1_📝_ブログ記事作成.py`をモデルにした以下の構成に従うこと:

```python
import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="<ページ名>", page_icon="<絵文字>")
model = render_common_sidebar()

st.title("<絵文字> <ページ名>")
st.caption("<説明>")

# 入力ウィジェット(必要に応じて st.text_input / st.text_area / st.selectbox / st.select_slider)

if st.button("<実行ボタン名>", type="primary", disabled=not <required_input>):
    prompt = f"""<プロンプトテンプレート>"""
    with st.spinner("処理中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["<page>_result"] = result
            add_history("<カテゴリ名>", <input_summary>, result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "<page>_result" in st.session_state:
    st.markdown("### 結果")
    st.markdown(st.session_state["<page>_result"])
    st.text_area("コピー用テキスト", st.session_state["<page>_result"], height=250)
```

守るべきルール:
- セッションステートのキーと履歴カテゴリ名はページごとに一意にすること(既存ページのキーと衝突させない)。
- `add_history()`の第2引数は短い入力要約文字列にすること(長いテキスト入力は`source_text[:50]`のように切り詰める)。
- 既存ページと同様に`generate_text`の呼び出しを`st.spinner` + `try/except`で囲み、APIエラーがページをクラッシュさせず`st.error`として表示されるようにすること。
- 作成後は新規ファイルがコンパイルできることを確認すること: `.venv/Scripts/python.exe -m py_compile pages/<new_file>.py`。
