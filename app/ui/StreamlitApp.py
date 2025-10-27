import streamlit as st
import requests, os
st.set_page_config(page_title="LegalDocGen", layout="wide")
st.title("⚖️ LegalDocGen — AI Legal Document Generator (MVP)")
backend = os.getenv("BACKEND_URL", "http://localhost:8001")
with st.sidebar:
    st.header("案件資訊")
    case_title = st.text_input("案件標題", "催告返還・侵權停止請求")
    principal = st.text_input("當事人", "林ＯＯ")
    facts = st.text_area("事實", "對方未經擅用素材...")
    demands = st.text_area("請求", "七日內返還並停止侵權，逾期依法處理。")
    query = st.text_input("檢索關鍵詞", "契約 無效 第71條")
    template = st.selectbox("模板", ["lawyer_letter.md", "evidence_letter.md"])
col1, col2 = st.columns([3, 2])
if st.button("生成文件"):
    payload = dict(case_title=case_title, principal=principal, facts=facts, demands=demands, query=query, template_name=template)
    try:
        r = requests.post(f"{backend}/generate", json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        st.session_state["md"] = data["markdown"]
        st.success("生成成功！")
    except Exception as e:
        st.error(f"生成失敗：{e}")
with col1:
    st.subheader("📄 Markdown 預覽")
    md = st.session_state.get("md", "")
    st.markdown(md or "_尚未生成_", unsafe_allow_html=False)
with col2:
    if st.button("匯出 PDF", disabled=not st.session_state.get("md")):
        try:
            r = requests.post(f"{backend}/export_pdf", json={"md_text": st.session_state["md"]}, timeout=30)
            st.write(r.json())
        except Exception as e:
            st.error(f"匯出失敗：{e}")
    st.info("此為簡化 PDF，後續可改為 HTML→PDF 提升版面品質。")
