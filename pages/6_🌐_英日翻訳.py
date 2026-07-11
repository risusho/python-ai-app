import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="英日翻訳", page_icon="🌐")
model = render_common_sidebar()

st.title("🌐 英日翻訳")
st.caption("英語の文章を貼り付けると、日本語に翻訳します。")

source_text = st.text_area("翻訳したい英文", height=250, placeholder="ここに英語の文章を貼り付けてください")
style = st.selectbox("翻訳のスタイル", ["自然な日本語(意訳)", "原文に忠実(直訳)", "ビジネス文書調", "カジュアル"])
notes = st.text_input("補足(専門用語・文脈など、任意)", placeholder="例: ITの専門用語が多い記事です")

if st.button("翻訳する", type="primary", disabled=not source_text):
    prompt = f"""あなたはプロの翻訳者です。以下の英文を日本語に翻訳してください。

# 翻訳する英文
{source_text}

# 翻訳のスタイル
{style}

# 補足情報
{notes if notes else "特になし"}

自然に読める日本語で、原文の意味を漏らさず翻訳してください。"""
    with st.spinner("翻訳中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["translate_result"] = result
            add_history("英日翻訳", source_text[:50], result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "translate_result" in st.session_state:
    st.markdown("### 翻訳結果")
    st.markdown(st.session_state["translate_result"])
    st.text_area("コピー用テキスト", st.session_state["translate_result"], height=250)
