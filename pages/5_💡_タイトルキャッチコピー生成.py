import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="タイトル・キャッチコピー生成", page_icon="💡")
model = render_common_sidebar()

st.title("💡 タイトル・キャッチコピー生成")
st.caption("トピックを入力すると、記事タイトル案やキャッチコピー案を複数生成します。")

topic = st.text_input("トピック・記事の内容", placeholder="例: 副業で月5万円を稼ぐ方法")
target = st.text_input("ターゲット読者(任意)", placeholder="例: 20代の会社員")
style = st.selectbox("スタイル", ["クリックしたくなる(SEO・煽り強め)", "上品・落ち着いた", "驚き・数字を使う", "疑問形"])
count = st.slider("生成する案の数", min_value=3, max_value=15, value=8)

if st.button("生成する", type="primary", disabled=not topic):
    prompt = f"""あなたは優秀なコピーライターです。以下の条件でタイトル・キャッチコピー案を{count}個生成してください。

テーマ: {topic}
ターゲット読者: {target if target else "指定なし"}
スタイル: {style}

番号付きリストで、案のみを簡潔に出力してください。"""
    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["title_result"] = result
            add_history("タイトル・キャッチコピー生成", topic, result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "title_result" in st.session_state:
    st.markdown("### 生成結果")
    st.markdown(st.session_state["title_result"])
