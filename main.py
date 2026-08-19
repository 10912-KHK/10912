import streamlit as st
import requests
import random
import time

# --- 1. 페이지 테마 설정 ---
st.set_page_config(page_title="Cosmic Master Quiz", page_icon="🔭", layout="wide")

# 우주 분위기를 위한 CSS 주입
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #1c92d2; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 방대한 데이터베이스 (NASA 실패 시 및 가짜 보기용) ---
# 실제 천체 데이터 (이름, 종류, 설명, 사실)
SPACE_DB = [
    {"url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564", "name": "오리온 성운 (M42)", "type": "성운 (Nebula)", "expl": "지구에서 가장 가까운 거대 별 형성 구역입니다.", "fact": "육안으로도 볼 수 있는 몇 안 되는 성운 중 하나입니다."},
    {"url": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5", "name": "달 (The Moon)", "type": "위성 (Moon)", "expl": "지구의 유일한 자연 위성입니다.", "fact": "달은 매년 지구에서 약 3.8cm씩 멀어지고 있습니다."},
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9", "name": "화성 (Mars)", "type": "행성 (Planet)", "expl": "태양계의 4번째 행성으로 '붉은 행성'이라 불립니다.", "fact": "화성에는 에베레스트보다 3배 높은 올림푸스 화산이 있습니다."},
    {"url": "https://images.unsplash.com/photo-1464802686167-b939a6910659", "name": "안드로메다 은하 (M31)", "type": "은하 (Galaxy)", "expl": "우리 은하와 가장 가까운 거대 나선 은하입니다.", "fact": "약 40억 년 후 우리 은하와 안드로메다는 충돌하여 하나가 됩니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6", "name": "토성 (Saturn)", "type": "행성 (Planet)", "expl": "고리가 가장 아름다운 거대 가스 행성입니다.", "fact": "토성의 밀도는 물보다 낮아, 거대한 욕조가 있다면 물에 뜰 것입니다."},
    {"url": "https://images.unsplash.com/photo-1614730321146-b6fa6a46bac4", "name": "목성 (Jupiter)", "type": "행성 (Planet)", "expl": "태양계에서 가장 거대한 행성입니다.", "fact": "목성의 '대적점'은 지구 2개가 들어갈 정도의 거대한 폭풍입니다."},
    {"url": "https://images.unsplash.com/photo-1543722530-d2c3201371e7", "name": "소용돌이 은하 (M51)", "type": "은하 (Galaxy)", "expl": "사냥개자리에 있는 전형적인 나선 은하입니다.", "fact": "동반 은하와 중력적으로 상호작용하며 아름다운 나선을 유지합니다."},
    {"url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bc04", "name": "플레이아데스 성단 (M45)", "type": "항성/성단 (Star)", "expl": "황소자리에 있는 젊은 산개 성단입니다.", "fact": "한국에서는 '좀생이별'이라는 정겨운 이름으로 불렸습니다."},
    {"url": "https://images.unsplash.com/photo-1538370910416-0411a3ee3f47", "name": "말머리 성운", "type": "성운 (Nebula)", "expl": "오리온자리에 있는 암흑 성운입니다.", "fact": "가스 구름의 모양이 말의 머리를 닮아 붙여진 이름입니다."}
]

# 전문가용 가짜 명칭 리스트 (난이도 향상용)
EXPERT_NAMES = ["NGC 6960", "Messier 87", "IC 1101", "Kepler-186f", "V838 Mon", "Sombrero Galaxy", "Abell 2744", "M104", "NGC 224", "HD 189733b"]

# --- 3. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'high_score': 0,
        'answered': False,
        'hint_used': False,
        'history': []
    })

# --- 4. 로직 함수 ---
def fetch_game_data():
    """NASA API 시도 + 실패 시 DB 믹스"""
    pool = []
    with st.status("🛰️ 심우주 네트워크 접속 중...", expanded=True) as status:
        try:
            # NASA에서 10장 시도
            res = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=10", timeout=5).json()
            for item in res:
                if item.get("media_type") == "image":
                    pool.append({
                        "url": item['url'],
                        "name": item['title'],
                        "type": "CHECK", # 나중에 판별
                        "expl": item['explanation'],
                        "fact": "실시간 NASA 관측 데이터입니다."
                    })
        except:
            pass

        # 부족분은 내부 DB에서 보충
        needed = 5 - len(pool)
        if needed > 0:
            pool.extend(random.sample(SPACE_DB, min(needed, len(SPACE_DB))))
        
        random.shuffle(pool)
        st.session_state.quiz_pool = pool[:5]
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

# --- 5. UI 화면 구성 ---

# [메인 타이틀]
st.sidebar.title("🔭 탐사 관제소")
st.sidebar.write(f"🏆 최고 점수: {st.session_state.high_score}")
st.sidebar.write(f"💰 현재 점수: {st.session_state.score}")
if st.sidebar.button("게임 리셋"):
    st.session_state.game_state = "START"
    st.rerun()

# [시작 화면]
if st.session_state.game_state == "START":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🌌 Cosmic Master: 우주 탐사 퀴즈")
        st.markdown("""
        이 게임은 NASA의 실시간 데이터와 천문학 데이터베이스를 결합한 본격 우주 맞히기 게임입니다.
        
        **[게임 규칙]**
        1. **1-2 라운드**: 천체의 종류(은하, 성운 등)를 맞히세요. (각 20점)
        2. **3-4 라운드**: 천체의 이름을 맞히세요. (각 20점)
        3. **5 라운드**: 전문가 난이도! 정확한 명칭을 고르세요. (20점)
        
        **[힌트]**
        - 설명을 미리 볼 수 있지만, 해당 라운드 점수가 절반으로 깎입니다.
        """)
        if st.button("탐사 시작하기 🚀", use_container_width=True):
            fetch_game_data()
    with col2:
        st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500", caption="Deep Space Network")

# [게임 진행 화면]
elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    # 상단 정보부
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.subheader(f"🚀 라운드 {st.session_state.round + 1} / 5")
        st.progress((st.session_state.round + 1) / 5)
    with col_b:
        st.write(f"**현재 점수: {st.session_state.score}**")

    st.write("---")

    # 메인 퀴즈부
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.image(cur['url'], use_container_width=True, caption="제시된 천체")
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 사용 (설명 미리보기 -10점)"):
                st.session_state.hint_used = True
                st.rerun()
        
        if st.session_state.hint_used:
            st.warning(f"**힌트:** {cur['expl'][:150]}...")

    with c2:
        # 난이도별 정답 및 보기 구성
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 **종류**는 무엇입니까?")
            correct = get_category(cur)
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 천체"]
        else:
            st.warning("🎯 이 천체의 **정확한 이름**은 무엇입니까?")
            correct = cur['name']
            # 가짜 정답 섞기
            distractors = random.sample([n for n in EXPERT_NAMES if n != correct], 3)
            options = distractors + [correct]
            random.shuffle(options)

        # 버튼 레이아웃 (2열)
        b_cols = st.columns(2)
        for i, opt in enumerate(options):
            with b_cols[i % 2]:
                if st.button(opt, key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                    st.session_state.answered = True
                    if opt == correct:
                        reward = 10 if st.session_state.hint_used else 20
                        st.session_state.score += reward
                        st.success(f"🎊 정답입니다! (+{reward}점)")
                    else:
                        st.error(f"😱 오답입니다! 정답은: {correct}")
                    
                    st.markdown(f"**🔭 상세 설명:** {cur['expl']}")
                    st.markdown(f"**✨ 흥미로운 사실:** {cur['fact']}")

        if st.session_state.answered:
            if st.button("다음 라운드로 전진 ➡️", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5:
                    st.session_state.game_state = "FINISHED"
                st.rerun()

# [게임 결과 화면]
elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 임무 완료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
        st.write("🔥 **새로운 최고 기록 달성!**")

    # 등급 평가
    if st.session_state.score == 100: grade = "🌌 우주의 지배자 (Perfect)"
    elif st.session_state.score >= 70: grade = "🔭 수석 천문학자"
    elif st.session_state.score >= 40: grade = "🚀 베테랑 우주 비행사"
    else: grade = "👶 우주 꿈나무"
    
    st.info(f"당신의 우주 등급: **{grade}**")
    
    if st.button("새로운 탐사 시작", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()
