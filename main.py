import streamlit as st
import requests
import random
import base64
from io import BytesIO
from PIL import Image

# --- 1. 설정 및 고화질 이미지 아카이브 ---
st.set_page_config(page_title="완벽한 우주 퀴즈", page_icon="🌌", layout="centered")

# 위키미디어 기반 고화질 우주 사진 (NASA 서버 장애 시 무조건 호출)
BACKUP_ARCHIVE = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "title": "NGC 4414", "type": "은하 (Galaxy)", "expl": "머리털자리에 위치한 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "title": "게성운 (M1)", "type": "성운 (Nebula)", "expl": "초신성 폭발 후 남은 잔해 가스 구름입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "title": "창조의 기둥", "type": "성운 (Nebula)", "expl": "별들이 탄생하는 거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/800px-HST_Andromeda_Galaxy.jpg", "title": "안드로메다 은하", "type": "은하 (Galaxy)", "expl": "우리 은하와 가장 가까운 거대 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Saturn_during_Equinox.jpg/800px-Saturn_during_Equinox.jpg", "title": "토성", "type": "행성 (Planet)", "expl": "고리가 특징인 태양계의 가스 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Hubble_v_and_v838mon.jpg/800px-Hubble_v_and_v838mon.jpg", "title": "V838 Mon", "type": "항성/성단 (Star)", "expl": "빛의 메아리가 퍼져나가는 거대 변광성입니다."}
]

FORBIDDEN = ["earth", "rocket", "iss", "astronaut", "shuttle", "person", "satellite"]
EXPERT_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Kepler-452b", "Sombrero Galaxy", "Whirlpool Galaxy", "Lagoon Nebula", "Horsehead Nebula", "Orion Nebula"]

# --- 2. 이미지 처리 핵심 함수 (Base64 변환) ---
def get_image_base64(url):
    """URL에서 이미지를 서버가 직접 가져와 Base64 문자열로 변환 (사진 노출 보장)"""
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        # 속도를 위해 이미지 크기 최적화 (가로 800px)
        img.thumbnail((800, 800))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return None

# --- 3. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "START"
    st.session_state.quiz_pool = []
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False

# --- 4. 문제 준비 로직 ---
def prepare_game():
    with st.status("🌌 우주에서 고화질 사진을 전송받는 중...", expanded=True) as status:
        pool = []
        try:
            # NASA API에서 데이터 가져오기 시도
            res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=15", timeout=10).json()
            for item in res:
                if item.get("media_type") == "image":
                    title = item.get("title", "").lower()
                    if not any(bad in title for bad in FORBIDDEN):
                        # 서버가 이미지를 직접 가져와서 변환 (여기서 안 되면 건너뜀)
                        b64_data = get_image_base64(item['url'])
                        if b64_data:
                            pool.append({
                                "b64": b64_data,
                                "title": item['title'],
                                "expl": item['explanation'],
                                "type": "CHECK"
                            })
                if len(pool) >= 5: break
        except:
            pass

        # 부족하면 백업 아카이브에서 채움
        if len(pool) < 5:
            for item in random.sample(BACKUP_ARCHIVE, 5 - len(pool)):
                b64 = get_image_base64(item['url'])
                if b64:
                    pool.append({
                        "b64": b64,
                        "title": item['title'],
                        "expl": item['expl'],
                        "type": item['type']
                    })
        
        st.session_state.quiz_pool = pool[:5]
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        status.update(label="🚀 준비 완료!", state="complete", expanded=False)
    st.rerun()

# --- 5. 화면 레이아웃 ---

if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 우주 천체 맞히기")
    st.write("---")
    st.info("NASA와 위키미디어의 데이터를 분석하여 고화질 우주 사진 5장을 준비합니다.")
    if st.button("탐사 시작 🚀", use_container_width=True):
        prepare_game()

elif st.session_state.game_state == "PLAYING":
    current_q = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    # [사진 노출 핵심] Base64 데이터를 사용해 직접 출력 (차단 불가)
    st.image(f"data:image/jpeg;base64,{current_q['b64']}", use_container_width=True)

    # 문제 로직
    def get_category(q):
        if q['type'] != "CHECK": return q['type']
        txt = (q['title'] + q['expl']).lower()
        if "galaxy" in txt: return "은하 (Galaxy)"
        if "nebula" in txt: return "성운 (Nebula)"
        if "planet" in txt: return "행성 (Planet)"
        if "star" in txt or "cluster" in txt: return "항성/성단 (Star)"
        return "기타 천체"

    if st.session_state.round < 2:
        st.write("### Q. 이 천체의 종류는?")
        correct = get_category(current_q)
        options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "기타 천체"]
    else:
        st.write("### Q. 이 천체의 실제 이름은?")
        correct = current_q['title']
        others = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
        options = others + [correct]
        random.shuffle(options)

    # 버튼 인터페이스
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    st.success(f"정답입니다! 🎉")
                    st.session_state.score += 20
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                st.info(f"**📚 설명:** {current_q['expl'][:400]}...")

    if st.session_state.answered:
        if st.button("다음 문제 ➡️", use_container_width=True):
            st.session_state.round += 1
            st.session_state.answered = False
            if st.session_state.round >= 5:
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
