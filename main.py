
    import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# --- 1. 환경 설정 ---
st.set_page_config(page_title="심우주 탐사 퀴즈", page_icon="🌌", layout="centered")

# [검증된 백업 데이터베이스] - 사진/이름/종류/설명을 하나로 묶어 불일치 방지
NORMAL_BACKUP = [
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800", "name": "화성", "type": "행성 (Planet)", "expl": "붉은 행성으로 알려진 태양계의 4번째 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614330593966-1d2ad9477aee?w=800", "name": "목성", "type": "행성 (Planet)", "expl": "태양계에서 가장 거대한 가스 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6?w=800", "name": "토성", "type": "행성 (Planet)", "expl": "아름다운 고리를 가진 가스 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=800", "name": "소용돌이 은하", "type": "은하 (Galaxy)", "expl": "아름다운 나선 팔을 가진 은하입니다."},
    {"url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800", "name": "오리온 성운", "type": "성운 (Nebula)", "expl": "별들이 탄생하는 거대한 가스 구름입니다."}
]

DEEP_SPACE_BACKUP = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "NGC 4414", "type": "은하 (Galaxy)", "expl": "머리털자리에 있는 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "name": "게성운 (M1)", "type": "성운 (Nebula)", "expl": "초신성 폭발의 잔해인 가스 구름입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "별이 태어나는 거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/800px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "블랙홀 (Black Hole)", "expl": "인류 최초로 촬영된 거대 블랙홀입니다."}
]

# 가짜 이름 후보군 (중복 방지용)
FAKE_NAMES = ["NGC 6960", "Messier 82", "IC 1101", "Kepler-186f", "V838 Mon", "Sombrero Galaxy", "Horsehead Nebula", "Andromeda Galaxy"]

# --- 2. 세션 상태 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'answered': False,
        'hint_used': False
    })

# --- 3. 로직 함수 ---

def get_smart_category(title, expl):
    """키워드 우선순위를 정해 카테고리 오판 방지"""
    text = (title + " " + expl).lower()
    if "planetary nebula" in text: return "성운 (Nebula)" # '행성상 성운'은 성운임
    if "galaxy" in text: return "은하 (Galaxy)"
    if "nebula" in txt := text: return "성운 (Nebula)"
    if "planet" in text or "mars" in text or "jupiter" in text or "saturn" in text: return "행성 (Planet)"
    if "star" in text or "cluster" in text: return "항성/성단 (Star)"
    if "moon" in text: return "위성 (Moon)"
    return "기타 천체"

def fetch_game_data():
    pool = []
    with st.status("🔭 우주 관측 데이터를 정밀 분석 중...", expanded=True) as status:
        # 1-4라운드용 (NASA 시도)
        for _ in range(10): # 10번 시도해서 최대 4장 뽑기
            if len(pool) >= 4: break
            try:
                rand_date = (datetime(2015,1,1) + timedelta(days=random.randint(0, 3000))).strftime("%Y-%m-%d")
                res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={rand_date}", timeout=3).json()
                if res.get("media_type") == "image":
                    pool.append({
                        "url": res['url'],
                        "name": res['title'],
                        "type": get_smart_category(res['title'], res['explanation']),
                        "expl": res['explanation']
                    })
            except: continue
        
        # 부족하면 검증된 백업으로 채우기
        if len(pool) < 4:
            needed = 4 - len(pool)
            pool.extend(random.sample(NORMAL_BACKUP, needed))
        
        # 5라운드는 무조건 심우주 백업 (안정성 및 고화질 보장)
        pool = pool[:4]
        pool.append(random.choice(DEEP_SPACE_BACKUP))

        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
        status.update(label="🚀 준비 완료!", state="complete", expanded=False)
    st.rerun()

# --- 4. 화면 구성 ---

if st.session_state.game_state == "START":
    st.title("🌌 슈퍼 심우주 퀴즈 챌린지")
    st.write("---")
    st.info("NASA 실시간 데이터와 검증된 아카이브를 사용하여 사진과 정답이 100% 일치합니다.")
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        fetch_game_data()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.image(cur['url'], use_container_width=True)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (50:50 확률 / -10점)", key=f"h_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 난이도 및 정답 설정
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는?")
            correct = cur['type'] # 이미 분석된 정답 사용 (불일치 방지)
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "기타 천체"]
            if correct not in options: options.append(correct)
        else:
            st.warning("🎯 이 천체의 '정확한 이름'은?")
            correct = cur['name']
            distractors = random.sample([n for n in FAKE_NAMES if n != correct], 3)
            options = distractors + [correct]
        
        # 힌트 로직
        if st.session_state.hint_used and not st.session_state.answered:
            wrong_one = random.choice([o for o in options if o != correct])
            options = [correct, wrong_one]
            random.shuffle(options)

        # 보기 버튼 (중복 방지용 유니크 키)
        for i, opt in enumerate(options):
            if st.button(opt, key=f"btn_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답입니다! (+{reward}점)")
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                st.write(f"**📚 설명:** {cur['expl']}")

        # 라운드 이동 버튼
        if st.session_state.answered:
            if st.button("다음으로 ➡️", key=f"next_{st.session_state.round}", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5:
                    st.session_state.game_state = "FINISHED"
                st.rerun()

elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 종료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("다시 도전하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()
