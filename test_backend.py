#!/usr/bin/env python3
"""
バックエンドスイッチング機能のテストスクリプト
"""
import ollama
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

"""ModelManagerの基本機能をテスト"""
print("=== Fair-News バックエンドテスト ===\n")

print("\n--- Ollamaテスト ---")

# 利用可能なOllamaモデル一覧を取得
ollama_models = ollama.list()
# print(f"利用可能なOllamaモデル: {ollama_models}")

# modelsリストから最初のモデルを取得
if ollama_models['models']:
    use_model = ollama_models['models'][0]
    print(f"使用するモデル: {use_model}")
    print(f"モデル名: {use_model.model}")
    print(f"サイズ: {use_model.size / (1024**3):.2f}GB")
    print(f"パラメータサイズ: {use_model.details.parameter_size}")
    start_time = time.time()
    # Generate your response here

    res = ollama.generate(
        model=use_model["model"], prompt='なぜ空は青いのか？日本語で回答してください。')

    end_time = time.time()
    print(f"実行時間: {end_time - start_time:.2f}秒")
    print(res['response'], res['total_duration'])
else:
    print("利用可能なOllamaモデルがありません")
