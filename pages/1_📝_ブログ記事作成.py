import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="ブログ記事作成", page_icon="📝")
model = render_common_sidebar()

st.title("📝 ブログ記事作成")
st.caption("トピックを入力すると、Geminiがブログ記事の下書きを生成します。")

topic = st.text_input("記事のトピック・テーマ", placeholder="例: 在宅ワークの生産性を上げる方法")
keywords = st.text_input("含めたいキーワード(任意、カンマ区切り)", placeholder="例: 集中力, タイムマネジメント")
tone = st.selectbox("文体・トーン", ["カジュアル", "フォーマル", "専門的", "親しみやすい"])
length = st.select_slider("目安の文字数", options=[300, 500, 800, 1200, 2000], value=800)

if st.button("記事を生成", type="primary", disabled=not topic):
    prompt = f"""あなたはSEOに精通したプロのブログライターです。以下の条件で、検索エンジンからの流入を意識したブログ記事を書いてください。

テーマ: {topic}
SEOキーワード: {keywords if keywords else "指定なし"}
文体・トーン: {tone}
文字数目安: 約{length}文字

# SEOに関する指示
- 本文の一番最初に「タイトル案:」に続けて、検索結果のタイトルタグとして使える32文字前後のタイトル案を1つ書く
- 次に「メタディスクリプション:」に続けて、120文字前後の要約文を1つ書く(クリックしたくなる内容にする)
- SEOキーワードは、タイトル案・冒頭の1段落目・少なくとも1つの見出しに、不自然にならない範囲で自然に含める
- 本文の見出しは##(h2)と###(h3)を使い、読者の検索意図(知りたい/比較したい/やり方を知りたい、など)に沿った論理的な階層構成にする
- 各段落は3〜4行以内に収め、必要に応じて箇条書きや表を使って読みやすくする
- 冒頭で結論・要点を先に述べ(結論ファースト)、後半で詳細を展開する
- 最後に「## まとめ」の見出しを置き、要点を箇条書きで再掲する

読者が最後まで読みたくなるような記事にしてください。"""
    with st.spinner("記事を生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["blog_result"] = result
            add_history("ブログ記事作成", topic, result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "blog_result" in st.session_state:
    st.markdown("### 生成結果")
    st.markdown(st.session_state["blog_result"])
    st.text_area("コピー用テキスト", st.session_state["blog_result"], height=300)
