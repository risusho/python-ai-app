import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="校正・リライト", page_icon="✍️")
model = render_common_sidebar()

st.title("✍️ 校正・リライト")
st.caption("文章の誤字脱字チェックや、文体の変更・簡潔化を行います。")

source_text = st.text_area("校正・リライトしたい文章", height=250, placeholder="ここに文章を貼り付けてください")
mode = st.selectbox(
    "モード",
    [
        "誤字脱字・文法チェック",
        "丁寧語(です・ます調)にする",
        "カジュアルな文体にする",
        "簡潔にする",
        "より説得力のある文章にする",
    ],
)

if st.button("実行", type="primary", disabled=not source_text):
    if mode == "誤字脱字・文法チェック":
        instruction = "誤字脱字・文法的な誤りを指摘し、修正案を提示してください。修正箇所と理由も簡潔に説明してください。"
    else:
        instruction = f"次の指示に従って文章をリライトしてください: {mode}"

    prompt = f"""あなたはプロの校正者・編集者です。以下の文章に対して次の作業を行ってください。

# 作業内容
{instruction}

# 対象の文章
{source_text}"""
    with st.spinner("処理中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["rewrite_result"] = result
            add_history("校正・リライト", f"[{mode}] {source_text[:40]}", result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "rewrite_result" in st.session_state:
    st.markdown("### 結果")
    st.markdown(st.session_state["rewrite_result"])
    st.text_area("コピー用テキスト", st.session_state["rewrite_result"], height=250)
