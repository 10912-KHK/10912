import streamlit as st
import requests
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="우주 탐사 대시보드", page_icon="🚀", layout="wide")

# 2. 제목 및 스타일
st.title("🌌 NASA 오늘의 천문 사진 (APOD)")
st.markdown("""
이 앱은 NASA의 APOD API를 사용하여 매일 다른 우주 사진을 보여줍니다.  
원하는 날짜를 선택해서 신비로운 우주를 탐험해보세요!
""")

# 3. 사이드바 - 날짜 선택
st.sidebar.header("설정")
target_date = st.sidebar.date_input(
    "날짜를 선택하세요",
    value=datetime.now(),
    min_value=datetime(1995, 6, 16), # APOD 서비스 시작일
    max_value=datetime.now()
)

# 4. NASA API 호출 함수
def get_nasa_data(date):
    # NASA에서 제공하는 공용 데모 키를 사용합니다.
    api_key = "DEMO_KEY" 
    formatted_date = date.strftime("%Y-%m-%d")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={formatted_date}"
    
    response = requests.get(url)
    return response.json()

# 5. 데이터 표시
with st.spinner('우주에서 데이터를 가져오는 중...'):
    data = get_nasa_data(target_date)

    if "url" in data:
        col1, col2 = st.columns([1.5, 1])

        with col1:
            # 사진 또는 영상 출력
            if data.get("media_type") == "video":
                st.video(data["url"])
            else:
                st.image(data["url"], use_container_width=True, caption=data.get("title"))

        with col2:
            st.subheader(data.get("title"))
            st.info(f"📅 날짜: {data.get('date')}")
            st.write(data.get("explanation"))
            
            if "copyright" in data:
                st.caption(f"© 저작권: {data['copyright']}")
    else:
        st.error("데이터를 가져오지 못했습니다. 날짜를 다시 확인하거나 잠시 후 시도해주세요.")

# 6. 하단 정보
st.divider()
st.caption("Powered by NASA API | Created with Streamlit")
