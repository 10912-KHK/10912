import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np

# ------------------------
# 시뮬레이션 기본 설정
# ------------------------

H0 = 70  # 허블 상수 (km/s/Mpc)
G_MAP_CENTER = [50.0, -120.0]  # 지도 중심

# 은하 초기 위치 데이터 (위도, 경도)
galaxies = {
    "Andromeda": [51.0, -114.0],
    "Messier 81": [48.5, -123.0],
    "Whirlpool": [52.0, -117.0],
    "Sombrero": [50.0, -122.0],
    "Cartwheel": [49.0, -115.5],
}

# ------------------------
# Streamlit UI
# ------------------------

st.set_page_config(layout="wide")
st.title("🪐 10억 년 뒤 우주의 은하 이동 시뮬레이션")

years = st.slider("미래 시점 (단위: 억 년)", min_value=1, max_value=100, value=10, step=1)
delta_time_sec = years * 1e8 * 3.154e7  # 억 년을 초로 변환

st.markdown(f"**🕒 시점:** {years}억 년 뒤 &nbsp;&nbsp;&nbsp;🧮 시뮬레이션 시간: {int(delta_time_sec):,}초")

# ------------------------
# 지도 생성
# ------------------------

m = folium.Map(location=G_MAP_CENTER, zoom_start=5, tiles="cartodb dark_matter")

for name, (lat, lon) in galaxies.items():
    # 현재 위치 기준 거리 (단순 유클리드 거리)
    d_lat = lat - G_MAP_CENTER[0]
    d_lon = lon - G_MAP_CENTER[1]
    initial_distance = np.sqrt(d_lat**2 + d_lon**2)

    # 허블 법칙: v = H0 * d
    velocity_km_s = H0 * initial_distance * 1000  # km/s
    delta_d_km = velocity_km_s * delta_time_sec  # 총 거리 이동 (km)
    delta_deg = delta_d_km / 1e9  # 위도/경도로 변환하는 단순 스케일

    # 방향 벡터 계산
    if initial_distance == 0:
        dir_lat = 0
        dir_lon = 0
    else:
        dir_lat = d_lat / initial_distance
        dir_lon = d_lon / initial_distance

    # 새로운 위치 계산
    new_lat = lat + delta_deg * dir_lat * 0.2
    new_lon = lon + delta_deg * dir_lon * 0.2

    # 시각화
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        color="orange",
        fill=True,
        fill_opacity=0.6,
        popup=f"{name} (현재 위치)"
    ).add_to(m)

    folium.CircleMarker(
        location=[new_lat, new_lon],
        radius=7,
        color="cyan",
        fill=True,
        fill_opacity=0.9,
        popup=f"{name} (미래 위치)\n이동 거리: {int(delta_d_km / 1e6):,}M km"
    ).add_to(m)

    folium.PolyLine(
        locations=[[lat, lon], [new_lat, new_lon]],
        color="white",
        weight=1.5,
        opacity=0.6,
        tooltip=f"{name} 이동 방향"
    ).add_to(m)

# ------------------------
# Streamlit에 지도 출력
# ------------------------

st_data = st_folium(m, width=1000, height=600)


   
