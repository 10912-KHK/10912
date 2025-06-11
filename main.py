import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 앱 제목 및 설명
st.set_page_config(page_title="10억년 뒤 우주 시뮬레이션", layout="centered")
st.title("🌌 10억 년 뒤 지구에서 본 우주의 모습")
st.markdown("""
이 앱은 **허블 법칙**을 바탕으로 10억 년 뒤, 지구에서 보이는 은하들의 위치를 극좌표로 시각화합니다.
""")

# 허블 상수 (km/s/Mpc)
H0 = 70

# 슬라이더로 미래 시점 설정 (1~100억 년)
years = st.slider("시뮬레이션 연도 (단위: 억 년)", 1, 100, 10)
delta_time_sec = years * 1e8 * 3.154e7  # 초로 환산

# 은하 목록 (이름: (방향 각도, 초기 거리 [Mpc]))
galaxies = {
    "안드로메다": (20, 30),
    "M81": (60, 50),
    "소용돌이 은하": (120, 40),
    "솜브레로 은하": (200, 35),
    "카트휠 은하": (310, 25),
}

# 시각화
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, polar=True)
ax.set_theta_direction(-1)
ax.set_theta_zero_location("N")
ax.set_title(f"{years}억 년 뒤 은하 위치 (극좌표 시각화)", pad=20)

for name, (angle_deg, distance_mpc) in galaxies.items():
    theta = np.deg2rad(angle_deg)
    velocity_km_s = H0 * distance_mpc * 1000  # 허블 속도
    delta_distance_km = velocity_km_s * delta_time_sec
    delta_distance_mpc = delta_distance_km / 3.086e19
    future_distance = distance_mpc + delta_distance_mpc

    # 현재 위치
    ax.plot(theta, distance_mpc, 'o', color='orange', label=f"{name} (현재)")
    # 미래 위치
    ax.plot(theta, future_distance, 'o', color='cyan', label=f"{name} (미래)")
    # 이동 선
    ax.plot([theta, theta], [distance_mpc, future_distance], linestyle='--', color='gray')

# 중복 제거된 범례
handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), loc='lower right', fontsize=8)

ax.set_rmax(150)
ax.set_rticks([20, 50, 100, 150])
ax.set_rlabel_position(225)

# 출력
st.pyplot(fig)

# 설명 추가
st.markdown(f"""
#### ℹ️ 설명
- 허블 상수: {H0} km/s/Mpc
- 미래 시점: {years}억 년
- 은하들은 우주 팽창에 따라 멀어집니다.
""")
