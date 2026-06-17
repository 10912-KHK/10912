import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(page_title="우주 천체 맞히기 게임", page_icon="🔭")

# --- 게임 로직 함수 ---
def get_random_date():
    start_date = datetime(2010, 1, 1) # 너무 오래된 날짜는 화질이 낮아 2010년부터 설정
    end_date = datetime.now() - timedelta(days=1)
    days_between = (end_date - start_date).days
    random_days = random.randrange(days_between)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

@st.cache_data(show_spinner=False)
def fetch_quiz_data(date_str):
    api_key = "DEMO_KEY"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date_str}"
    try:
        res = requests.get(url, timeout=10).json()
        # 이미지가 아니거나 에러가 있으면 다시 시도하기 위해 None 반환
        if res.get("media_type") != "image":
            return None
        return res
    except:
        return None

def determine_answer(explanation, title):
    # 키워드 기반으로 정답 카테고리 분류
    text = (explanation + " " + title).lower()
    if "galaxy" in text: return "은하 (Galaxy)"
    if "nebula" in text: return "성운 (Nebula)"
    if "planet" in text or "mars" in text or "jupiter" in text or "saturn" in text: return "행성 (Planet)"
    if "star cluster" in text or "stars" in text: return "항성/성단 (Star)"
    if "moon" in text: return "위성/달 (Moon)"
    if "sun" in text: return "태양 (Sun)"
    return "기타 천체 (Comet, Asteroid, etc.)"

# --- 세션 상태 초기화 (게임 데이터 유지) ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
    st.session_state.score = 0
    st.session_state.answered = False

# --- UI 레이아웃 ---
st.title("🔭 우주 천체 맞히기 퀴즈")
st.write(f"현재 점수: **{st.session_state.score}**")

# 새로운 문제 불러오기 버튼
if st.button("새 문제 불러오기") or st.session_state.quiz_data is None:
    with st.spinner("우주에서 문제를 가져오는 중..."):
        while True: # 유효한 이미지 데이터를 얻을 때까지 반복
            date = get_random_date()
            data = fetch_quiz_data(date)
            if data:
                st.session_state.quiz_data = data
                st.session_state.correct_answer = determine_answer(data['explanation'], data['title'])
                st.session_state.answered = False
                break
    st.rerun()

# 문제 표시
if st.session_state.quiz_data:
    data = st.session_state.quiz_data
    
    st.image(data['url'], caption="이 천체는 무엇일까요?", use_container_width=True)

    # 보기 생성
    options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성/달 (Moon)", "태양 (Sun)", "기타 천체 (Comet, Asteroid, etc.)"]
    
    # 정답 선택 루프
    cols = st.columns(2)
    for i, option in enumerate(options):
        with cols[i % 2]:
            if st.button(option, disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if option == st.session_state.correct_answer:
                    st.success(f"정답입니다! 🎯\n\n**제목:** {data['title']}")
                    st.session_state.score += 10
                else:
                    st.error(f"아쉽네요! 정답은 **{st.session_state.correct_answer}** 입니다.")
                st.info(f"**설명:** {data['explanation'][:300]}...") # 설명 앞부분만 노출

# 게임 리셋
if st.sidebar.button("점수 초기화"):
    st.session_state.score = 0
    st.rerun()
