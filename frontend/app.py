### --- frontend/app.py ---
import streamlit as st
import requests

st.title("オフライン・フェイクニュース判定アプリ")

article = st.text_area("ニュース記事を入力してください", height=200)

if st.button("判定する"):
    with st.status("判定を開始します...", expanded=True) as status:
        res = requests.post(
            "http://localhost:8000/api/v1/judge",
            json={"article": article}
        )
        if res.status_code == 200:
            data = res.json()
            status.update(label="判定完了", state="complete")
            st.markdown("## 判定結果")
            for agent in ["liberal", "conservative", "neutral"]:
                st.subheader(agent.capitalize())
                st.markdown(f"**バイアススコア:** {data['results'][agent]['bias_score']}")
                st.markdown("**要約:**")
                st.write(data['results'][agent]['summary'])
        else:
            status.update(label="APIリクエストに失敗しました", state="error")
            st.error("APIリクエストに失敗しました")