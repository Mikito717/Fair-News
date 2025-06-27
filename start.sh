#!/bin/bash

# Fair News - 起動スクリプト

echo "🚀 Fair News - AI自動コンテンツ生成システムを起動しています..."

# 仮想環境の確認
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 仮想環境が有効: $VIRTUAL_ENV"
else
    echo "⚠️  仮想環境が検出されませんでした。依存関係の問題が発生する可能性があります。"
fi

# 依存関係のインストール確認
echo "📦 依存関係を確認中..."
pip install -r requirements.txt > /dev/null 2>&1

# 環境設定ファイルの確認
if [ ! -f "config/.env" ]; then
    echo "⚠️  環境設定ファイル (config/.env) が見つかりません。"
    echo "config/.env.example を参考に設定ファイルを作成してください。"
fi

# データディレクトリの作成
mkdir -p data/saved_articles

echo "🌟 アプリケーションを起動します..."
echo "ブラウザで http://localhost:8501 にアクセスしてください"

# Streamlitアプリを起動
streamlit run main.py
