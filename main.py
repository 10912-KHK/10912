import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# --- 설정 및 상수 ---
st.set_page_config(page_title="심우주 천체 맞히기 챌린지", page_icon="🌌", layout="centered")

MAX_ROUNDS = 5
API_KEY = "DEMO_KEY"

# 필터링 키워드 (천체가 아닌 것들 제외)
FORBIDDEN_KEYWORDS = ["earth", "launch", "rocket", "shuttle", "station", "iss", "astronaut", "rover", "landing", "telescope", "observatory", "person"]

# 천체 카테고리 (쉬운 단계용)
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]

# 전문가용 가짜 명칭 (심화 문제용)
EXPERT_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "V838 Mon", "Pillars of Creation", "Sombrero Galaxy", "Horsehead Nebula", "M101", "NGC 6960"]

# --- 로직 함수 ---

def get_unique_random_date():
    """중복되지 않는 날짜 생성"""
    while True:
        start_date = datetime(2010, 1, 1)
        end_date = datetime.now() - timedelta(days=1)
        days_between = (end_date - start_date).days
        random_days = random.randrange(days_between)
        date_str = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        if date_str not in st.session_state.used_dates:
            return date_str

def fetch_deep_space_data():
    """우주 천체만 필터링해서 가져오기"""
    attempts = 0
    while attempts < 15:  # 최대 15번 시도해서 천체 사진 찾기
        date = get_unique_random_date()
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date}"
        try:
            res = requests.get(url, timeout=5).json()
            if res.get("media_type") == "image":
                title = res.get("title", "").lower()
                explanation = res.get("explanation", "").lower()
                
                # 지구, 인공물 필터링
                if any(word in title or word in explanation for word in FORBIDDEN_KEYWORDS):
                    continue
                
                # 최소한의 천체 키워드가 있는지 확인
                if any(word in title or word in explanation for word in ["galaxy", "nebula", "star", "planet", "cluster", "comet", "sun", "moon"]):
                    st.session_state.used_dates.append(date)
                    return res
        except:
            pass
        attempts += 1
    return None

def determine_category(text):
    text = text.lower()
    if "galaxy" in text: return "은하 (Galaxy)"
    if "nebula" in text: return "성운 (Nebula)"
    if "planet" in text: return "행성 (Planet)"
    if "star" in text: return "항성/성단 (Star)"
    if "moon" in text: return "위성 (Moon)"
    if "sun" in text: return "태양 (Sun)"
    return "기타 (Comet/Asteroid)"

# --- 세션 상태 초기화 ---
if 'round' not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.quiz_data = None
    st.session_state.answered = False
    st.session_state.game_over = False
    st.session_state.used_dates = []

def next_question():
    if st.session_state.round >= MAX_ROUNDS:
        st.session_state.game_over = True
    else:
        st.session_state.round += 1
        st.session_state.quiz_data = None
        st.session_state.answered = False

def restart_game():
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.quiz_data = None
    st.session_state.answered = False
    st.session_state.game_over = False
    st.session_state.used_dates = []

# --- UI 레이아웃 ---
st.title("🌌 심우주 천체 맞히기 챌린지")

if not st.session_state.game_over:
    st.write(f"**진행도: {st.session_state.round} / {MAX_ROUNDS}**")
    st.progress(st.session_state.round / MAX_ROUNDS)

    # 데이터 로딩
    if st.session_state.quiz_data is None:
        with st.spinner("광활한 우주에서 천체를 찾는 중..."):
            data = fetch_deep_space_data()
            if data:
                st.session_state.quiz_data = data
            else:
                st.error("우주 데이터를 가져오는데 실패했습니다. 다시 시도해주세요.")
                st.stop()

    data = st.session_state.quiz_data
    st.image(data['url'], caption="이 우주 천체는 무엇일까요?", use_container_width=True)

    # 정답 설정 및 난이도 조절
    correct_ans = ""
    options = []

    if st.session_state.round <= 2:
        # 1-2단계: 종류 맞히기 (쉬움)
        st.info("Level: 입문 - 천체의 종류를 맞히세요.")
        correct_ans = determine_category(data['explanation'] + data['title'])
        options = CATEGORIES
    elif st.session_state.round <= 4:
        # 3-4단계: 실제 이름 찾기 (중간)
        st.info("Level: 숙련 - 이 천체의 이름을 맞히세요.")
        correct_ans = data['title']
        options = random.sample(EXPERT_NAMES, 3) + [correct_ans]
        random.shuffle(options)
    else:
        # 5단계: 전문가 난이도 (어려움)
        st.warning("Level: 전문가 - 매우 구체적인 명칭을 고르세요.")
        correct_ans = data['title']
        # 전문적인 느낌의 보기들 섞기
        options = random.sample(EXPERT_NAMES, 3) + [correct_ans]
        random.shuffle(options)

    # 퀴즈 UI
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct_ans:
                    st.success(f"정답입니다! 🎉")
                    st.session_state.score += (st.session_state.round * 20)
                else:
                    st.error(f"틀렸습니다! 정답은: **{correct_ans}**")
                
                with st.expander("천체 정보 상세보기"):
                    st.write(data['explanation'])

    if st.session_state.answered:
        if st.button("다음 라운드로 넘어가기 🚀"):
            next_question()
            st.rerun()

else:
    # 최종 결과 화면
    st.balloons()
    st.header("🏁 챌린지 종료!")
    st.subheader(f"당신의 최종 점수: {st.session_state.score}점")
    
    # 등급 매기기
    if st.session_state.score >= 250:
        grade = "우주 마스터 (Cosmic Master)"
    elif st.session_state.score >= 150:
        grade = "천문학 학사 (Astronomy Major)"
    else:
        grade = "우주 여행자 (Space Traveler)"
    
    st.info(f"등급: **{grade}**")
    
    if st.button("새 게임 시작하기"):
        restart_game()
        st.rerun()

# 사이드바 정보
with st.sidebar:
    st.title("Game Info")
    st.write(f"현재 점수: {st.session_state.score}")
    st.write("---")
    st.write("NASA의 오늘의 천체 사진(APOD) 데이터를 사용하여 매번 새로운 문제를 생성합니다.")
    if st.button("데이터 초기화"):
        restart_game()
        st.rerun()
