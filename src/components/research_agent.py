"""
LangGraphベースのリサーチエージェント
ディープリサーチ機能を提供
"""

import os
import sys
from typing import Dict, List, Optional, Tuple
import logging
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from google.genai import Client

# プロジェクトルートを追加してresearchモジュールからインポート
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from src.research.agent.graph import graph
    from src.research.agent.configuration import Configuration
    from src.research.agent.state import OverallState
except ImportError as e:
    logging.error(f"LangGraphエージェントのインポートに失敗しました: {e}")
    graph = None
    Configuration = None
    OverallState = None

logger = logging.getLogger(__name__)


class ResearchAgent:
    """ディープリサーチを実行するエージェント"""

    def __init__(self, gemini_api_key: str):
        """
        初期化

        Args:
            gemini_api_key (str): Gemini APIキー
        """
        self.gemini_api_key = gemini_api_key
        os.environ["GEMINI_API_KEY"] = gemini_api_key

        # graphの初期化は遅延させる
        self._graph = None
        self._genai_client = None

    @property
    def graph(self):
        """LangGraphグラフを遅延初期化"""
        if self._graph is None:
            if graph is None:
                raise ImportError("LangGraphエージェントの初期化に失敗しました")
            self._graph = graph
        return self._graph

    @property
    def genai_client(self):
        """GenAIクライアントを遅延初期化"""
        if self._genai_client is None:
            from google.genai import Client
            self._genai_client = Client(api_key=self.gemini_api_key)
        return self._genai_client

    def research(
        self,
        topic: str,
        max_research_loops: int = 2,
        number_of_initial_queries: int = 3
    ) -> Tuple[bool, Dict, Optional[str]]:
        """
        トピックについてディープリサーチを実行

        Args:
            topic (str): リサーチするトピック
            max_research_loops (int): 最大リサーチループ数
            number_of_initial_queries (int): 初期検索クエリ数

        Returns:
            Tuple[bool, Dict, Optional[str]]: (成功フラグ, リサーチ結果, エラーメッセージ)
        """
        try:
            logger.info(f"ディープリサーチ開始: {topic}")

            # 初期状態を設定
            initial_state = {
                "messages": [HumanMessage(content=topic)],
                "search_query": [],
                "web_research_result": [],
                "sources_gathered": [],
                "initial_search_query_count": number_of_initial_queries,
                "max_research_loops": max_research_loops,
                "research_loop_count": 0,
                "reasoning_model": "gemini-2.5-flash"
            }

            # 設定を作成
            config = {
                "configurable": {
                    "number_of_initial_queries": number_of_initial_queries,
                    "max_research_loops": max_research_loops,
                    "query_generator_model": "gemini-2.0-flash",
                    "reflection_model": "gemini-2.5-flash",
                    "answer_model": "gemini-2.5-pro"
                }
            }

            # リサーチを実行
            result = self.graph.invoke(initial_state, config=config)

            logger.info("ディープリサーチ完了")

            # 結果を整理
            research_result = {
                "topic": topic,
                "final_answer": result.get("messages", [])[-1].content if result.get("messages") else "",
                "sources": result.get("sources_gathered", []),
                "search_queries": result.get("search_query", []),
                "research_summaries": result.get("web_research_result", []),
                "research_loops": result.get("research_loop_count", 0)
            }

            return True, research_result, None

        except Exception as e:
            error_msg = f"リサーチ中にエラーが発生しました: {str(e)}"
            logger.error(error_msg)
            return False, {}, error_msg

    def get_research_summary(self, research_result: Dict) -> str:
        """
        リサーチ結果をサマリー形式で取得

        Args:
            research_result (Dict): リサーチ結果

        Returns:
            str: サマリーテキスト
        """
        if not research_result:
            return "リサーチ結果がありません。"

        summary = "## リサーチサマリー\n\n"
        summary += f"**トピック:** {research_result.get('topic', 'N/A')}\n\n"
        summary += f"**リサーチループ数:** {research_result.get('research_loops', 0)}\n\n"
        summary += f"**検索クエリ数:** {len(research_result.get('search_queries', []))}\n\n"

        # メインの調査結果
        final_answer = research_result.get('final_answer', '')
        if final_answer:
            summary += f"### 調査結果\n\n{final_answer}\n\n"

        # ソース情報
        sources = research_result.get('sources', [])
        if sources:
            summary += f"### 参考ソース ({len(sources)}件)\n\n"
            for i, source in enumerate(sources[:10], 1):  # 最大10件表示
                url = source.get('value', source.get('short_url', 'N/A'))
                summary += f"{i}. [{url}]({url})\n"

        return summary

    def format_for_article_generation(self, research_result: Dict) -> str:
        """
        リサーチ結果を記事生成用にフォーマット

        Args:
            research_result (Dict): リサーチ結果

        Returns:
            str: 記事生成用のテキスト
        """
        if not research_result:
            return ""

        formatted_text = f"# {research_result.get('topic', 'リサーチトピック')}\n\n"

        # メインのリサーチ内容
        final_answer = research_result.get('final_answer', '')
        if final_answer:
            formatted_text += f"{final_answer}\n\n"

        # 追加のリサーチサマリー
        summaries = research_result.get('research_summaries', [])
        if summaries:
            formatted_text += "## 詳細調査内容\n\n"
            for i, summary in enumerate(summaries, 1):
                formatted_text += f"### 調査 {i}\n\n{summary}\n\n"

        # ソース情報
        sources = research_result.get('sources', [])
        if sources:
            formatted_text += "## 参考文献・ソース\n\n"
            for source in sources:
                url = source.get('value', source.get('short_url', 'N/A'))
                formatted_text += f"- {url}\n"

        return formatted_text
