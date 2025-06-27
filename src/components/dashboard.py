"""
Streamlitダッシュボードコンポーネント
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict, List
from ..utils.article_manager import ArticleManager

def create_dashboard(article_manager: ArticleManager):
    """
    ダッシュボードの作成
    
    Args:
        article_manager (ArticleManager): 記事管理インスタンス
    """
    st.markdown('<div class="main-header">📊 ダッシュボード</div>', unsafe_allow_html=True)
    
    # 統計情報の取得
    stats = article_manager.get_statistics()
    articles = article_manager.get_all_articles()
    
    # メトリクス表示
    _display_metrics(stats)
    
    # グラフ表示
    if articles:
        col1, col2 = st.columns(2)
        
        with col1:
            _display_article_type_chart(articles)
        
        with col2:
            _display_monthly_chart(articles)
    else:
        st.info("まだ記事が生成されていません。サイドバーから記事を生成してみてください。")

def _display_metrics(stats: Dict):
    """メトリクス表示"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>📝 総記事数</h3>
                <h2>{stats.get('total_articles', 0)}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>📊 総文字数</h3>
                <h2>{stats.get('total_words', 0):,}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        avg_words = stats.get('average_words', 0)
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>📈 平均文字数</h3>
                <h2>{avg_words:.0f}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>🗓️ 今月の記事</h3>
                <h2>{stats.get('monthly_articles', 0)}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )

def _display_article_type_chart(articles: List[Dict]):
    """記事タイプ別分布グラフ"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📋 記事タイプ別分布")
    
    # データ準備
    type_counts = {}
    for article in articles:
        article_type = article.get('type', '未分類')
        type_counts[article_type] = type_counts.get(article_type, 0) + 1
    
    if type_counts:
        df = pd.DataFrame(list(type_counts.items()), columns=['タイプ', '記事数'])
        
        fig = px.pie(
            df,
            values='記事数',
            names='タイプ',
            title="記事タイプ別分布",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("データがありません")
    
    st.markdown('</div>', unsafe_allow_html=True)

def _display_monthly_chart(articles: List[Dict]):
    """月別記事数グラフ"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📅 月別記事数推移")
    
    # データ準備
    monthly_counts = {}
    for article in articles:
        created_at = article.get('created_at', '')
        if created_at:
            # YYYY-MM-DD形式から年月を抽出
            try:
                year_month = created_at[:7]  # YYYY-MM
                monthly_counts[year_month] = monthly_counts.get(year_month, 0) + 1
            except:
                continue
    
    if monthly_counts:
        # データフレーム作成
        df = pd.DataFrame(list(monthly_counts.items()), columns=['年月', '記事数'])
        df = df.sort_values('年月')
        
        fig = px.line(
            df,
            x='年月',
            y='記事数',
            title="月別記事数推移",
            markers=True,
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(
            xaxis_title="年月",
            yaxis_title="記事数",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("データがありません")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_article_preview(article_data: Dict, article_content: str):
    """記事プレビュー表示"""
    st.markdown('<div class="article-preview">', unsafe_allow_html=True)
    
    # メタデータ表示
    st.markdown(
        f"""
        <div class="article-metadata">
            <strong>タイプ:</strong> {article_data.get('type', 'N/A')} | 
            <strong>トーン:</strong> {article_data.get('tone', 'N/A')} | 
            <strong>文字数:</strong> {len(article_content)} 文字 | 
            <strong>作成日:</strong> {article_data.get('created_at', 'N/A')}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 記事内容表示
    st.markdown(article_content)
    
    st.markdown('</div>', unsafe_allow_html=True)
