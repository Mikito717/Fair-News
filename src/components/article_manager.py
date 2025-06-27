"""
記事管理コンポーネント
"""

import streamlit as st
from typing import List, Dict, Optional
from ..utils.article_manager import ArticleManager

def create_article_manager_ui(article_manager: ArticleManager):
    """
    記事管理UIの作成
    
    Args:
        article_manager (ArticleManager): 記事管理インスタンス
    """
    st.markdown('<div class="main-header">📚 記事管理</div>', unsafe_allow_html=True)
    
    # 検索・フィルター機能
    search_filters = _create_search_filters()
    
    # 記事一覧の取得と表示
    articles = article_manager.get_all_articles()
    filtered_articles = _filter_articles(articles, search_filters)
    
    if filtered_articles:
        _display_articles_list(filtered_articles, article_manager)
    else:
        st.info("条件に一致する記事がありません。")

def _create_search_filters() -> Dict:
    """検索・フィルター機能"""
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("🔍 検索・フィルター")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input(
            "キーワード検索",
            placeholder="タイトルや内容で検索...",
            key="search_term"
        )
    
    with col2:
        article_type_filter = st.selectbox(
            "記事タイプ",
            ["すべて", "ブログ記事", "ニュース記事", "解説記事", "レビュー記事", "その他"],
            key="type_filter"
        )
    
    with col3:
        sort_order = st.selectbox(
            "並び順",
            ["新しい順", "古い順", "文字数順(多)", "文字数順(少)"],
            key="sort_order"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        "search_term": search_term,
        "article_type": article_type_filter,
        "sort_order": sort_order
    }

def _filter_articles(articles: List[Dict], filters: Dict) -> List[Dict]:
    """記事のフィルタリング"""
    filtered = articles.copy()
    
    # キーワード検索
    if filters["search_term"]:
        search_term = filters["search_term"].lower()
        filtered = [
            article for article in filtered
            if (search_term in article.get('title', '').lower() or
                search_term in article.get('theme', '').lower())
        ]
    
    # 記事タイプフィルター
    if filters["article_type"] != "すべて":
        filtered = [
            article for article in filtered
            if article.get('type') == filters["article_type"]
        ]
    
    # ソート
    if filters["sort_order"] == "新しい順":
        filtered.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    elif filters["sort_order"] == "古い順":
        filtered.sort(key=lambda x: x.get('created_at', ''))
    elif filters["sort_order"] == "文字数順(多)":
        filtered.sort(key=lambda x: x.get('word_count', 0), reverse=True)
    elif filters["sort_order"] == "文字数順(少)":
        filtered.sort(key=lambda x: x.get('word_count', 0))
    
    return filtered

def _display_articles_list(articles: List[Dict], article_manager: ArticleManager):
    """記事一覧の表示"""
    st.subheader(f"📋 記事一覧 ({len(articles)}件)")
    
    for i, article in enumerate(articles):
        with st.expander(f"📄 {article.get('title', '無題')} - {article.get('created_at', 'N/A')}"):
            _display_article_details(article, article_manager)

def _display_article_details(article: Dict, article_manager: ArticleManager):
    """記事詳細の表示"""
    filename = article.get('filename', '')
    
    # メタ情報表示
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**テーマ:** {article.get('theme', 'N/A')}")
        st.write(f"**タイプ:** {article.get('type', 'N/A')}")
        st.write(f"**トーン:** {article.get('tone', 'N/A')}")
    
    with col2:
        st.write(f"**文字数:** {article.get('word_count', 0)} 文字")
        st.write(f"**作成日:** {article.get('created_at', 'N/A')}")
        st.write(f"**ファイル名:** {filename}")
    
    # 記事内容の一部を表示
    if filename:
        try:
            content = article_manager.load_article(filename)
            if content:
                st.markdown("**記事プレビュー:**")
                # 最初の200文字を表示
                preview = content[:200] + "..." if len(content) > 200 else content
                st.markdown(preview)
                
                # アクション用ボタン
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📖 全文表示", key=f"view_{filename}"):
                        st.session_state[f"show_full_{filename}"] = True
                
                with col2:
                    if st.button("📝 編集", key=f"edit_{filename}"):
                        st.session_state[f"edit_mode_{filename}"] = True
                
                with col3:
                    if st.button("🗑️ 削除", key=f"delete_{filename}"):
                        _handle_article_deletion(filename, article_manager)
                
                # 全文表示
                if st.session_state.get(f"show_full_{filename}", False):
                    st.markdown("**全文:**")
                    st.markdown(content)
                    if st.button("閉じる", key=f"close_{filename}"):
                        st.session_state[f"show_full_{filename}"] = False
                
                # 編集モード
                if st.session_state.get(f"edit_mode_{filename}", False):
                    _handle_article_editing(filename, content, article, article_manager)
                    
        except Exception as e:
            st.error(f"記事読み込みエラー: {e}")

def _handle_article_deletion(filename: str, article_manager: ArticleManager):
    """記事削除処理"""
    if st.button("本当に削除しますか？", key=f"confirm_delete_{filename}"):
        try:
            article_manager.delete_article(filename)
            st.success("記事を削除しました。")
            st.rerun()
        except Exception as e:
            st.error(f"削除エラー: {e}")

def _handle_article_editing(filename: str, content: str, article: Dict, article_manager: ArticleManager):
    """記事編集処理"""
    st.markdown("**記事編集:**")
    
    # タイトル編集
    new_title = st.text_input(
        "タイトル",
        value=article.get('title', ''),
        key=f"edit_title_{filename}"
    )
    
    # 内容編集
    new_content = st.text_area(
        "内容",
        value=content,
        height=400,
        key=f"edit_content_{filename}"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 保存", key=f"save_{filename}"):
            try:
                # 記事を更新
                updated_article = article.copy()
                updated_article['title'] = new_title
                updated_article['word_count'] = len(new_content)
                
                # ファイルと メタデータを更新
                article_manager.update_article(filename, new_content, updated_article)
                st.success("記事を更新しました。")
                st.session_state[f"edit_mode_{filename}"] = False
                st.rerun()
            except Exception as e:
                st.error(f"更新エラー: {e}")
    
    with col2:
        if st.button("❌ キャンセル", key=f"cancel_{filename}"):
            st.session_state[f"edit_mode_{filename}"] = False
            st.rerun()
