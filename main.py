import streamlit as st
import requests
import random

# --- 설정 ---
st.set_page_config(page_title="우주 천체 퀴즈", page_icon="🌌")

API_KEY = "DEMO_KEY"
# 지구나 인공물을 거르기 위한 키워드
BAD_WORDS = ["earth", "rocket", "shuttle", "station", "iss", "astronaut", "rover", "telescope", "launch", "person"]
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]
EXPERT_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "V838 Mon", "Pillars of Creation", "Sombrero Galaxy", "M101", "NGC 6960"]

# --- 세션 상태 초기화 ---
if 'quiz_pool' not in st.session_state:
    st.session_state.quiz_pool = []  # 5개의 사진 데이터가 들어갈 곳
    st.session_state.score = 0
    st.session_state.round = 0       # 0~4 인덱스
    st.session_state.answered = False

# --- 데이터 가져오기 함수 ---
def prepare_game():
    with st.spinner("우주에서 사진 5장을 엄선하고 있습니다..."):
        pool = []
        # 필터링을 고려해 20개를 먼저 가져온 뒤 조건에 맞는 5개만 선택
        try:
            res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=20").json()
            for item in res:
                if item.get("media_type") == "image":
                    title = item.get("title", "").lower()
                    # 지구, 인공물 제외
                    if not any(bad in title for bad in BAD_WORDS):
                        pool.append(item)
                if len(pool) == 5: break # 5개 다 채우면 중단
            
            st.session_state.quiz_pool = pool
            st.session_state.round = 0
            st.session_state.score = 0
            st.session_state.answered = False
        except:
            st.error("데이터 로딩 실패! 다시 시작해 주세요.")

# --- 게임 화면 구성 ---
st.title("🌌 우주 천체 맞히기 챌린지 (5판)")

# 게임 시작 전이거나 리셋 시
if not st.session_state.quiz_pool:
    if st.button("게임 시작하기"):
        prepare_game()
        st.rerun()
    st.stop()

# 모든 라운드를 종료했을 때
if st.session_state.round >= 5:
    st.balloons()
    st.header("🏁 게임 종료!")
    st.subheader(f"최종 점수: {st.session_state.score} / 100")
    if st.button("다시 도전"):
        st.session_state.quiz_pool = []
        st.rerun()
    st.stop()

# --- 현재 라운드 진행 ---
current_q = st.session_state.quiz_pool[st.session_state.round]
st.write(f"### 라운드 {st.session_state.round + 1} / 5")
st.progress((st.session_state.round + 1) / 5)

st.image(current_q['url'], use_container_width=True)

# 난이도별 정답 및 보기 설정
def get_category(data):
    txt = (data['title'] + data['explanation']).lower()
    if "galaxy" in txt: return "은하 (Galaxy)"
    if "nebula" in txt: return "성운 (Nebula)"
    if "planet" in txt: return "행성 (Planet)"
    if "star" in txt: return "항성/성단 (Star)"
    if "moon" in txt: return "위성 (Moon)"
    if "sun" in txt: return "태양 (Sun)"
    return "기타 (Comet/Asteroid)"

# 1-2라운드는 종류, 3-5라운드는 이름 맞히기
if st.session_state.round < 2:
    correct_ans = get_category(current_q)
    options = CATEGORIES
    st.info("이 천체의 종류는 무엇일까요?")
else:
    correct_ans = current_q['title']
    options = random.sample(EXPERT_NAMES, 3) + [correct_ans]
    random.shuffle(options)
    st.warning("이 천체의 정확한 이름은 무엇일까요?")

# 버튼 UI
cols = st.columns(2)
for i, opt in enumerate(options):
    with cols[i % 2]:
        if st.button(opt, key=f"btn_{i}", disabled=st.session_state.answered, use_container_width=True):
            st.session_state.answered = True
            if opt == correct_ans:
                st.success("정답입니다! +20점")
                st.session_state.score += 20
            else:
                st.error(f"오답! 정답은: {correct_ans}")
            st.info(f"💡 설명: {current_q['explanation'][:300]}...")

# 다음 문제 버튼
if st.session_state.answered:
    if st.button("다음으로 ➡️"):
        st.session_state.round += 1
        st.session_state.answered = False
        st.rerun()
