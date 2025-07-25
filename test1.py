import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("나만의 북마크 지도")

# 북마크 저장용 세션 상태
if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []

# 입력 폼
with st.form("bookmark_form"):
    name = st.text_input("장소 이름")
    lat = st.number_input("위도", value=37.5665, format="%.6f")
    lon = st.number_input("경도", value=126.9780, format="%.6f")
    submitted = st.form_submit_button("북마크 추가")
    if submitted and name:
        st.session_state["bookmarks"].append({"name": name, "lat": lat, "lon": lon})

# 지도 생성 (초기 위치: 서울)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 북마크 마커 추가
for bm in st.session_state["bookmarks"]:
    folium.Marker([bm["lat"], bm["lon"]], popup=bm["name"]).add_to(m)

# 지도 표시
st_folium(m, width=700, height=500)