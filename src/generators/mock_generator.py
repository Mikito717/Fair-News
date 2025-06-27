"""
テスト用のモックモジュール
実際のOpenAI APIやGemini APIを使用せずにテストを実行するためのモック機能
"""

class MockArticleGenerator:
    """テスト用のモックArticleGenerator（OpenAI用）"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
    
    def generate_article(self, theme: str, article_type: str, tone: str, word_count: int, include_seo: bool = False, max_retries: int = 3):
        """モック記事生成"""
        
        # テスト用の記事内容を生成
        mock_article = f"""# {theme}について

## はじめに

{theme}は現代社会において重要なトピックです。この記事では、{theme}について詳しく解説していきます。

## {theme}の基本概念

{theme}の基本的な概念について説明します。{article_type}として、{tone}なトーンでお伝えします。

### 重要なポイント

1. **第一のポイント**: {theme}の重要性について
2. **第二のポイント**: 実際の活用方法について  
3. **第三のポイント**: 将来の展望について

## 具体的な事例

{theme}に関する具体的な事例をいくつか紹介します。

### 事例1: 基本的な活用方法

基本的な活用方法について詳しく説明します。この方法は初心者にも理解しやすく、すぐに実践できる内容です。

### 事例2: 応用的な活用方法

より応用的な活用方法について解説します。経験者向けの内容も含まれています。

## まとめ

{theme}について詳しく解説してきました。重要なポイントを以下にまとめます：

- {theme}の基本概念の理解
- 具体的な活用方法の習得
- 将来の展望への理解

今後も{theme}に関する情報を継続的に学習し、実践に活かしていくことが重要です。

---

*この記事は約{word_count}文字で構成されています。*"""

        if include_seo:
            mock_article += f"""

## SEO情報

**メタディスクリプション**: {theme}について詳しく解説。基本概念から実践的な活用方法まで、わかりやすく説明します。

**主要キーワード**: {theme}, 活用方法, 基本概念, 実践

**関連キーワード**: 解説, 方法, 重要性, 将来性"""

        return True, mock_article, None
    
    def generate_titles(self, theme: str, article_type: str):
        """モックタイトル生成"""
        
        mock_titles = f"""以下が{theme}に関する{article_type}のタイトル候補です：

1. **{theme}の完全ガイド：初心者から上級者まで**
   - 包括的で信頼性の高い印象を与えるタイトル

2. **今すぐ始められる{theme}の活用方法5選**
   - 具体的で実践的な内容を示すタイトル

3. **{theme}で変わる未来：知っておくべき重要ポイント**
   - 将来性と重要性を強調したタイトル

4. **専門家が教える{theme}の基本と応用**
   - 権威性と専門性をアピールするタイトル

5. **{theme}入門：基礎から学ぶ実践的アプローチ**
   - 初心者向けで学習要素を強調したタイトル"""

        return True, mock_titles, None
    
    def generate_outline(self, theme: str, article_type: str, tone: str):
        """モック構成生成"""
        
        mock_outline = f"""# {theme}に関する{article_type}の構成案

## 1. タイトル
「{theme}の完全ガイド：基礎から実践まで」

## 2. 導入部分の要点
- {theme}の重要性と現在の状況
- 読者が得られる価値の明確化
- 記事の構成と読み方の説明

## 3. 本文の見出しと内容概要

### 3.1 {theme}の基本概念
- 定義と基本的な理解
- 歴史的背景と発展経緯
- 現在の位置づけ

### 3.2 {theme}の重要性
- 社会的な意義
- 個人レベルでの影響
- 経済的な側面

### 3.3 実践的な活用方法
- 基本的な活用法
- 応用的な活用法
- 注意点とベストプラクティス

### 3.4 成功事例の紹介
- 具体的な事例1
- 具体的な事例2
- 事例から学ぶポイント

### 3.5 将来の展望
- 今後の発展予測
- 新しい可能性
- 準備すべきこと

## 4. まとめの要点
- 重要ポイントの再確認
- 読者への行動提案
- 継続学習の重要性

**トーン**: {tone}
**想定読者**: {theme}に興味を持つ初心者から中級者
**記事の目的**: {theme}の理解促進と実践的な活用支援"""

        return True, mock_outline, None
    
    def validate_api_key(self):
        """モックAPIキー検証"""
        if self.api_key == "test_key_for_demo":
            return True, "テスト用APIキーが有効です（OpenAI モックモード）"
        else:
            return False, "テスト用APIキーが設定されていません"


class MockGeminiArticleGenerator:
    """テスト用のモックGeminiArticleGenerator"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
    
    def generate_article(self, theme: str, article_type: str, tone: str, word_count: int, include_seo: bool = False, max_retries: int = 3):
        """モック記事生成（Gemini版）"""
        
        # テスト用の記事内容を生成（Geminiスタイル）
        mock_article = f"""# {theme}について - Gemini AI生成

## 概要

{theme}は現代において注目されている重要なテーマです。本記事では、{theme}について包括的に解説し、読者の理解を深めることを目的としています。

## {theme}の詳細解説

### 基本的な理解

{theme}の基本的な概念について、{tone}なアプローチで説明します。{article_type}として、実用的な情報をお届けします。

### 主要な特徴

{theme}には以下のような特徴があります：

- **特徴1**: 革新性と実用性の両立
- **特徴2**: 幅広い応用可能性
- **特徴3**: 継続的な発展と改善

### 実践的な応用

{theme}を実際に活用する方法について詳しく説明します。

#### 基本的な応用方法

初心者でも取り組みやすい基本的な方法から始めましょう。段階的にスキルを向上させることが重要です。

#### 高度な応用方法

経験を積んだ後は、より高度な応用方法にチャレンジできます。創造性と技術力を組み合わせることで、新しい可能性が開けます。

## 成功のためのポイント

{theme}を成功させるためには、以下の点に注意が必要です：

1. 継続的な学習と実践
2. 最新情報の収集と活用
3. 他者との協力とネットワーキング

## 将来の展望

{theme}の将来性について考察します。技術の進歩とともに、新しい機会と課題が生まれることが予想されます。

## 結論

{theme}は多くの可能性を秘めた分野です。適切な理解と実践により、個人や組織の成長に大きく貢献できるでしょう。

---

*本記事はGemini AIにより生成されました（約{word_count}文字）*"""

        if include_seo:
            mock_article += f"""

## SEO最適化情報

**メタディスクリプション**: {theme}の完全ガイド。基本から応用まで、実践的な情報を分かりやすく解説します。

**主要キーワード**: {theme}, 活用法, 実践, ガイド

**関連キーワード**: 解説, 方法論, 成功事例, 将来性, 応用"""

        return True, mock_article, None
    
    def generate_titles(self, theme: str, article_type: str):
        """モックタイトル生成（Gemini版）"""
        
        mock_titles = f"""Gemini AIが提案する{theme}に関する{article_type}のタイトル候補：

1. **{theme}マスターガイド：2025年版完全攻略法**
   - 最新性と包括性を強調した権威的なタイトル

2. **{theme}で成功する5つの戦略とその実践方法**
   - 具体的な数字と実践性を前面に出したタイトル

3. **{theme}の真実：専門家が語る本当に重要なこと**
   - 権威性と独自性を強調したタイトル

4. **初心者から上級者まで：{theme}の段階別学習法**
   - ターゲット層を明確にした学習指向のタイトル

5. **{theme}革命：変化する世界で生き残る方法**
   - インパクトと緊急性を強調したタイトル"""

        return True, mock_titles, None
    
    def generate_outline(self, theme: str, article_type: str, tone: str):
        """モック構成生成（Gemini版）"""
        
        mock_outline = f"""# Gemini AI提案：{theme}に関する{article_type}の詳細構成

## 1. 記事タイトル
「{theme}完全マスターガイド：基礎から実践まで」

## 2. 導入セクション
- {theme}の現在の重要性と社会的影響
- 読者が本記事から得られる具体的な価値
- 記事の構成と効果的な読み方のガイド

## 3. メインコンテンツ構成

### 3.1 基礎知識編
- {theme}の定義と基本概念
- 歴史的発展と現在の位置づけ
- 関連する重要な用語と概念

### 3.2 理論と原理
- {theme}の根本的な原理
- 科学的・技術的背景
- 理論的フレームワーク

### 3.3 実践応用編
- 基本的な実践方法
- 段階別スキル習得法
- 実際の活用事例とケーススタディ

### 3.4 高度な応用
- 専門的な応用技術
- 創造的な活用方法
- 業界別の特殊な応用例

### 3.5 トラブルシューティング
- よくある問題と解決法
- 失敗例から学ぶ教訓
- 予防策とベストプラクティス

### 3.6 未来展望
- 技術的発展の予測
- 新しい可能性と機会
- 準備すべき知識とスキル

## 4. まとめと行動指針
- 重要ポイントの総括
- 読者への具体的な行動提案
- 継続学習のためのリソース紹介

**記事の特徴**:
- トーン: {tone}
- 対象読者: {theme}に関心を持つ幅広い層
- 記事の目標: 理解促進と実践的スキル向上の支援
- 推定読了時間: 15-20分"""

        return True, mock_outline, None
    
    def validate_api_key(self):
        """モックAPIキー検証（Gemini版）"""
        if self.api_key == "test_gemini_key_for_demo":
            return True, "テスト用Gemini APIキーが有効です（Gemini モックモード）"
        else:
            return False, "テスト用Gemini APIキーが設定されていません"

