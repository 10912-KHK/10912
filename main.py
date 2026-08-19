
import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="심우주 탐사 퀴즈", page_icon="🌌", layout="centered")

# --- 2. 100% 작동 보장 데이터베이스 (NASA 실패 대비 내장) ---
# 모든 사진은 위키미디어/언스플래쉬의 고속 서버 링크입니다.
MASTER_DB = [
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800", "name": "화성", "type": "행성 (Planet)", "expl": "붉은 행성이라 불리는 태양계 4번째 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614330593966-1d2ad9477aee?w=800", "name": "목성", "type": "행성 (Planet)", "expl": "태양계에서 가장 거대한 가스 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6?w=800", "name": "토성", "type": "행성 (Planet)", "expl": "아름다운 고리를 가진 토성입니다."},
    {"url": "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=800", "name": "나선 은하", "type": "은하 (Galaxy)", "expl": "수천억 개의 별이 소용돌이치며 모여 있는 은하입니다."},
    {"url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800", "name": "오리온 성운", "type": "성운 (Nebula)", "expl": "가스와 먼지가 모여 별이 탄생하는 곳입니다."},
    {"url": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=800", "name": "달", "type": "위성 (Moon)", "expl": "지구의 유일한 자연 위성입니다."},
    {"url": "https://images.unsplash.com/photo-1529788295308-1eace6f67388?w=800", "name": "태양", "type": "태양 (Sun)", "expl": "우리 태양계의 중심 항성입니다."},
    {"url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bc04?w=800", "name": "플레이아데스 성단", "type": "항성/성단 (Star)", "expl": "밤하늘에 푸르게 빛나는 젊은 별들의 모임입니다."}
]

# 5라운드 전용 심우주 데이터 (반드시 먼 우주)
DEEP_SPACE_DB = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "NGC 4414 나선은하", "type": "은하 (Galaxy)", "expl": "6,000만 광년 떨어진 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "name": "게성운", "type": "성운 (Nebula)", "expl": "초신성이 폭발한 후 남은 신비로운 가스 구름입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "별들이 탄생하는 거대한 먼지와 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/800px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "기타 (Black Hole)", "expl": "인류가 최초로 촬영한 거대 질량 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/800px-HST_Andromeda_Galaxy.jpg", "name": "안드로메다 은하", "type": "은하 (Galaxy)", "expl": "우리 은하와 가장 가까운 거대 은하입니다."}
]

FAKE_NAMES = ["NGC 6960", "Messier 87", "IC 1101", "Kepler-186f", "V838 Mon", "Sombrero Galaxy", "Horsehead Nebula", "M104"]

# --- 3. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'answered': False,
        'hint_used': False
    })

# --- 4. 게임 준비 로직 (API 없이 내부 DB 사용하여 즉시 로딩) ---
def init_game():
    # 1-4라운드용 랜덤 추출
    pool = random.sample(MASTER_DB, 4)
    # 5라운드용 심우주 추출
    pool.append(random.choice(DEEP_SPACE_DB))
    
    st.session_state.quiz_pool = pool
    st.session_state.game_state = "PLAYING"
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.hint_used = False
    st.rerun()

# --- 5. UI 화면 ---

# [시작 화면]
if st.session_state.game_state == "START":
    st.title("🌌 슈퍼 심우주 퀴즈 챌린지")
    st.write("---")
    st.info("실행 즉시 즐기는 고화질 우주 퀴즈! 총 5문제가 출제됩니다.")
    st.write("- 1~2단계: 종류 맞히기")
    st.write("- 3~4단계: 이름 맞히기")
    st.write("- 5단계: 심우주(Deep Space) 탐사")
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        init_game()

# [게임 진행 화면]
elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.image(cur['url'], use_container_width=True)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (선택지 2개로 축소 / -10점)", key=f"hint_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 난이도 설정
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는 무엇입니까?")
            correct = cur['type']
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Black Hole)"]
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

        # 버튼 생성
        for i, opt in enumerate(options):
            if st.button(opt, key=f"ans_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답입니다! 🎉 (+{reward}점)")
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

# [결과 화면]
elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 임무 완료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("다시 도전하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()

# [사이드바 현황]
st.sidebar.title("📊 관제소 현황")
st.sidebar.write(f"현재 라운드: {st.session_state.round + 1}")
st.sidebar.write(f"누적 점수: {st.session_state.score}")
