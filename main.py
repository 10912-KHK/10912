
import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# --- 1. 환경 설정 ---
st.set_page_config(page_title="심우주 탐사 퀴즈", page_icon="🌌", layout="centered")

# [절대 깨지지 않는 백업용 고화질 사진 DB]
NORMAL_BACKUP = [
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800", "name": "화성", "expl": "붉은 행성으로 알려진 태양계의 4번째 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6?w=800", "name": "토성", "expl": "거대한 고리를 가진 가스 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614730321146-b6fa6a46bac4?w=800", "name": "목성", "expl": "태양계에서 가장 큰 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1529788295308-1eace6f67388?w=800", "name": "태양", "expl": "우리 태양계의 중심인 항성입니다."}
]

DEEP_SPACE_BACKUP = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "NGC 4414 나선은하", "expl": "약 6천만 광년 떨어진 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "name": "게성운 (M1)", "expl": "초신성 폭발 후 남은 가스 구름입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "expl": "별이 태어나는 거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/800px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "expl": "인류가 최초로 촬영한 블랙홀입니다."}
]

EXPERT_NAMES = ["NGC 6960", "Messier 87", "IC 1101", "Kepler-186f", "V838 Monocerotis", "Sombrero Galaxy", "Horsehead Nebula", "M104"]

# --- 2. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'answered': False,
        'hint_used': False
    })

# --- 3. 핵심 로직 함수 ---

def get_random_date():
    start = datetime(2015, 1, 1)
    diff = (datetime.now() - timedelta(days=1) - start).days
    return (start + timedelta(days=random.randint(0, diff))).strftime("%Y-%m-%d")

def fetch_game_data():
    """게임을 시작할 때 한 번에 5문제를 모두 로드"""
    pool = []
    with st.status("🚀 우주 관측 사진 수집 중...", expanded=True) as status:
        # 1~4라운드용 (NASA 우선, 실패 시 백업)
        for _ in range(4):
            try:
                res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={get_random_date()}", timeout=3).json()
                if res.get("media_type") == "image":
                    pool.append({"url": res['url'], "name": res['title'], "expl": res['explanation'], "type": "NASA"})
                else: raise Exception()
            except:
                pool.append(random.choice(NORMAL_BACKUP))
        
        # 5라운드용 (심우주 고정)
        pool.append(random.choice(DEEP_SPACE_BACKUP))

        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
        status.update(label="✅ 준비 완료!", state="complete", expanded=False)
    st.rerun()

def get_category(q):
    txt = (q['name'] + q['expl']).lower()
    if "galaxy" in txt: return "은하 (Galaxy)"
    if "nebula" in txt: return "성운 (Nebula)"
    if "planet" in txt: return "행성 (Planet)"
    if "star" in txt or "cluster" in txt: return "항성/성단 (Star)"
    return "기타 천체"

# --- 4. 화면 구성 ---

# [시작 화면]
if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 우주 탐사 퀴즈")
    st.write("---")
    st.info("지구/로켓을 제외한 진짜 우주 사진 5장이 출제됩니다. 5라운드는 심우주가 나옵니다.")
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        fetch_game_data()

# [게임 진행 화면]
elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(cur['url'], use_container_width=True)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (50:50 / -10점)", key=f"hint_btn_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 난이도별 보기 구성
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는?")
            correct = get_category(cur)
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "기타 천체"]
        else:
            st.warning("🎯 이 천체의 '이름'은?")
            correct = cur['name']
            distractors = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
            options = distractors + [correct]
        
        # 힌트 로직
        if st.session_state.hint_used and not st.session_state.answered:
            wrong_one = random.choice([o for o in options if o != correct])
            options = [correct, wrong_one]
            random.shuffle(options)

        # 선택 버튼 (매 라운드 고유한 Key 부여)
        for i, opt in enumerate(options):
            if st.button(opt, key=f"ans_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답! (+{reward}점)")
                else:
                    st.error(f"오답! 정답: {correct}")
                st.write(f"**📚 설명:** {cur['expl']}")

        # [진행 버튼] 이 버튼이 확실히 눌려야 다음 라운드로 감
        if st.session_state.answered:
            if st.button("다음 라운드로 전진 ➡️", key=f"next_btn_{st.session_state.round}", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5:
                    st.session_state.game_state = "FINISHED"
                st.rerun()

# [결과 화면]
elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 종료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("다시 도전하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()

# [사이드바 점수]
st.sidebar.write(f"현재 점수: {st.session_state.score}")
