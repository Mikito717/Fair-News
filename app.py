import streamlit as st
import os
import sys
from datetime import datetime
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.generators.article_generator import ArticleGenerator
from src.generators.gemini_generator import GeminiArticleGenerator
from src.utils.article_manager import ArticleManager

# 環境変数を読み込み
load_dotenv("config/.env")

# ページ設定
st.set_page_config(
    page_title="AI自動コンテンツ生成システム",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """セッション状態の初期化"""
    if 'generated_article' not in st.session_state:
        st.session_state.generated_article = ""
    if 'article_metadata' not in st.session_state:
        st.session_state.article_metadata = {}
    if 'api_validated' not in st.session_state:
        st.session_state.api_validated = False
    if 'current_generator' not in st.session_state:
        st.session_state.current_generator = None

def create_sidebar():
    """サイドバーの作成"""
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # AIプロバイダー選択
        ai_provider = st.selectbox(
            "AIプロバイダー",
            ["OpenAI", "Gemini"],
            help="使用するAIサービスを選択してください"
        )
        
        if ai_provider == "OpenAI":
            # OpenAI設定
            api_key = st.text_input(
                "OpenAI APIキー",
                type="password",
                value=os.getenv("OPENAI_API_KEY", ""),
                help="OpenAI APIキーを入力してください"
            )
            
            model = st.selectbox(
                "AIモデル選択",
                ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                index=0,
                help="使用するOpenAIモデルを選択してください"
            )
            
        else:  # Gemini
            # Gemini設定
            api_key = st.text_input(
                "Gemini APIキー",
                type="password",
                value=os.getenv("GEMINI_API_KEY", ""),
                help="Google Gemini APIキーを入力してください"
            )
            
            model = st.selectbox(
                "AIモデル選択",
                ["gemini-1.5-flash", "gemini-1.5-pro"],
                index=0,
                help="使用するGeminiモデルを選択してください"
            )
        
        # APIキー検証
        if st.button("🔍 APIキー検証"):
            if api_key:
                try:
                    if ai_provider == "OpenAI":
                        generator = ArticleGenerator(api_key, model)
                    else:
                        generator = GeminiArticleGenerator(api_key, model)
                    
                    is_valid, message = generator.validate_api_key()
                    if is_valid:
                        st.success(message)
                        st.session_state.api_validated = True
                        st.session_state.current_generator = generator
                    else:
                        st.error(message)
                        st.session_state.api_validated = False
                        st.session_state.current_generator = None
                except Exception as e:
                    st.error(f"APIキー検証エラー: {str(e)}")
                    st.session_state.api_validated = False
                    st.session_state.current_generator = None
            else:
                st.warning("APIキーを入力してください")
        
        # 現在の設定表示
        if st.session_state.api_validated:
            st.success(f"✅ {ai_provider} APIキーが有効です")
        
        return ai_provider, api_key, model

def create_article_generation_tab():
    """記事生成タブの作成"""
    st.header("🎯 記事生成")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 記事設定
        theme = st.text_input(
            "記事のテーマまたはキーワード",
            value="人工知能の活用方法",
            placeholder="例: 人工知能の未来、健康的な食事、..."
        )
        
        article_type = st.selectbox(
            "記事の種類",
            ["ブログ記事", "ニュース記事", "解説記事", "レビュー記事", "ハウツー記事"]
        )
        
        tone = st.selectbox(
            "記事のトーン",
            ["フォーマル", "カジュアル", "専門的", "親しみやすい", "説得力のある"]
        )
    
    with col2:
        word_count = st.slider(
            "記事の文字数（目安）",
            min_value=300,
            max_value=3000,
            value=1000,
            step=100
        )
        
        include_seo = st.checkbox("SEO要素を含める", value=True)
        
        tags = st.text_input(
            "タグ（カンマ区切り）",
            placeholder="例: AI, 技術, 未来"
        )
    
    # 記事生成ボタン
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 記事を生成", type="primary"):
            if not st.session_state.api_validated or not st.session_state.current_generator:
                st.error("まずAPIキーを設定し、検証してください")
                return
            
            if not theme.strip():
                st.error("記事のテーマを入力してください")
                return
            
            with st.spinner("記事を生成中..."):
                success, content, error = st.session_state.current_generator.generate_article(
                    theme, article_type, tone, word_count, include_seo
                )
                
                if success:
                    st.session_state.generated_article = content
                    st.session_state.article_metadata = {
                        "theme": theme,
                        "article_type": article_type,
                        "tone": tone,
                        "word_count": len(content),
                        "include_seo": include_seo,
                        "tags": tags,
                        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.success("記事生成が完了しました！")
                else:
                    st.error(f"記事生成に失敗しました: {content}")
                    if error:
                        st.error(f"詳細: {error}")
    
    with col2:
        if st.button("📋 構成を生成"):
            if not st.session_state.api_validated or not st.session_state.current_generator:
                st.error("まずAPIキーを設定し、検証してください")
                return
            
            if not theme.strip():
                st.error("記事のテーマを入力してください")
                return
            
            with st.spinner("構成を生成中..."):
                success, outline, error = st.session_state.current_generator.generate_outline(
                    theme, article_type, tone
                )
                
                if success:
                    st.subheader("📋 生成された記事構成")
                    st.markdown(outline)
                else:
                    st.error(f"構成生成に失敗しました: {outline}")

def create_generated_article_section():
    """生成された記事セクションの作成"""
    if st.session_state.generated_article:
        st.header("📄 生成された記事")
        
        # メタデータ表示
        if st.session_state.article_metadata:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**テーマ**: {st.session_state.article_metadata.get('theme', 'N/A')}")
            with col2:
                st.info(f"**生成時刻**: {st.session_state.article_metadata.get('generated_at', 'N/A')}")
            with col3:
                st.info(f"**文字数**: {st.session_state.article_metadata.get('word_count', 0)}文字")
        
        # 記事内容（編集可能）
        edited_article = st.text_area(
            "記事内容（編集可能）",
            value=st.session_state.generated_article,
            height=400
        )
        
        # 記事保存・ダウンロードボタン
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 記事を保存"):
                manager = ArticleManager()
                filename = manager.save_article(
                    edited_article,
                    st.session_state.article_metadata
                )
                if filename:
                    st.success(f"記事が保存されました: {filename}")
                else:
                    st.error("記事の保存に失敗しました")
        
        with col2:
            st.download_button(
                label="📥 ダウンロード",
                data=edited_article,
                file_name=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

def create_article_management_tab():
    """記事管理タブの作成"""
    st.header("📚 記事管理")
    
    manager = ArticleManager()
    
    # 検索機能
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 記事を検索", placeholder="テーマやタグで検索")
    with col2:
        if st.button("検索"):
            pass  # 検索ロジックは後で実装
    
    # 記事一覧
    articles = manager.list_articles()
    
    if articles:
        st.subheader(f"📄 全記事 ({len(articles)}件)")
        
        for article in articles:
            with st.expander(f"📄 {article['theme']} ({article['created_at'][:10]})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**種類**: {article.get('article_type', 'N/A')}")
                    st.write(f"**トーン**: {article.get('tone', 'N/A')}")
                    st.write(f"**文字数**: {article.get('word_count', 0)}文字")
                    if article.get('tags'):
                        st.write(f"**タグ**: {article['tags']}")
                
                with col2:
                    if st.button(f"👁️ 表示", key=f"view_{article['id']}"):
                        success, content, _ = manager.load_article(article['id'])
                        if success:
                            st.text_area(
                                "記事内容",
                                value=content,
                                height=200,
                                key=f"content_{article['id']}"
                            )
                        else:
                            st.error("記事の読み込みに失敗しました")
                
                with col3:
                    if st.button(f"🗑️ 削除", key=f"delete_{article['id']}"):
                        if manager.delete_article(article['id']):
                            st.success("記事を削除しました")
                            st.rerun()
                        else:
                            st.error("削除に失敗しました")
    else:
        st.info("保存された記事がありません")

def create_statistics_tab():
    """統計情報タブの作成"""
    st.header("📊 統計情報")
    
    manager = ArticleManager()
    articles = manager.list_articles()
    
    if articles:
        # 基本統計
        total_articles = len(articles)
        total_words = sum(article.get('word_count', 0) for article in articles)
        avg_words = total_words // total_articles if total_articles > 0 else 0
        
        # 記事タイプの集計
        article_types = {}
        for article in articles:
            article_type = article.get('article_type', 'その他')
            article_types[article_type] = article_types.get(article_type, 0) + 1
        
        # メトリクス表示
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("総記事数", total_articles)
        with col2:
            st.metric("総文字数", f"{total_words:,}")
        with col3:
            st.metric("平均文字数", avg_words)
        with col4:
            st.metric("記事タイプ数", len(article_types))
        
        # 記事タイプ別分布グラフ
        if article_types:
            st.subheader("📈 記事タイプ別分布")
            df = pd.DataFrame(list(article_types.items()), columns=['記事タイプ', '記事数'])
            fig = px.bar(df, x='記事タイプ', y='記事数', title="記事タイプ別分布")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("統計情報を表示するには、まず記事を生成してください")

def create_advanced_features_tab():
    """高度な機能タブの作成"""
    st.header("🔧 高度な機能")
    
    # タイトル生成機能
    st.subheader("💡 タイトル候補生成")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        title_theme = st.text_input("テーマ", placeholder="記事のテーマを入力")
        title_type = st.selectbox("記事タイプ", ["ブログ記事", "ニュース記事", "解説記事"])
    
    with col2:
        if st.button("🎯 タイトル生成"):
            if not st.session_state.api_validated or not st.session_state.current_generator:
                st.error("まずAPIキーを設定し、検証してください")
            elif not title_theme.strip():
                st.error("テーマを入力してください")
            else:
                with st.spinner("タイトルを生成中..."):
                    success, titles, error = st.session_state.current_generator.generate_titles(
                        title_theme, title_type
                    )
                    
                    if success:
                        st.subheader("💡 生成されたタイトル候補")
                        st.markdown(titles)
                    else:
                        st.error(f"タイトル生成に失敗しました: {titles}")
    
    st.divider()
    
    # 設定のエクスポート/インポート
    st.subheader("⚙️ 設定管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 設定をエクスポート"):
            settings = {
                "default_theme": "人工知能の活用方法",
                "default_article_type": "ブログ記事",
                "default_tone": "フォーマル",
                "default_word_count": 1000
            }
            st.download_button(
                label="設定ファイルをダウンロード",
                data=str(settings),
                file_name="ai_content_generator_settings.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📥 設定をインポート", type=['json'])
        if uploaded_file is not None:
            st.success("設定ファイルがアップロードされました")

def main():
    """メイン関数"""
    # セッション状態の初期化
    initialize_session_state()
    
    # ヘッダー
    st.markdown('<h1 class="main-header">📝 AI自動コンテンツ生成システム</h1>', unsafe_allow_html=True)
    
    # サイドバー
    ai_provider, api_key, model = create_sidebar()
    
    # メインコンテンツ
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 記事生成", "📚 記事管理", "📊 統計情報", "🔧 高度な機能"])
    
    with tab1:
        create_article_generation_tab()
        create_generated_article_section()
    
    with tab2:
        create_article_management_tab()
    
    with tab3:
        create_statistics_tab()
    
    with tab4:
        create_advanced_features_tab()
    
    # フッター
    st.divider()
    st.markdown(
        f"<div style='text-align: center; color: #666;'>"
        f"AI自動コンテンツ生成システム - Powered by {ai_provider}<br>"
        f"バージョン 2.0.0（{ai_provider}サポート対応）"
        f"</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

