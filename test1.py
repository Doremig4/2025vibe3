import streamlit as st

# folium, streamlit-folium, geopy가 설치되어 있는지 확인
try:
    import folium
    from streamlit_folium import st_folium
    from geopy.geocoders import Nominatim
except ModuleNotFoundError as e:
    st.error(
        f"필요한 패키지가 설치되어 있지 않습니다: {e.name}\n"
        "아래 명령어로 설치 후 다시 실행하세요:\n"
        "pip install streamlit folium streamlit-folium geopy"
    )
    st.stop()

st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도")
st.write("원하는 장소를 입력하거나 지도에서 위치를 선택해 북마크를 추가하세요!")

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

# folium 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 기존 북마크 마커 추가
for bm in st.session_state.bookmarks:
    popup_html = f"<b>{bm['name']}</b><br>{bm['desc']}"
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=popup_html,
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 클릭 이벤트 처리
map_data = st_folium(m, width=1000, height=600, returned_objects=["last_clicked"])

# 클릭한 위치 임시 마커 표시 및 안내
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.session_state.selected_location = (lat, lon)
    st.info(f"선택된 위치: 위도 {lat:.5f}, 경도 {lon:.5f}")

# 폼: 위치 입력 또는 지도 클릭
with st.form("bookmark_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("📌 북마크 이름", "")
        location_input = st.text_input("🗺️ 주소 또는 위도,경도", "")
    with col2:
        description = st.text_area("📝 설명", "")
        submit = st.form_submit_button("북마크 추가")

    if submit and name.strip():
        lat, lon = None, None
        # 지도에서 선택한 위치가 있으면 우선 사용
        if st.session_state.selected_location:
            lat, lon = st.session_state.selected_location
        # 아니면 입력값 사용
        elif location_input.strip():
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
        if lat is not None and lon is not None:
            st.session_state.bookmarks.append({
                "name": name,
                "lat": lat,
                "lon": lon,
                "desc": description
            })
            st.success(f"✅ '{name}' 북마크가 추가되었습니다!")
            st.session_state.selected_location = None  # 선택 초기화
        else:
            st.error("위치를 입력하거나 지도에서 선택해 주세요.")

# 북마크 리스트 출력
with st.expander("📋 북마크 목록 보기"):
    for bm in st.session_state.bookmarks:
        st.markdown(f"- **{bm['name']}** ({bm['lat']:.4f}, {bm['lon']:.4f})  \n  {bm['desc']}")