import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np

st.set_page_config(layout="wide")
st.title("🪐 10억 년 뒤 우주의 모습: 은하 팽창 시뮬레이션")

# 허블 상수 (간단히 사용)
H0 = 70  # km/s/Mpc

# 10억 년을 초 단위로
years = st.slider("미래 시점 (단위: 억 년)", 0, 100, 10)
delta_time_sec = years * 1e8 * 3.154e7  # 초

st.write(f"🕒 시뮬레이션 시점: {years}억 년 뒤")

# 가상의 은하 초기 위치들 (위도/경도처럼 단순 좌표계에 배치)
galaxies = {
    "Andromeda": [51.0, -114.0],
    "Messier 81": [48.5, -123.0],
    "Whirlpool": [52.0, -117.0],
    "Sombrero": [50.0, -122.0],
    "Cartwheel": [49.0, -115.5],
}

# 지도 중심
m = folium.Map(location=[50, -120], zoom_start=5, tiles="cartodb dark_matter")

# 은하 위치 계산 및 표시
for name, (lat, lon) in galaxies.items():
    # 초기 거리 (임의 단위, Mpc)
    initial_distance = np.sqrt((lat - 50)**2 + (lon + 120)**2)

    # 허블 법칙으로 거리 증가량 계산
    # v = H0 * d → Δd = v * t
    velocity = H0 * initial_distance * 1000  # km/s
    delta_d_km = velocity * delta_time_sec  # km
    delta_deg = delta_d_km / 1e9  # 간단하게 스케일 맞추기 (지도 좌표용)

    # 은하 이동 (단순하게 오른쪽 위로 밀어냄)
    new_lat = lat + delta_deg * 0.01
    new_lon = lon + delta_deg * 0.01

    folium.CircleMarker(
        location=[new_lat, new_lon],
        radius=6,
        color="cyan",
        fill=True,
        fill_opacity=0.7,
        popup=f"{name} (거리 증가: {int(delta_d_km/1e6):,} million km)"
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=900, height=600)

   
