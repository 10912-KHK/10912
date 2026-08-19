import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🌌", layout="centered")

# --- 2. 내장 이미지 데이터베이스 (사진-이름-종류-설명을 완벽히 매칭) ---
# [1~4라운드용 일반 풀]
NORMAL_POOL = [
    {"url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800", "name": "화성", "type": "행성 (Planet)", "expl": "산화철 성분 때문에 붉게 보이는 태양계의 4번째 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1614330593966-1d2ad9477aee?w=800", "name": "목성", "type": "행성 (Planet)", "expl": "태양계에서 가장 거대한 가스 행성으로 줄무늬와 대적점이 특징입니다."},
    {"url": "https://images.unsplash.com/photo-1614313913007-2b4ae8ce32d6?w=800", "name": "토성", "type": "행성 (Planet)", "expl": "얼음 조각과 먼지로 이루어진 거대한 고리를 가진 행성입니다."},
    {"url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800", "name": "오리온 성운", "type": "성운 (Nebula)", "expl": "밤하늘에서 가장 밝은 성운 중 하나로, 별들이 탄생하는 구역입니다."},
    {"url": "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=800", "name": "소용돌이 은하", "type": "은하 (Galaxy)", "expl": "회오리 모양의 나선 팔을 가진 전형적인 나선 은하입니다."},
    {"url": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=800", "name": "보름달", "type": "위성 (Moon)", "expl": "지구의 유일한 자연 위성으로, 태양 빛을 반사해 빛납니다."},
    {"url": "https://images.unsplash.com/photo-1529788295308-1eace6f67388?w=800", "name": "태양", "type": "태양 (Sun)", "expl": "우리 태양계의 중심 항성으로, 스스로 빛을 내는 거대한 가스 덩어리입니다."},
    {"url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bc04?w=800", "name": "플레이아데스 성단", "type": "항성/성단 (Star)", "expl": "푸르게 빛나는 젊은 별들이 모여 있는 산개 성단입니다."},
    {"url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800", "name": "우주 성간 먼지", "type": "기타", "expl": "별과 별 사이를 채우고 있는 차가운 가스와 먼지 구름입니다."},
    {"url": "https://images.unsplash.com/photo-1614730321146-b6fa6a46bac4?w=800", "name": "가스 행성 내부", "type": "행성 (Planet)", "expl": "거대 가스 행성의 대기 소용돌이를 가까이서 본 모습입니다."}
]

# [5라운드용 심우주(Deep Space) 풀] - 태양계 밖 먼 곳
DEEP_SPACE_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/800px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "NGC 4414", "type": "은하 (Galaxy)", "expl": "약 6,200만 광년 떨어진 머리털자리에 위치한 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/800px-Crab_Nebula.jpg", "name": "게성운", "type": "성운 (Nebula)", "expl": "1054년에 폭발한 초신성의 잔해가 만든 신비로운 가스 구름입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/800px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "독수리 성운 중심부에 있는 거대한 가스와 먼지 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/800px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "기타", "expl": "인류가 최초로 직접 촬영에 성공한 거대 질량 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/800px-HST_Andromeda_Galaxy.jpg", "name": "안드로메다 은하", "type": "은하 (Galaxy)", "expl": "약 250만 광년 거리에 있는 우리 은하의 가장 가까운 이웃 은하입니다."}
]

# 오답용 가짜 이름들
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

# --- 4. 게임 로직 ---
def init_new_game():
    # 1-4라운드는 일반 풀에서 무작위 4개 추출
    q_1_4 = random.sample(NORMAL_POOL, 4)
    # 5라운드는 심우주 풀에서 무작위 1개 추출
    q_5 = [random.choice(DEEP_SPACE_POOL)]
    
    st.session_state.quiz_pool = q_1_4 + q_5
    st.session_state.game_state = "PLAYING"
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.hint_used = False
    st.rerun()

# --- 5. UI 화면 구성 ---

# [시작 화면]
if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 우주 탐사 퀴즈")
    st.write("---")
    st.info("검증된 우주 아카이브 사진 5장이 출제됩니다. 매 게임마다 사진과 순서가 바뀝니다!")
    if st.button("탐사 시작 🚀", use_container_width=True):
        init_new_game()

# [게임 진행 화면]
elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # 사진 표시 (이미 저장된 신뢰도 높은 링크 사용)
        st.image(cur['url'], use_container_width=True)
        
        # 힌트 시스템 (50:50)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (선택지 2개로 줄이기 / -10점)", key=f"hint_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 문제 설정
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는?")
            correct = cur['type']
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타"]
        else:
            if st.session_state.round == 4: st.error("🔥 최종 라운드: 심우주(Deep Space) 탐사")
            else: st.warning("🎯 이 천체의 '정확한 이름'은?")
            correct = cur['name']
            distractors = random.sample([n for n in FAKE_NAMES if n != correct], 3)
            options = distractors + [correct]
        
        # 힌트 로직 (정답 1 + 오답 1)
        if st.session_state.hint_used and not st.session_state.answered:
            wrong_one = [o for o in options if o != correct][0]
            options = [correct, wrong_one]
            random.shuffle(options)

        # 버튼 생성
        for i, opt in enumerate(options):
            if st.button(opt, key=f"btn_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    reward = 10 if st.session_state.hint_used else 20
                    st.session_state.score += reward
                    st.success(f"정답! 🎉 (+{reward}점)")
                else:
                    st.error(f"오답! 정답은: {correct}")
                st.write(f"**📚 탐사 메모:** {cur['expl']}")

        # 라운드 전환 버튼
        if st.session_state.answered:
            if st.button("다음으로 전진 ➡️", key=f"next_{st.session_state.round}", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5:
                    st.session_state.game_state = "FINISHED"
                st.rerun()

# [결과 화면]
elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 탐사 임무 종료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("새로운 탐사 시작하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()
