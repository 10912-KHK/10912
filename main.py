import streamlit as st
import random
from datetime import datetime, timedelta

st.title("👨‍🚀 우주 타임머신 퀴즈")

# 1. 무작위 날짜 생성
if 'random_date' not in st.session_state:
    start_date = datetime(1995, 6, 16)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    st.session_state.random_date = start_date + timedelta(days=random_number_of_days)

# 2. 문제 출제
st.subheader("이 사진은 언제 촬영된 것일까요?")
# (여기에 이전 NASA API 코드를 넣어 사진을 불러옵니다)
st.image(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={st.session_state.random_date.strftime('%Y-%m-%d')}")

# 3. 정답 입력
user_answer = st.number_input("연도를 맞춰보세요 (예: 2023)", min_value=1995, max_value=2024)

if st.button("정답 확인"):
    if user_answer == st.session_state.random_date.year:
        st.balloons()
        st.success(f"정답입니다! 정확한 날짜는 {st.session_state.random_date} 였습니다.")
        del st.session_state.random_date # 새로운 게임을 위해 날짜 초기화
    else:
        st.error("틀렸습니다! 다시 생각해보세요.")
