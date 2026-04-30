import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

if "cat" not in st.session_state:
    st.session_state.cat = "전체"

if "selected" not in st.session_state:
    st.session_state.selected = None


def fetch(url, params=None):
    try:
        res = requests.get(f"{BASE_URL}/{url}", params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"API 오류: {e}")
        return None


st.title("📊 K-STOCK NAVIGATOR")

# 카테고리
cats = fetch("stock/categories") or []
if not cats:
    st.error("❌ 카테고리 데이터 없음 (서버 확인)")
    st.stop()

cols = st.columns(len(cats)+1)

if cols[0].button("전체"):
    st.session_state.cat = "전체"

for i,c in enumerate(cats):
    if cols[i+1].button(c["name"]):
        st.session_state.cat = c["name"]


# 종목 리스트
data = fetch("stock/realtime", {"category": st.session_state.cat}) or []

st.subheader("📈 종목")

for i,d in enumerate(data):
    col1,col2,col3 = st.columns([1,4,2])

    col1.write(i+1)

    if col2.button(d["name"], key=i):
        st.session_state.selected = d["ticker"]
        st.rerun()

    color = "red" if d["change"] > 0 else "blue"
    col3.markdown(f"{d['price_str']} <span style='color:{color}'>({d['change']}%)</span>", unsafe_allow_html=True)


# 상세
if st.session_state.selected:
    st.divider()
    st.subheader(f"📊 {st.session_state.selected}")

    detail = fetch("stock/detail", {"ticker": st.session_state.selected})
    chart = fetch("stock/chart", {"ticker": st.session_state.selected})

    st.write(detail)

    if isinstance(chart, dict) and chart.get("dates") and chart.get("prices"):
        df = pd.DataFrame({
            "date": chart["dates"],
            "price": chart["prices"]
        }).set_index("date")

        st.line_chart(df)
    else:
        st.warning("차트 데이터를 불러오지 못했습니다.")
