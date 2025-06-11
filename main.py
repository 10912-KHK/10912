import streamlit as st

st.set_page_config(page_title="10억 년 뒤 우주 시뮬레이션")
st.title("🌌 10억 년 뒤 우주의 모습 시뮬레이션")
st.markdown("""
이 시뮬레이션은 **허블의 법칙**을 기반으로 하여,  
미래에 은하들이 지구로부터 얼마나 멀어지는지를 계산합니다.

> 허블 상수 (H₀): `70 km/s/Mpc`  
> 시간: 1억 년 단위로 조절 가능  
> 거리 단위: Mpc (메가파섹) ≈ 326만 광년
""")

# --- 설정값 ---
H0 = 70  # km/s/Mpc
YEAR_SEC = 3.154e7  # 1년 = 초
PARSEC_KM = 3.086e13  # 1pc = km (주의: 여긴 kpc, Mpc 단위로 변환함)

# --- 시뮬레이션 시간 입력 ---
years = st.slider("미래 시간 설정 (억 년)", 1, 100, 10)
delta_time = years * 1e8 * YEAR_SEC  # 초

# --- 은하 데이터 (각도는 제외하고 이름 + 초기 거리만) ---
galaxies = {
    "안드로메다": 0.78,
    "M81": 3.6,
    "소용돌이 은하": 7,
    "솜브레로 은하": 9,
    "카트휠 은하": 12,
}

# --- 결과 테이블 ---
st.markdown(f"### 🧮 {years}억 년 뒤 예상 거리")

st.markdown("| 은하 | 현재 거리 (Mpc) | 예상 거리 (Mpc) | 이동 거리 (Mpc) |")
st.markdown("|------|------------------|------------------|------------------|")

for name, dist_mpc in galaxies.items():
    # 허블 법칙 → 속도 = H0 × 거리
    velocity_km_s = H0 * dist_mpc * 1000  # km/s
    moved_km = velocity_km_s * delta_time
    moved_mpc = moved_km / (1e6 * PARSEC_KM)  # km → Mpc
    future_distance = dist_mpc + moved_mpc

    st.markdown(f"| {name} | {dist_mpc:.2f} | {future_distance:.2f} | {moved_mpc:.2f} |")

st.markdown("""
---

🛰️ 이 계산은 단순한 허블 팽창 모델을 사용하므로, 실제 우주 진화는 **중력/암흑에너지** 등 복잡한 요인에 따라 달라질 수 있습니다.
""")
