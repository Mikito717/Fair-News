# Fair-News

このリポジトリは、ニュース記事のバイアス判定を行うWebアプリケーションです。

## 構成
- backend: FastAPIによるAPIサーバ
- frontend: Streamlitによるフロントエンド

## 使い方

### 1. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. バックエンド（FastAPIサーバ）の起動

```bash
cd backend
uvicorn main:app --reload
```

### 3. フロントエンド（Streamlitアプリ）の起動

別ターミナルで以下を実行：

```bash
cd frontend
streamlit run app.py
```

### 4. ブラウザでアクセス

Streamlitの指示に従い、表示されたURLにアクセスしてください。

## 注意事項
- モデルの初期化時に大きなメモリを消費します。
- APIキーやパスワード等の機密情報は含まれていません。

## 開発者
- GitHub: https://github.com/Mikito717/Fair-News
