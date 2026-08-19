import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# --- 설정 및 상수 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈 마스터", page_icon="🚀", layout="centered")

MAX_ROUNDS = 5
API_KEY = "DEMO_KEY" # 실제 운영시에는 NASA API KEY 발급 권장

# 천체 카테고리 (쉬운 단계용)
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성/달 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]

# 전문가용 가짜 이름들 (5단계 난이도용)
FAKE_NAMES = ["NGC 1234", "Messier 87", "Kepler-186f", "HD 189733b", "V838 Monocerotis", "Sagittarius A*", "Pillars of Creation", "IC 1101", "Abell 2744"]

# --- 로직 함수 ---

def get_random_date():
    start_date = datetime(2015, 1, 1)
    end_date = datetime.now() - timedelta(days=1)
    days_between = (end_date - start_date).days
    random_days = random.randrange(days_between)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

@st.cache_data(show_spinner=False)
def fetch_quiz_data(date_str):
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date_str}"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("media_type") == "image":
            return res
        return None
    except:
        return None

def determine_category(text):
    text = text.lower()
    if "galaxy" in text: return "은하 (Galaxy)"
    if "nebula" in text: return "성운 (Nebula)"
    if "planet" in text or "mars" in text or "jupiter" in text or "saturn" in text: return "행성 (Planet)"
    if "star cluster" in text or "stars" in text: return "항성/성단 (Star)"
    if "moon" in text: return "위성/달 (Moon)"
    if "sun" in text: return "태양 (Sun)"
    return "기타 (Comet/Asteroid)"

# --- 세션 상태 관리 ---
if 'round' not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.quiz_data = None
    st.session_state.answered = False
    st.session_state.game_over = False

def next_question():
    st.session_state.round += 1
    st.session_state.quiz_data = None
    st.session_state.answered = False
    if st.session_state.round > MAX_ROUNDS:
        st.session_state.game_over = True

def restart_game():
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.quiz_data = None
    st.session_state.answered = False
    st.session_state.game_over = False

# --- UI 레이아웃 ---
st.title("🚀 슈퍼 우주 퀴즈 마스터")

if not st.session_state.game_over:
    # 진행도 표시
    st.progress(st.session_state.round / MAX_ROUNDS)
    st.subheader(f"라운드 {st.session_state.round} / {MAX_ROUNDS}")

    # 문제 로딩
    if st.session_state.quiz_data is None:
        with st.spinner("우주에서 문제를 가져오는 중..."):
            while True:
                data = fetch_quiz_data(get_random_date())
                if data:
                    st.session_state.quiz_data = data
                    break

    data = st.session_state.quiz_data
    st.image(data['url'], use_container_width=True)

    # 난이도별 문제 구성
    correct_ans = ""
    options = []

    if st.session_state.round <= 2:
        st.write("### [Lv.1] 이 천체는 어떤 종류인가요?")
        correct_ans = determine_category(data['explanation'] + data['title'])
        options = CATEGORIES
    elif st.session_state.round <= 4:
        st.write("### [Lv.2] 이 천체의 구체적인 이름은 무엇일까요?")
        correct_ans = data['title']
        # 가짜 보기 생성
        options = random.sample(FAKE_NAMES, 3) + [correct_ans]
        random.shuffle(options)
    else:
        st.write("### [Lv.MAX] 전문가 난이도! 이 천체의 공식 명칭은?")
        correct_ans = data['title']
        options = random.sample(FAKE_NAMES, 3) + [correct_ans]
        random.shuffle(options)

    # 정답 버튼
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct_ans:
                    st.balloons()
                    st.success(f"정답입니다! +{st.session_state.round * 10}점")
                    st.session_state.score += st.session_state.round * 10
                else:
                    st.error(f"오답입니다! 정답은: {correct_ans}")
                
                st.info(f"**🔭 천체 설명:** {data['explanation'][:500]}...")

    if st.session_state.answered:
        if st.button("다음 문제로 ➡️"):
            next_question()
            st.rerun()

else:
    # 게임 종료 화면
    st.balloons()
    st.header("🎊 게임 종료!")
    st.subheader(f"최종 점수: {st.session_state.score}점")
    
    # 점수별 등급
    grade = ""
    if st.session_state.score >= 120: grade = "🌌 우주의 지배자"
    elif st.session_state.score >= 80: grade = "👨‍🚀 베테랑 우주 비행사"
    elif st.session_state.score >= 40: grade = "🔭 아마추어 천문가"
    else: grade = "👶 우주 아기"
    
    st.write(f"당신의 우주 등급은: **{grade}** 입니다!")
    
    if st.button("다시 도전하기"):
        restart_game()
        st.rerun()

# 사이드바
with st.sidebar:
    st.header("설정")
    st.write(f"현재 점수: {st.session_state.score}")
    if st.button("게임 리셋"):
        restart_game()
        st.rerun()
