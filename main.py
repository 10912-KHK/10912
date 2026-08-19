import streamlit as st
import requests
import random
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta

# --- 1. 설정 ---
st.set_page_config(page_title="심우주 탐사 챌린지", page_icon="🔭", layout="wide")

# --- 2. 데이터베이스 ---
# 5라운드 전용 심우주(Deep Space) 고해상도 리스트 (태양계 밖)
DEEP_SPACE_DB = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "NGC 4414 나선은하", "expl": "머리털자리에 위치한 약 6천만 광년 떨어진 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "name": "게성운 (M1)", "expl": "1054년에 관측된 초신성 폭발의 잔해입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/800px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "expl": "인류 최초로 촬영된 5,500만 광년 거리의 거대 질량 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Hubble_v_and_v838mon.jpg/800px-Hubble_v_and_v838mon.jpg", "name": "V838 Mon", "expl": "외뿔소자리에 있는 거대 변광성으로 빛의 메아리 현상을 보여줍니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "expl": "독수리 성운 내부에 있는 별들이 탄생하는 거대 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/800px-HST_Andromeda_Galaxy.jpg", "name": "안드로메다 은하", "expl": "우리 은하와 가장 가까운 약 250만 광년 거리의 거대 은하입니다."}
]

EXPERT_NAMES = ["NGC 6960", "Messier 87", "IC 1101", "Kepler-186f", "V838 Mon", "Sombrero Galaxy", "Abell 2744", "Horsehead Nebula", "M104"]

# --- 3. 유틸리티 함수 ---
def get_image_as_b64(url):
    """이미지를 Base64로 변환하여 로딩 문제 해결"""
    try:
        res = requests.get(url, timeout=10)
        img = Image.open(BytesIO(res.content))
        img.thumbnail((800, 800)) # 최적화
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return None

def get_random_nasa_date():
    """매번 다른 날짜를 생성하여 중복 방지"""
    start = datetime(2015, 1, 1)
    end = datetime.now() - timedelta(days=1)
    random_days = random.randrange((end - start).days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

# --- 4. 세션 상태 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'answered': False,
        'hint_used': False
    })

# --- 5. 데이터 패치 로직 ---
def fetch_game_data():
    pool = []
    with st.status("🌌 우주의 신호를 수신 중...", expanded=True) as status:
        # 1~4라운드: NASA 무작위 날짜 데이터
        attempts = 0
        while len(pool) < 4 and attempts < 15:
            attempts += 1
            date = get_random_date = get_random_nasa_date()
            try:
                res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={date}", timeout=5).json()
                if res.get("media_type") == "image":
                    b64 = get_image_as_b64(res['url'])
                    if b64:
                        pool.append({"b64": b64, "name": res['title'], "expl": res['explanation'], "type": "CHECK"})
            except: continue
        
        # 5라운드: 심우주 데이터 (무조건 하나 뽑기)
        deep_target = random.choice(DEEP_SPACE_DB)
        deep_b64 = get_image_as_b64(deep_target['url'])
        pool.append({"b64": deep_b64, "name": deep_target['name'], "expl": deep_target['expl'], "type": "DEEP"})

        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
        status.update(label="🚀 탐사 준비 완료!", state="complete", expanded=False)
    st.rerun()

def get_category(q):
    txt = (q['name'] + q['expl']).lower()
    if "galaxy" in txt: return "은하 (Galaxy)"
    if "nebula" in txt: return "성운 (Nebula)"
    if "planet" in txt: return "행성 (Planet)"
    if "star" in txt or "cluster" in txt: return "항성/성단 (Star)"
    if "moon" in txt: return "위성 (Moon)"
    return "기타 천체"

# --- 6. UI 화면 ---
if st.session_state.game_state == "START":
    st.title("🔭 Cosmic Master Quiz")
    st.write("---")
    st.markdown("### **매번 새로운 무작위 데이터로 우주를 탐사하세요!**")
    st.info("1~4라운드는 무작위 NASA 데이터, 5라운드는 심우주 전용 데이터가 출제됩니다.")
    if st.button("탐사 시작 🚀", use_container_width=True):
        fetch_game_data()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if cur['b64']:
            st.image(f"data:image/jpeg;base64,{cur['b64']}", use_container_width=True)
        else:
            st.error("이미지 전송 오류! 다음 문제로 넘어가세요.")
            
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (선택지 2개로 축소 / -10점)"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 종류는?")
            correct = get_category(cur)
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 천체"]
        else:
            st.warning("🎯 이 천체의 실제 이름은?")
            correct = cur['name']
            distractors = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
            options = distractors + [correct]
        
        # 힌트 로직: 정답 1개 + 오답 1개로 압축
        if st.session_state.hint_used and not st.session_state.answered:
            wrong_one = random.choice([o for o in options if o != correct])
            options = [correct, wrong_one]
            random.shuffle(options)
            st.warning("힌트: 정답 확률 50%!")

        # 버튼 생성
        for i, opt in enumerate(options):
            if st.button(opt, key=f"ans_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답! (+{reward}점)")
                else:
                    st.error(f"오답! 정답은: {correct}")
                st.write(f"**🔭 설명:** {cur['expl']}")

        if st.session_state.answered:
            if st.button("다음으로 ➡️", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5:
                    st.session_state.game_state = "FINISHED"
                st.rerun()

elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 결과")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("새로운 탐사 시작", use_container_width=True):
        st.session_state.game_state = "START"
        st.session_state.quiz_pool = []
        st.rerun()

# 사이드바 리셋
with st.sidebar:
    st.write(f"현재 점수: {st.session_state.score}")
    if st.button("완전 리셋"):
        st.session_state.game_state = "START"
        st.session_state.quiz_pool = []
        st.rerun()
