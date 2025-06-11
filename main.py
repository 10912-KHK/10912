import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="10억 년 뒤 우주 시뮬레이션", layout="centered")
st.title("🌌 10억 년 뒤 지구에서 본 우주 시뮬레이션")
st.markdown("""
**허블 법칙**을 기반으로, 미래에 은하들이 어떻게 멀어지는지 2D 평면상에서 시각화합니다.  
(원형 확산 형태로 팽창하며, 방향은 고정된 채 거리만 증가합니다)
""")

# 설정
H0 = 70  # 허블 상수 (km/s/Mpc)
years = st.slider("시뮬레이션할 시간 (억 년 후)", 1, 100, 10)
delta_t_sec = years * 1e8 * 3.154e7

# 초기 은하 데이터: [이름, 각도(°), 거리(Mpc)]
galaxies = [
    ("안드로메다", 20, 30),
    ("M81", 60, 50),
    ("소용돌이 은하", 120, 40),
    ("솜브레로 은하", 200, 35),
    ("카트휠 은하", 310, 25),
]

# 좌표 계산
galaxy_data = []
for name, angle_deg, dist_mpc in galaxies:
    theta_rad = np.deg2rad(angle_deg)
    vx = H0 * dist_mpc * 1000  # 속도 (km/s)
    delta_km = vx * delta_t_sec
    delta_mpc = delta_km / 3.086e19
    new_dist = dist_mpc + delta_mpc

    x_now = dist_mpc * np.cos(theta_rad)
    y_now = dist_mpc * np.sin(theta_rad)
    x_future = new_dist * np.cos(theta_rad)
    y_future = new_dist * np.sin(theta_rad)

    galaxy_data.append((name, x_now, y_now, x_future, y_future))

# Plotly 시각화
fig = go.Figure()

for name, x0, y0, x1, y1 in galaxy_data:
    # 현재 위치
    fig.add_trace(go.Scatter(x=[x0], y=[y0], mode='markers+text',
                             name=f"{name} (현재)",
                             text=[name], textposition="top center",
                             marker=dict(color="orange", size=10)))
    # 미래 위치
    fig.add_trace(go.Scatter(x=[x1], y=[y1], mode='markers',
                             name=f"{name} (미래)",
                             marker=dict(color="cyan", size=10)))
    # 이동 방향선
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1],
                             mode='lines',
                             line=dict(color='gray', dash='dash'),
                             showlegend=False))

# 그래프 설정
fig.update_layout(
    title=f"{years}억 년 후 우주의 은하 위치 변화 (허블 팽창 시뮬레이션)",
    xaxis_title="X (Mpc)",
    yaxis_title="Y (Mpc)",
    width=700,
    height=700,
    showlegend=True,
    template="plotly_dark",
    margin=dict(l=40, r=40, t=60, b=40),
)

st.plotly_chart(fig)

st.markdown(f"""
---
#### 📌 참고:
- 허블 상수: **{H0} km/s/Mpc**
- 시뮬레이션 시간: **{years}억 년** → 약 {int(delta_t_sec):,}초
- 거리 단위: Mpc (메가파섹, 약 326만 광년)
""")
