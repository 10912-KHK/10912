import streamlit as st
import requests
import random

# --- 1. 환경 설정 ---
st.set_page_config(page_title="Cosmic Master", page_icon="🔭", layout="wide")

# --- 2. 데이터베이스 ---
# 1~4라운드용 일반 DB
NORMAL_DB = [
    {"url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564", "name": "오리온 성운", "type": "성운 (Nebula)", "expl": "지구에서 가장 가까운 거대 별 형성 구역입니다."},
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9", "name": "화성", "type": "행성 (Planet)", "expl": "태양계의 4번째 행성으로 붉은 색이 특징입니다."},
    {"url": "https://images.unsplash.com/photo-1464802686167-b939a6910659", "name": "안드로메다 은하", "type": "은하 (Galaxy)", "expl": "우리 은하와 가장 가까운 거대 나선 은하입니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6", "name": "토성", "type": "행성 (Planet)", "expl": "고리가 아름다운 가스 행성입니다."}
]

# 5라운드 전용 심우주(Deep Space) DB - 태양계 밖 아주 먼 곳
DEEP_SPACE_DB = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/1024px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "expl": "인류 최초로 촬영된 거대 질량 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Point_of_Light_-_Artist%27s_impression_of_the_quasar_3C_273.jpg/1024px-Point_of_Light_-_Artist%27s_impression_of_the_quasar_3C_273.jpg", "name": "퀘이사 3C 273", "expl": "우주에서 가장 밝은 천체 중 하나로, 수십억 광년 떨어져 있습니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/1024px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥 (JWST)", "expl": "독수리 성운 깊숙한 곳의 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Exoplanet_Comparison_Kepler-186f_with_Earth.png/1024px-Exoplanet_Comparison_Kepler-186f_with_Earth.png", "name": "케플러-186f", "expl": "지구와 크기가 비슷한 최초의 거주 가능 구역 외계 행성입니다."}
]

EXPERT_NAMES = ["NGC 6960", "Messier 87", "IC 1101", "Kepler-186f", "V838 Mon", "Sombrero Galaxy", "Quasar 3C 273", "Gravitational Lens"]

# --- 3. 세션 상태 초기화 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'answered': False,
        'hint_used': False
    })

# --- 4. 데이터 로직 ---
def fetch_game_data():
    pool = []
    with st.status("🚀 우주 경로 탐색 중...", expanded=True) as status:
        try:
            # 1~4라운드용 NASA 데이터 (랜덤하게)
            res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=10", timeout=5).json()
            for item in res:
                if item.get("media_type") == "image":
                    title = item.get("title", "").lower()
                    # 5라운드 제외 키워드 (1-4라운드는 자유롭게)
                    pool.append({"url": item['url'], "name": item['title'], "type": "CHECK", "expl": item['explanation']})
                if len(pool) >= 4: break
        except:
            pass

        # 4장까지 부족하면 Normal DB 사용
        if len(pool) < 4:
            pool.extend(random.sample(NORMAL_DB, 4 - len(pool)))
        
        # 5라운드용: 반드시 태양계를 벗어난 심우주 데이터 추가
        pool = pool[:4]
        pool.append(random.choice(DEEP_SPACE_DB))
        
        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
        status.update(label="✅ 탐사 준비 완료!", state="complete", expanded=False)
    st.rerun()

def get_category(q):
    if "type" in q and q['type'] != "CHECK": return q['type']
    txt = (q['name'] + q['expl']).lower()
    if "galaxy" in txt: return "은하 (Galaxy)"
    if "nebula" in txt: return "성운 (Nebula)"
    if "planet" in txt: return "행성 (Planet)"
    if "star" in txt or "cluster" in txt: return "항성/성단 (Star)"
    if "moon" in txt: return "위성 (Moon)"
    return "기타 천체"

# --- 5. UI 화면 ---

if st.session_state.game_state == "START":
    st.title("🌌 Cosmic Master: Deep Space Edition")
    st.markdown("""
    - **1-4라운드**: 주변 우주 천체 맞히기 (난이도 중)
    - **5라운드**: 태양계를 벗어난 **심우주(Deep Space)** 탐사 (난이도 상)
    - **힌트**: 정답 확률을 50%로 높여주지만, 점수는 절반만 획득합니다.
    """)
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        fetch_game_data()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"🚀 라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(cur['url'], use_container_width=True)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 사용 (선택지 2개로 축소 / -10점)"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 난이도별 정답 설정
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 **종류**는?")
            correct = get_category(cur)
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 천체"]
        elif st.session_state.round < 4:
            st.warning("🎯 이 천체의 **이름**은?")
            correct = cur['name']
            distractors = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
            options = distractors + [correct]
        else:
            st.error("🔥 **최종 라운드: 심우주(Deep Space) 탐사**")
            st.write("이 천체는 태양계 밖 아주 먼 곳에 있습니다. 명칭은?")
            correct = cur['name']
            distractors = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
            options = distractors + [correct]
        
        # 힌트 적용 로직 (선택지 2개로 줄이기)
        if st.session_state.hint_used and not st.session_state.answered:
            # 정답 1개 + 오답 1개만 남김
            wrong_one = random.choice([o for o in options if o != correct])
            options = [correct, wrong_one]
            random.shuffle(options)
            st.warning("힌트 적용: 정답 후보가 2개로 압축되었습니다.")

        # 버튼 인터페이스
        for i, opt in enumerate(options):
            if st.button(opt, key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답입니다! (+{reward}점)")
                else:
                    st.error(f"오답입니다! 정답은: {correct}")
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
    st.title("🏁 임무 완료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("새로운 탐사 시작", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()

# 사이드바 점수판
st.sidebar.title("📊 탐사 관제소")
st.sidebar.write(f"현재 점수: {st.session_state.score}")
