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

from st_chat import message as st_message

st.header("💬 채팅")

# 세션 상태에 채팅 내역 저장
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("메시지를 입력하세요", key="chat_input")
if st.button("전송", key="send_btn") and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # 예시: 간단한 자동응답
    if "지도" in user_input:
        bot_reply = "지도를 활용해 북마크를 추가해보세요!"
    else:
        bot_reply = "안녕하세요! 무엇을 도와드릴까요?"
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# 채팅 내역 출력
for chat in st.session_state.chat_history:
    st_message(chat["content"], is_user=(chat["role"] == "user"))