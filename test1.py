import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도")
st.write("원하는 장소를 입력하고 북마크를 지도에 추가하세요!")

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 폼: 위치 입력
with st.form("bookmark_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("📌 북마크 이름", "")
        location_input = st.text_input("🗺️ 주소 또는 위도,경도", "")
    with col2:
        description = st.text_area("📝 설명", "")
        submit = st.form_submit_button("북마크 추가")

    if submit and location_input.strip() and name.strip():
        # 주소 → 위도/경도 변환
        geolocator = Nominatim(user_agent="bookmark_map")
        try:
            if "," in location_input:
                lat, lon = map(float, location_input.split(","))
            else:
                location = geolocator.geocode(location_input)
                lat, lon = location.latitude, location.longitude
        except Exception as e:
            st.error(f"❌ 위치를 찾을 수 없습니다: {e}")
        else:
            st.session_state.bookmarks.append({
                "name": name,
                "lat": lat,
                "lon": lon,
                "desc": description
            })
            st.success(f"✅ '{name}' 북마크가 추가되었습니다!")

# folium 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

for bm in st.session_state.bookmarks:
    popup_html = f"<b>{bm['name']}</b><br>{bm['desc']}"
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=popup_html,
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 표시
st_folium(m, width=1000, height=600)

# 북마크 리스트 출력
with st.expander("📋 북마크 목록 보기"):
    for bm in st.session_state.bookmarks:
        st.markdown(f"- **{bm['name']}** ({bm['lat']:.4f}, {bm['lon']:.4f})  \n  {bm['desc']}")
