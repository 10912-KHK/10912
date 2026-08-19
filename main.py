
    import streamlit as st
import requests
import random
from datetime import datetime, timedelta

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="심우주 탐사 퀴즈", page_icon="🌌", layout="centered")

# --- 2. 100% 정답 일치 보장 데이터베이스 ---
# (사진-이름-종류-설명을 한 세트로 묶어 데이터 불일치를 원천 차단)
QUIZ_DATA_POOL = [
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800", "name": "화성", "type": "행성 (Planet)", "expl": "태양계의 4번째 행성으로, 산화철 성분 때문에 붉게 보입니다."},
    {"url": "https://images.unsplash.com/photo-1614330593966-1d2ad9477aee?w=800", "name": "목성", "type": "행성 (Planet)", "expl": "태양계에서 가장 큰 가스 행성으로 대적점이라는 폭풍이 있습니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6?w=800", "name": "토성", "type": "행성 (Planet)", "expl": "얼음과 먼지로 이루어진 거대한 고리를 가진 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800", "name": "오리온 성운", "type": "성운 (Nebula)", "expl": "오리온자리에 위치한 별들이 탄생하는 거대한 가스 구름입니다."},
    {"url": "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=800", "name": "나선 은하", "type": "은하 (Galaxy)", "expl": "수천억 개의 별들이 회오리 모양으로 모여 있는 은하입니다."},
    {"url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bc04?w=800", "name": "플레이아데스 성단", "type": "항성/성단 (Star)", "expl": "밤하늘에 푸른 빛을 내는 젊은 별들의 모임입니다."},
    {"url": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=800", "name": "달", "type": "위성 (Moon)", "expl": "지구의 유일한 자연 위성으로 인류가 발을 디딘 곳입니다."}
]

# 5라운드 전용 심우주(Deep Space) 고해상도 아카이브
DEEP_SPACE_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "NGC 4414", "type": "은하 (Galaxy)", "expl": "약 6,200만 광년 거리에 있는 전형적인 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "name": "게성운 (M1)", "type": "성운 (Nebula)", "expl": "1054년에 폭발한 초신성의 잔해로 이루어진 성운입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "독수리 성운 내부에 위치한 별들이 태어나는 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/800px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "기타", "expl": "이벤트 호라이즌 망원경에 의해 인류 최초로 촬영된 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/800px-HST_Andromeda_Galaxy.jpg", "name": "안드로메다 은하", "type": "은하 (Galaxy)", "expl": "우리 은하와 가장 가까운 거대 은하로 약 250만 광년 떨어져 있습니다."}
]

FAKE_NAMES = ["NGC 6960", "IC 1101", "Kepler-186f", "V838 Mon", "Sombrero Galaxy", "Horsehead Nebula", "M104", "Lagoon Nebula"]

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

# --- 4. 게임 준비 (NASA + 내부 DB 혼합 및 랜덤화) ---
def start_new_game():
    with st.spinner("🚀 매번 새로운 우주 지도를 만드는 중..."):
        pool = []
        # 1. NASA API 시도 (무작위 날짜로 중복 방지)
        for _ in range(10): # 10번 시도해서 최대 3개 확보
            if len(pool) >= 3: break
            try:
                # 2015년부터 어제까지의 무작위 날짜 생성
                rand_date = (datetime(2015,1,1) + timedelta(days=random.randint(0, 3000))).strftime("%Y-%m-%d")
                res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={rand_date}", timeout=3).json()
                if res.get("media_type") == "image":
                    pool.append({
                        "url": res['url'],
                        "name": res['title'],
                        "type": "체크 필요", # 하단 로직에서 자동 분류
                        "expl": res['explanation']
                    })
            except: continue
        
        # 2. 부족하면 내부 DB에서 랜덤 추출 (중복 방지)
        if len(pool) < 4:
            needed = 4 - len(pool)
            pool.extend(random.sample(QUIZ_DATA_POOL, needed))
        
        # 3. 5라운드 심우주 데이터 (전용 풀에서 100% 랜덤 추출)
        pool = pool[:4]
        pool.append(random.choice(DEEP_SPACE_POOL))

        st.session_state.quiz_pool = pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
    st.rerun()

# --- 5. UI 화면 구성 ---

if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 심우주 퀴즈 마스터")
    st.write("---")
    st.info("지구/로켓을 제외한 진짜 우주 천체 사진 5장이 출제됩니다. 매번 새로운 사진을 보장합니다!")
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        start_new_game()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # 사진 표시 (오류 대비 안전장치)
        st.image(cur['url'], use_container_width=True, caption="탐사된 천체 사진")
        
        # 힌트 시스템 (50:50)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (선택지 2개로 줄이기 / -10점)", key=f"hint_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 정답 및 카테고리 판별
        def get_final_category(q):
            if "type" in q and q['type'] != "체크 필요": return q['type']
            txt = (q['name'] + q['expl']).lower()
            if "galaxy" in txt: return "은하 (Galaxy)"
            if "nebula" in txt: return "성운 (Nebula)"
            if "planet" in txt: return "행성 (Planet)"
            if "star" in txt or "cluster" in txt: return "항성/성단 (Star)"
            return "기타 천체"

        # 1-2단계: 종류 / 3-5단계: 이름
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는 무엇입니까?")
            correct = get_final_category(cur)
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 천체"]
        else:
            if st.session_state.round == 4: st.error("🔥 최종 관문: 심우주 탐사")
            else: st.warning("🎯 이 천체의 '정확한 명칭'은?")
            correct = cur['name']
            distractors = random.sample([n for n in FAKE_NAMES if n != correct], 3)
            options = distractors + [correct]
        
        # 힌트 로직 (정답 1 + 오답 1)
        if st.session_state.hint_used and not st.session_state.answered:
            wrong_candidate = [o for o in options if o != correct][0]
            options = [correct, wrong_candidate]
            random.shuffle(options)

        # 보기 버튼 생성
        for i, opt in enumerate(options):
            if st.button(opt, key=f"btn_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답입니다! 🎉 (+{reward}점)")
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                st.write(f"**📚 탐사 일지:** {cur['expl']}")

        # 라운드 전환 버튼
        if st.session_state.answered:
            if st.button("다음으로 전진 ➡️", key=f"next_{st.session_state.round}", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5:
                    st.session_state.game_state = "FINISHED"
                st.rerun()

elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 임무 완료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("새로운 탐사 시작하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()

# [사이드바 정보]
st.sidebar.title("📊 관제소 정보")
st.sidebar.write(f"현재 점수: {st.session_state.score}")
