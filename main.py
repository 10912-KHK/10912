def visualize_future_earth():
    # 1. 데이터 설정: 미래 지구 온도 및 광도 변화 예측 (대략적 과학 데이터 기반)
    # 현재로부터 10억 년 후까지의 변화
    years_from_now = np.array([0, 100, 1000, 10000, 1000000, 100000000, 250000000, 1000000000])
    temp_change = np.array([15, 17, 20, 19, 18, 25, 35, 100]) # 평균 기온 (섭씨)

    # 2. 미래 지구 예측 이미지 가져오기 (초대륙 판게아 프록시마 가상도)
    # 위키미디어의 2억 5천만 년 후 초대륙 형성 이미지
    img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Pangea_Proxima.jpg/800px-Pangea_Proxima.jpg"
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
    except:
        img = None

    # 3. 시각화 설정 (1행 2열)
    fig = plt.figure(figsize=(15, 6), facecolor='#0a0a0a')
    
    # --- 왼쪽: 미래의 지구 모습 (초대륙) ---
    ax1 = fig.add_subplot(1, 2, 1)
    if img:
        ax1.imshow(img)
        ax1.set_title("Future Earth: Pangea Proxima\n(Approx. 250 Million Years Later)", 
                      color='cyan', fontsize=14, pad=15)
        ax1.axis('off')

    # --- 오른쪽: 지구 장기 온도 변화 그래프 ---
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_facecolor('#111111')
    
    # 로그 스케일을 사용하여 시간 흐름 시각화
    ax2.plot(years_from_now, temp_change, color='#ff4500', marker='o', linewidth=2, markersize=8)
    ax2.set_xscale('symlog', linthresh=100) # 초기 100년은 선형, 이후는 로그 스케일
    
    # 그래프 스타일링
    ax2.set_title("Predicted Global Temperature Trend", color='white', fontsize=15)
    ax2.set_xlabel("Years from Now (Log Scale)", color='white')
    ax2.set_ylabel("Average Temperature (°C)", color='white')
    ax2.tick_params(axis='both', colors='white')
    ax2.grid(True, which="both", ls="-", alpha=0.1, color='white')

    # 주석 추가
    ax2.annotate('Global Warming', xy=(100, 17), xytext=(500, 25),
                 arrowprops=dict(facecolor='yellow', shrink=0.05), color='yellow')
    ax2.annotate('Pangea Proxima', xy=(250000000, 35), xytext=(1000000, 50),
                 arrowprops=dict(facecolor='cyan', shrink=0.05), color='cyan')
    ax2.annotate('Ocean Evaporation', xy=(1000000000, 100), xytext=(10000000, 90),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red')

    plt.tight_layout()
    
    # 저장 및 출력
    print("미래 지구 변화 시각화 데이터를 생성했습니다.")
    plt.savefig("future_earth_vision.png", dpi=300, facecolor='#0a0a0a')
    plt.show()

if __name__ == "__main__":
    visualize_future_earth()
