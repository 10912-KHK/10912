import streamlit as st
import requests
import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="슈퍼 우주 퀴즈", page_icon="🌌", layout="centered")

# --- 2. 검증된 우주 데이터셋 ---
MASTER_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg/600px-Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg", "name": "창조의 기둥", "type": "성운 (Nebula)", "expl": "거대한 가스 기둥입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Saturn_during_Equinox.jpg/600px-Saturn_during_Equinox.jpg", "name": "토성", "type": "행성 (Planet)", "expl": "고리가 아름다운 가스 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/NGC_4414_%28NASA-Hubble%29.jpg/600px-NGC_4414_%28NASA-Hubble%29.jpg", "name": "나선 은하 NGC 4414", "type": "은하 (Galaxy)", "expl": "나선 팔을 가진 은하입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Appearance_of_the_Moon_during_the_Lunar_Eclipse_of_August_28_2007.jpg/600px-Appearance_of_the_Moon_during_the_Lunar_Eclipse_of_August_28_2007.jpg", "name": "달", "type": "위성 (Moon)", "expl": "지구의 동반자 위성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/600px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg", "name": "목성", "type": "행성 (Planet)", "expl": "태양계의 왕이라 불리는 가스 거대 행성입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mars_atmosphere.jpg/600px-Mars_atmosphere.jpg", "name": "화성", "type": "행성 (Planet)", "expl": "붉은 표면을 가진 지구의 이웃 행성입니다."}
]

DEEP_SPACE_POOL = [
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Crab_Nebula.jpg/600px-Crab_Nebula.jpg", "name": "게성운", "type": "성운 (Nebula)", "expl": "초신성 폭발의 잔해입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/600px-Black_hole_-_Messier_87_crop_max_res.jpg", "name": "M87 블랙홀", "type": "기타 (Black Hole)", "expl": "인류 최초 촬영 블랙홀입니다."},
    {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/M104_ngc4594_sombrero_galaxy_hi-res.jpg/600px-M104_ngc4594_sombrero_galaxy_hi-res.jpg", "name": "솜브레로 은하", "type": "은하 (Galaxy)", "expl": "모양새가 모자를 닮은 은하입니다."}
]

FAKE_NAMES = ["NGC 6960", "IC 1101", "Kepler-186f", "V838 Mon", "Abell 2744", "Horsehead Nebula", "Eagle Nebula"]

# --- 3. 이미지 처리 함수 ---
def create_emergency_image(name):
    """인터넷이 아예 안될 때 직접 그림을 그려주는 비상 시스템"""
    img = Image.new('RGB', (600, 400), color=(10, 10, 30))
    d = ImageDraw.Draw(img)
    d.ellipse([150, 50, 450, 350], fill=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 255)))
    d.text((250, 180), "Deep Space", fill=(255, 255, 255))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_base64_img(url, name):
    """보안 네트워크를 우회하여 사진을 전송"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((600, 600))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        # 사진 못 가져오면 비상용 그림 생성 (절대 오류 안 남)
        return create_emergency_image(name)

# --- 4. 세션 상태 관리 ---
if 'game_state' not in st.session_state:
    st.session_state.update({'game_state': "START", 'quiz_pool': [], 'round': 0, 'score': 0, 'answered': False, 'hint_used': False})

# --- 5. 게임 로직 ---
def prepare_new_game():
    with st.spinner("🚀 우주 관측 데이터를 준비 중입니다..."):
        # 1-4라운드 랜덤 추출 및 5라운드 심우주 추출
        q14 = random.sample(MASTER_POOL, 4)
        q5 = [random.choice(DEEP_SPACE_POOL)]
        full_pool = q14 + q5
        
        # 데이터를 돌면서 사진을 미리 구움 (Base64 변환)
        new_pool = []
        for item in full_pool:
            temp = item.copy()
            temp['b64'] = get_base64_img(item['url'], item['name'])
            new_pool.append(temp)
        
        st.session_state.quiz_pool = new_pool
        st.session_state.game_state = "PLAYING"
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.hint_used = False
    st.rerun()

# --- 6. 화면 구성 ---
if st.session_state.game_state == "START":
    st.title("🔭 슈퍼 심우주 퀴즈 챌린지")
    st.write("---")
    st.info("이 게임은 사진 전송이 차단된 환경에서도 비상 이미지를 생성하여 100% 작동합니다.")
    if st.button("탐사 시작 🚀", use_container_width=True):
        prepare_new_game()

elif st.session_state.game_state == "PLAYING":
    cur = st.session_state.quiz_pool[st.session_state.round]
    st.subheader(f"라운드 {st.session_state.round + 1} / 5")
    st.progress((st.session_state.round + 1) / 5)
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.image(f"data:image/jpeg;base64,{cur['b64']}", use_container_width=True)
        if not st.session_state.answered and not st.session_state.hint_used:
            if st.button("💡 힌트 (50:50 / -10점)", key=f"h_{st.session_state.round}"):
                st.session_state.hint_used = True
                st.rerun()

    with col2:
        if st.session_state.round < 2:
            st.info("🎯 천체 종류 맞히기")
            correct = cur['type']
            options = ["은하 (Galaxy)", "성운 (Nebula)", "행성 (Planet)", "항성/성단 (Star)", "위성 (Moon)", "태양 (Sun)", "기타 (Black Hole)"]
        else:
            st.warning("🎯 천체 이름 맞히기")
            correct = cur['name']
            distractors = random.sample([n for n in FAKE_NAMES if n != correct], 3)
            options = distractors + [correct]

        if st.session_state.hint_used and not st.session_state.answered:
            wrong = [o for o in options if o != correct][0]
            options = [correct, wrong]
            random.shuffle(options)

        for i, opt in enumerate(options):
            if st.button(opt, key=f"b_{st.session_state.round}_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == correct:
                    st.session_state.score += (10 if st.session_state.hint_used else 20)
                    st.success("정답입니다! 🎉")
                else:
                    st.error(f"오답입니다. 정답은: {correct}")
                st.write(f"**📚 설명:** {cur['expl']}")

        if st.session_state.answered:
            if st.button("다음으로 전진 ➡️", key=f"n_{st.session_state.round}", use_container_width=True):
                st.session_state.round += 1
                st.session_state.answered = False
                st.session_state.hint_used = False
                if st.session_state.round >= 5: st.session_state.game_state = "FINISHED"
                st.rerun()

elif st.session_state.game_state == "FINISHED":
    st.balloons()
    st.title("🏁 임무 종료!")
    st.header(f"최종 점수: {st.session_state.score} / 100")
    if st.button("다시 도전하기 🚀", use_container_width=True):
        st.session_state.game_state = "START"
        st.rerun()

