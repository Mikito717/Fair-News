# Fair News - AI自動コンテンツ生成システム

Streamlitを使用したAI自動コンテンツ生成システムです。**LangGraphによるディープリサーチ機能**を統合し、最新情報をWeb検索して高品質なニュース記事を自動生成できます。

## 🚀 主な機能

### � **ディープリサーチ記事生成（NEW!）**
- **LangGraph + Gemini**による高度なWeb検索とリサーチ
- 最新情報を複数のソースから収集
- 検索結果を分析・統合して信頼性の高い記事を生成
- リサーチループによる段階的な情報深掘り
- 参考ソースの自動引用とリンク生成

### �📝 記事生成機能
- テーマやキーワードに基づいた記事の自動生成
- **Gemini API**、**OpenAI API**の両方に対応
- 記事の種類（ブログ記事、ニュース記事、解説記事など）の選択
- 記事のトーン（フォーマル、カジュアル、専門的など）の調整
- 文字数の指定（300〜3000文字）
- SEO要素の自動組み込み

### 📚 記事管理機能
- 生成した記事の保存と管理
- 記事の検索機能
- 記事の編集と更新
- 記事の削除機能
- Markdownファイルとしてのダウンロード

### 📊 統計情報
- 総記事数、総文字数、平均文字数の表示
- 記事タイプ別の分布グラフ
- 月別記事数の推移

### 🔧 高度な機能
- タイトル候補の生成
- 記事構成の生成
- 設定のエクスポート/インポート

## 📋 必要な環境

- Python 3.11以上
- Gemini APIキー（ディープリサーチ機能に必要）
- OpenAI APIキー（OpenAI記事生成機能利用時）

## 🛠️ インストールと実行

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example`ファイルを`.env`にコピーし、APIキーを設定してください：

```bash
cp .env.example .env
```

`.env`ファイルに以下を設定：

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # オプション
```

`.env`ファイルを編集：
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3. アプリケーションの実行

#### 通常モード（OpenAI API使用）
```bash
streamlit run app.py
```

#### テストモード（モック機能使用）
```bash
TEST_MODE=true streamlit run app_test.py
```

アプリケーションは `http://localhost:8501` で利用できます。

## 📁 プロジェクト構造

```
streamlit_ai_content_generator/
├── app.py                    # メインアプリケーション
├── app_test.py              # テスト用アプリケーション
├── article_generator.py     # AI記事生成機能
├── article_manager.py       # 記事管理機能
├── prompts.py              # プロンプト管理
├── mock_generator.py       # テスト用モック機能
├── requirements.txt        # 依存関係
├── .env.example           # 環境変数テンプレート
├── .env                   # 環境変数（実際の設定）
├── todo.md               # 開発タスク管理
├── E2E_TEST_REPORT.md    # E2Eテスト結果
├── README.md             # このファイル
└── saved_articles/       # 保存された記事（自動作成）
```

## 🧪 テスト

### E2Eテストの実行

テストモードでアプリケーションを起動し、ブラウザで動作確認を行ってください：

```bash
TEST_MODE=true streamlit run app_test.py
```

テスト用APIキー: `test_key_for_demo`

詳細なテスト結果は `E2E_TEST_REPORT.md` を参照してください。

## 🔧 設定

### OpenAI API設定

- `OPENAI_API_KEY`: OpenAI APIキー
- `OPENAI_MODEL`: 使用するモデル（推奨: gpt-4o-mini）

### Gemini API設定

- `GEMINI_API_KEY`: Google Gemini APIキー
- `GEMINI_MODEL`: 使用するモデル（推奨: gemini-2.5-flash）

#### 利用可能なGeminiモデル

| モデル | 特徴 | 推奨用途 |
|--------|------|----------|
| `gemini-2.5-flash` ⭐ | 最新の高性能モデル | 一般的な記事生成（推奨） |
| `gemini-2.5-pro` | 最高性能の思考モデル | 専門記事・複雑な内容 |
| `gemini-2.5-flash-lite-preview-06-17` | 高スループット・低コスト | 大量生成・シンプルな記事 |
| `gemini-2.0-flash` | 次世代機能・高速 | リアルタイム生成 |
| `gemini-1.5-flash` | 安定版高速モデル | 安定性重視 |
| `gemini-1.5-pro` | 安定版高性能モデル | 高品質記事 |

詳細は [Geminiモデルガイド](docs/GEMINI_MODELS.md) を参照してください。

### テストモード

- `TEST_MODE=true`: モック機能を使用してテスト実行

## 📖 使用方法

### 1. 記事生成
1. サイドバーでOpenAI APIキーを設定
2. 記事のテーマやキーワードを入力
3. 記事の種類、トーン、文字数を選択
4. 「記事を生成」ボタンをクリック
5. 生成された記事を確認・編集
6. 「記事を保存」で保存

### 2. 記事管理
1. 「記事管理」タブに移動
2. 保存された記事の一覧を確認
3. 検索機能で特定の記事を検索
4. 記事の表示、編集、削除が可能

### 3. 統計情報
1. 「統計情報」タブに移動
2. 記事数や文字数の統計を確認
3. グラフで記事の分布を視覚化

## 🚨 注意事項

- OpenAI APIの使用には料金が発生します
- APIキーは安全に管理してください
- 生成された記事の内容は必ず確認してから使用してください
- テストモードでは実際のAPIは使用されません

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

バグ報告や機能要望は、GitHubのIssueでお知らせください。

## 📞 サポート

質問や問題がある場合は、プロジェクトのドキュメントを参照するか、開発者にお問い合わせください。

---

**バージョン**: 1.0.0  
**最終更新**: 2025年6月27日

