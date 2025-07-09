import streamlit as st
import math

st.set_page_config(page_title="10억 년 뒤 우주 시뮬레이션", layout="centered")

# 타이틀
st.title("🌌 1억 년 뒤 우주의 모습 시뮬레이션")
st.caption("허블 팽창 모델 기반 텍스트 시뮬레이션 + 이미지")

# 배경 이미지
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/0/0f/NASA-HubbleDeepField.800px.jpg",
    caption="허블 딥 필드 (NASA)",
    use_column_width=True
)

st.markdown("""
우주는 계속 팽창하고 있으며, 멀리 있는 은하일수록 더 빠르게 멀어집니다.  
이 시뮬레이션은 은하들이 **10억 년 뒤 어디쯤 위치할지** 예측해봅니다.

**가정**
- 허블 상수 H₀ = 70 km/s/Mpc
- 방향은 유지하고 거리만 변화
""")

# 사용자 입력
years = st.slider("미래 시간 설정 (억 년)", 1, 100, 10)
seconds = years * 1e8 * 3.154e7
H0 = 70  # 허블 상수
KM_PER_MPC = 3.086e19

# 은하 좌표 (3차원)
galaxies = [
    ("안드로메다", 0.5, 0.3, 0.1),
    ("M81", 1.2, -0.5, 0.8),
    ("소용돌이 은하", -1.0, 1.5, -0.3),
    ("솜브레로 은하", -2.0, -1.0, 1.0),
    ("카트휠 은하", 1.5, 2.0, -1.2),
]

# 테이블 출력
st.subheader(f"📡 {years}억 년 뒤 은하 거리 변화")
st.markdown("| 은하 | 현재 거리 (Mpc) | 예상 거리 (Mpc) | Δ거리 (Mpc) |")
st.markdown("|------|------------------|------------------|------------------|")

for name, x, y, z in galaxies:
    r0 = math.sqrt(x**2 + y**2 + z**2)
    v_kms = H0 * r0 * 1000
    delta_km = v_kms * seconds
    delta_mpc = delta_km / KM_PER_MPC
    r1 = r0 + delta_mpc

    st.markdown(f"| {name} | {r0:.2f} | {r1:.2f} | {delta_mpc:.2f} |")

st.markdown("---")
st.info("※ 실제 우주는 암흑에너지, 중력, 다중 구조 등 다양한 요인으로 더 복잡합니다.")
