import streamlit as st

from utils.gemini_client import get_api_key
from utils.history import load_history

st.set_page_config(page_title="AI ライティングツール", page_icon="✍️", layout="wide")

st.title("✍️ AI ライティングツール")
st.caption("Gemini APIを使った個人用ライティング支援ツール")

if not get_api_key():
    st.warning(
        "GEMINI_API_KEY が設定されていません。プロジェクト直下に `.env` ファイルを作成し、"
        "`GEMINI_API_KEY=あなたのAPIキー` を記載してください(`.env.example` を参考にしてください)。"
    )

st.markdown("### 機能一覧")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_📝_ブログ記事作成.py", label="📝 ブログ記事作成", help="トピックからブログ記事を生成")
    st.page_link("pages/2_📧_メール返信作成.py", label="📧 メール返信作成", help="受信メールへの返信文を生成")
    st.page_link("pages/3_📄_文章要約.py", label="📄 文章要約", help="長文を要約")
with col2:
    st.page_link("pages/4_✍️_校正リライト.py", label="✍️ 校正・リライト", help="誤字脱字チェックや文体変更")
    st.page_link(
        "pages/5_💡_タイトルキャッチコピー生成.py",
        label="💡 タイトル・キャッチコピー生成",
        help="タイトル案・キャッチコピー案を複数生成",
    )
    st.page_link("pages/6_🌐_英日翻訳.py", label="🌐 英日翻訳", help="英語の文章を日本語に翻訳")

st.markdown("---")
st.markdown("### 最近の生成履歴")

history = load_history()
if not history:
    st.info("まだ生成履歴がありません。")
else:
    for item in history[:5]:
        title = f"[{item['category']}] {item['timestamp']} - {item['input_summary'][:40]}"
        with st.expander(title):
            st.write(item["output_text"])
