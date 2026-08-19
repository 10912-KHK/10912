import streamlit as st
import requests
import random

# --- 1. 환경 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🔭", layout="centered")

# --- 2. 상수 및 백업 데이터 ---
API_KEY = "DEMO_KEY" 
MAX_ROUNDS = 5

# NASA 서버가 먹통일 때 사용할 고퀄리티 백업 데이터 (절대 실패 방지)
FALLBACK_DATA = [
    {"url": "https://apod.nasa.gov/apod/image/2303/STSCI-J-P2307a-m-2000x1374.jpg", "title": "The Pillars of Creation", "explanation": "This is a famous nebula in the Eagle Nebula, captured by JWST. It consists of interstellar gas and dust."},
    {"url": "https://apod.nasa.gov/apod/image/2301/NGC2264_HubbleSubaru_1080.jpg", "title": "The Cone Nebula", "explanation": "A star-forming region in the constellation Monoceros. It has a distinctive conical shape."},
    {"url": "https://apod.nasa.gov/apod/image/2207/main_release_refined_final_bw_web.jpg", "title": "SMACS 0723 Deep Field", "explanation": "The deepest and sharpest infrared image of the distant universe to date by James Webb."},
    {"url": "https://apod.nasa.gov/apod/image/2004/M106_HubbleV_2427.jpg", "title": "Spiral Galaxy M106", "explanation": "A majestic spiral galaxy located in the constellation Canes Venatici."},
    {"url": "https://apod.nasa.gov/apod/image/2109/M31_Subaru_960.jpg", "title": "Andromeda Galaxy (M31)", "explanation": "Our closest large galactic neighbor, a massive spiral galaxy."}
]

FORBIDDEN = ["earth", "rocket", "iss", "astronaut", "rover", "launch", "shuttle", "observatory", "person", "satellite"]
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]
FAKE_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "V838 Mon", "Pillars of Creation", "Sombrero Galaxy", "Lagoon Nebula", "Crab Nebula"]

# --- 3. 세션 상태 초기화 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "START"
    st.session_state.quiz_pool = []
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False

# --- 4. 데이터 수집 함수 (스마트 필터링 + 백업) ---
def prepare_quiz():
    pool = []
    with st.status("🚀 우주 데이터 분석 중...", expanded=True) as status:
        try:
            # 1. NASA API 시도
            response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=30", timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    if item.get("media_type") == "image":
                        title = item.get("title", "").lower()
                        # 필터링: 지구나 인공물 제외
                        if not any(bad in title for bad in FORBIDDEN):
                            pool.append(item)
                    if len(pool) >= MAX_ROUNDS: break
        except Exception as e:
            st.warning("NASA 실시간 서버 연결이 원활하지 않아 준비된 탐사 데이터를 사용합니다.")

        # 2. 만약 API에서 5장을 못 구했다면? 백업 데이터로 채움 (절대 실패 방지)
        if len(pool) < MAX_ROUNDS:
            needed = MAX_ROUNDS - len(pool)
            pool.extend(random.sample(FALLBACK_DATA, needed))
        
        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        status.update(label="✅ 탐사 준비 완료!", state="complete", expanded=False)
    
    st.rerun()

# --- 5. 화면 레이아웃 ---

# [시작 화면]
if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 우주 천체 맞히기")
    st.write("NASA의 실제 관측 데이터를 바탕으로 구성된 5단계 퀴즈입니다.")
    st.write("- **1~2단계:** 천체의 카테고리 맞히기")
    st.write("- **3~5단계:** 천체의 실제 이름 맞히기 (전문가)")
    if st.button("게임 시작", use_container_width=True):
        prepare_quiz()

# [게임 진행 화면]
elif st.session_state.game_state == "PLAYING":
    current_q = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / {MAX_ROUNDS}")
    st.progress((st.session_state.round + 1) / MAX_ROUNDS)
    
    st.image(current_q['url'], use_container_width=True)

    # 문제 및 정답 설정
    def get_ans_category(d):
        t = (d['title'] + d['explanation']).lower()
        if "galaxy" in t: return "은하 (Galaxy)"
        if "nebula" in t: return "성운 (Nebula)"
        if "planet" in t: return "행성 (Planet)"
        if "star" in t or "cluster" in t: return "항성/성단 (Star)"
        if "moon" in t: return "위성 (Moon)"
        if "sun" in t: return "태양 (Sun)"
        return "기타 (Comet/Asteroid)"

    if st.session_state.round < 2:
        st.write("### Q. 이 천체는 무엇일까요?")
        correct = get_ans_category(current_q)
        options = CATEGORIES
    else:
        st.write("### Q. 이 천체의 구체적인 명칭은?")
        correct = current_q['title']
        others = [f for f in FAKE_NAMES if f != correct]
        options = random.sample(others, 3) + [correct]
        random.shuffle(options)

    # 버튼 레이아웃
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    st.success(f"정답입니다! 🎉 (+20점)\n\n**{current_q['title']}**")
                    st.session_state.score += 20
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                
                with st.expander("천체 설명 확인"):
                    st.write(current_q['explanation'])

    if st.session_state.answered:
        if st.button("다음으로 ➡️", use_container_width=True):
            st.session_state.round += 1
            st.session_state.answered = False
            if st.session_state.round >= MAX_ROUNDS:
                st.session_state.game_over = True # (실제로는 game_state 변경)
                st.session_state.game_state = "FINISHED"
            st.rerun()

# [결과 화면]
elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐험 종료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    
    if st.session_state.score == 100: grade = "🌌 우주 마스터"
    elif st.session_state.score >= 60: grade = "🔭 숙련된 관측자"
    else: grade = "🚀 견습 탐험가"
    
    st.info(f"당신의 등급은: **{grade}**")
    if st.button("다시 도전", use_container_width=True):
        st.session_state.game_state = "START"
        st.session_state.quiz_pool = []
        st.rerun()
