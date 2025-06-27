"""
Fair News - AI自動コンテンツ生成システム
メインアプリケーションファイル (Streamlit最適化版)
"""

import streamlit as st
import os
import sys
from datetime import datetime

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from dotenv import load_dotenv
from config.settings import Config
from src.utils.article_manager import ArticleManager
from src.components.sidebar import create_sidebar, create_generation_settings
from src.components.dashboard import create_dashboard, display_article_preview
from src.components.article_manager import create_article_manager_ui

# 環境変数を読み込み
load_dotenv(Config.get_env_path())

def configure_page():
    """ページ設定"""
    st.set_page_config(
        page_title=Config.get_setting("app_title"),
        page_icon=Config.get_setting("app_icon"),
        layout=Config.get_setting("page_layout"),
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    """カスタムCSSの読み込み"""
    css_path = Config.get_css_path()
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    """セッション状態の初期化"""
    if 'generated_article' not in st.session_state:
        st.session_state.generated_article = ""
    if 'article_metadata' not in st.session_state:
        st.session_state.article_metadata = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "記事生成"

def create_navigation():
    """ナビゲーションメニュー"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 メニュー")
    
    pages = ["記事生成", "ダッシュボード", "記事管理", "設定"]
    
    for page in pages:
        if st.sidebar.button(page, key=f"nav_{page}"):
            st.session_state.current_page = page
            st.rerun()

def create_article_generation_page(generator, generation_settings):
    """記事生成ページ"""
    st.markdown('<div class="main-header">📝 AI記事生成</div>', unsafe_allow_html=True)
    
    if not generator:
        st.warning("AIプロバイダーの設定を完了してください。")
        return
    
    if not generation_settings["theme"]:
        st.info("記事のテーマを入力してください。")
        return
    
    # 記事生成ボタン
    if st.button("🚀 記事を生成", type="primary", use_container_width=True):
        generate_article(generator, generation_settings)
    
    # 生成された記事の表示
    if st.session_state.generated_article:
        display_generated_article()

def generate_article(generator, settings):
    """記事生成処理"""
    with st.spinner("記事を生成中..."):
        try:
            result = generator.generate_article(
                theme=settings["theme"],
                article_type=settings["article_type"],
                tone=settings["tone"],
                word_count=settings["word_count"],
                include_seo=settings["include_seo"],
                max_retries=Config.get_setting("max_retries")
            )
            
            if result["success"]:
                st.session_state.generated_article = result["content"]
                st.session_state.article_metadata = {
                    "theme": settings["theme"],
                    "type": settings["article_type"],
                    "tone": settings["tone"],
                    "word_count": len(result["content"]),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "include_seo": settings["include_seo"]
                }
                st.success("記事が正常に生成されました！")
            else:
                st.error(f"記事生成に失敗しました: {result.get('error', '不明なエラー')}")
                
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")

def display_generated_article():
    """生成された記事の表示"""
    st.markdown("---")
    st.subheader("📄 生成された記事")
    
    # 記事プレビュー
    display_article_preview(
        st.session_state.article_metadata,
        st.session_state.generated_article
    )
    
    # 保存・ダウンロードボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 記事を保存", use_container_width=True):
            save_article()
    
    with col2:
        st.download_button(
            label="📥 Markdownダウンロード",
            data=st.session_state.generated_article,
            file_name=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 新しい記事を生成", use_container_width=True):
            st.session_state.generated_article = ""
            st.session_state.article_metadata = {}
            st.rerun()

def save_article():
    """記事保存処理"""
    try:
        article_manager = ArticleManager(Config.get_articles_dir())
        
        filename = article_manager.save_article(
            content=st.session_state.generated_article,
            metadata=st.session_state.article_metadata
        )
        
        st.success(f"記事を保存しました: {filename}")
        
    except Exception as e:
        st.error(f"保存に失敗しました: {str(e)}")

def create_settings_page():
    """設定ページ"""
    st.markdown('<div class="main-header">⚙️ 設定</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("🔧 アプリケーション設定")
    
    # 設定項目
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input(
            "デフォルト文字数",
            min_value=300,
            max_value=3000,
            value=Config.get_setting("default_word_count"),
            step=100
        )
        
        st.selectbox(
            "デフォルト記事タイプ",
            Config.ARTICLE_TYPES,
            index=Config.ARTICLE_TYPES.index(Config.get_setting("default_article_type"))
        )
    
    with col2:
        st.number_input(
            "最大リトライ回数",
            min_value=1,
            max_value=5,
            value=Config.get_setting("max_retries")
        )
        
        st.selectbox(
            "デフォルトトーン",
            Config.TONES,
            index=Config.TONES.index(Config.get_setting("default_tone"))
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # データ管理
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.subheader("📁 データ管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**記事保存ディレクトリ:** `{Config.get_articles_dir()}`")
        st.write(f"**設定ファイル:** `{Config.get_env_path()}`")
    
    with col2:
        if st.button("🧹 キャッシュクリア"):
            st.cache_data.clear()
            st.success("キャッシュをクリアしました")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """メイン関数"""
    # 基本設定
    configure_page()
    load_custom_css()
    initialize_session_state()
    
    # サイドバー作成
    _, generator, _ = create_sidebar()
    generation_settings = create_generation_settings()
    create_navigation()
    
    # 記事管理インスタンス
    article_manager = ArticleManager(Config.get_articles_dir())
    
    # ページルーティング
    current_page = st.session_state.get('current_page', '記事生成')
    
    if current_page == "記事生成":
        create_article_generation_page(generator, generation_settings)
    elif current_page == "ダッシュボード":
        create_dashboard(article_manager)
    elif current_page == "記事管理":
        create_article_manager_ui(article_manager)
    elif current_page == "設定":
        create_settings_page()
    
    # フッター
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; font-size: 0.8rem;">'
        f'{Config.get_setting("app_title")} v{Config.get_setting("version", "1.0.0")} | '
        'Powered by Streamlit</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
