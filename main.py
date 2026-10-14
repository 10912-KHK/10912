import requests
import random
import re
from datetime import datetime, timedelta

# 1. NASA APOD API를 이용해 무작위 우주 사진 및 정보 가져오기
def get_random_space_trivia():
    # 2000년 이후부터 어제까지의 날짜 중 무작위 하루 선택
    start_date = datetime(2000, 1, 1)
    end_date = datetime.now() - timedelta(days=1)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    date_str = random_date.strftime("%Y-%m-%d")
    
    # NASA APOD API 호출 (무료 DEMO_KEY 사용)
    url = f"https://nasa.gov{date_str}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # 동영상 페이지인 경우 사진이 없으므로 재시도
        if data.get("media_type") != "image":
            return get_random_space_trivia()
            
        return {
            "title": data.get("title"),
            "url": data.get("url"),
            "explanation": data.get("explanation")
        }
    except Exception as e:
        print("데이터를 가져오는 중 오류가 발생했습니다. 다시 시도합니다.")
        return get_random_space_trivia()

# 2. 퀴즈 게임 실행 함수
def start_quiz_game():
    print("🚀 NASA 우주 천체 맞추기 퀴즈 게임을 시작합니다! 🚀")
    print("잠시만 기다려주세요... NASA에서 데이터를 가져오는 중입니다...\n")
    
    # 데이터 로드
    trivia = get_random_space_trivia()
    correct_answer = trivia["title"]
    
    # 오답으로 사용할 가짜 천체 이름 목록
    fake_answers = [
        "Andromeda Galaxy (M31)", "Orion Nebula (M42)", "Crab Nebula (M1)", 
        "Hubble Deep Field", "Pillars of Creation", "Jupiter's Great Red Spot",
        "Saturn's Rings", "Mars Rover Perseverance", "James Webb Space Telescope"
    ]
    
    # 정답이 오답 목록에 있다면 제거 후 3개 무작위 선택
    if correct_answer in fake_answers:
        fake_answers.remove(correct_answer)
    options = random.sample(fake_answers, 3)
    options.append(correct_answer)
    random.shuffle(options) # 보기 섞기
    
    # 퀴즈 출제
    print("======= [ QUIZ ] =======")
    print(f"📷 힌트 사진 (링크를 클릭해 확인하세요!):")
    print(f"👉 {trivia['url']}\n")
    
    # 설명문에서 정답 단어가 포함되어 있다면 매스킹(***) 처리하여 힌트로 제공
    masked_explanation = re.sub(re.escape(correct_answer), " [ 정답 천체 ] ", trivia["explanation"], flags=re.IGNORECASE)
    print("📝 천체 설명 (영문 힌트):")
    print(f"{masked_explanation[:400]}...\n") # 너무 길면 잘라서 출력
    
    print("❓ 다음 중 사진 속 천체의 이름은 무엇일까요?")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
        
    # 사용자 입력 받기
    while True:
        try:
            user_input = int(input("\n정답 번호를 입력하세요 (1~4): "))
            if 1 <= user_input <= 4:
                break
            print("1에서 4 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("숫자만 입력 가능합니다.")
            
    # 정답 확인
    selected_answer = options[user_input - 1]
    if selected_answer == correct_answer:
        print("\n🎉 정답입니다! 우주 전문가이시군요! 🧑‍🚀")
    else:
        print(f"\n❌ 아쉽게도 틀렸습니다. 정답은 [{correct_answer}] 입니다.")
        
    print(f"\n✨ 이 천체의 풀 네임: {trivia['title']}")

# 게임 실행
if __name__ == "__main__":
    start_quiz_game()
