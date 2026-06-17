import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from io import BytesIO

def visualize_cosmic_expansion():
    # 1. 데이터 설정 (허블의 법칙: v = H0 * d)
    # H0 (허블 상수)는 약 70 km/s/Mpc로 가정
    h0 = 70 
    distances = np.linspace(0, 500, 50) # 거리 (단위: 백만 파섹, Mpc)
    velocities = h0 * distances         # 후퇴 속도 (단위: km/s)

    # 2. 우주 팽창 타임라인 이미지 가져오기 (NASA/WMAP 제공)
    img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/CMB_Timeline300_no_text.jpg/800px-CMB_Timeline300_no_text.jpg"
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
    except:
        img = None

    # 3. 그래프 그리기 (1행 2열 구성)
    fig = plt.subplots(figsize=(14, 6), facecolor='#050505')
    
    # --- 왼쪽: 우주 팽창 이미지 ---
    ax1 = plt.subplot(1, 2, 1)
    if img:
        ax1.imshow(img)
        ax1.set_title("Cosmic Timeline (Expansion)", color='white', fontsize=14)
        ax1.axis('off') # 이미지 테두리 제거

    # --- 오른쪽: 허블의 법칙 그래프 ---
    ax2 = plt.subplot(1, 2, 2)
    ax2.set_facecolor('#050505')
    
    # 팽창 데이터를 점과 선으로 표현
    ax2.plot(distances, velocities, color='cyan', linestyle='--', alpha=0.5)
    scatter = ax2.scatter(distances, velocities, c=velocities, cmap='magma', s=50)
    
    # 그래프 꾸미기
    ax2.set_title("Hubble's Law: $v = H_0 \\cdot d$", color='white', fontsize=16)
    ax2.se
