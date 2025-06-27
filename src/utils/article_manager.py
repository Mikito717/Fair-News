"""
記事管理機能モジュール
記事の保存、読み込み、一覧表示、削除などの機能を提供
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ArticleManager:
    """記事管理クラス"""
    
    def __init__(self, storage_dir: str = "data/saved_articles"):
        """
        初期化
        
        Args:
            storage_dir (str): 記事保存ディレクトリ
        """
        self.storage_dir = storage_dir
        self.metadata_file = os.path.join(storage_dir, "metadata.json")
        self._ensure_storage_dir()
        
    def _ensure_storage_dir(self):
        """保存ディレクトリが存在することを確認"""
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def _load_metadata(self) -> Dict:
        """
        メタデータファイルを読み込み
        
        Returns:
            Dict: メタデータ辞書
        """
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"メタデータ読み込みエラー: {e}")
                return {}
        return {}
    
    def _save_metadata(self, metadata: Dict):
        """
        メタデータファイルを保存
        
        Args:
            metadata (Dict): 保存するメタデータ辞書
        """
        try:
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"メタデータ保存エラー: {e}")
    
    def save_article(
        self, 
        content: str, 
        metadata: Dict
    ) -> Optional[str]:
        """
        記事を保存
        
        Args:
            content (str): 記事内容
            metadata (Dict): 記事のメタデータ
        
        Returns:
            Optional[str]: 保存されたファイル名、またはNone（失敗時）
        """
        
        try:
            # ファイル名を生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"article_{timestamp}.md"
            filepath = os.path.join(self.storage_dir, filename)
            
            # 記事を保存
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            # メタデータを更新
            all_metadata = self._load_metadata()
            article_id = timestamp
            
            # メタデータにファイル名とIDを追加
            metadata["filename"] = filename
            metadata["id"] = article_id
            metadata["created_at"] = datetime.now().isoformat()
            metadata["updated_at"] = datetime.now().isoformat()
            metadata["word_count"] = len(content)
            metadata["status"] = "draft"

            all_metadata[article_id] = metadata
            
            self._save_metadata(all_metadata)
            
            logger.info(f"記事保存成功: {filepath}")
            return filename
            
        except Exception as e:
            logger.error(f"記事保存エラー: {e}")
            return None
    
    def load_article(self, article_id: str) -> Tuple[bool, str, Optional[str]]:
        """
        記事を読み込み
        
        Args:
            article_id (str): 記事ID
        
        Returns:
            Tuple[bool, str, Optional[str]]: (成功フラグ, 記事内容またはエラーメッセージ, エラー詳細)
        """
        
        try:
            metadata = self._load_metadata()
            
            if article_id not in metadata:
                return False, "記事が見つかりません", None
            
            filename = metadata[article_id]["filename"]
            filepath = os.path.join(self.storage_dir, filename)
            
            if not os.path.exists(filepath):
                return False, "記事ファイルが見つかりません", None
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            return True, content, None
            
        except Exception as e:
            logger.error(f"記事読み込みエラー: {e}")
            return False, f"記事読み込みに失敗しました: {str(e)}", str(e)
    
    def update_article(self, article_id: str, content: str) -> Tuple[bool, str, Optional[str]]:
        """
        記事を更新
        
        Args:
            article_id (str): 記事ID
            content (str): 更新後の記事内容
        
        Returns:
            Tuple[bool, str, Optional[str]]: (成功フラグ, メッセージ, エラー詳細)
        """
        
        try:
            metadata = self._load_metadata()
            
            if article_id not in metadata:
                return False, "記事が見つかりません", None
            
            filename = metadata[article_id]["filename"]
            filepath = os.path.join(self.storage_dir, filename)
            
            # 記事内容を更新
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            # メタデータを更新
            metadata[article_id]["updated_at"] = datetime.now().isoformat()
            metadata[article_id]["word_count"] = len(content)
            self._save_metadata(metadata)
            
            logger.info(f"記事更新成功: {filepath}")
            return True, "記事が更新されました", None
            
        except Exception as e:
            logger.error(f"記事更新エラー: {e}")
            return False, f"記事更新に失敗しました: {str(e)}", str(e)
    
    def delete_article(self, article_id: str) -> Tuple[bool, str, Optional[str]]:
        """
        記事を削除
        
        Args:
            article_id (str): 記事ID
        
        Returns:
            Tuple[bool, str, Optional[str]]: (成功フラグ, メッセージ, エラー詳細)
        """
        
        try:
            metadata = self._load_metadata()
            
            if article_id not in metadata:
                return False, "記事が見つかりません", None
            
            filename = metadata[article_id]["filename"]
            filepath = os.path.join(self.storage_dir, filename)
            
            # ファイルを削除
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # メタデータから削除
            del metadata[article_id]
            self._save_metadata(metadata)
            
            logger.info(f"記事削除成功: {filepath}")
            return True, "記事が削除されました", None
            
        except Exception as e:
            logger.error(f"記事削除エラー: {e}")
            return False, f"記事削除に失敗しました: {str(e)}", str(e)
    
    def list_articles(self, limit: int = 50) -> List[Dict]:
        """
        記事一覧を取得
        
        Args:
            limit (int): 取得する記事数の上限
        
        Returns:
            List[Dict]: 記事情報のリスト
        """
        
        try:
            metadata = self._load_metadata()
            
            # 作成日時でソート（新しい順）
            articles = []
            for article_id, info in metadata.items():
                article_info = {
                    "id": article_id,
                    **info
                }
                articles.append(article_info)
            
            articles.sort(key=lambda x: x["created_at"], reverse=True)
            
            return articles[:limit]
            
        except Exception as e:
            logger.error(f"記事一覧取得エラー: {e}")
            return []
    
    def search_articles(self, query: str) -> List[Dict]:
        """
        記事を検索
        
        Args:
            query (str): 検索クエリ
        
        Returns:
            List[Dict]: 検索結果の記事情報リスト
        """
        
        try:
            all_articles = self.list_articles()
            results = []
            
            query_lower = query.lower()
            
            for article in all_articles:
                # テーマ、タグで検索
                if (query_lower in article["theme"].lower() or
                    any(query_lower in tag.lower() for tag in article.get("tags", []))):
                    results.append(article)
                    continue
                
                # 記事内容でも検索（パフォーマンスを考慮して制限）
                success, content, _ = self.load_article(article["id"])
                if success and query_lower in content.lower():
                    results.append(article)
            
            return results
            
        except Exception as e:
            logger.error(f"記事検索エラー: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        記事の統計情報を取得
        
        Returns:
            Dict: 統計情報
        """
        
        try:
            articles = self.list_articles()
            
            total_articles = len(articles)
            total_words = sum(article.get("word_count", 0) for article in articles)
            
            # 記事タイプ別の統計
            type_stats = {}
            for article in articles:
                article_type = article.get("article_type", "不明")
                type_stats[article_type] = type_stats.get(article_type, 0) + 1
            
            # 月別の統計
            monthly_stats = {}
            for article in articles:
                created_at = article.get("created_at", "")
                if created_at:
                    month = created_at[:7]  # YYYY-MM
                    monthly_stats[month] = monthly_stats.get(month, 0) + 1
            
            return {
                "total_articles": total_articles,
                "total_words": total_words,
                "average_words": total_words // total_articles if total_articles > 0 else 0,
                "type_distribution": type_stats,
                "monthly_distribution": monthly_stats
            }
            
        except Exception as e:
            logger.error(f"統計情報取得エラー: {e}")
            return {}



