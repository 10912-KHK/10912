import streamlit as st
import folium
from streamlit_folium import st_folium

# 여행지 데이터 정의
places = {
    "밴프 국립공원": {
        "location": [51.4968, -115.9281],
        "description": "로키 산맥 속 아름다운 자연 경관을 감상할 수 있는 밴프 국립공원은 하이킹, 온천, 겨울 스포츠로 유명합니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Moraine_Lake_17092005.jpg/1024px-Moraine_Lake_17092005.jpg"
    },
    "퀘벡 시티": {
        "location": [46.8139, -71.2082],
        "description": "프랑스풍 건축 양식과 고풍스러운 거리로 유명한 퀘벡 시티는 캐나다에서 가장 유럽적인 도시로 꼽힙니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Quebec_City_from_Levis.jpg/1024px-Quebec_City_from_Levis.jpg"
    },
    "토론토": {
        "location": [43.651070, -79.347015],
        "description": "캐나다 최대의 도시 토론토는 CN 타워, 다양한 문화 공연, 쇼핑, 음식으로 가득한 다채로운 도시입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Toronto_Skyline.jpg/1024px-Toronto_Skyline.jpg"
    },
    "밴쿠버": {
        "location": [49.2827, -123.1207],
        "description": "바다와 산이 어우러진 밴쿠버는 아름다운 자연 환경과 다양한 액티비티로 많은 관광객에게 인기입니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Vancouver_Skyline.jpg/1024px-Vancouver_Skyline.jpg"
    }
}

# 스트림릿 앱 구성
st.set_page_config(page_title="캐나다 여행 가이드", layout="wide")
st.title("🇨🇦 캐나다 여행 가이드")
st.markdown("캐나다의 주요 관광지를 지도와 함께 쉽게 살펴보세요!")

# 사이드바에서 여행지 선택
place_names = list(places.keys())
selected_place = st.sidebar.selectbox("여행지를 선택하세요", place_names)

# 선택한 여행지 정보 표시
info = places[selected_place]
st.header(f"📍 {selected_place}")
st.image(info["image"], use_column_width=True)
st.write(info["description"])

# Folium 지도 생성
m = folium.Map(location=[56.1304, -106.3468], zoom_start=4)

# 마커 추가
for name, data in places.items():
    folium.Marker(
        location=data["location"],
        popup=f"<b>{name}</b><br>{data['description']}",
        tooltip=name,
    ).add_to(m)

# 지도 표시
st.subheader("🗺️ 위치 보기")
st_folium(m, width=800, height=500)
