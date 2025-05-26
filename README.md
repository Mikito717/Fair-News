# Fair-News

このリポジトリは、ニュース記事のバイアス判定を行うWebアプリケーションです。複数のAIモデルバックエンド（OllamaおよびTransformers）をサポートしています。

## 特徴
- 🔄 **マルチバックエンド対応**: OllamaとTransformersの両方をサポート
- 🎯 **3つの視点**: リベラル、保守的、中立的な視点からの分析
- 🌐 **リアルタイムスイッチング**: フロントエンドからバックエンドを切り替え可能
- 📊 **詳細な分析**: バイアススコアと詳細な要約を提供

## 構成
- **backend**: FastAPIによるAPIサーバ（OllamaおよびTransformers対応）
- **frontend**: Streamlitによるフロントエンド

## 使い方

### 1. モデルバックエンドの準備

#### Option A: Ollama（推奨）
```bash
# macOSの場合
brew install ollama

# または公式サイトからダウンロード: https://ollama.ai
```

Ollamaを起動し、必要なモデルをダウンロード：
```bash
ollama serve  # バックグラウンドで起動
ollama pull llama3.2  # 日本語対応モデル
ollama pull qwen2.5   # その他のモデル（オプション）
```

#### Option B: Transformers（ローカルGPU使用）
GPU環境での使用を推奨。以下のモデルなどが利用可能：
- `rinna/japanese-gpt-neox-3.6b-instruction-sft`
- その他のHugging Faceモデル

### 2. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 3. バックエンド（FastAPIサーバ）の起動

```bash
cd backend
uvicorn main:app --reload
```

### 4. フロントエンド（Streamlitアプリ）の起動

別ターミナルで以下を実行：

```bash
cd frontend
streamlit run app.py
```

### 5. ブラウザでアクセス

Streamlitの指示に従い、表示されたURLにアクセスしてください。

## API仕様

### エンドポイント

#### `GET /api/v1/status`
システムの状態と利用可能なバックエンドを返します。

#### `POST /api/v1/switch-backend`
モデルバックエンドを切り替えます。
```json
{
  "backend": "ollama",  // "ollama" or "transformers"
  "model_name": "llama3.2"  // オプション
}
```

#### `POST /api/v1/judge`
ニュース記事を分析します。
```json
{
  "article": "分析したいニュース記事",
  "backend": "ollama",    // オプション（一時的な切り替え）
  "model_name": "llama3.2"  // オプション
}
```

## バックエンドの特徴

### Ollama
- ✅ **軽量**: システムリソースの使用量が少ない
- ✅ **簡単**: インストールと管理が簡単
- ✅ **多言語対応**: 日本語対応モデルが豊富
- ⚠️ **ネットワーク**: 初回モデルダウンロード時にインターネット接続が必要

### Transformers
- ✅ **高精度**: より高度なモデルが利用可能
- ✅ **カスタマイズ**: 細かいパラメータ調整が可能
- ⚠️ **リソース**: GPUまたは高性能CPUが推奨
- ⚠️ **初期化**: モデル読み込みに時間がかかる場合がある

## トラブルシューティング

### Ollamaモデルが見つからない場合
```bash
ollama list  # インストール済みモデルを確認
ollama pull llama3.2  # モデルをダウンロード
```

### Transformersでメモリ不足の場合
- より小さなモデルを使用
- `torch_dtype=torch.float16`による精度低下で対応

### ポート競合の場合
```bash
# バックエンドのポートを変更
uvicorn main:app --port 8001

# フロントエンドのポートを変更
streamlit run app.py --server.port 8502
```

## 注意事項
- Ollamaとモデルがインストールされている必要があります。
- Ollamaサーバーが起動している必要があります（`ollama serve`）。
- 使用するモデルによってメモリ使用量が変わります。

## 開発者
- GitHub: https://github.com/Mikito717/Fair-News
