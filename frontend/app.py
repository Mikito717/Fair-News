# --- frontend/app.py ---
import streamlit as st
import requests

st.title("オフライン・フェイクニュース判定アプリ")

# サイドバーでバックエンド設定
st.sidebar.header("設定")

# システム状態を取得
try:
    status_res = requests.get("http://localhost:8000/api/v1/status")
    if status_res.status_code == 200:
        status_data = status_res.json()
        available_backends = status_data.get("available_backends", [])
        current_backend = status_data.get("current_backend")
        available_ollama_models = status_data.get(
            "available_ollama_models", [])
        suggested_models = status_data.get("suggested_models", [])
    else:
        available_backends = []
        current_backend = None
        available_ollama_models = []
        suggested_models = []
except:
    available_backends = []
    current_backend = None
    available_ollama_models = []
    suggested_models = []

# バックエンド選択
if available_backends:
    backend_choice = st.sidebar.selectbox(
        "モデルバックエンド",
        available_backends,
        index=available_backends.index(
            current_backend) if current_backend in available_backends else 0
    )

    # モデル名選択・入力
    if backend_choice == "ollama":
        if available_ollama_models:
            # 利用可能なOllamaモデルがある場合はselectboxで選択
            model_name = st.sidebar.selectbox(
                "Ollamaモデルを選択",
                available_ollama_models,
                help="現在利用可能なOllamaモデル一覧"
            )
        else:
            # 利用可能なモデルがない場合は手動入力と推奨モデル表示
            st.sidebar.warning("利用可能なOllamaモデルがありません")
            if suggested_models:
                st.sidebar.info("推奨モデル:")
                for model in suggested_models:
                    st.sidebar.code(f"ollama pull {model}")
            model_name = st.sidebar.text_input(
                "モデル名を入力",
                value="llama3.2",
                help="まずモデルをダウンロードしてください: ollama pull <model_name>"
            )
    else:
        # Transformersの場合は手動入力
        model_name = st.sidebar.text_input(
            "Transformersモデル名",
            value="rinna/japanese-gpt-neox-3.6b-instruction-sft",
            help="Hugging Faceのモデル名を入力してください"
        )

    # バックエンド切り替えボタン
    if st.sidebar.button("バックエンドを切り替え"):
        try:
            switch_res = requests.post(
                "http://localhost:8000/api/v1/switch-backend",
                json={"backend": backend_choice, "model_name": model_name}
            )
            if switch_res.status_code == 200:
                st.sidebar.success(f"{backend_choice} に切り替えました")
                st.experimental_rerun()
            else:
                st.sidebar.error("バックエンドの切り替えに失敗しました")
        except Exception as e:
            st.sidebar.error(f"エラー: {e}")
else:
    st.sidebar.warning("利用可能なバックエンドがありません")
    backend_choice = None
    model_name = None

# 現在の状態表示
if current_backend:
    st.sidebar.info(f"現在のバックエンド: {current_backend}")

# 利用可能なモデル一覧の表示
if available_ollama_models:
    with st.sidebar.expander("利用可能なOllamaモデル"):
        for model in available_ollama_models:
            st.write(f"• {model}")

article = st.text_area("ニュース記事を入力してください", height=200)

if st.button("判定する"):
    if not article.strip():
        st.error("記事を入力してください")
    else:
        with st.status("判定を開始します...", expanded=True) as status:
            request_data = {"article": article}
            if backend_choice and model_name:
                request_data["backend"] = backend_choice
                request_data["model_name"] = model_name

            res = requests.post(
                "http://localhost:8000/api/v1/judge",
                json=request_data
            )
            if res.status_code == 200:
                data = res.json()
                status.update(label="判定完了", state="complete")

                # メタ情報表示
                meta = data.get('meta', {})
                st.markdown("## 判定結果")
                st.caption(
                    f"実行時間: {meta.get('execution_time', 'N/A')} | バックエンド: {meta.get('backend', 'N/A')} | モデル: {meta.get('model_name', 'N/A')}")

                # エージェント別結果表示
                for agent in ["liberal", "conservative", "neutral"]:
                    agent_names = {
                        "liberal": "🌿 リベラル視点",
                        "conservative": "🏛️ 保守的視点",
                        "neutral": "⚖️ 中立的視点"
                    }

                    st.subheader(agent_names[agent])
                    bias_score = data['results'][agent]['bias_score']
                    st.markdown(
                        f"**バイアススコア:** {bias_score:.2f} ({'中立' if bias_score < 0.3 else '軽度の偏り' if bias_score < 0.7 else '強い偏り'})")
                    st.markdown("**分析:**")
                    st.write(data['results'][agent]['summary'])
                    st.divider()
            else:
                status.update(label="APIリクエストに失敗しました", state="error")
                st.error(f"APIリクエストに失敗しました: {res.status_code}")
                try:
                    error_detail = res.json()
                    st.error(
                        f"詳細: {error_detail.get('detail', 'Unknown error')}")
                except:
                    pass
