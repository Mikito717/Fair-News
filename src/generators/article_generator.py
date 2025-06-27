"""
AI記事生成機能のコアモジュール
OpenAI APIとの連携とエラーハンドリングを管理
"""

import openai
from typing import Dict, Optional, Tuple
import time
import logging
from ..utils.prompts import get_article_generation_prompt, get_title_generation_prompt, get_outline_generation_prompt

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleGenerator:
    """AI記事生成クラス"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        初期化
        
        Args:
            api_key (str): OpenAI APIキー
            model (str): 使用するモデル名
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
    def generate_article(
        self, 
        theme: str, 
        article_type: str, 
        tone: str, 
        word_count: int, 
        include_seo: bool = False,
        max_retries: int = 3
    ) -> Tuple[bool, str, Optional[str]]:
        """
        記事を生成
        
        Args:
            theme (str): 記事のテーマ
            article_type (str): 記事の種類
            tone (str): 記事のトーン
            word_count (int): 目標文字数
            include_seo (bool): SEO要素を含めるかどうか
            max_retries (int): 最大リトライ回数
        
        Returns:
            Tuple[bool, str, Optional[str]]: (成功フラグ, 生成された記事またはエラーメッセージ, エラー詳細)
        """
        
        prompt = get_article_generation_prompt(theme, article_type, tone, word_count, include_seo)
        
        for attempt in range(max_retries):
            try:
                logger.info(f"記事生成開始 (試行 {attempt + 1}/{max_retries})")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "あなたは優秀なライターです。読者にとって価値のある高品質な記事を作成してください。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=3000,
                    temperature=0.7,
                    timeout=60
                )
                
                generated_content = response.choices[0].message.content
                
                if generated_content and len(generated_content.strip()) > 100:
                    logger.info("記事生成成功")
                    return True, generated_content, None
                else:
                    logger.warning("生成された記事が短すぎます")
                    if attempt == max_retries - 1:
                        return False, "生成された記事が短すぎます。", None
                        
            except openai.RateLimitError as e:
                logger.warning(f"レート制限エラー (試行 {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数バックオフ
                else:
                    return False, "APIのレート制限に達しました。しばらく待ってから再試行してください。", str(e)
                    
            except openai.APIError as e:
                logger.error(f"API エラー (試行 {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return False, f"APIエラーが発生しました: {str(e)}", str(e)
                    
            except Exception as e:
                logger.error(f"予期しないエラー (試行 {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return False, f"予期しないエラーが発生しました: {str(e)}", str(e)
        
        return False, "記事生成に失敗しました。", None
    
    def generate_titles(self, theme: str, article_type: str) -> Tuple[bool, str, Optional[str]]:
        """
        タイトル候補を生成
        
        Args:
            theme (str): 記事のテーマ
            article_type (str): 記事の種類
        
        Returns:
            Tuple[bool, str, Optional[str]]: (成功フラグ, 生成されたタイトル候補またはエラーメッセージ, エラー詳細)
        """
        
        prompt = get_title_generation_prompt(theme, article_type)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたは優秀なライターです。魅力的で効果的なタイトルを提案してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.8
            )
            
            titles = response.choices[0].message.content
            return True, titles, None
            
        except Exception as e:
            logger.error(f"タイトル生成エラー: {str(e)}")
            return False, f"タイトル生成に失敗しました: {str(e)}", str(e)
    
    def generate_outline(self, theme: str, article_type: str, tone: str) -> Tuple[bool, str, Optional[str]]:
        """
        記事構成を生成
        
        Args:
            theme (str): 記事のテーマ
            article_type (str): 記事の種類
            tone (str): 記事のトーン
        
        Returns:
            Tuple[bool, str, Optional[str]]: (成功フラグ, 生成された構成またはエラーメッセージ, エラー詳細)
        """
        
        prompt = get_outline_generation_prompt(theme, article_type, tone)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたは優秀なライターです。論理的で読みやすい記事構成を作成してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.6
            )
            
            outline = response.choices[0].message.content
            return True, outline, None
            
        except Exception as e:
            logger.error(f"構成生成エラー: {str(e)}")
            return False, f"構成生成に失敗しました: {str(e)}", str(e)
    
    def validate_api_key(self) -> Tuple[bool, str]:
        """
        APIキーの有効性を検証
        
        Returns:
            Tuple[bool, str]: (有効フラグ, メッセージ)
        """
        
        try:
            # 簡単なテストリクエストを送信
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True, "APIキーは有効です"
            
        except openai.AuthenticationError:
            return False, "APIキーが無効です"
        except Exception as e:
            return False, f"APIキー検証エラー: {str(e)}"

