import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ------------------------
# 기본 설정
# ------------------------

st.set_page_config(page_title="10억년 뒤 우주 시뮬레이션", layout="centered")
st.title("🌌 지구에서 본 10억년 뒤 우주의 은하 위치 시뮬레이션")

st.markdown("""
이 앱은 허블 법칙을 이용해 **우주 팽창**이 은하의 위치에 어떤 영향을 주는지 보여줍니다.  
**극좌표 그래프**에서 각 은하의 방향은 고정되고, 거리는 시간에 따라 멀어집니다.
""")

# ------------------------
# 사용자 입력
# ------------------------

years = st.slider("시뮬레이션할 미래 시점 (억 년)", min_value=1, max_value=100, value=10, step=1)
delta_time_sec = years * 1e8 * 3.154e7  # 초

# 허블 상수 (km/s/Mpc)
H0 = 70

# 은하 정보 (방향 각도, 초기 거리 Mpc)
galaxies = {
    "Andromeda": (20, 30),
    "Messier 81": (60, 50),
    "Whirlpool": (120, 40),
    "Sombrero": (200, 35),
    "Cartwheel": (310, 25),
}

# ------------------------
# 시뮬레이션 및 시각화
# ------------------------

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, polar=True)
ax.set_theta_direction(-1)
ax.set_theta_zero_location("N")
ax.set_title(f"지구에서 본 {years}억 년 뒤 우주 (극좌표)", pad=20)

for name, (angle_deg, distance_mpc) in galaxies.items():
    theta_rad = np.deg2rad(angle_deg)

    # 이동 거리 계산 (허블 법칙 v = H0 * d)
    v_km_s = H0 * distance_mpc * 1000
    delta_d_km = v_km_s * delta_time_sec
    delta_d_mpc = delta_d_km / 3.086e19  # km → Mpc

    future_distance = distance_mpc + delta_d_mpc

    # 현재 위치
    ax.plot(theta_rad, distance_mpc, 'o', color='orange', label=f"{name} (현재)")
    # 미래 위치
    ax.plot(theta_rad, future_distance, 'o', color='cyan', label=f"{name} (미래)")
    # 선 연결
    ax.plot([theta_rad, theta_rad], [distance_mpc, future_distance], color='gray', linestyle='--')

# 범례 최적화
handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
ax.legend(unique_labels.values(), unique_labels.keys(), loc="lower right", fontsize=8)

ax.set_rmax(150)
ax.set_rticks([20, 50, 100, 150])
ax.set_rlabel_position(225)

st.pyplot(fig)

# ------------------------
# 부가 설명
# ------------------------

st.markdown(f"""
#### 🔭 요약:
- **허블 상수**: {H0} km/s/Mpc
- **시뮬레이션 시간**: {years}억 년 = {int(delta_time_sec):,}초
- **멀어지는 거리**는 허블 법칙을 바탕으로 계산됩니다.

> 실제 시뮬레이션은 단순화를 위해 2D와 선형 모델로 작성되었습니다.  
> 정밀 우주 모델은 일반상대성이론, 암흑에너지 등을 고려해야 합니다.
""")
