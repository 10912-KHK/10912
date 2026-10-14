<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 NASA 우주 천체 맞추기 퀴즈</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #ffffff; text-align: center; padding: 20px; margin: 0; }
        .container { max-width: 600px; margin: 0 auto; background: #161d30; padding: 30px; border-radius: 15px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
        h1 { color: #4dadff; font-size: 24px; margin-bottom: 20px; }
        #space-img { max-width: 100%; max-height: 350px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: none; margin-left: auto; margin-right: auto; }
        .loading { font-size: 18px; color: #aaa; margin: 40px 0; }
        .options-grid { display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 20px; }
        button { background-color: #243454; color: white; border: 2px solid #3b5382; padding: 14px; font-size: 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; text-align: left; padding-left: 20px; }
        button:hover { background-color: #3b5382; border-color: #4dadff; }
        #result { margin-top: 25px; font-size: 20px; font-weight: bold; }
        #next-btn { background-color: #00aa6c; border: none; text-align: center; padding: 12px 25px; display: none; margin: 20px auto 0 auto; border-radius: 25px; font-weight: bold; }
        #next-btn:hover { background-color: #00cc82; }
    </style>
</head>
<body>

<div class="container">
    <h1>🌌 NASA 천체 맞추기 퀴즈</h1>
    <div id="loading" class="loading">🔄 NASA에서 무작위 우주 사진을 불러오는 중...</div>
    <img id="space-img" alt="NASA Space Object">
    <div class="options-grid" id="options"></div>
    <div id="result"></div>
    <button id="next-btn" onclick="startQuiz()">다음 문제 풀기 ➡️</button>
</div>

<script>
    const fakeAnswers = [
        "Andromeda Galaxy (M31)", "Orion Nebula (M42)", "Crab Nebula (M1)", 
        "Hubble Deep Field", "Pillars of Creation", "Jupiter's Great Red Spot",
        "Saturn's Rings", "Mars Rover Perseverance", "James Webb Space Telescope",
        "Helix Nebula", "Pleiades Star Cluster", "Sombrero Galaxy"
    ];

    let correctAnswer = "";

    // 무작위 날짜 생성 (2015년 이후 생성된 APOD 데이터 기준)
    function getRandomDate() {
        const start = new Date(2015, 0, 1);
        const end = new Date();
        end.setDate(end.getDate() - 2); // 안전하게 이틀 전 날짜까지
        const randomDate = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
        return randomDate.toISOString().split('T')[0];
    }

    async function startQuiz() {
        // UI 초기화
        document.getElementById('loading').style.display = 'block';
        document.getElementById('space-img').style.display = 'none';
        document.getElementById('options').innerHTML = '';
        document.getElementById('result').innerText = '';
        document.getElementById('next-btn').style.display = 'none';

        try {
            const date = getRandomDate();
            // NASA APOD 오픈 API 호출
            const response = await fetch(`https://nasa.gov{date}`);
            const data = await response.json();

            // 동영상이거나 이미지가 없을 경우 다시 뽑기
            if (data.media_type !== 'image' || !data.url) {
                startQuiz();
                return;
            }

            correctAnswer = data.title;
            
            // 이미지 표시
            const imgElement = document.getElementById('space-img');
            imgElement.src = data.url;
            imgElement.style.display = 'block';
            document.getElementById('loading').style.display = 'none';

            // 보기 리스트 만들기 (정답 1개 + 오답 3개)
            let filteredFake = fakeAnswers.filter(ans => ans !== correctAnswer);
            let shuffledFake = filteredFake.sort(() => 0.5 - Math.random()).slice(0, 3);
            let choices = [...shuffledFake, correctAnswer].sort(() => 0.5 - Math.random());

            // 보기 버튼 생성
            const optionsContainer = document.getElementById('options');
            choices.forEach((choice, index) => {
                const btn = document.createElement('button');
                btn.innerText = `${index + 1}. ${choice}`;
                btn.onclick = () => checkAnswer(choice, btn);
                optionsContainer.appendChild(btn);
            });

        } catch (error) {
            console.error("데이터 로드 실패, 재시도합니다.", error);
            startQuiz();
        }
    }

    function checkAnswer(selected, selectedBtn) {
        const buttons = document.querySelectorAll('#options button');
        buttons.forEach(btn => btn.disabled = true); // 클릭 방지

        const resultDiv = document.getElementById('result');
        if (selected === correctAnswer) {
            resultDiv.innerText = "🎉 정답입니다! 우주 전문가이시군요! 🧑‍🚀";
            resultDiv.style.color = "#00ffa3";
            selectedBtn.style.backgroundColor = "#006641";
            selectedBtn.style.borderColor = "#00ffa3";
        } else {
            resultDiv.innerText = `❌ 틀렸습니다!\n정답은 [ ${correctAnswer} ] 입니다.`;
            resultDiv.style.color = "#ff4d4d";
            selectedBtn.style.backgroundColor = "#661c1c";
            selectedBtn.style.borderColor = "#ff4d4d";
        }

        document.getElementById('next-btn').style.display = 'block';
    }

    // 페이지 접속 시 첫 게임 시작
    window.onload = startQuiz;
</script>

</body>
</html>
