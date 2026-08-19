import streamlit as st
import requests
import random

# --- 1. 설정 및 고화질 고속 이미지 아카이브 (NASA 실패 시 대비) ---
st.set_page_config(page_title="슈퍼 우주 탐사 퀴즈", page_icon="🔭", layout="centered")

# 위키미디어 및 허블 아카이브에서 가져온 '무조건 뜨는' 고화질 사진들
DEEP_SPACE_BACKUP = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/1024px-NGC_4414_%28NASA-Hubble%29.jpg", "title": "NGC 4414 나선은하", "type": "은하 (Galaxy)", "expl": "머리털자리에 있는 전형적인 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/1024px-Crab_Nebula.jpg", "title": "게성운 (M1)", "type": "성운 (Nebula)", "expl": "1054년에 폭발한 초신성의 잔해입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/1024px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "title": "창조의 기둥", "type": "성운 (Nebula)", "expl": "독수리 성운 내부에 있는 별들이 탄생하는 거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/1024px-HST_Andromeda_Galaxy.jpg", "title": "안드로메다 은하 (M31)", "type": "은하 (Galaxy)", "expl": "우리 은하와 충돌 궤도에 있는 가장 가까운 거대 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Saturn_during_Equinox.jpg/1024px-Saturn_during_Equinox.jpg", "title": "토성 (Saturn)", "type": "행성 (Planet)", "expl": "얼음과 먼지로 이루어진 거대한 고리를 가진 가스 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Hubble_v_and_v838mon.jpg/1024px-Hubble_v_and_v838mon.jpg", "title": "외뿔소자리 V838", "type": "항성/성단 (Star)", "expl": "거대한 변광성 주위로 빛의 메아리가 퍼져나가는 모습입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/M101_hires_STScI-PRC2006-10a.jpg/1024px-M101_hires_STScI-PRC2006-10a.jpg", "title": "바람개비 은하 (M101)", "type": "은하 (Galaxy)", "expl": "정면을 향하고 있는 아주 거대한 나선 은하입니다."}
]

FORBIDDEN = ["earth", "rocket", "iss", "astronaut", "launch", "shuttle", "satellite", "person", "telescope"]
EXPERT_NAMES = ["NGC 4567", "Messier 82", "IC 1101", "Abell 2744", "Kepler-452b", "Sombrero Galaxy", "Whirlpool Galaxy", "Lagoon Nebula", "Horsehead Nebula", "M104", "Omega Centauri", "Carina Nebula"]

# --- 2. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "START" # START, PLAYING, FINISHED
    st.session_state.quiz_pool = []
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False

# --- 3. 사진 수집 로직 (하이브리드) ---
def prepare_game():
    with st.status("🔭 우주 탐사 경로를 탐색 중...", expanded=True) as status:
        pool = []
        try:
            # 1단계: NASA에서 20장을 가져와 필터링 시도
            res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=20", timeout=7).json()
            for item in res:
                if item.get("media_type") == "image":
                    title = item.get("title", "").lower()
                    if not any(bad in title for bad in FORBIDDEN):
                        pool.append({
                            "url": item['url'],
                            "title": item['title'],
                            "expl": item['explanation'],
                            "source": "NASA"
                        })
                if len(pool) >= 5: break
        except:
            pass

        # 2단계: NASA 데이터가 부족(5장 미만)하면 고속 백업 아카이브에서 무작위로 채움
        if len(pool) < 5:
            needed = 5 - len(pool)
            pool.extend(random.sample(DEEP_SPACE_BACKUP, needed))
        
        random.shuffle(pool)
        st.session_state.quiz_pool = pool[:5]
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        status.update(label="✅ 탐사 준비 완료!", state="complete", expanded=False)
    st.rerun()

# --- 4. 게임 화면 구현 ---

if st.session_state.game_state == "START":
    st.title("🌌 슈퍼 심우주 퀴즈 챌린지")
    st.write("---")
    st.write("지구와 인공물을 제외한 실제 우주 천체 사진 5장이 출제됩니다.")
    st.info("💡 1~2라운드는 종류(카테고리), 3~5라운드는 정확한 명칭을 맞히세요!")
    if st.button("게임 시작 🚀", use_container_width=True):
        prepare_game()

elif st.session_state.game_state == "PLAYING":
    current_q = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    # [사진 표시 핵심]
    try:
        st.image(current_q['url'], use_container_width=True)
    except:
        st.error("사진 로딩에 실패했습니다. 다음 문제로 넘어가거나 링크를 확인하세요.")
        st.write(f"[사진 직접 보기]({current_q['url']})")

    # 정답 판별기
    def get_ans_category(q):
        if "type" in q: return q['type'] # 백업 데이터용
        txt = (q['title'] + q['expl']).lower()
        if "galaxy" in txt: return "은하 (Galaxy)"
        if "nebula" in txt: return "성운 (Nebula)"
        if "planet" in txt: return "행성 (Planet)"
        if "star" in txt or "cluster" in txt: return "항성/성단 (Star)"
        if "moon" in txt: return "위성 (Moon)"
        return "기타 천체"

    if st.session_state.round < 2:
        st.write("### Q. 이 천체의 종류(카테고리)는 무엇일까요?")
        correct = get_ans_category(current_q)
        options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "기타 천체"]
    else:
        st.write("### Q. 이 천체의 정확한 이름은 무엇일까요?")
        correct = current_q['title']
        others = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
        options = others + [correct]
        random.shuffle(options)

    # 선택 버튼
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    st.success("정답입니다! 🎉 (+20점)")
                    st.session_state.score += 20
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                st.info(f"**📚 설명:** {current_q['expl'][:400]}...")

    if st.session_state.answered:
        if st.button("다음으로 ➡️", use_container_width=True):
            st.session_state.round += 1
            st.session_state.answered = False
            if st.session_state.round >= 5:
                st.session_state.game_state = "FINISHED"
            st.rerun()

elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 종료!")
    st.header(f"당신의 최종 점수: {st.session_state.score} / 100")
    
    if st.session_state.score >= 80:
        st.success("등급: 🌌 우주 마스터")
    elif st.session_state.score >= 40:
        st.info("등급: 🔭 우주 탐험가")
    else:
        st.warning("등급: 🚀 우주 꿈나무")
        
    if st.button("새 게임 시작", use_container_width=True):
        st.session_state.game_state = "START"
        st.session_state.quiz_pool = []
        st.rerun()
