import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from io import BytesIO

def draw_milky_way_speed():
    # 1. 데이터 설정 (단위: km/s)
    # 기준: 우주 배경 복사(CMB) 및 주요 천체 운동
    data = {
        "Earth's Rotation": 0.46,
        "Earth's Orbit": 30,
        "Solar System Orbit": 230,
        "Milky Way Speed\n(Relative to CMB)": 630
    }

    labels = list(data.keys())
    values = list(data.values())

    # 2. 배경 이미지 가져오기 (NASA/Wikimedia 공개 이미지)
    img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/The_Milky_Way_seen_from_Black_Rock_Desert%2C_Nevada.jpg/800px-The_Milky_Way_seen_from_Black_Rock_Desert%2C_Nevada.jpg"
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
    except:
        img = None # 이미지 로드 실패 시 대비

    # 3. 그래프 설정
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 배경에 이미지 삽입 (이미지가 있을 경우)
    if img:
        ax.imshow(img, extent=[-0.5, len(labels)-0.5, 0, 750], aspect='auto', alpha=0.4)

    # 4. 막대 그래프 그리기
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=2)

    # 각 막대 위에 숫자 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{height} km/s', ha='center', va='bottom', 
                color='white', fontweight='bold', fontsize=12)

    # 5. 스타일링 (다크 모드 느낌)
    ax.set_facecolor('black')
    fig.patch.set_facecolor('#111111')
    
    ax.set_title("How Fast is the Milky Way Moving?", fontsize=18, color='white', pad=20)
    ax.set_ylabel("Velocity (km/s)", color='white', fontsize=12)
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white')
    
    # 불필요한 테두리 제거
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    
    # 6. 결과 출력 및 저장
    print("그래프를 생성 중입니다... (우리 은하 이동 속도: 약 630km/s)")
    plt.savefig("milky_way_speed.png", dpi=300) # 깃허브 업로드용 이미지 저장
    plt.show()

if __name__ == "__main__":
    draw_milky_way_speed()
