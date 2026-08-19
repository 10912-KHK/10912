import streamlit as st
import requests
import random

# --- 설정 ---
st.set_page_config(page_title="우주 천체 퀴즈", page_icon="🌌")

API_KEY = "DEMO_KEY"
BAD_WORDS = ["earth", "rocket", "shuttle", "station", "iss", "astronaut", "rover", "telescope", "launch", "person", "satellite"]
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]
# 전문가용 보기 리스트
EXPERT_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "V838 Mon", "Pillars of Creation", "Sombrero Galaxy", "M101", "NGC 6960", "Andromeda Galaxy", "Whirlpool Galaxy"]

# --- 세션 상태 초기화 ---
if 'quiz_pool' not in st.session_state:
    st.session_state.quiz_pool = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'round' not in st.session_state:
    st.session_state.round = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False

# --- 데이터 가져오기 함수 ---
def fetch_five_images():
    pool = []
    attempts = 0
    with st.status("🚀 우주에서 깨끗한 사진 5장을 가져오는 중...", expanded=True) as status:
        while len(pool) < 5 and attempts < 3: # 최대 3번 재시도
            attempts += 1
            try:
                # 한 번에 25장씩 요청 (확률을 높임)
                res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=25", timeout=15).json()
                for item in res:
                    if item.get("media_type") == "image":
                        title = item.get("title", "").lower()
                        # 필터링: 지구나 인공물 제외
                        if not any(bad in title for bad in BAD_WORDS):
                            pool.append(item)
                    if len(pool) >= 5: break
            except Exception as e:
                st.error(f"연결 오류 발생: {e}")
                break
        
        if len(pool) >= 5:
            st.session_state.quiz_pool = pool[:5]
            st.session_state.round = 0
            st.session_state.score = 0
            st.session_state.answered = False
            status.update(label="✅ 준비 완료!", state="complete", expanded=False)
            return True
        else:
            status.update(label="❌ 사진을 충분히 찾지 못했습니다. 다시 시도해주세요.", state="error")
            return False

# --- 게임 화면 구성 ---
st.title("🌌 심우주 천체 퀴즈 (5판)")

# 1. 게임 시작 화면
if not st.session_state.quiz_pool:
    st.write("지구와 인공물을 제외한 실제 우주 천체 사진 5장을 맞히는 게임입니다.")
    if st.button("게임 시작하기", use_container_width=True):
        if fetch_five_images():
            st.rerun()

# 2. 결과 화면 (5판 다 깼을 때)
elif st.session_state.round >= 5:
    st.balloons()
    st.header("🏁 게임 종료!")
    st.subheader(f"최종 점수: {st.session_state.score} / 100")
    if st.button("새 게임 시작"):
        st.session_state.quiz_pool = []
        st.rerun()

# 3. 게임 진행 화면
else:
    current_q = st.session_state.quiz_pool[st.session_state.round]
    
    st.write(f"### 문제 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    # 사진 표시
    st.image(current_q['url'], use_container_width=True)

    # 문제 로직
    def get_category(data):
        txt = (data['title'] + data['explanation']).lower()
        if "galaxy" in txt: return "은하 (Galaxy)"
        if "nebula" in txt: return "성운 (Nebula)"
        if "planet" in txt: return "행성 (Planet)"
        if "star" in txt: return "항성/성단 (Star)"
        if "moon" in txt: return "위성 (Moon)"
        if "sun" in txt: return "태양 (Sun)"
        return "기타 (Comet/Asteroid)"

    # 난이도: 1-2번(종류), 3-5번(이름)
    if st.session_state.round < 2:
        st.info("이 천체의 '종류'는 무엇일까요?")
        correct_ans = get_category(current_q)
        options = CATEGORIES
    else:
        st.warning("이 천체의 '정확한 이름'은 무엇일까요?")
        correct_ans = current_q['title']
        # 전문가용 가짜 보기 3개 + 정답 1개
        temp_experts = [name for name in EXPERT_NAMES if name != correct_ans]
        options = random.sample(temp_experts, 3) + [correct_ans]
        random.shuffle(options)

    # 버튼 인터페이스
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct_ans:
                    st.success("정답입니다! 🎉 (+20점)")
                    st.session_state.score += 20
                else:
                    st.error(f"오답입니다. 정답은: {correct_ans}")
                
                with st.expander("자세한 설명 보기"):
                    st.write(current_q['explanation'])

    # 다음으로 넘어가기 버튼
    if st.session_state.answered:
        if st.button("다음 문제로 ➡️", use_container_width=True):
            st.session_state.round += 1
            st.session_state.answered = False
            st.rerun()

# 리셋 버튼 (사이드바)
with st.sidebar:
    if st.button("강제 초기화"):
        st.session_state.quiz_pool = []
        st.rerun()
