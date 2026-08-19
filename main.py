import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# --- 설정 및 상수 ---
st.set_page_config(page_title="심우주 퀴즈 마스터", page_icon="🌌", layout="centered")

MAX_ROUNDS = 5
# NASA API DEMO_KEY는 시간당 요청 제한이 있으므로, 한 번에 여러 개를 가져오는 방식을 사용합니다.
API_URL = "https://api.nasa.gov/planetary/apod"
API_KEY = "DEMO_KEY" 

# 천체가 아닌 것들을 걸러내기 위한 키워드
BAD_WORDS = ["earth", "rocket", "shuttle", "station", "iss", "astronaut", "rover", "telescope", "observatory", "person", "launch"]
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]
EXPERT_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "V838 Mon", "Pillars of Creation", "Sombrero Galaxy", "Horsehead Nebula", "M101", "NGC 6960", "M31 Andromeda"]

# --- 핵심 로직: 문제 은행 만들기 ---

def fetch_questions():
    """NASA에서 한 번에 20~30개의 데이터를 가져와서 필터링 후 저장"""
    try:
        # count=30을 쓰면 랜덤하게 30장을 한 번에 가져옵니다 (API 호출 횟수 절약)
        params = {"api_key": API_KEY, "count": 30}
        res = requests.get(API_URL, params=params, timeout=10).json()
        
        valid_data = []
        for item in res:
            if item.get("media_type") == "image":
                title = item.get("title", "").lower()
                expl = item.get("explanation", "").lower()
                
                # 지구 사진이나 인공물 제외 필터링
                if any(bad in title or bad in expl for bad in BAD_WORDS):
                    continue
                
                valid_data.append(item)
        
        return valid_data
    except Exception as e:
        st.error(f"데이터를 가져오는데 오류가 발생했습니다: {e}")
        return []

# --- 세션 상태 관리 ---
if 'game_pool' not in st.session_state:
    st.session_state.game_pool = [] # 문제 은행
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.game_over = False

def determine_category(text):
    text = text.lower()
    if "galaxy" in text: return "은하 (Galaxy)"
    if "nebula" in text: return "성운 (Nebula)"
    if "planet" in text: return "행성 (Planet)"
    if "star" in text: return "항성/성단 (Star)"
    if "moon" in text: return "위성 (Moon)"
    if "sun" in text: return "태양 (Sun)"
    return "기타 (Comet/Asteroid)"

def restart_game():
    st.session_state.game_pool = []
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.game_over = False

# --- UI 레이아웃 ---
st.title("🌌 심우주 천체 맞히기 챌린지")

# 1. 문제 은행이 비어있으면 채우기
if not st.session_state.game_over and not st.session_state.game_pool:
    with st.spinner("우주 깊은 곳에서 사진을 가져오고 있습니다..."):
        new_questions = fetch_questions()
        if new_questions:
            st.session_state.game_pool = new_questions
        else:
            st.warning("NASA 서버 연결이 불안정합니다. 잠시 후 다시 시도해주세요.")
            if st.button("다시 시도"):
                st.rerun()
            st.stop()

# 2. 게임 진행 화면
if not st.session_state.game_over:
    st.write(f"**문제: {st.session_state.round} / {MAX_ROUNDS}**")
    st.progress(st.session_state.round / MAX_ROUNDS)

    # 현재 문제 데이터 추출
    current_data = st.session_state.game_pool[0]
    
    st.image(current_data['url'], use_container_width=True)

    # 난이도별 설정
    correct_ans = ""
    options = []

    if st.session_state.round <= 2:
        st.info("Level: 입문 - 천체의 종류를 맞히세요.")
        correct_ans = determine_category(current_data['explanation'] + current_data['title'])
        options = CATEGORIES
    else:
        st.warning(f"Level: {'전문가' if st.session_state.round == 5 else '숙련'} - 천체의 이름을 맞히세요.")
        correct_ans = current_data['title']
        # 가짜 보기 3개 + 정답 1개
        options = random.sample(EXPERT_NAMES, 3) + [correct_ans]
        random.shuffle(options)

    # 정답 버튼 UI
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{st.session_state.round}_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct_ans:
                    st.balloons()
                    st.success("정답입니다! 🎯")
                    st.session_state.score += (st.session_state.round * 20)
                else:
                    st.error(f"틀렸습니다! 정답은: **{correct_ans}**")
                
                with st.expander("천체 설명 보기"):
                    st.write(current_data['explanation'])

    if st.session_state.answered:
        if st.button("다음 라운드로 🚀"):
            # 다음 라운드 준비: 현재 문제 제거
            st.session_state.game_pool.pop(0)
            st.session_state.answered = False
            st.session_state.round += 1
            if st.session_state.round > MAX_ROUNDS:
                st.session_state.game_over = True
            st.rerun()

else:
    # 최종 결과 화면
    st.balloons()
    st.header("🏁 챌린지 종료!")
    st.subheader(f"최종 점수: {st.session_state.score}점")
    
    if st.session_state.score >= 200: grade = "🌌 우주 마스터"
    elif st.session_state.score >= 100: grade = "🔭 우주 탐험가"
    else: grade = "🚀 우주 꿈나무"
    
    st.info(f"당신의 등급: **{grade}**")
    
    if st.button("새 게임 시작하기"):
        restart_game()
        st.rerun()

with st.sidebar:
    st.write(f"현재 점수: {st.session_state.score}")
    if st.button("전체 초기화"):
        restart_game()
        st.rerun()
