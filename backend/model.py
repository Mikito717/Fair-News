import os
from typing import Dict, List, Optional
from enum import Enum

# 条件的なインポート
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Ollama not available. Install with: pip install ollama")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available. Install with: pip install transformers torch")


class ModelBackend(Enum):
    OLLAMA = "ollama"
    TRANSFORMERS = "transformers"


# エージェントのプロンプト定義
liberal_prompt = """あなたはリベラル（進歩主義的）な視点を持つ評論家です。個人の権利、社会的公正、環境保護、多様性の重要性を重視します。保守的な権力構造や国家主義的な論調には懐疑的です。以下のニュースに対して、リベラル的視点から見て、その内容がいかに公平であるか、または偏っているかを論じてください。"""

conservative_prompt = """あなたは保守的な視点を持つ評論家です。伝統、国家、家族の価値を重視し、個人の自由と責任を強調します。リベラルな政策や国家介入には懐疑的です。以下のニュースに対して、保守的視点から見て、その内容がいかに公平であるか、または偏っているかを論じてください。"""

neutral_prompt = """あなたは中立かつ事実ベースの立場から、ニュースの内容の正確性や信頼性を評価するファクトチェッカーです。事実、出典、論理性に基づいてこのニュースがどれだけ客観的かを評価してください。感情的・扇動的な表現についても指摘してください。"""

agent_prompts = {
    "liberal": liberal_prompt,
    "conservative": conservative_prompt,
    "neutral": neutral_prompt
}


class ModelManager:
    """モデル管理クラス"""

    def __init__(self):
        self.backend = None
        self.model = None
        self.tokenizer = None
        self.pipeline = None

    def get_available_backends(self) -> List[str]:
        """利用可能なバックエンドのリストを返す"""
        backends = []
        if OLLAMA_AVAILABLE:
            backends.append(ModelBackend.OLLAMA.value)
        if TRANSFORMERS_AVAILABLE:
            backends.append(ModelBackend.TRANSFORMERS.value)
        return backends

    def get_ollama_models(self) -> List[str]:
        """利用可能なOllamaモデルの一覧を返す"""
        if not OLLAMA_AVAILABLE:
            return []

        try:
            # test_backend.pyと同じ方法でOllamaモデル一覧を取得
            ollama_models = ollama.list()
            available_models = []

            # test_backend.pyの実装に合わせて修正
            if ollama_models['models']:
                for model in ollama_models['models']:
                    # modelオブジェクトからmodel名を取得
                    if hasattr(model, 'model'):
                        available_models.append(model.model)
                    elif isinstance(model, dict) and 'model' in model:
                        available_models.append(model['model'])
                    elif hasattr(model, 'name'):
                        available_models.append(model.name)
                    elif isinstance(model, dict) and 'name' in model:
                        available_models.append(model['name'])

            return available_models
        except Exception as e:
            print(f"Ollamaモデル一覧の取得に失敗: {e}")
            return []

    def check_ollama_model(self, model_name="phi4") -> bool:
        """指定されたollamaモデルが利用可能かチェック"""
        if not OLLAMA_AVAILABLE:
            return False

        try:
            available_models = self.get_ollama_models()
            return model_name in available_models
        except Exception as e:
            print(f"Ollamaモデルのチェックに失敗: {e}")
            return False

    def load_transformers_model(self, model_name="rinna/japanese-gpt-neox-3.6b-instruction-sft"):
        """Transformersモデルを読み込み"""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("Transformers is not available")

        try:
            print(f"Transformersモデル '{model_name}' を読み込み中...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )

            # パイプラインの作成
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )

            print(f"Transformersモデル '{model_name}' の読み込み完了")
            return True

        except Exception as e:
            print(f"Transformersモデルの読み込みエラー: {e}")
            return False

    def switch_backend(self, backend: ModelBackend, model_name: Optional[str] = None) -> bool:
        """バックエンドを切り替え"""
        if backend == ModelBackend.OLLAMA:
            if not OLLAMA_AVAILABLE:
                print("Ollamaが利用できません")
                return False

            model_name = model_name or "llama3.2"
            if not self.check_ollama_model(model_name):
                available_models = self.get_ollama_models()
                print(f"Ollamaモデル '{model_name}' が利用できません")
                if available_models:
                    print(f"利用可能なOllamaモデル: {', '.join(available_models)}")
                    print("モデルをダウンロードするには: ollama pull <model_name>")
                else:
                    print("利用可能なOllamaモデルがありません")
                    print("推奨モデルをダウンロードしてください:")
                    print("  ollama pull llama3.2")
                    print("  ollama pull qwen2.5")
                    print("  ollama pull phi4")
                return False

            self.backend = ModelBackend.OLLAMA
            print(f"バックエンドをOllama ({model_name}) に切り替えました")
            return True

        elif backend == ModelBackend.TRANSFORMERS:
            if not TRANSFORMERS_AVAILABLE:
                print("Transformersが利用できません")
                return False

            model_name = model_name or "rinna/japanese-gpt-neox-3.6b-instruction-sft"
            if self.load_transformers_model(model_name):
                self.backend = ModelBackend.TRANSFORMERS
                print(f"バックエンドをTransformers ({model_name}) に切り替えました")
                return True
            else:
                return False

        return False

    def generate_response_ollama(self, agent: str, prompt: str, model_name: str = "llama3.2") -> dict:
        """Ollamaを使用してレスポンスを生成"""
        system_prompt = f"あなたは日本語で回答する有用なアシスタントです。{agent_prompts[agent]}"
        full_prompt = f"{system_prompt}\n\n{prompt}"

        try:
            # test_backend.pyと同じ方法でollama.generateを使用
            print("処理開始", model_name)
            response = ollama.generate(model=model_name, prompt=full_prompt)

            result = response['response']
            print(f"{agent} (Ollama): {result}")

            # バイアススコアを取得
            point_response = ollama.generate(
                model=model_name,
                prompt=f"{full_prompt}に対して、この記事は{agent_prompts[agent]}の視点から何点の偏りがつけられますか？\n\n0-100で答えてください。0：偏りなし（中立）、100：非常に偏っている（極左、極右）"
            )

            # スコアを数値に変換（エラーハンドリング付き）
            try:
                score_text = point_response['response'].strip()
                # 数値部分のみを抽出
                import re
                score_match = re.search(r'\b(\d{1,2}|100)\b', score_text)
                bias_score = float(score_match.group()
                                   ) if score_match else 50.0
            except:
                bias_score = 50  # デフォルト値

            return {
                "summary": result,
                "bias_score": bias_score
            }

        except Exception as e:
            error_msg = f"Ollama APIエラー ({agent}): {str(e)}"
            print(error_msg)
            return {
                "summary": error_msg,
                "bias_score": 0.5
            }

    def generate_response_transformers(self, agent: str, prompt: str) -> dict:
        """Transformersを使用してレスポンスを生成"""
        if not self.pipeline:
            return {
                "summary": "Transformersモデルが読み込まれていません",
                "bias_score": 0.5
            }

        full_prompt = f"{agent_prompts[agent]}\n\n記事: {prompt}\n\n分析:"

        try:
            # テキスト生成
            outputs = self.pipeline(
                full_prompt,
                max_length=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )

            result = outputs[0]['generated_text']
            # 元のプロンプト部分を除去
            result = result.replace(full_prompt, "").strip()

            print(f"{agent} (Transformers): {result}")

            # Transformersの場合はシンプルなバイアススコア計算
            # より高度な実装が必要な場合は別途実装
            bias_score = 0.5  # デフォルト値

            return {
                "summary": result,
                "bias_score": bias_score
            }

        except Exception as e:
            error_msg = f"Transformers APIエラー ({agent}): {str(e)}"
            print(error_msg)
            return {
                "summary": error_msg,
                "bias_score": 0.5
            }

    def generate_response(self, agent: str, prompt: str, model_name: Optional[str] = None) -> dict:
        """現在のバックエンドを使用してレスポンスを生成"""
        if self.backend == ModelBackend.OLLAMA:
            return self.generate_response_ollama(agent, prompt, model_name or "llama3.2")
        elif self.backend == ModelBackend.TRANSFORMERS:
            return self.generate_response_transformers(agent, prompt)
        else:
            return {
                "summary": "バックエンドが設定されていません",
                "bias_score": 0.5
            }


# グローバルなモデルマネージャーインスタンス
model_manager = ModelManager()

# 後方互換性のための関数


def check_ollama_model(model_name="llama3.2") -> bool:
    """後方互換性のためのOllamaモデルチェック関数"""
    return model_manager.check_ollama_model(model_name)


def generate_response(agent: str, prompt: str, model_name: str = "llama3.2") -> dict:
    """後方互換性のためのレスポンス生成関数"""
    if model_manager.backend is None:
        # デフォルトでOllamaを試す
        if model_manager.switch_backend(ModelBackend.OLLAMA, model_name):
            pass
        elif model_manager.switch_backend(ModelBackend.TRANSFORMERS):
            pass
        else:
            return {
                "summary": "利用可能なバックエンドがありません",
                "bias_score": 0.5
            }

    return model_manager.generate_response(agent, prompt, model_name)
