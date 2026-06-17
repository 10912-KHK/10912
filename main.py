import streamlit as st
import requests
from datetime import datetime, date

# [중요] set_page_config는 반드시 스트림릿 명령 중 가장 위에 와야 합니다.
st.set_page_config(
    page_title="우주 사진 탐사선",
    page_icon="🚀",
    layout="wide"
)

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 제목 ---
st.title("🌌 NASA 오늘의 우주 사진 (APOD)")
st.write("NASA에서 제공하는 신비로운 우주 사진을 매일 확인해보세요.")

# --- 사이드바: 날짜 선택 ---
st.sidebar.header("📅 날짜 선택")
# APOD 서비스는 1995년 6월 16일부터 시작되었습니다.
selected_date = st.sidebar.date_input(
    "보고 싶은 날짜를 골라보세요",
    value=date.today(),
    min_value=date(1995, 6, 16),
    max_value=date.today()
)

# --- NASA API 호출 함수 (오류 방지 로직 포함) ---
@st.cache_data # 데이터를 캐시하여 속도를 높이고 API 호출 낭비를 방지합니다.
def fetch_nasa_apod(date_str):
    api_key = "DEMO_KEY"  # NASA 제공 공용 키
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date_str}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            return {"error": "NASA 서버 요청 제한이 초과되었습니다. 잠시 후 다시 시도해주세요."}
        else:
            return {"error": f"API 오류 (코드: {response.status_code})"}
    except requests.exceptions.RequestException as e:
        return {"error": f"네트워크 연결 오류: {e}"}

# --- 데이터 가져오기 실행 ---
data = fetch_nasa_apod(selected_date.strftime("%Y-%m-%d"))

# --- 화면 출력 부분 ---
if "error" in data:
    st.error(data["error"])
else:
    # 2컬럼 레이아웃
    col1, col2 = st.columns([1.5, 1])

    with col1:
        # 미디어 타입 체크 (사진 vs 동영상)
        media_type = data.get("media_type", "image")
        url = data.get("url")
        hd_url = data.get("hdurl", url)

        if media_type == "video":
            st.video(url)
            st.caption("📽️ 이 날은 사진 대신 영상이 제공되었습니다.")
        else:
            st.image(url, use_container_width=True, caption=data.get("title"))
            st.markdown(f"[📷 고화질 이미지 보기]({hd_url})")

    with col2:
        st.header(data.get("title", "제목 없음"))
        st.write(f"**날짜:** {data.get('date')}")
        
        # 설명글 한글 번역 기능은 없으므로 영문 그대로 표시하거나 도움말 추가
        with st.expander("📝 상세 설명 보기 (영어)", expanded=True):
            st.write(data.get("explanation", "설명이 없습니다."))
        
        if "copyright" in data:
            st.caption(f"© Copyright: {data['copyright']}")

# --- 하단 안내 ---
st.divider()
st.markdown("🚀 **Tip**: 사이드바에서 날짜를 바꾸면 해당 날짜의 우주 사진을 볼 수 있습니다!")
