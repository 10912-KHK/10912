import streamlit as st
import requests
import random

# --- 1. 환경 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🔭", layout="centered")

# --- 2. 상수 및 백업 데이터 (절대 깨지지 않는 링크로 교체) ---
API_KEY = "DEMO_KEY" 
MAX_ROUNDS = 5

# 절대 안 깨지는 고화질 우주 사진 링크 (위키미디어 등 신뢰도 높은 서버)
FALLBACK_DATA = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "title": "Spiral Galaxy NGC 4414", "explanation": "A majestic spiral galaxy located in the constellation Coma Berenices."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Katrina_and_the_Waves_NGC_6357.jpg/800px-Katrina_and_the_Waves_NGC_6357.jpg", "title": "Lobster Nebula", "explanation": "A diffuse nebula near the Cat's Paw Nebula in the constellation Scorpius."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Hubble_v_and_v838mon.jpg/800px-Hubble_v_and_v838mon.jpg", "title": "V838 Monocerotis", "explanation": "A red variable star in the constellation Monoceros."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/NASA_Mars_Rover.jpg/800px-NASA_Mars_Rover.jpg", "title": "Mars Surface", "explanation": "The red planet's dusty and rocky surface as seen by a rover."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/OSIRIS_Mars_true_color.jpg/800px-OSIRIS_Mars_true_color.jpg", "title": "Planet Mars", "explanation": "True color image of Mars captured by the Rosetta spacecraft."}
]

FORBIDDEN = ["earth", "rocket", "iss", "astronaut", "launch", "shuttle", "person", "satellite"]
CATEGORIES = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]
FAKE_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "Pillars of Creation", "Sombrero Galaxy", "Lagoon Nebula", "Crab Nebula", "Orion Nebula"]

# --- 3. 세션 상태 초기화 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "START"
    st.session_state.quiz_pool = []
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False

# --- 4. 데이터 수집 함수 ---
def prepare_quiz():
    pool = []
    with st.status("🚀 우주 사진을 고화질로 불러오는 중...", expanded=True) as status:
        try:
            # 1. NASA API 시도 (한 번에 40장 가져와서 검사)
            response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=40", timeout=15)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    # 이미지만 허용 + 너무 큰 원본 대신 hdurl이 아닌 일반 url 사용 권장
                    url = item.get("url", "")
                    if item.get("media_type") == "image" and url.endswith(('.jpg', '.png', '.jpeg')):
                        title = item.get("title", "").lower()
                        if not any(bad in title for bad in FORBIDDEN):
                            pool.append(item)
                    if len(pool) >= MAX_ROUNDS: break
        except:
            pass

        # 2. 사진이 부족하면 무조건 백업 데이터로 채움
        if len(pool) < MAX_ROUNDS:
            needed = MAX_ROUNDS - len(pool)
            pool.extend(random.sample(FALLBACK_DATA, needed))
        
        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        status.update(label="✅ 준비 완료!", state="complete", expanded=False)
    st.rerun()

# --- 5. 메인 UI ---

if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 우주 천체 맞히기")
    st.write("---")
    st.info("NASA 실시간 데이터와 고화질 우주 아카이브를 결합했습니다.")
    if st.button("게임 시작", use_container_width=True):
        prepare_quiz()

elif st.session_state.game_state == "PLAYING":
    current_q = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / {MAX_ROUNDS}")
    st.progress((st.session_state.round + 1) / MAX_ROUNDS)
    
    # [사진 표시 핵심 로직]
    # 사진 로딩이 느릴 수 있음을 안내하고, 링크도 함께 제공
    st.markdown(f'<p style="color:gray; font-size:12px;">사진 로딩이 느리다면 잠시만 기다려주세요...</p>', unsafe_allow_html=True)
    
    # 사진 표시 (이미지 로딩 에러 방지를 위해 예외처리 느낌으로 시도)
    try:
        st.image(current_q['url'], use_container_width=True, caption="제시된 천체 사진")
    except:
        st.error("이미지를 불러오는데 실패했습니다. 아래 링크를 클릭해 확인하거나 다음으로 넘어가주세요.")
        st.write(f"[사진 직접 보기]({current_q['url']})")

    # 문제 로직
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
        st.write("### Q. 이 천체의 '종류'는?")
        correct = get_ans_category(current_q)
        options = CATEGORIES
    else:
        st.write("### Q. 이 천체의 '이름'은?")
        correct = current_q['title']
        others = [f for f in FAKE_NAMES if f != correct]
        options = random.sample(others, 3) + [correct]
        random.shuffle(options)

    # 버튼 인터페이스
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    st.success(f"정답입니다! 🎉 (+20점)")
                    st.session_state.score += 20
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                
                with st.expander("설명 보기"):
                    st.write(current_q['explanation'])

    if st.session_state.answered:
        if st.button("다음 문제 ➡️", use_container_width=True):
            st.session_state.round += 1
            st.session_state.answered = False
            if st.session_state.round >= MAX_ROUNDS:
                st.session_state.game_state = "FINISHED"
            st.rerun()

elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐험 완료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("다시 도전", use_container_width=True):
        st.session_state.game_state = "START"
        st.session_state.quiz_pool = []
        st.rerun()
