"""
Streamlitサイドバーコンポーネント
"""

import streamlit as st
import os
from typing import Tuple, Optional
from ..generators.article_generator import ArticleGenerator
from ..generators.gemini_generator import GeminiArticleGenerator
from ..generators.mock_generator import MockArticleGenerator
from config.settings import Config

def create_sidebar() -> Tuple[str, object, dict]:
    """
    サイドバーの作成
    
    Returns:
        Tuple[str, object, dict]: (provider, generator, settings)
    """
    with st.sidebar:
        st.markdown('<div class="sidebar-title">⚙️ 設定</div>', unsafe_allow_html=True)
        
        # AIプロバイダー選択
        ai_provider = st.selectbox(
            "AIプロバイダー",
            ["OpenAI", "Gemini", "Mock (テスト用)"],
            help="使用するAIサービスを選択してください"
        )
        
        generator = None
        settings = {}
        
        if ai_provider == "OpenAI":
            generator, settings = _create_openai_settings()
        elif ai_provider == "Gemini":
            generator, settings = _create_gemini_settings()
        else:  # Mock
            generator, settings = _create_mock_settings()
        
        return ai_provider, generator, settings

def _create_openai_settings() -> Tuple[Optional[ArticleGenerator], dict]:
    """OpenAI設定UI"""
    api_key = st.text_input(
        "OpenAI APIキー",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="OpenAI APIキーを入力してください"
    )
    
    model = st.selectbox(
        "AIモデル選択",
        Config.GENERATORS["openai"]["models"],
        index=0,
        help="使用するOpenAIモデルを選択してください"
    )
    
    generator = None
    if api_key:
        try:
            generator = ArticleGenerator(api_key=api_key, model=model)
        except Exception as e:
            st.error(f"OpenAI設定エラー: {e}")
    
    return generator, {"api_key": api_key, "model": model}

def _create_gemini_settings() -> Tuple[Optional[GeminiArticleGenerator], dict]:
    """Gemini設定UI"""
    api_key = st.text_input(
        "Gemini APIキー",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Google Gemini APIキーを入力してください"
    )
    
    # モデルの説明を追加
    model_descriptions = {
        "gemini-2.5-flash": "🚀 最新の高性能モデル（推奨）- 適応的思考、費用対効果",
        "gemini-2.5-pro": "🧠 最高性能の思考モデル - 複雑な推論と分析に最適",
        "gemini-2.5-flash-lite-preview-06-17": "⚡ 高スループット・低コスト - 大量処理向け",
        "gemini-2.0-flash": "🌟 次世代機能・高速 - リアルタイムストリーミング対応",
        "gemini-2.0-flash-lite": "💨 低レイテンシ・低コスト - 高速応答が必要な場合",
        "gemini-1.5-flash": "🔄 安定版高速モデル - 汎用性の高いパフォーマンス",
        "gemini-1.5-pro": "🎯 安定版高性能モデル - 複雑な推論タスク向け",
        "gemini-1.5-flash-8b": "🪶 軽量モデル - 大規模でシンプルなタスク向け"
    }
    
    # モデル選択の表示用リスト
    model_options = []
    for model in Config.GENERATORS["gemini"]["models"]:
        description = model_descriptions.get(model, "")
        model_options.append(f"{model} - {description}" if description else model)
    
    selected_option = st.selectbox(
        "AIモデル選択",
        model_options,
        index=0,
        help="使用するGeminiモデルを選択してください。最新の2.5ファミリーが推奨です。"
    )
    
    # 実際のモデル名を抽出
    model = selected_option.split(" - ")[0]
    
    generator = None
    if api_key:
        try:
            generator = GeminiArticleGenerator(api_key=api_key, model=model)
        except Exception as e:
            st.error(f"Gemini設定エラー: {e}")
    
    return generator, {"api_key": api_key, "model": model}

def _create_mock_settings() -> Tuple[MockArticleGenerator, dict]:
    """Mock設定UI"""
    st.info("テスト用のモックジェネレーターです。実際のAPIは使用されません。")
    
    model = st.selectbox(
        "モックモデル",
        ["mock-gpt-4", "mock-gemini"],
        help="テスト用のモックモデルを選択してください"
    )
    
    generator = MockArticleGenerator(api_key="test", model=model)
    
    return generator, {"api_key": "test", "model": model}

def create_generation_settings() -> dict:
    """記事生成設定UI"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📝 記事設定")
        
        theme = st.text_input(
            "記事テーマ",
            placeholder="例: 最新のAI技術について",
            help="記事のテーマやキーワードを入力してください"
        )
        
        article_type = st.selectbox(
            "記事タイプ",
            Config.ARTICLE_TYPES,
            help="生成する記事の種類を選択してください"
        )
        
        tone = st.selectbox(
            "文体・トーン",
            Config.TONES,
            help="記事の文体やトーンを選択してください"
        )
        
        word_count = st.slider(
            "文字数",
            min_value=Config.get_setting("min_word_count"),
            max_value=Config.get_setting("max_word_count"),
            value=Config.get_setting("default_word_count"),
            step=100,
            help="生成する記事の文字数を指定してください"
        )
        
        include_seo = st.checkbox(
            "SEO要素を含める",
            value=Config.get_setting("enable_seo"),
            help="メタディスクリプション、キーワードなどのSEO要素を含めます"
        )
        
        return {
            "theme": theme,
            "article_type": article_type,
            "tone": tone,
            "word_count": word_count,
            "include_seo": include_seo
        }
