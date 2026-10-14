import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(page_title="NASA 우주 퀴즈", layout="centered")

# HTML/JavaScript 소스 코드
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 NASA 우주 천체 맞추기 퀴즈</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #ffffff; text-align: center; padding: 10px; margin: 0; }
        .container { max-width: 100%; margin: 0 auto; background: #161d30; padding: 20px; border-radius: 15px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); box-sizing: border-radius; }
        h1 { color: #4dadff; font-size: 22px; margin-bottom: 20px; }
        #space-img { max-width: 100%; max-height: 300px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: none; margin-left: auto; margin-right: auto; }
        .loading { font-size: 16px; color: #aaa; margin: 40px 0; }
        .options-grid { display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 20px; }
        button { background-color: #243454; color: white; border: 2px solid #3b5382; padding: 14px; font-size: 15px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; text-align: left; padding-left: 20px; width: 100%; }
        button:hover { background-color: #3b5382; border-color: #4dadff; }
        #result { margin-top: 25px; font-size: 18px; font-weight: bold; white-space: pre-line; }
        #next-btn { background-color: #00aa6c; border: none; text-align: center; padding: 12px 25px; display: none; margin: 20px auto 0 auto; border-radius: 25px; font-weight: bold; width: auto; cursor: pointer; }
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

    function getRandomDate() {
        const start = new Date(2015, 0, 1);
        const end = new Date();
        end.setDate(end.getDate() - 2);
        return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime())).toISOString().split('T')[0];
    }

    async function startQuiz() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('space-img').style.display = 'none';
        document.getElementById('options').innerHTML = '';
        document.getElementById('result').innerText = '';
        document.getElementById('next-btn').style.display = 'none';

        try {
            const date = getRandomDate();
            const response = await fetch(`https://nasa.gov{date}`);
            const data = await response.json();

            if (data.media_type !== 'image' || !data.url) {
                startQuiz();
                return;
            }

            correctAnswer = data.title;
            
            const imgElement = document.getElementById('space-img');
            imgElement.src = data.url;
            imgElement.style.display = 'block';
            document.getElementById('loading').style.display = 'none';

            let filteredFake = fakeAnswers.filter(ans => ans !== correctAnswer);
            let shuffledFake = filteredFake.sort(() => 0.5 - Math.random()).slice(0, 3);
            let choices = [...shuffledFake, correctAnswer].sort(() => 0.5 - Math.random());

            const optionsContainer = document.getElementById('options');
            choices.forEach((choice, index) => {
                const btn = document.createElement('button');
                btn.innerText = `${index + 1}. ${choice}`;
                btn.onclick = () => checkAnswer(choice, btn);
                optionsContainer.appendChild(btn);
            });

        } catch (error) {
            startQuiz();
        }
    }

    function checkAnswer(selected, selectedBtn) {
        const buttons = document.querySelectorAll('#options button');
        buttons.forEach(btn => btn.disabled = true);

        const resultDiv = document.getElementById('result');
        if (selected === correctAnswer) {
            resultDiv.innerText = "🎉 정답입니다! 우주 전문가이시군요! 🧑‍🚀";
            resultDiv.style.color = "#00ffa3";
            selectedBtn.style.backgroundColor = "#006641";
            selectedBtn.style.borderColor = "#00ffa3";
        } else {
            resultDiv.innerText = `❌ 틀렸습니다!\\n정답은 [ ${correctAnswer} ] 입니다.`;
            resultDiv.style.color = "#ff4d4d";
            selectedBtn.style.backgroundColor = "#661c1c";
            selectedBtn.style.borderColor = "#ff4d4d";
        }

        document.getElementById('next-btn').style.display = 'block';
    }

    window.onload = startQuiz;
</script>

</body>
</html>
"""

# 파이썬 웹 화면에 HTML 컴포넌트 띄우기
components.html(html_code, height=650, scroller=True)
