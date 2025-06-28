"""
ディープリサーチ統合記事生成器
LangGraphリサーチとLLM記事生成を組み合わせ
"""

import os
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime

from ..components.research_agent import ResearchAgent
from .article_generator import ArticleGenerator
from .gemini_generator import GeminiArticleGenerator
from ..utils.prompts import get_research_based_article_prompt

logger = logging.getLogger(__name__)


class DeepResearchArticleGenerator:
    """ディープリサーチベースの記事生成器"""

    def __init__(self, openai_api_key: str = None, gemini_api_key: str = None):
        """
        初期化

        Args:
            openai_api_key (str, optional): OpenAI APIキー
            gemini_api_key (str, optional): Gemini APIキー
        """
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key

        # リサーチエージェントの初期化
        self.research_agent = None
        if gemini_api_key:
            try:
                self.research_agent = ResearchAgent(gemini_api_key)
                logger.info("リサーチエージェントを初期化しました")
            except Exception as e:
                logger.error(f"リサーチエージェントの初期化に失敗しました: {e}")

        # 記事生成器の初期化
        self.article_generator = None
        self.gemini_generator = None

        if openai_api_key:
            try:
                self.article_generator = ArticleGenerator(openai_api_key)
                logger.info("OpenAI記事生成器を初期化しました")
            except Exception as e:
                logger.error(f"OpenAI記事生成器の初期化に失敗しました: {e}")

        if gemini_api_key:
            try:
                self.gemini_generator = GeminiArticleGenerator(gemini_api_key)
                logger.info("Gemini記事生成器を初期化しました")
            except Exception as e:
                logger.error(f"Gemini記事生成器の初期化に失敗しました: {e}")

    def generate_researched_article(
        self,
        query: str,
        article_type: str = "ニュース記事",
        tone: str = "情報的",
        word_count: int = 1000,
        include_seo: bool = False,
        max_research_loops: int = 2,
        number_of_initial_queries: int = 3,
        generator_type: str = "gemini"  # "openai" or "gemini"
    ) -> Dict:
        """
        クエリに対してディープリサーチを行い、その結果をもとに記事を生成

        Args:
            query (str): 検索・リサーチクエリ
            article_type (str): 記事の種類
            tone (str): 記事のトーン
            word_count (int): 目標文字数
            include_seo (bool): SEO要素を含めるかどうか
            max_research_loops (int): 最大リサーチループ数
            number_of_initial_queries (int): 初期検索クエリ数
            generator_type (str): 使用する生成器タイプ

        Returns:
            Dict: 生成結果
        """
        result = {
            "success": False,
            "content": "",
            "research_data": {},
            "error": None,
            "metadata": {
                "query": query,
                "article_type": article_type,
                "tone": tone,
                "word_count": word_count,
                "generator_type": generator_type,
                "timestamp": datetime.now().isoformat()
            }
        }

        try:
            # Step 1: ディープリサーチの実行
            logger.info(f"ディープリサーチを開始: {query}")

            if not self.research_agent:
                raise ValueError(
                    "リサーチエージェントが初期化されていません。Gemini APIキーを確認してください。")

            research_success, research_data, research_error = self.research_agent.research(
                topic=query,
                max_research_loops=max_research_loops,
                number_of_initial_queries=number_of_initial_queries
            )

            if not research_success:
                result["error"] = f"リサーチに失敗しました: {research_error}"
                return result

            result["research_data"] = research_data
            logger.info("ディープリサーチが完了しました")

            # Step 2: リサーチ結果をもとに記事生成
            logger.info("記事生成を開始")

            # リサーチデータを記事生成用にフォーマット
            research_content = self.research_agent.format_for_article_generation(
                research_data)

            # 記事生成用プロンプトの作成
            article_prompt = get_research_based_article_prompt(
                original_query=query,
                research_content=research_content,
                article_type=article_type,
                tone=tone,
                word_count=word_count,
                include_seo=include_seo
            )

            # 選択された生成器で記事を生成
            article_success = False
            article_content = ""
            article_error = None

            if generator_type == "openai" and self.article_generator:
                article_success, article_content, article_error = self.article_generator.generate_article(
                    theme=article_prompt,
                    article_type=article_type,
                    tone=tone,
                    word_count=word_count,
                    include_seo=include_seo
                )
            elif generator_type == "gemini" and self.gemini_generator:
                article_result = self.gemini_generator.generate_article(
                    theme=article_prompt,
                    article_type=article_type,
                    tone=tone,
                    word_count=word_count,
                    include_seo=include_seo
                )
                article_success = article_result.get("success", False)
                article_content = article_result.get("content", "")
                article_error = article_result.get("error")
            else:
                raise ValueError(f"指定された生成器タイプ '{generator_type}' は利用できません")

            if not article_success:
                result["error"] = f"記事生成に失敗しました: {article_error}"
                return result

            # Step 3: 結果をまとめる
            result["success"] = True
            result["content"] = article_content
            result["metadata"]["research_loops"] = research_data.get(
                "research_loops", 0)
            result["metadata"]["sources_count"] = len(
                research_data.get("sources", []))
            result["metadata"]["search_queries_count"] = len(
                research_data.get("search_queries", []))

            logger.info("ディープリサーチベース記事生成が完了しました")

        except Exception as e:
            result["error"] = f"予期しないエラーが発生しました: {str(e)}"
            logger.error(result["error"])

        return result

    def get_research_summary(self, research_data: Dict) -> str:
        """
        リサーチ結果のサマリーを取得

        Args:
            research_data (Dict): リサーチデータ

        Returns:
            str: サマリーテキスト
        """
        if self.research_agent:
            return self.research_agent.get_research_summary(research_data)
        return "リサーチエージェントが利用できません。"

    def is_research_available(self) -> bool:
        """
        リサーチ機能が利用可能かチェック

        Returns:
            bool: 利用可能かどうか
        """
        return self.research_agent is not None

    def is_generator_available(self, generator_type: str) -> bool:
        """
        指定された生成器が利用可能かチェック

        Args:
            generator_type (str): 生成器タイプ

        Returns:
            bool: 利用可能かどうか
        """
        if generator_type == "openai":
            return self.article_generator is not None
        elif generator_type == "gemini":
            return self.gemini_generator is not None
        return False
