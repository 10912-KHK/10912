import streamlit as st
import math

st.set_page_config(page_title="10억 년 뒤 우주 3D 시뮬레이션")
st.title("🌌 10억 년 뒤 은하의 3차원 위치 변화 (텍스트 기반)")

st.markdown("""
**허블의 법칙**과 초기 3차원 좌표를 기반으로,  
우주의 팽창에 따라 은하들의 위치가 어떻게 변하는지 계산합니다.

> - 단위: Mpc (메가파섹)
> - 허블 상수: 70 km/s/Mpc  
> - 3차원 공간: X, Y, Z 좌표 사용
""")

# 사용자 입력
years = st.slider("시뮬레이션할 시간 (억 년)", 1, 100, 10)
seconds = years * 1e8 * 3.154e7
H0 = 70  # km/s/Mpc
KM_PER_MPC = 3.086e19

# 은하 초기 위치 (이름, x, y, z in Mpc)
galaxies = [
    ("안드로메다", 0.5, 0.3, 0.1),
    ("M81", 1.2, -0.5, 0.8),
    ("소용돌이 은하", -1.0, 1.5, -0.3),
    ("솜브레로 은하", -2.0, -1.0, 1.0),
    ("카트휠 은하", 1.5, 2.0, -1.2),
]

# 결과 테이블 헤더
st.markdown("| 은하 | 초기 거리 (Mpc) | 미래 거리 (Mpc) | Δ거리 (Mpc) |")
st.markdown("|------|------------------|------------------|------------------|")

for name, x, y, z in galaxies:
    r0 = math.sqrt(x**2 + y**2 + z**2)
    v_kms = H0 * r0 * 1000
    delta_km = v_kms * seconds
    delta_mpc = delta_km / KM_PER_MPC
    r1 = r0 + delta_mpc

    st.markdown(f"| {name} | {r0:.2f} | {r1:.2f} | {delta_mpc:.2f} |")

st.markdown("---")
st.info("이 시뮬레이션은 거리만 변하고, 방향(벡터)은 유지된다는 단순화된 가정을 따릅니다.")

