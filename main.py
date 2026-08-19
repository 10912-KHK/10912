import streamlit as st
import random
import time

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="Sol d 생존 시뮬레이터", page_icon="🚀", layout="centered")

# --- 2. 게임 데이터 (이벤트 및 시나리오) ---
EVENTS = [
    {
        "title": "☄️ 소행성 지대 발견",
        "description": "선체 레이더에 거대한 소행성 군락이 감지되었습니다. 어떻게 하시겠습니까?",
        "options": {
            "공격적으로 돌파한다 (연료 소모↑, 시간 단축)": {"fuel": -20, "hull": -10, "dist": 500, "msg": "소행성 파편에 부딪혔지만 빠르게 통과했습니다!"},
            "조심스럽게 우회한다 (연료 소모↓, 시간 지연)": {"fuel": -10, "hull": 0, "dist": 200, "msg": "시간은 걸렸지만 안전하게 우회했습니다."},
            "소행성에서 자원을 채굴한다": {"fuel": 5, "hull": -20, "dist": 50, "msg": "자원을 얻었지만 채굴 중 선체가 손상되었습니다."}
        }
    },
    {
        "title": "🛸 정체불명의 신호",
        "description": "근처 Abell-2744 좌표 방향에서 정체불명의 무선 신호가 들려옵니다.",
        "options": {
            "신호를 추적하여 접근한다": {"fuel": -15, "hull": 10, "dist": 100, "msg": "버려진 탐사선을 발견해 선체를 수리했습니다!"},
            "무시하고 항로를 유지한다": {"fuel": 0, "hull": 0, "dist": 300, "msg": "안전이 제일입니다. 항로를 유지합니다."},
            "교신을 시도한다": {"fuel": -5, "hull": -5, "dist": 50, "msg": "강한 전자기파 공격을 받아 시스템이 일시 마비되었습니다."}
        }
    },
    {
        "title": "🌀 우주 폭풍 (Solar Flare)",
        "description": "Sol(태양)에서 강력한 플레어가 발생했습니다. 방사선 수치가 급증합니다!",
        "options": {
            "방어막에 모든 에너지를 집중한다": {"fuel": -30, "hull": 0, "dist": 100, "msg": "연료를 많이 썼지만 선체는 멀쩡합니다."},
            "행성 뒤로 숨는다": {"fuel": -10, "hull": -10, "dist": 50, "msg": "완벽히 숨지 못해 약간의 피해를 입었습니다."},
            "엔진을 과부하시켜 구역을 이탈한다": {"fuel": -20, "hull": -20, "dist": 600, "msg": "엄청난 속도로 도망쳤지만 선체에 무리가 갔습니다."}
        }
    }
]

# --- 3. 세션 상태 초기화 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'fuel': 100,
        'hull': 100,
        'distance': 0,
        'log': ["항해를 시작합니다. 목표는 Sol d 시스템 이탈입니다."],
        'turn': 0
    })

# --- 4. 게임 로직 함수 ---
def reset_game():
    st.session_state.update({
        'game_state': "PLAYING",
        'fuel': 100,
        'hull': 100,
        'distance': 0,
        'log': ["Sol d(지구) 궤도를 떠나 심우주로 향합니다."],
        'turn': 1
    })

def process_choice(effect, msg):
    st.session_state.fuel += effect.get("fuel", 0)
    st.session_state.hull += effect.get("hull", 0)
    st.session_state.distance += effect.get("dist", 0)
    st.session_state.log.insert(0, f"Round {st.session_state.turn}: {msg}")
    st.session_state.turn += 1
    
    # 패배 조건 체크
    if st.session_state.fuel <= 0 or st.session_state.hull <= 0:
        st.session_state.game_state = "GAMEOVER"
    # 승리 조건 체크 (예: 2000km 이동)
    elif st.session_state.distance >= 2000:
        st.session_state.game_state = "VICTORY"

# --- 5. UI 화면 구성 ---

# [메인 타이틀]
st.title("🚀 Sol d: Galactic Survivor")
st.write(f"**현재 위치:** Sol d(지구)로부터 {st.session_state.distance} 광년 이탈 중")

# [상태바 표시]
col1, col2, col3 = st.columns(3)
col1.metric("⛽ 연료", f"{st.session_state.fuel}%")
col2.metric("🛠 선체 내구도", f"{st.session_state.hull}%")
col3.metric("📅 항해 일수", f"{st.session_state.turn}일")

st.write("---")

# [화면 전환 로직]
if st.session_state.game_state == "START":
    st.subheader("인류의 모성, Sol d를 떠나 심우주로...")
    st.write("당신은 탐사선 '테라(Terra)'호의 함장입니다. 자원이 바닥나기 전에 가능한 멀리 우주를 탐사하십시오.")
    if st.button("엔진 점화 (게임 시작)", use_container_width=True):
        reset_game()
        st.rerun()

elif st.session_state.game_state == "PLAYING":
    # 랜덤 이벤트 발생
    event = random.choice(EVENTS)
    st.subheader(event['title'])
    st.write(event['description'])
    
    st.write("---")
    st.write("**어떤 조치를 취하시겠습니까?**")
    
    # 선택지 버튼 생성
    for option_text, effect in event['options'].items():
        if st.button(option_text, use_container_width=True):
            process_choice(effect, effect['msg'])
            st.rerun()

    # 항해 일지 (최근 3개만)
    st.write("---")
    st.write("**📋 항해 일지**")
    for l in st.session_state.log[:3]:
        st.write(f"- {l}")

elif st.session_state.game_state == "GAMEOVER":
    st.error("🚨 임무 실패! 🚨")
    if st.session_state.fuel <= 0:
        st.write("연료가 바닥나 우주 미아가 되었습니다...")
    else:
        st.write("선체가 파괴되어 우주의 먼지가 되었습니다...")
    
    st.write(f"최종 탐사 거리: {st.session_state.distance} 광년")
    if st.button("새로운 기체로 재시작", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()

elif st.session_state.game_state == "VICTORY":
    st.balloons()
    st.success("🎉 임무 성공! 🎉")
    st.write("인류 최초로 Sol d 시스템을 완벽히 벗어나 Abell-2744 경계에 도달했습니다!")
    st.write(f"최종 항해 일수: {st.session_state.turn}일")
    if st.button("새로운 항로 탐사 (다시 하기)", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()
