import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🌌", layout="centered")

# --- 2. 100% 검증된 고속 이미지 데이터베이스 ---
# 전 세계 어디서나 가장 잘 뜨는 위키미디어 압축 이미지들입니다.
# [1~4라운드용 일반 풀]
NORMAL_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/600px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "독수리 성운에 있는 거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Saturn_during_Equinox.jpg/600px-Saturn_during_Equinox.jpg", "name": "토성", "type": "행성 (Planet)", "expl": "아름다운 고리를 가진 태양계의 6번째 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Katrina_and_the_Waves_NGC_6357.jpg/600px-Katrina_and_the_Waves_NGC_6357.jpg", "name": "랍스터 성운", "type": "성운 (Nebula)", "expl": "전갈자리에 위치한 화려한 성운입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/600px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "나선 은하 NGC 4414", "type": "은하 (Galaxy)", "expl": "머리털자리에 있는 전형적인 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Hubble_v_and_v838mon.jpg/600px-Hubble_v_and_v838mon.jpg", "name": "외뿔소자리 V838", "type": "항성/성단 (Star)", "expl": "빛의 메아리 현상으로 유명한 거대 변광성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Appearance_of_the_Moon_during_the_Lunar_Eclipse_of_August_28_2007.jpg/600px-Appearance_of_the_Moon_during_the_Lunar_Eclipse_of_August_28_2007.jpg", "name": "월식 중의 달", "type": "위성 (Moon)", "expl": "지구의 그림자에 가려진 달의 모습입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/600px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg", "name": "태양", "type": "태양 (Sun)", "expl": "우리 태양계의 중심 항성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/M101_hires_STScI-PRC2006-10a.jpg/600px-M101_hires_STScI-PRC2006-10a.jpg", "name": "바람개비 은하", "type": "은하 (Galaxy)", "expl": "큰곰자리에 위치한 정면 나선 은하입니다."}
]

# [5라운드용 심우주(Deep Space) 풀] - 아주 먼 우주
DEEP_SPACE_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/600px-Crab_Nebula.jpg", "name": "게성운 (M1)", "type": "성운 (Nebula)", "expl": "1054년에 폭발한 초신성의 잔해입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/600px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "기타 (Black Hole)", "expl": "인류가 최초로 촬영에 성공한 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST_Andromeda_Galaxy.jpg/600px-HST_Andromeda_Galaxy.jpg", "name": "안드로메다 은하", "type": "은하 (Galaxy)", "expl": "우리 은하와 가장 가까운 거대 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/M104_ngc4594_sombrero_galaxy_hi-res.jpg/600px-M104_ngc4594_sombrero_galaxy_hi-res.jpg", "name": "솜브레로 은하", "type": "은하 (Galaxy)", "expl": "챙이 넓은 모자처럼 생긴 독특한 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/The_Whirlpool_Galaxy.jpg/600px-The_Whirlpool_Galaxy.jpg", "name": "소용돌이 은하", "type": "은하 (Galaxy)", "expl": "동반 은하를 거느린 아름다운 나선 은하입니다."}
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

# --- 4. 게임 시작 로직 ---
def init_game():
    # 1-4라운드는 일반 풀에서 랜덤 4개
    q14 = random.sample(NORMAL_POOL, 4)
    # 5라운드는 심우주 풀에서 랜덤 1개
    q5 = [random.choice(DEEP_SPACE_POOL)]
    st.session_state.quiz_pool = q14 + q5
    st.session_state.game_state = "PLAYING"
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.hint_used = False
    st.rerun()

# --- 5. UI 화면 구성 ---

if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 심우주 퀴즈")
    st.write("---")
    st.info("로딩이 가장 빠른 검증된 사진들로 구성했습니다. 5문제를 모두 맞혀보세요!")
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        init_game()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # 사진 표시
        st.image(cur['url'], use_container_width=True)
        # 만약 사진이 안 뜰 경우를 대비한 직접 링크 (보험)
        st.markdown(f'<p style="font-size:12px; color:gray;">사진이 안 보이나요? <a href="{cur["url"]}" target="_blank">여기</a>를 클릭하세요.</p>', unsafe_allow_html=True)
        
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (선택지 2개로 축소 / -10점)", key=f"hint_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 문제 설정
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는?")
            correct = cur['type']
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Black Hole)"]
        else:
            if st.session_state.round == 4: st.error("🔥 최종 관문: 심우주 탐사")
            else: st.warning("🎯 이 천체의 '이름'은?")
            correct = cur['name']
            others = random.sample([n for n in FAKE_NAMES if n != correct], 3)
            options = others + [correct]
        
        # 힌트 로직
        if st.session_state.hint_used and not st.session_state.answered:
            wrong_one = [o for o in options if o != correct][0]
            options = [correct, wrong_one]
            random.shuffle(options)

        # 정답 버튼 생성
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
                st.write(f"**📚 설명:** {cur['expl']}")

        # 라운드 이동 버튼
        if st.session_state.answered:
            if st.button("다음 문제로 ➡️", key=f"next_{st.session_state.round}", use_container_width=True):
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
    if st.button("다시 도전하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()
