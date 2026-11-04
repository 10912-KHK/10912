import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(page_title="우주 천체 탐험 퀴즈", layout="centered")

st.title("🚀 신비로운 우주 천체 탐험 퀴즈")

# 5가지 우주 천체 데이터 (보내주신 1번 및 3번 사진 주소 완벽 반영)
quiz_data = [
    {
        "question": "방패자리 방향으로 불타오르는 듯한 붉은빛의 초거성, 태양 반지름의 약 2,150배에 달하는 거대한 체적을 자랑하는 이 별은 무엇일까요? 태양계 중심에 놓는다면 그 표면은 토성 궤도를 넘어설 정도로 압도적인 크기를 가집니다.",
        "image": "https://mblogthumb-phinf.pstatic.net/MjAyNDA2MThfNjUg/MDAxNzE4Njg5MTU0MjU4.Vz110f47LeoErFjCBw3AKFh7oVI862wf2pCm88Gdmtgg.yqz0u8PEg5cTDBglo6uKK94-MEguVOgjIMBXVKDFdD0g.JPEG/3.jpg?type=w800", # [반영] 보내주신 스테파니손 2-18 크기 비교 사진
        "options": ["베텔게우스", "안타레스", "스테파니손 2-18", "VY 캔이스 마요리스"],
        "answer": "스테파니손 2-18",
        "reason": "스테파니손 2-18은 현재 인류가 관측한 가장 거대한 항성 순위 최상위권에 위치한 초거성입니다.",
        "background": "✨ **우주 배경지식:** 이 별의 부피는 태양의 약 100억 배에 달합니다. 빛의 속도(초속 30만km)로 이 별의 둘레를 한 바퀴 도는 데만 무려 8.7시간이 걸립니다. (태양은 단 14.5초가 걸립니다.) 현재는 두터운 우주 먼지에 가려져 있어 적외선 망원경을 통해 그 압도적인 위용을 자세히 관측하고 있습니다."
    },
    {
        "question": "지구에서 약 250만 광년 떨어져 있으며, 약 40억~45억 년 뒤 우리 은하와 완전히 충돌하여 하나의 거대한 은하를 이룰 예정인 이웃 은하의 이름은 무엇일까요?",
        "image": "https://wikimedia.org", 
        "options": ["마젤란 은하", "안드로메다 은하", "솜브레로 은하", "삼각자리 은하"],
        "answer": "안드로메다 은하",
        "reason": "안드로메다 은하는 약 250만 광년 떨어져 있으며 중력에 의해 우리 은하와 점점 가까워지고 있습니다.",
        "background": "✨ **우주 배경지식:** 안드로메다 은하와 우리 은하는 시속 약 40만km의 속도로 서로를 향해 돌진하고 있습니다. 두 은하가 충돌하더라도 별과 별 사이의 거리가 너무나도 멀기 때문에 실제로 항성끼리 정면충돌할 확률은 거의 없습니다. 충돌이 끝나면 두 은하는 하나로 합쳐져 '밀코메다(Milkomeda)'라는 거대한 타원 은하를 형성하게 됩니다."
    },
    {
        "question": "태양 질량의 약 660억 배라는 상상을 초월하는 초거대 질량을 가졌으며, 사방으로 강력한 에너지를 토해내며 우주 최고 순위를 다투는 초대질량 블랙홀은 무엇일까요?",
        "image": "https://gstatic.com", # [반영] 이전에 보내주신 TON 618 크기 비교 사진
        "options": ["궁수자리 A*", "M87 블랙홀", "시그너스 X-1", "TON 618"],
        "answer": "TON 618",
        "reason": "TON 618은 현재까지 인류가 발견한 블랙홀 중 가장 무겁고 거대한 규모를 가집니다.",
        "background": "✨ **우주 배경지식:** TON 618은 사실 블랙홀 자체가 직접 관측된 것이 아니라, 블랙홀 주변의 가스가 광속에 가까운 속도로 회전하며 엄청난 빛을 내뿜는 '퀘이사(Quasar)' 형태로 발견되었습니다. 이미지에서 보시다시피 중심부 블랙홀의 크기(사건의 지평선 지름)는 우리 태양계 전체 크기의 무려 30~40배에 달할 정도로 상상을 초월하는 규모입니다."
    },
    {
        "question": "허블과 제임스 웹 우주망원경이 포착한 가장 경이로운 우주 풍경 중 하나인 '창조의 기둥(Pillars of Creation)'입니다. 독수리 성운(M16) 내부에 위치한 이 가스 기둥은 지구로부터 약 6,500광년 떨어져 있습니다. 주로 어떤 성분으로 이루어져 있을까요?",
        "image": "https://wikimedia.org", 
        "options": ["고온의 플라즈마와 철 입자", "액체 메탄과 얼음 결정", "차가운 수소 가스와 우주 먼지", "산소 가스와 규산염 암석"],
        "answer": "차가운 수소 가스와 우주 먼지",
        "reason": "창조의 기둥은 차가운 가스와 성간 먼지들이 중력으로 뭉치며 끊임없이 아기 별들이 태어나는 요람입니다.",
        "background": "✨ **우주 배경지식:** 이 거대한 가스 기둥들의 길이는 수 광년(몇 조 킬로미터)에 이릅니다. 기둥 내부의 밀도가 높은 곳에서는 중력에 의해 가스가 뭉치면서 새로운 별들이 계속해서 태어나고 있습니다. 최근 제임스 웹 망원경은 적외선 카메라를 이용해 이 두터운 먼지 기둥을 투과하여, 기둥 속에서 붉게 빛나는 아기 별들의 모습을 인류 역사상 가장 선명하게 포착해냈습니다."
    },
    {
        "question": "천칭자리 방향에 위치하며 은빛으로 고요하게 빛나는 HD 140283입니다. 나이가 무려 약 135억 년으로 추정되어 빅뱅 직후 우주 초기 환경의 비밀을 고스란히 간직하고 있는 이 최고령 별의 별명은 무엇일까요?",
        "image": "https://wikimedia.org", 
        "options": ["므두셀라 별 (HD 140283)", "프록시마", "폴라리스", "리겔"],
        "answer": "므두셀라 별 (HD 140283)",
        "reason": "우주 전체 나이(약 138억 년) 직후에 태어나 우주 역사상 최고령 나이 순위를 자랑하며 성경 속 인물의 이름을 땄습니다.",
        "background": "✨ **우주 배경지식:** 구약성경에서 969세까지 살았다고 기록된 인물 '므두셀라'의 이름을 딴 별입니다. 이 별은 우주 초기에 만들어졌기 때문에 철이나 헬륨보다 무거운 '금속 성분'이 태양의 250분의 1 수준으로 매우 희박합니다. 한때 관측 오차로 인해 별의 나이가 우주 나이보다 많게 측정되어 과학계를 멘붕에 빠뜨렸으나, 최신 장비로 재측정하여 우주 탄생 직후인 135억 년 전 태어난 것으로 확인되었습니다."
    }
]

# 시스템 변수 초기화
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
    st.write(current["question"])
    
    # 정답 제출 전에는 라디오 버튼 활성화, 제출 후에는 비활성화
    choice = st.radio(
        "정답을 선택하세요:", 
        current["options"], 
        key=f"radio_{idx}",
        disabled=state["submitted"]
    )
    
    # 제출 및 다음 문제 제어 버튼
    if not state["submitted"]:
        if st.button("정답 확인하기", key=f"submit_{idx}"):
            state["submitted"] = True
            if choice == current["answer"]:
                if idx not in state["scored_questions"]:
                    state["score"] += 1
                    state["scored_questions"].add(idx)
            st.rerun()
            
    # 정답 제출 후에 사진과 배경지식 해설을 출력
    if state["submitted"]:
        if choice == current["answer"]:
            st.success(f"⭕ **정답입니다!** \n\n {current['reason']}")
        else:
            st.error(f"❌ **오답입니다!** 정답은 **[{current['answer']}]** 입니다. \n\n {current['reason']}")
        
        st.divider()
        st.image(current["image"], caption=f"📷 {current['answer']} 관련 이미지", use_container_width=True)
        st.info(current["background"])
        st.divider()
            
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
