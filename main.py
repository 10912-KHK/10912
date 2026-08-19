import streamlit as st
import requests
import random
import time

# --- 1. 환경 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🔭", layout="centered")

# --- 2. 상수 설정 ---
API_KEY = "DEMO_KEY"
MAX_ROUNDS = 5
# 절대 나오면 안 되는 키워드 (지구, 인공물)
FORBIDDEN = ["earth", "rocket", "shuttle", "station", "iss", "astronaut", "rover", "telescope", "observatory", "launch", "person", "satellite", "atmosphere", "horizon", "clouds", "skyline", "landscape"]
# 우주 천체임을 보장하는 키워드
REQUIRED = ["galaxy", "nebula", "star", "cluster", "planet", "comet", "supernova", "m1", "m31", "ngc", "messier", "asteroid", "sun", "moon", "pulsar"]
# 전문가용 오답 후보
FAKE_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "V838 Mon", "Pillars of Creation", "Sombrero Galaxy", "Whirlpool Galaxy", "Lagoon Nebula", "Crab Nebula", "Andromeda Galaxy"]

# --- 3. 세션 상태 관리 (앱 재실행 시 데이터 유지 핵심) ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "START" # START, PLAYING, FINISHED
    st.session_state.quiz_pool = []
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_feedback = None # 정답/오답 메시지 저장

# --- 4. 데이터 로직 ---
def get_category(data):
    txt = (data['title'] + data['explanation']).lower()
    if "galaxy" in txt: return "은하 (Galaxy)"
    if "nebula" in txt: return "성운 (Nebula)"
    if "planet" in txt: return "행성 (Planet)"
    if "star" in txt: return "항성/성단 (Star)"
    if "moon" in txt: return "위성 (Moon)"
    if "sun" in txt: return "태양 (Sun)"
    return "기타 (Comet/Asteroid)"

def fetch_valid_data():
    """조건에 맞는 우주 사진 5장을 찾을 때까지 무한 반복 (최대 3회 시도)"""
    pool = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for attempt in range(1, 4):
        status_text.write(f"🚀 우주 탐색 중... (시도 {attempt}/3)")
        try:
            # 한 번에 50장을 가져와 확률 극대화
            res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=50", timeout=20).json()
            for item in res:
                if item.get("media_type") == "image":
                    title = item.get("title", "").lower()
                    expl = item.get("explanation", "").lower()
                    full_text = title + " " + expl
                    
                    # 1. 금지 단어 필터링
                    if any(bad in title for bad in FORBIDDEN): continue
                    # 2. 필수 단어 포함 여부 (우주 천체인지 확인)
                    if any(good in full_text for good in REQUIRED):
                        pool.append(item)
                
                if len(pool) >= MAX_ROUNDS: break
            
            if len(pool) >= MAX_ROUNDS: break
        except Exception as e:
            st.error(f"연결 오류: {e}")
            return None
        progress_bar.progress(attempt * 33)
    
    status_text.empty()
    progress_bar.empty()
    return pool[:MAX_ROUNDS] if len(pool) >= MAX_ROUNDS else None

# --- 5. 게임 UI 로직 ---

def start_game():
    data = fetch_valid_data()
    if data:
        st.session_state.quiz_pool = data
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()
    else:
        st.error("우주 데이터를 충분히 가져오지 못했습니다. 다시 눌러주세요!")

def next_round():
    st.session_state.round += 1
    st.session_state.answered = False
    st.session_state.last_feedback = None
    if st.session_state.round >= MAX_ROUNDS:
        st.session_state.game_state = "FINISHED"
    st.rerun()

# --- 6. 화면 렌더링 ---

# (1) 시작 화면
if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 우주 천체 맞히기")
    st.write("---")
    st.info("실제 NASA의 실시간 데이터를 사용하여 '진짜 우주'만 선별했습니다.")
    st.write("1~2라운드: 천체의 종류 맞히기 (쉬움)")
    st.write("3~5라운드: 천체의 이름 맞히기 (어려움)")
    if st.button("게임 시작", use_container_width=True):
        start_game()

# (2) 게임 진행 화면
elif st.session_state.game_state == "PLAYING":
    current_q = st.session_state.quiz_pool[st.session_state.round]
    st.subheader(f"라운드 {st.session_state.round + 1} / {MAX_ROUNDS}")
    st.progress((st.session_state.round + 1) / MAX_ROUNDS)
    
    st.image(current_q['url'], use_container_width=True)
    
    # 난이도 설정
    if st.session_state.round < 2:
        st.write("**Q. 이 사진 속 천체는 어떤 종류인가요?**")
        correct_ans = get_category(current_q)
        options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Comet/Asteroid)"]
    else:
        st.write("**Q. 이 천체의 구체적인 명칭(제목)은 무엇일까요?**")
        correct_ans = current_q['title']
        # 오답 리스트 생성 (중복 제거)
        others = [n for n in FAKE_NAMES if n != correct_ans]
        options = random.sample(others, 3) + [correct_ans]
        random.shuffle(options)

    # 버튼 인터페이스
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            # 정답 선택 전후 상태 관리
            if st.button(opt, key=f"btn_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct_ans:
                    st.session_state.score += 20
                    st.session_state.last_feedback = ("SUCCESS", f"정답입니다! 🎉 (+20점)\n\n**제목:** {current_q['title']}")
                else:
                    st.session_state.last_feedback = ("ERROR", f"아쉽네요! 정답은 **{correct_ans}** 입니다.")
                st.rerun()

    # 피드백 표시
    if st.session_state.answered and st.session_state.last_feedback:
        fb_type, fb_msg = st.session_state.last_feedback
        if fb_type == "SUCCESS": st.success(fb_msg)
        else: st.error(fb_msg)
        
        with st.expander("천체 백과사전 보기 (설명)"):
            st.write(current_q['explanation'])
        
        if st.button("다음 라운드로 ➡️", use_container_width=True):
            next_round()

# (3) 게임 결과 화면
elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐험 완료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    
    if st.session_state.score == 100: grade = "🌌 우주 마스터 (완벽합니다!)"
    elif st.session_state.score >= 60: grade = "🔭 숙련된 천문학자"
    else: grade = "🚀 견습 우주 비행사"
    
    st.info(f"등급: {grade}")
    
    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state.game_state = "START"
        st.session_state.quiz_pool = []
        st.rerun()
