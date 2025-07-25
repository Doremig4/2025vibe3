import streamlit as st

# folium, streamlit-folium, geopy가 설치되어 있는지 확인
try:
    import folium
    from streamlit_folium import st_folium
    from geopy.geocoders import Nominatim
except ModuleNotFoundError as e:
    st.error(
        "필요한 패키지가 설치되어 있지 않습니다: {e.name}\n"
        "아래 명령어로 설치 후 다시 실행하세요:\n"
        "pip install streamlit folium streamlit-folium geopy"
    )
    st.stop()

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
                if location is None:
                    raise ValueError("주소를 찾을 수 없습니다.")
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
    try:
        folium.Marker(
            location=[float(bm["lat"]), float(bm["lon"])],
            popup=f"<b>{bm['name']}</b><br>{bm['desc']}",
            icon=folium.Icon(color="blue", icon="bookmark")
        ).add_to(m)
    except Exception as e:
        st.write(f"마커 추가 오류: {e}")

# 지도 표시
st_folium(m, width=1000, height=600)

# 북마크 리스트 출력
with st.expander("📋 북마크 목록 보기"):
    st.write(f"현재 북마크 개수: {len(st.session_state.bookmarks)}")
    for bm in st.session_state.bookmarks:
        st.markdown(f"- **{bm['name']}** ({bm['lat']:.4f}, {bm['lon']:.4f})  \n  {bm['desc']}")