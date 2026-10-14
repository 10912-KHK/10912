import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 화면 레이아웃 깔끔하게 설정
st.set_page_config(page_title="우주 천체 탐험 퀴즈", layout="centered")

# 2. 끊겨 있던 HTML/JS 문법을 완벽하게 복구 및 결합
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>신비로운 우주 천체 탐험 퀴즈</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c20, #03001e, #23074d);
            color: #ffffff;
            margin: 0;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .quiz-container {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            padding: 30px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            border: 1px rgba(255, 255, 255, 0.1) solid;
            text-align: center;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 5px;
            color: #4facfe;
            text-shadow: 0 0 10px rgba(79, 172, 254, 0.6);
        }
        .progress {
            font-size: 14px;
            color: #aaa;
            margin-bottom: 20px;
        }
        .image-box {
            width: 100%;
            height: 250px;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
            background-color: #000;
        }
        .image-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .question-box {
            font-size: 17px;
            line-height: 1.6;
            margin-bottom: 25px;
            text-align: left;
            word-break: keep-all;
        }
        .options-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .option-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px rgba(255, 255, 255, 0.2) solid;
            color: white;
            padding: 14px;
            border-radius: 8px;
            cursor: pointer;
            text-align: left;
            font-size: 15px;
            transition: all 0.2s ease;
        }
        .option-btn:hover:not(:disabled) {
            background: rgba(79, 172, 254, 0.2);
            border-color: #4facfe;
        }
        .correct {
            background-color: rgba(46, 204, 113, 0.3) !important;
            border-color: #2ecc71 !important;
        }
        .wrong {
            background-color: rgba(231, 76, 60, 0.3) !important;
            border-color: #e74c3c !important;
        }
        .feedback-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            font-size: 15px;
            line-height: 1.5;
            text-align: left;
            display: none;
            background: rgba(0, 0, 0, 0.4);
            border-left: 4px solid #4facfe;
        }
        .next-btn {
            margin-top: 20px;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            color: black;
            font-weight: bold;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            display: none;
        }
    </style>
</head>
<body>

<div class="quiz-container" id="quiz-card">
    <h1>🚀 신비로운 우주 천체 탐험</h1>
    <div class="progress" id="progress-text">문제 1 / 5</div>
    
    <div class="image-box">
        <img id="space-img" src="" alt="우주 천체 이미지">
    </div>
    
    <div class="question-box" id="question-text">불러오는 중...</div>
    <div class="options-container" id="options-box"></div>
    <div class="feedback-box" id="feedback-text"></div>
    <button class="next-btn" id="next-button" onclick="nextQuestion()">다음 문제로 이동 ➡️</button>
</div>

<script>
    const quizData = [
        {
            question: "방패자리 방향으로 불타오르는 듯한 붉은빛의 초거성, 태양 반지름의 약 2,150배에 달하는 거대한 체적을 자랑하는 이 별은 현재까지 인류가 발견한 가장 거대한 항성 중 하나입니다. 태양계의 태양을 이 별의 중심에 놓는다면 그 표면은 토성 궤도를 넘어설 정도로 압도적인 크기를 가집니다. 이 거대한 초거성의 이름은 무엇일까요?",
            image: "https://unsplash.com",
            options: [
                { text: "스테파니손 2-18 (Stephenson 2-18)", isCorrect: true, reason: "정답입니다! 스테파니손 2-18은 현재 인류가 관측한 적색초거성 중 크기 순위 최상위권에 위치한 가장 거대한 항성입니다." },
                { text: "베텔게우스 (Betelgeuse)", isCorrect: false, reason: "오답입니다. 오리온자리의 베텔게우스도 거대하지만, 태양 반지름의 약 700~1,000배로 스테파니손보다 훨씬 작습니다." },
                { text: "안타레스 (Antares)", isCorrect: false, reason: "오답입니다. 전갈자리의 안타레스는 태양 반지름의 약 700배 수준입니다." },
                { text: "VY 캔이스 마요리스 (VY Canis Majoris)", isCorrect: false, reason: "오답입니다. 과거 가장 큰 별로 불렸으나 정밀 측정 결과 태양의 1,420배 수준으로 순위가 밀려났습니다." }
            ]
        },
        {
            question: "우리 은하의 가장 거대한 이웃이자, 수천억 개의 별들이 소용돌이치는 눈부신 빛의 성운형 은하입니다. 지구에서 이 은하까지의 거리와 과학자들이 예상하는 두 은하의 충돌·합병 시기는 언제일까요?",
            image: "https://unsplash.com",
            options: [
                { text: "약 250만 광년 / 약 40억~45억 년 뒤", isCorrect: true, reason: "정답입니다! 안드로메다 은하는 지구에서 약 250만 광년 떨어져 있으며, 약 40억~45억 년 뒤 우리 은하와 완전히 충돌하여 하나의 거대한 타원 은하를 이룰 예정입니다." },
                { text: "약 50만 광년 / 약 10억 년 뒤", isCorrect: false, reason: "오답입니다. 50만 광년은 너무 가까운 거리이며 충돌 주기도 실제 계산보다 빠릅니다." },
                { text: "약 1,000만 광년 / 충돌하지 않고 영원히 멀어짐", isCorrect: false, reason: "오답입니다. 국부 은하군 내부의 강력한 중력으로 인해 두 은하는 계속 가까워지고 있습니다." },
                { text: "약 10만 광년 / 약 5억 년 뒤", isCorrect: false, reason: "오답입니다. 10만 광년은 안드로메다까지의 거리가 아닌 우리 은하 자체의 대략적인 지름 크기입니다." }
            ]
        },
        {
            question: "우주 심연에서 태양 질량의 수백억 배에 달하는 무게로 시공간을 극단적으로 휘어잡고 있는 거대한 괴물 퀘이사, TON 618입니다. 사방으로 눈이 멀 정도로 강력한 빛과 에너지를 토해내며 은하 중심에서 군림하는 이 초대질량 블랙홀의 추정 질량은 태양 질량의 약 몇 배로 우주 최고 순위를 다투고 있을까요?",
            image: "https://unsplash.com",
            options: [
                { text: "약 660억 배", isCorrect: true, reason: "정답입니다! TON 618은 발견된 초대질량 블랙홀 중 최대 규모 중 하나로, 태양 질량의 약 660억 배라는 상상을 초월하는 초거대 질량을 가집니다." },
                { text: "약 400만 배", isCorrect: false, reason: "오답입니다. 400만 배는 고작 우리 은하 중심에 위치한 궁수자리 A* 블랙홀의 무게입니다." },
                { text: "약 1억 배", isCorrect: false, reason: "오답입니다. 일반적인 거대 은하 중심 블랙홀 수준의 질량이며, TON 618의 규모에는 한참 못 미칩니다." },
                { text: "약 5천만 배", isCorrect: false, reason: "오답입니다. TON 618은 우주 초기 생성되어 빛나고 있는 극단적인 천체입니다." }
            ]
        },
        {
            question: "허블과 제임스 웹 우주망원경이 포착한 가장 경이로운 우주 풍경 중 하나인 '창조의 기둥(Pillars of Creation)'입니다. 독수리 성운(M16) 내부에 위치한 이곳은 아기 별들이 쉴 새 없이 생성되는 요람입니다. 이 가스 기둥은 지구로부터 얼마나 떨어져 있으며, 주로 어떤 성분으로 이루어져 있을까요?",
            image: "https://unsplash.com",
            options: [
                { text: "약 6,500광년 / 저온의 수소 가스와 우주 먼지", isCorrect: true, reason: "정답입니다! 창조의 기둥은 지구에서 약 6,500광년 거리에 있으며, 짙은 밀도의 차가운 수소 가스와 먼지들이 뭉쳐지면서 지속적으로 수많은 새로운 별들을 생성하고 있습니다." },
                { text: "약 450광년 / 액체 메탄과 얼음 결정", isCorrect: false, reason: "오답입니다. 성운의 주성분은 액체가 아닌 차가운 가스 성간 물질입니다." },
                { text: "약 3억 광년 / 고온의 플라즈마와 철 입자", isCorrect: false, reason: "오답입니다. 3억 광년은 우리 은하 밖 훨씬 먼 외부 우주 공간의 거리입니다." },
                { text: "약 150광년 / 산소 가스와 규산염 암석 파편", isCorrect: false, reason: "오답입니다. 지구와 훨씬 가깝게 오인된 수치입니다." }
            ]
        },
        {
            question: "천칭자리 방향에 위치하며 은빛으로 고요하게 빛나는 HD 140283, 이른바 '므두셀라 별(Methuselah star)'입니다. 우주 역사상 나이 순위가 가장 높은 천체 중 하나인 이 별은 과학자들이 추정한 이 최고령 준거성의 나이는 대략 얼마일까요?",
            image: "https://unsplash.com",
            options: [
                { text: "약 135억 년", isCorrect: true, reason: "정답입니다! 므두셀라 별의 추정 나이는 약 135억 년 이상으로, 우주 전체 나이(약 138억 년) 직후에 태어난 우주 조상님 격인 별입니다." },
                { text: "약 45억 년", isCorrect: false, reason: "오답입니다. 45억 년은 우리 태양계와 지구가 생성된 나이입니다. 이 별은 태양보다 훨씬 늙었습니다." },
                { text: "약 20억 년", isCorrect: false, reason: "오답입니다. 은하계 기준으로는 아주 젊은 청년 별에 해당하는 나이입니다." },
                { text: "약 300억 년", isCorrect: false, reason: "오답입니다. 우주가 탄생한 전체 나이가 138억 년이기 때문에, 물리학적으로 300억 년이 될 수는 없습니다." }
            ]
        }
    ];

    let currentQuestionIndex = 0;
    let score = 0;

    function shuffle(array) {
        return array.sort(() => Math.random() - 0.5);
    }

    function loadQuestion() {
        const currentQuiz = quizData[currentQuestionIndex];
        document.getElementById("progress-text").innerText = `문제 ${currentQuestionIndex + 1} / ${quizData.length}`;
        document.getElementById("space-img").src = currentQuiz.image;
        document.getElementById("question-text").innerText = currentQuiz.question;
        
        const optionsBox = document.getElementById("options-box");
        optionsBox.innerHTML = "";
        
        document.getElementById("feedback-text").style.display = "none";
        document.getElementById("next-button").style.display = "none";

        const shuffledOptions = shuffle([...currentQuiz.options]);
        
        shuffledOptions.forEach(opt => {
            const button = document.createElement("button");
            button.className = "option-btn";
            button.innerText = opt.text;
            button.onclick = () => selectOption(button, opt.isCorrect, opt.reason);
            optionsBox.appendChild(button);
        });
    }

    function selectOption(selectedBtn, isCorrect, reason) {
        const allButtons = document.querySelectorAll(".option-btn");
        allButtons.forEach(btn => btn.disabled = true);
        if (isCorrect) {
            selectedBtn.classList.add("correct");
score++;
} else {
selectedBtn.classList.add("wrong");
const currentQuiz = quizData[currentQuestionIndex];
allButtons.forEach(btn => {
const matchedOption = currentQuiz.options.find(o => o.text === btn.innerText);
if (matchedOption && matchedOption.isCorrect) btn.classList.add("correct");
});
}
const feedbackBox = document.getElementById("feedback-text");
feedbackBox.innerText = (isCorrect ? "💡 [정답] " : "❌ [오답] ") + reason;
feedbackBox.style.display = "block";
document.getElementById("next-button").style.display = "inline-block";
}
function nextQuestion() {
currentQuestionIndex++;
if (currentQuestionIndex < quizData.length) loadQuestion();
else showFinalResult();
}
function showFinalResult() {
const quizCard = document.getElementById("quiz-card");
quizCard.innerHTML = <h1 style="color: #00f2fe; font-size: 28px; margin-bottom: 10px;">🌌 탐험 완료!</h1> <p style="font-size: 18px; margin-bottom: 20px;">당신이 획득한 우주 지식 점수</p> <div style="font-size: 48px; font-weight: bold; color: #00f2fe; margin-bottom: 20px;">${score} / ${quizData.length}</div> <p style="line-height: 1.6; color: #ddd; margin-bottom: 30px; font-size: 15px;"> ${score === 5 ? '완벽합니다! 당신은 걸어 다니는 천문학 사전이시군요! 🪐' : '멋진 도전이었습니다! 우주의 비밀들을 알아가는 즐거운 시간이 되었기를 바랍니다. ✨'} </p> <button class="next-btn" style="display:inline-block;" onclick="location.reload()">다시 도전하기 🔄</button>;
}
window.onload = loadQuestion;
