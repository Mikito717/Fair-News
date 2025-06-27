"""
アプリケーション設定
"""

import os
from typing import Dict, Any

class Config:
    """アプリケーション設定クラス"""
    
    # デフォルト設定
    DEFAULT_SETTINGS = {
        "app_title": "AI自動コンテンツ生成システム",
        "app_icon": "📝",
        "page_layout": "wide",
        "default_word_count": 800,
        "max_word_count": 3000,
        "min_word_count": 300,
        "default_article_type": "ブログ記事",
        "default_tone": "フォーマル",
        "enable_seo": True,
        "max_retries": 3,
        "data_dir": "data",
        "articles_dir": "data/saved_articles",
        "config_dir": "config",
        "assets_dir": "assets"
    }
    
    # 記事タイプ
    ARTICLE_TYPES = [
        "ブログ記事",
        "ニュース記事", 
        "解説記事",
        "レビュー記事",
        "ハウツー記事",
        "インタビュー記事",
        "コラム",
        "プレスリリース"
    ]
    
    # トーン
    TONES = [
        "フォーマル",
        "カジュアル", 
        "専門的",
        "親しみやすい",
        "説得力のある",
        "情報的",
        "エンターテイメント"
    ]
    
    # ジェネレーター設定
    GENERATORS = {
        "openai": {
            "name": "OpenAI (GPT)",
            "models": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            "env_key": "OPENAI_API_KEY",
            "model_env_key": "OPENAI_MODEL"
        },
        "gemini": {
            "name": "Google Gemini",
            "models": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
            "env_key": "GEMINI_API_KEY", 
            "model_env_key": "GEMINI_MODEL"
        }
    }
    
    @classmethod
    def get_setting(cls, key: str, default: Any = None) -> Any:
        """設定値を取得"""
        return cls.DEFAULT_SETTINGS.get(key, default)
    
    @classmethod
    def get_env_path(cls) -> str:
        """環境設定ファイルのパスを取得"""
        return os.path.join(cls.get_setting("config_dir"), ".env")
    
    @classmethod
    def get_css_path(cls) -> str:
        """CSSファイルのパスを取得"""
        return os.path.join(cls.get_setting("assets_dir"), "styles", "main.css")
    
    @classmethod
    def get_articles_dir(cls) -> str:
        """記事保存ディレクトリのパスを取得"""
        return cls.get_setting("articles_dir")
