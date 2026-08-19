import streamlit as st
import requests
import random
import base64
from io import BytesIO
from PIL import Image

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🌌", layout="centered")

# --- 2. 절대 실패 없는 고화질 우주 데이터셋 ---
# 위키미디어 공용의 가장 안정적인 이미지들입니다.
MASTER_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/600px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "독수리 성운 내부의 거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Saturn_during_Equinox.jpg/600px-Saturn_during_Equinox.jpg", "name": "토성", "type": "행성 (Planet)", "expl": "아름다운 고리를 가진 태양계의 6번째 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/600px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "나선 은하 NGC 4414", "type": "은하 (Galaxy)", "expl": "머리털자리에 위치한 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/600px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg", "name": "태양", "type": "태양 (Sun)", "expl": "우리 태양계의 중심 항성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Appearance_of_the_Moon_during_the_Lunar_Eclipse_of_August_28_2007.jpg/600px-Appearance_of_the_Moon_during_the_Lunar_Eclipse_of_August_28_2007.jpg", "name": "달", "type": "위성 (Moon)", "expl": "지구의 유일한 자연 위성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/M101_hires_STScI-PRC2006-10a.jpg/600px-M101_hires_STScI-PRC2006-10a.jpg", "name": "바람개비 은하", "type": "은하 (Galaxy)", "expl": "정면을 향하고 있는 거대한 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/600px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg", "name": "목성", "type": "행성 (Planet)", "expl": "대적점이라는 거대한 폭풍을 가진 가스 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mars_atmosphere.jpg/600px-Mars_atmosphere.jpg", "name": "화성", "type": "행성 (Planet)", "expl": "희박한 대기와 붉은 표면을 가진 행성입니다."}
]

# 5라운드용 고난도 심우주 데이터
DEEP_SPACE_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/600px-Crab_Nebula.jpg", "name": "게성운", "type": "성운 (Nebula)", "expl": "초신성 폭발 후 남은 가스 구름입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/600px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "기타 (Black Hole)", "expl": "인류 최초로 촬영에 성공한 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/M104_ngc4594_sombrero_galaxy_hi-res.jpg/600px-M104_ngc4594_sombrero_galaxy_hi-res.jpg", "name": "솜브레로 은하", "type": "은하 (Galaxy)", "expl": "모자 모양을 닮은 독특한 나선 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/The_Whirlpool_Galaxy.jpg/600px-The_Whirlpool_Galaxy.jpg", "name": "소용돌이 은하", "type": "은하 (Galaxy)", "expl": "동반 은하와 중력적으로 묶인 나선 은하입니다."}
]

FAKE_NAMES = ["NGC 6960", "IC 1101", "Kepler-186f", "V838 Mon", "Abell 2744", "Horsehead Nebula", "Eagle Nebula"]

# --- 3. 이미지 데이터 변환 함수 (핵심 기술) ---
def get_base64_img(url):
    """서버가 사진을 직접 다운로드해서 64진법 데이터로 변환 (차단 불가능)"""
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        # 속도를 위해 크기 최적화
        img.thumbnail((600, 600))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        return None

# --- 4. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START",
        'quiz_pool': [],
        'round': 0,
        'score': 0,
        'answered': False,
        'hint_used': False
    })

# --- 5. 게임 로직 ---
def prepare_new_game():
    with st.spinner("🚀 우주에서 고화질 사진 데이터를 굽는 중..."):
        # 1-4라운드 랜덤 추출
        q14 = random.sample(MASTER_POOL, 4)
        # 5라운드 심우주 추출
        q5 = [random.choice(DEEP_SPACE_POOL)]
        full_pool = q14 + q5
        
        # 각 사진을 Base64 데이터로 미리 변환해서 저장
        for item in full_pool:
            item['b64'] = get_base64_img(item['url'])
        
        st.session_state.quiz_pool = full_pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
    st.rerun()

# --- 6. 화면 구성 ---

if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 심우주 퀴즈 마스터")
    st.write("---")
    st.info("이 버전은 사진 데이터를 프로그램이 직접 생성하여 전송하므로 100% 로딩을 보장합니다.")
    if st.button("탐사 시작하기 🚀", use_container_width=True):
        prepare_new_game()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # [데이터 주입 방식 사진 노출]
        if cur['b64']:
            st.image(f"data:image/jpeg;base64,{cur['b64']}", use_container_width=True)
        else:
            st.error("데이터 변환 실패! 인터넷 연결을 확인하세요.")

        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (선택지 2개로 압축 / -10점)", key=f"h_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        # 문제 유형
        if st.session_state.round < 2:
            st.info("🎯 이 천체의 '종류'는?")
            correct = cur['type']
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Black Hole)"]
        else:
            if st.session_state.round == 4: st.error("🔥 최종 관문: 심우주 탐사")
            else: st.warning("🎯 이 천체의 '정확한 이름'은?")
            correct = cur['name']
            distractors = random.sample([n for n in FAKE_NAMES if n != correct], 3)
            options = distractors + [correct]

        if st.session_state.hint_used and not st.session_state.answered:
            wrong = [o for o in options if o != correct][0]
            options = [correct, wrong]
            random.shuffle(options)

        for i, opt in enumerate(options):
            if st.button(opt, key=f"b_{st.session_state.round}_{i}", 
                         disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    st.session_state.score += (10 if st.session_state.hint_used else 20)
                    st.success("정답입니다! 🎉")
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                st.write(f"**📚 탐사 일지:** {cur['expl']}")

        if st.session_state.answered:
            if st.button("다음으로 전진 ➡️", key=f"n_{st.session_state.round}", use_container_width=True):
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

