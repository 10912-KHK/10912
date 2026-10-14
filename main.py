import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(page_title="우주 천체 탐험 퀴즈", layout="centered")

st.title("🚀 신비로운 우주 천체 탐험 퀴즈")

# 5가지 우주 천체 데이터 (거리, 생성 시기, 크기 순위 등 세부 정보 포함)
quiz_data = [
    {
        "question": "방패자리 방향으로 불타오르는 듯한 붉은빛의 초거성, 태양 반지름의 약 2,150배에 달하는 거대한 체적을 자랑하는 이 별은 무엇일까요? 태양계 중심에 놓는다면 그 표면은 토성 궤도를 넘어설 정도로 압도적인 크기를 가집니다.",
        "image": "https://unsplash.com",
        "options": ["스테파니손 2-18", "베텔게우스", "안타레스", "VY 캔이스 마요리스"],
        "answer": "스테파니손 2-18",
        "reason": "스테파니손 2-18은 현재 인류가 관측한 가장 거대한 항성 순위 최상위권에 위치한 초거성입니다."
    },
    {
        "question": "지구에서 약 250만 광년 떨어져 있으며, 약 40억~45억 년 뒤 우리 은하와 완전히 충돌하여 하나의 거대한 은하를 이룰 예정인 이웃 은하의 이름은 무엇일까요?",
        "image": "https://unsplash.com",
        "options": ["안드로메다 은하", "마젤란 은하", "솜브레로 은하", "삼각자리 은하"],
        "answer": "안드로메다 은하",
        "reason": "안드로메다 은하는 약 250만 광년 떨어져 있으며 중력에 의해 우리 은하와 점점 가까워지고 있습니다."
    },
    {
        "question": "태양 질량의 약 660억 배라는 상상을 초월하는 초거대 질량을 가졌으며, 사방으로 강력한 에너지를 토해내며 우주 최고 순위를 다투는 초대질량 블랙홀은 무엇일까요?",
        "image": "https://unsplash.com",
        "options": ["TON 618", "궁수자리 A*", "M87 블랙홀", "시그너스 X-1"],
        "answer": "TON 618",
        "reason": "TON 618은 현재까지 인류가 발견한 블랙홀 중 가장 무겁고 거대한 규모를 가집니다."
    },
    {
        "question": "허블과 제임스 웹 우주망원경이 포착한 가장 경이로운 우주 풍경 중 하나인 '창조의 기둥(Pillars of Creation)'입니다. 독수리 성운(M16) 내부에 위치한 이 가스 기둥은 지구로부터 약 6,500광년 떨어져 있습니다. 주로 어떤 성분으로 이루어져 있을까요?",
        "image": "https://unsplash.com",
        "options": ["차가운 수소 가스와 우주 먼지", "고온의 플라즈마와 철 입자", "액체 메탄และ 얼음 결정", "산소 가스와 규산염 암석"],
        "answer": "차가운 수소 가스와 우주 먼지",
        "reason": "창조의 기둥은 차가운 가스와 성간 먼지들이 중력으로 뭉치며 끊임없이 아기 별들이 태어나는 요람입니다."
    },
    {
        "question": "천칭자리 방향에 위치하며 은빛으로 고요하게 빛나는 HD 140283입니다. 나이가 무려 약 135억 년으로 추정되어 빅뱅 직후 우주 초기 환경의 비밀을 고스란히 간직하고 있는 이 최고령 별의 별명은 무엇일까요?",
        "image": "https://unsplash.com",
        "options": ["므두셀라 별 (HD 140283)", "프록시마", "폴라리스", "리겔"],
        "answer": "므두셀라 별 (HD 140283)",
        "reason": "우주 전체 나이(약 138억 년) 직후에 태어나 우주 역사상 최고령 나이 순위를 자랑하며 성경 속 인물의 이름을 땄습니다."
    }
]

# 시스템 변수 초기화 (에러 방지 딕셔너리 구조)
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "current_idx": 0,
        "score": 0,
        "submitted": False,
        "scored_questions": set()
    }

state = st.session_state.game_state
idx = state["current_idx"]

# 게임 진행 구문
if idx < len(quiz_data):
    current = quiz_data[idx]
    st.subheader(f"🎵 문제 {idx + 1} / {len(quiz_data)}")
    
    # 고화질 우주 이미지 출력
    st.image(current["image"], use_container_width=True)
    st.write(current["question"])
    
    # 사용자 선택 라디오 버튼
    choice = st.radio("정답을 선택하세요:", current["options"], key=f"radio_{idx}")
    
    # 제출 및 다음 문제 제어 버튼
    if not state["submitted"]:
        if st.button("정답 확인하기", key=f"submit_{idx}"):
            state["submitted"] = True
            st.rerun()
            
    if state["submitted"]:
        if choice == current["answer"]:
            st.success(f"⭕ 정답입니다! \n\n {current['reason']}")
            if idx not in state["scored_questions"]:
                state["score"] += 1
                state["scored_questions"].add(idx)
        else:
            st.error(f"❌ 오답입니다! 정답은 [{current['answer']}] 입니다. \n\n {current['reason']}")
            
        if st.button("다음 문제로 이동 ➡️", key=f"next_{idx}"):
            state["current_idx"] += 1
            state["submitted"] = False
            st.rerun()
else:
    # 최종 결과 화면
    st.balloons()
    st.success("🌌 우주 탐험 완료! 모든 문제를 해결하셨습니다.")
    st.metric(label="최종 획득 점수", value=f"{state['score']} / {len(quiz_data)}")
    
    if st.button("다시 도전하기 🔄"):
        st.session_state.game_state = {
            "current_idx": 0,
            "score": 0,
            "submitted": False,
            "scored_questions": set()
        }
        st.rerun()

