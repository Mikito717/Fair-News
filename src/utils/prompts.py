"""
プロンプト管理モジュール
記事生成用のプロンプトテンプレートを管理
"""


def get_article_generation_prompt(theme, article_type, tone, word_count, include_seo=False):
    """
    記事生成用のプロンプトを生成

    Args:
        theme (str): 記事のテーマ
        article_type (str): 記事の種類
        tone (str): 記事のトーン
        word_count (int): 目標文字数
        include_seo (bool): SEO要素を含めるかどうか

    Returns:
        str: 生成されたプロンプト
    """

    base_prompt = f"""あなたは優秀なライターです。以下の条件に従って高品質な記事を作成してください。

【記事の条件】
- テーマ: {theme}
- 記事の種類: {article_type}
- トーン: {tone}
- 文字数: 約{word_count}文字

【記事の構成】
1. 魅力的なタイトル（読者の興味を引く）
2. 導入部分（問題提起や興味を引く内容）
3. 本文（適切な見出しで構成された内容）
   - 見出しは ## を使用
   - 各セクションは読みやすく構成
   - 具体例や事例を含める
4. まとめ（要点の整理と読者への行動提案）

【記事の品質要件】
- 読者にとって価値のある情報を提供
- 論理的で分かりやすい構成
- 興味深く読みやすい文章
- 信頼性のある内容"""

    if include_seo:
        seo_section = """

【SEO要素】
- メタディスクリプション（120文字以内）
- 主要キーワードの自然な配置
- 関連キーワードの提案"""
        base_prompt += seo_section

    base_prompt += """

記事は日本語で作成し、読者が最後まで読みたくなるような魅力的な内容にしてください。"""

    return base_prompt


def get_title_generation_prompt(theme, article_type):
    """
    タイトル生成専用のプロンプト

    Args:
        theme (str): 記事のテーマ
        article_type (str): 記事の種類

    Returns:
        str: タイトル生成用プロンプト
    """

    return f"""以下の条件で魅力的な記事タイトルを5つ提案してください。

テーマ: {theme}
記事の種類: {article_type}

【タイトルの要件】
- 読者の興味を引く
- SEOに効果的
- 具体的で分かりやすい
- 30文字以内

各タイトルの後に、そのタイトルの特徴や狙いを簡潔に説明してください。"""


def get_outline_generation_prompt(theme, article_type, tone):
    """
    記事構成生成用のプロンプト

    Args:
        theme (str): 記事のテーマ
        article_type (str): 記事の種類
        tone (str): 記事のトーン

    Returns:
        str: 構成生成用プロンプト
    """

    return f"""以下の条件で記事の詳細な構成を作成してください。

テーマ: {theme}
記事の種類: {article_type}
トーン: {tone}

【構成の要件】
1. タイトル
2. 導入部分の要点
3. 本文の見出しと各セクションの内容概要
4. まとめの要点

各セクションで扱う内容を具体的に記載し、読者にとって価値のある構成にしてください。"""


def get_research_based_article_prompt(original_query, research_content, article_type, tone, word_count, include_seo=False):
    """
    リサーチ結果に基づく記事生成用のプロンプト

    Args:
        original_query (str): 元の検索クエリ
        research_content (str): リサーチ結果のコンテンツ
        article_type (str): 記事の種類
        tone (str): 記事のトーン
        word_count (int): 目標文字数
        include_seo (bool): SEO要素を含めるかどうか

    Returns:
        str: 生成されたプロンプト
    """

    base_prompt = f"""あなたは優秀なジャーナリストです。以下のリサーチ結果をもとに高品質な記事を作成してください。

【元のクエリ】
{original_query}

【リサーチ結果】
{research_content}

【記事の条件】
- 記事の種類: {article_type}
- トーン: {tone}
- 文字数: 約{word_count}文字

【記事の構成】
1. 魅力的なタイトル（読者の興味を引く）
2. 導入部分（クエリに対する背景情報や問題提起）
3. 本文（リサーチ結果をもとにした詳細な内容）
   - 見出しは ## を使用
   - リサーチで得られた具体的な情報や事例を含める
   - 信頼性のあるソースからの情報を活用
4. まとめ（要点の整理と読者への価値提供）

【記事の品質要件】
- リサーチ結果で得られた最新で正確な情報を使用
- 元のクエリに対する明確な回答を提供
- 論理的で分かりやすい構成
- 読者にとって価値のある洞察を含める
- 信頼性のある内容（リサーチソースを適切に活用）"""

    if include_seo:
        seo_section = """

【SEO要素】
- メタディスクリプション（120文字以内）
- 主要キーワードの自然な配置
- 関連キーワードの提案"""
        base_prompt += seo_section

    base_prompt += """

リサーチ結果に含まれる情報を正確に反映し、読者が最後まで読みたくなるような魅力的で価値ある記事を日本語で作成してください。
リサーチで得られた具体的な数値、事例、専門家の意見などを積極的に活用してください。"""

    return base_prompt
