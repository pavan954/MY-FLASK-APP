from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Number Game</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color:rgb(251, 251, 251);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
            padding: 10px;
        }
        .score-time {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 800px;
            margin-bottom: 20px;
        }
        .score {
            font-size: 2rem;
            font-weight: bold;
            color: #ff6600;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .timer {
            position: relative;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 8px solid #FF6347; /* Fun, vibrant tomato red */
            background-color: #FFD700; /* Bright, cheerful yellow */
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); /* Soft shadow for depth */
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 20px;
        }

        .timer-text {
            font-size: 1.8rem;
            font-weight: bold;
            color: #FFFFFF; /* White text for high contrast */
            position: absolute;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Subtle text shadow for a playful touch */
        }

        .circle-background {
            width: 100%;
            height: 100%;
            position: absolute;
            border-radius: 50%;
            background-color: #ADD8E6; /* Light blue background for contrast */
        }

        .progress-ring {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(#FF4500 calc(var(--percent) * 1%), #FFD700 calc(var(--percent) * 1%)); /* Fun orange-to-yellow gradient */
            transition: background 0.5s ease;
        }
        .question {
            margin: 20px;
            font-size: 5vw;
            text-align: center;
            font-weight: bold;
            color: #333;
            background-color: rgba(255, 255, 255, 0.8);
            border: 4px solid #333;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .options {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            width: 100%;
        }
        .option {
            flex: 1 1 calc(30% - 10px);
            min-width: 100px;
            max-width: 200px;
            padding: 15px;
            background-color: #ff5e62;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.5rem;
            text-align: center;
            transition: background-color 0.3s, transform 0.2s;
        }
        .option:hover {
            background-color: #ff3366;
            transform: scale(1.1);
        }
        .game-over {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background-color: rgba(255, 255, 255, 0.9);
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .game-over h2 {
            color: #ff6600;
            font-size: 2rem;
        }
        .game-over p {
            font-size: 1.5rem;
            margin-bottom: 20px;
        }
        button {
            padding: 15px 30px;
            font-size: 1.5rem;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            margin: 10px;
            transition: background-color 0.3s, transform 0.2s;
        }
        button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        .exit-button {
            background-color: #ff0000;
        }
        .exit-button:hover {
            background-color: #cc0000;
        }
        .skip-button {
            padding: 15px 30px;
            font-size: 1.5rem;
            background-color:rgb(255, 0, 136);
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            margin: 10px;
            transition: background-color 0.3s, transform 0.2s;
        }
        .skip-button:hover {
            background-color:rgb(204, 0, 0);
            transform: scale(1.05);
        }
        .confetti {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            z-index: 10;
        }
        .confetti-piece {
            position: absolute;
            width: 10px;
            height: 20px;
            background-color: var(--color);
            animation: fall 2s linear infinite;
        }
        @keyframes fall {
            0% {
                transform: translateY(-10px) rotate(0deg);
            }
            100% {
                transform: translateY(100vh) rotate(360deg);
            }
        }
        .correct {
            color: green;
            font-weight: bold;
        }
        .incorrect {
            color: red;
            font-weight: bold;
        }

        /* Media Queries for larger screens */
        @media (min-width: 768px) {
            .score-time {
                width: 80%;
            }
            .question {
                font-size: 4vw;
            }
            .option {
                flex: 1 1 calc(20% - 10px);
                font-size: 1.2rem;
            }
            .game-over h2 {
                font-size: 3rem;
            }
            .game-over p {
                font-size: 2rem;
            }
            button {
                padding: 20px 40px;
                font-size: 1.8rem;
            }
            .timer {
                width: 100px;
                height: 100px;
            }
            .timer-text {
                font-size: 2rem;
            }
        }

        @media (min-width: 1200px) {
            .score-time {
                width: 70%;
            }
            .question {
                font-size: 2vw;
            }
            .option {
                flex: 1 1 calc(15% - 10px);
            }
        }
        .level-info {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #fff;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            margin-bottom: 10px;
        }

        .xp-bar-container {
            flex-grow: 1;
            height: 20px;
            background: #eee;
            border-radius: 10px;
            overflow: hidden;
        }

        .xp-bar {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.3s ease;
        }

        .level-up-message {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.8);
            color: #fff;
            padding: 20px 40px;
            border-radius: 10px;
            font-size: 24px;
            animation: fadeInOut 3s ease;
            z-index: 1000;
        }

        @keyframes fadeInOut {
            0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
            10% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
            20% { transform: translate(-50%, -50%) scale(1); }
            80% { opacity: 1; }
            100% { opacity: 0; }
        }
    </style>
</head>
<body>
    <div class="container text-center">
        <div class="fs-3 fw-bold text-dark mb-2">Number Game</div>
        
        <!-- Score and Timer Section -->
        <div class="score-time row justify-content-between align-items-center mb-4">
            <div class="col-4 col-md-3 mb-3 mb-md-0">
                <div>Score: <span id="score" class="score">0</span></div>
            </div>
            <div class="col-4 col-md-3 mb-3 mb-md-0">
                <div id="lives" class="p-2 bg-danger text-white rounded-3 shadow-sm">Lives: 5</div>
            </div>
            <div class="col-4 col-md-3 mb-3 mb-md-0">
                <div class="timer">
                    <div class="circle-background"></div>
                    <div class="progress-ring" id="progress-ring" style="--percent: 100;"></div>
                    <span class="timer-text" id="timer-text">30</span>
                </div>
            </div>
        </div>
        <div class="level-info">
            <div id="level-display">Level: 1</div>
            <div class="xp-bar-container">
                <div id="xp-bar" class="xp-bar" style="width: 0%"></div>
            </div>
            <div id="xp-text">0/100 XP</div>
        </div>

        <!-- Question Section -->
        <div class="question" id="question">Loading...</div>

        <!-- Options Section -->
        <div class="options" id="options"></div>

        <!-- Skip Button -->
        <button id="skip" class="skip-button">Skip</button>

        <!-- Confetti -->
        <div class="confetti" id="confetti"></div>

        <!-- Game Over Section -->
        <div class="game-over" id="game-over" style="display: none;">
            <h2>Game Over!</h2>
            <p>Final Score: <span id="final-score">0</span></p>
            <div>
                <button id="try-again">Try Again</button>
                <button id="exit" class="exit-button">Exit</button>
            </div>
        </div>
    </div>
    <audio id="correct-sound" src="https://freesound.org/data/previews/85/85377_1037582-lq.mp3" preload="auto"></audio>
    <audio id="wrong-sound" src="https://freesound.org/data/previews/202/202438_302189-lq.mp3" preload="auto"></audio>
    <audio id="game-over-sound" src="https://soundbible.com/grab.php?id=1639&type=mp3" preload="auto"></audio>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const questionEl = document.getElementById('question');
        const optionsEl = document.getElementById('options');
        const scoreEl = document.getElementById('score');
        const gameOverEl = document.getElementById('game-over');
        const finalScoreEl = document.getElementById('final-score');
        const tryAgainBtn = document.getElementById('try-again');
        const exitBtn = document.getElementById('exit');
        const progressRing = document.getElementById('progress-ring');
        const timerText = document.getElementById('timer-text');
        const confettiContainer = document.getElementById('confetti');
        const skipBtn = document.getElementById('skip');

        let score = 0;
        let timer;
        let lives = 5;
        let timeLeft = 30;
        let questionCount = 0;
        let usedQuestions = [];
        let currentLevel = 1;
        let experiencePoints = 0;
        let experienceToNextLevel = 100;

        function calculateExperienceGain(questionDifficulty) {
            let baseXP = 10;
            let timeBonus = Math.floor(timeLeft / 3);
            let difficultyMultiplier = questionDifficulty || 1;
            return Math.floor((baseXP + timeBonus) * difficultyMultiplier);
        }

        function checkLevelUp() {
            if (experiencePoints >= experienceToNextLevel) {
                currentLevel++;
                experiencePoints = experiencePoints - experienceToNextLevel;
                experienceToNextLevel = Math.floor(experienceToNextLevel * 1.5);
                showLevelUpMessage();
                adjustDifficulty();
            }
            updateLevelDisplay();
        }

        function showLevelUpMessage() {
            const levelUpMessage = document.createElement('div');
            levelUpMessage.className = 'level-up-message';
            levelUpMessage.textContent = `Level Up! level ${currentLevel}!`;
            document.body.appendChild(levelUpMessage);
    
            setTimeout(() => {
                levelUpMessage.remove();
            }, 3000);
        }

        function adjustDifficulty() {
            if (currentLevel >= 5) {
                timeLeft = Math.max(20, 30 - Math.floor(currentLevel / 2));
            }
        }

        function updateLevelDisplay() {
            document.getElementById('level-display').textContent = `Level: ${currentLevel}`;
            const xpPercentage = (experiencePoints / experienceToNextLevel) * 100;
            document.getElementById('xp-bar').style.width = `${xpPercentage}%`;
            document.getElementById('xp-text').textContent = `${experiencePoints}/${experienceToNextLevel} XP`;
        }
        function startTimer() {
            timeLeft = 30;
            updateTimerDisplay();
            clearInterval(timer);
            timer = setInterval(() => {
                if (gameOverEl.style.display === 'none') {
                    timeLeft--;
                    updateTimerDisplay();
                    if (timeLeft <= 0) {
                        clearInterval(timer);
                        endGame();
                    }
                }
            }, 1000);
        }

        function updateTimerDisplay() {
            timerText.textContent = timeLeft;
            progressRing.style.setProperty('--percent', (timeLeft / 30) * 100);
        }

        function updateLivesDisplay() {
            document.getElementById('lives').textContent = `Lives: ${lives}`;
        }

        function generateQuestion() {
            const num1 = Math.floor(Math.random() * 20) + 1;
            const operationType = Math.floor(Math.random() * 40);
            let question, correctAnswer, options;

            switch (operationType) {
                case 0:
                    const resultAdd = Math.floor(Math.random() * 20) + num1;
                    question = `${num1} + __ = ${resultAdd}`;
                    correctAnswer = resultAdd - num1;
                    options = generateOptions(correctAnswer);
                    break;
                case 1:
                    const resultSub = num1 + Math.floor(Math.random() * 10) + 1;
                    question = `${num1} - __ = ${resultSub}`;
                    correctAnswer = num1 - resultSub;
                    options = generateOptions(correctAnswer);
                    break;
                case 2:
                    const resultMul = num1 * Math.floor(Math.random() * 12) + 1;
                    question = `${num1} * __ = ${resultMul}`;
                    correctAnswer = resultMul / num1;
                    options = generateOptions(correctAnswer);
                    break;
                case 3:
                    const divisor = Math.floor(Math.random() * 10) + 1;
                    const resultDiv = num1 * divisor;
                    question = `${resultDiv} ÷ __ = ${num1}`;
                    correctAnswer = divisor;
                    options = generateOptions(correctAnswer);
                    break;
                case 4:
                    const num2 = Math.floor(Math.random() * 20) + 1;
                    const resultAdd2 = Math.floor(Math.random() * 20) + num1 + num2;
                    question = `${num1} + __ + ${num2} = ${resultAdd2}`;
                    correctAnswer = resultAdd2 - num1 - num2;
                    options = generateOptions(correctAnswer);
                    break;
                case 5:
                    const num3 = Math.floor(Math.random() * 10) + 1;
                    const resultSub2 = num1 + num3;
                    question = `${num1} - __ - ${num3} = ${resultSub2}`;
                    correctAnswer = num1 - resultSub2 - num3;
                    options = generateOptions(correctAnswer);
                    break;
                case 6:
                    const num4 = Math.floor(Math.random() * 12) + 1;  // Random number between 1 and 12
                    const randomBlankValue = Math.floor(Math.random() * 12) + 1;  // Another random number to fill the blank
                    const resultMul2 = num1 * randomBlankValue * num4;  // Calculate the result using the random numbers
                    question = `${num1} * __ * ${num4} = ${resultMul2}`;  // The blank remains in the question
                    correctAnswer = randomBlankValue;  // The correct answer is the number in the blank
                    options = generateOptions(correctAnswer);  // Generate options for the multiple-choice question
                    break;
                case 7:
                    const num5 = Math.floor(Math.random() * 10) + 1;
                    const resultDiv2 = num1 * num5;
                    question = `${num1} ÷ __ ÷ ${num5} = ${resultDiv2}`;
                    correctAnswer = num1 / (resultDiv2 * num5);
                    options = generateOptions(correctAnswer);
                    break;
                case 8:
                    const startNum = Math.floor(Math.random() * 10) + 1;  // Random start number between 1 and 10
                    const difference = Math.floor(Math.random() * 5) + 1; // Random difference between 1 and 5
                    const num7 = startNum + difference * 2;  // num7 is startNum + 2*difference to avoid overlap
                    const num8 = num7 + difference;         // num8 is num7 + difference

                    question = `${startNum}, __, ${num7}, ${num8}`;  // Sequence with a missing number
                    correctAnswer = startNum + difference;  // The missing number is startNum + difference
                    options = generateOptions(correctAnswer);
                    break;
                case 9:
                    const num11 = Math.floor(Math.random() * 20) + 1;
                    question = `Is ${num11} odd or even? __`;
                    correctAnswer = num11 % 2 === 0 ? "Even" : "Odd";  // Identify odd or even number
                    options = generateOptionsForString(correctAnswer);
                    break;
                case 10:
                    const base = Math.floor(Math.random() * 5) + 2;  // Random base number (between 2 and 6)
                    const exponent = Math.floor(Math.random() * 3) + 2;  // Random exponent (between 2 and 4)
                    const resultExp = Math.pow(base, exponent);  // Calculate base^exponent
                    question = `${base} ^ __ = ${resultExp}`;  // Missing exponent in the question
                    correctAnswer = exponent;  // The correct answer is the exponent
                    options = generateOptions(correctAnswer);  // Use generateOptions for numeric answers
                    break;
                case 11:
                    const resultMod = num1 * Math.floor(Math.random() * 15) + 1;
                    question = `${resultMod} % __ = ${num1}`;
                    correctAnswer = resultMod % num1;
                    options = generateOptions(correctAnswer);
                    break;
                case 12:
                    const number = Math.floor(Math.random() * 100) + 1;
                    const resultSqrt = Math.sqrt(number).toFixed(2);  // Ensure the result has two decimal places
                    question = `What is the square root of ${number}? _____`;
                    correctAnswer = resultSqrt;
                    options = generateOptions(correctAnswer);
                    break;
                case 13:
                    const percent = Math.floor(Math.random() * 50) + 1;
                    const baseNumber = Math.floor(Math.random() * 100) + 1;
                    const resultPercentage = (percent / 100) * baseNumber;
                    question = `What is ${percent}% of ${baseNumber}? ______`;
                    correctAnswer = resultPercentage;
                    options = generateOptions(correctAnswer);
                    break;
                case 14:
                    const length = Math.floor(Math.random() * 10) + 1;
                    const width = Math.floor(Math.random() * 10) + 1;
                    const resultArea = length * width;
                    question = `What is the area of a rectangle with length ${length} and width ${width}? ____`;
                    correctAnswer = resultArea;
                    options = generateOptions(correctAnswer);
                    break;
                case 15:
                    const hours = Math.floor(Math.random() * 5) + 1;
                    const resultMinutes = hours * 60;
                    question = `How many minutes are in ${hours} hour${hours > 1 ? "s" : ""} ____ ?`;
                    correctAnswer = resultMinutes;
                    options = generateOptions(correctAnswer);
                    break;
                case 16:
                    const radius = Math.floor(Math.random() * 10) + 1;
                    const resultCircumference = (2 * Math.PI * radius).toFixed(2);  // Circumference = 2 * π * radius
                    question = `What is the circumference of a circle with radius ${radius}? ____`;
                    correctAnswer = resultCircumference;
                    options = generateOptions(correctAnswer);
                    break;
                case 17:
                    const side = Math.floor(Math.random() * 10) + 1;
                    const resultCubeVolume = Math.pow(side, 3);  // Volume of a cube = side^3
                    question = `What is the volume of a cube with side length ${side}? ____`;
                    correctAnswer = resultCubeVolume;
                    options = generateOptions(correctAnswer);
                    break;
                case 18:
                    const totalCost = Math.floor(Math.random() * 100) + 1;
                    const discountPercent = Math.floor(Math.random() * 30) + 5;
                    const discountAmount = (totalCost * discountPercent) / 100;
                    const finalPrice = totalCost - discountAmount;
                    question = `What is the final price after a ${discountPercent}% discount on ₹${totalCost}? ____`;
                    correctAnswer = finalPrice.toFixed(2);  // Rounded to 2 decimal places
                    options = generateOptions(correctAnswer);
                    break;
                case 19:
                    const speed = Math.floor(Math.random() * 60) + 1;  // Speed in km/h
                    const time = Math.floor(Math.random() * 6) + 1;  // Time in hours
                    const distance = speed * time;  // Distance = speed * time
                    question = `How far will a vehicle travel at ${speed} km/h for ${time} hour${time > 1 ? "s" : ""}? ____ km`;
                    correctAnswer = distance;
                    options = generateOptions(correctAnswer);
                    break;
                case 20:
                    const celsius = Math.floor(Math.random() * 50);  // Random temperature in Celsius
                    const fahrenheit = (celsius * 9/5) + 32;  // Convert to Fahrenheit
                    question = `Convert ${celsius}°C to Fahrenheit: __ °F`;
                    correctAnswer = Math.round(fahrenheit);  // Round to nearest whole number
                    options = generateOptions(correctAnswer);
                    break;
                case 21:
                    const numForFactorial = Math.floor(Math.random() * 6) + 1;  // Number between 1 and 6
                    const factorialResult = factorial(numForFactorial);
                    question = `What is ${numForFactorial}! (factorial of ${numForFactorial})? __`;
                    correctAnswer = factorialResult;
                    options = generateOptions(correctAnswer);
                    break;
                function factorial(n) {
                    if (n === 0 || n === 1) return 1;
                    return n * factorial(n - 1);
                }
                case 22:
                    const num1LCM = Math.floor(Math.random() * 10) + 1;
                    const num2LCM = Math.floor(Math.random() * 10) + 1;
                    const lcmResult = lcm(num1LCM, num2LCM);
                    question = `What is the LCM of ${num1LCM} and ${num2LCM}? __`;
                    correctAnswer = lcmResult;
                    options = generateOptions(correctAnswer);
                    break;
                function lcm(a, b) {
                    return (a * b) / gcd(a, b);
                }
                case 23:
                    const ratio1 = Math.floor(Math.random() * 5) + 2;  // Random ratio part between 2 and 6
                    const ratio2 = Math.floor(Math.random() * 5) + 3;  // Random ratio part between 3 and 7
                    const totalQuantity = Math.floor(Math.random() * 50) + 50;  // Total quantity
                    const part1 = (totalQuantity * ratio1) / (ratio1 + ratio2);  // Proportional part 1
                    question = `In a ratio of ${ratio1}:${ratio2}, what is the value of the first part from a total quantity of ${totalQuantity}? __`;
                    correctAnswer = part1;
                    options = generateOptions(correctAnswer);
                    break;
                case 24:
                    const a = Math.floor(Math.random() * 10) + 2;  // Random coefficient for x
                    const b = Math.floor(Math.random() * 10) + 3;  // Random constant
                    const c = Math.floor(Math.random() * 10) + 5;  // Random result
                    const xValue = (c - b) / a;  // Solve for x
                    question = `Find the x value: ${a}x + ${b} = ${c} = __`;
                    correctAnswer = xValue.toFixed(2);  // Round to two decimal places
                    options = generateOptions(correctAnswer);
                    break;
                case 25:
                    const radiusCylinder = Math.floor(Math.random() * 10) + 1;  // Random radius between 1 and 10
                    const heightCylinder = Math.floor(Math.random() * 10) + 5;  // Random height between 5 and 15
                    const volumeCylinder = (Math.PI * Math.pow(radiusCylinder, 2) * heightCylinder).toFixed(2);  // Volume = π * r² * h
                    question = `What is the volume of a cylinder with radius ${radiusCylinder} and height ${heightCylinder}? __`;
                    correctAnswer = volumeCylinder;
                    options = generateOptions(correctAnswer);
                    break;
                case 26:
                    const numA = Math.floor(Math.random() * 50) + 20;  // Random number between 20 and 70
                    const numB = Math.floor(Math.random() * 50) + 30;  // Random number between 30 and 80
                    const numC = Math.floor(Math.random() * 50) + 10;  // Random number between 10 and 60
                    const average = (numA + numB + numC) / 3;  // Average of the 3 numbers
                    question = `What is the average of ${numA}, ${numB}, and ${numC}? __`;
                    correctAnswer = average.toFixed(2);  // Rounded to 2 decimal places
                    options = generateOptions(correctAnswer);
                    break;
                case 27:
                    const num44 = Math.floor(Math.random() * 50) + 10;  // Random number between 10 and 60
                    let divisorsCount = 0;
                    for (let i = 1; i <= num44; i++) {
                        if (num44 % i === 0) {
                            divisorsCount++;
                        }
                    }
                    question = `How many divisors does the number ${num44} have? __`;
                    correctAnswer = divisorsCount;
                    options = generateOptions(correctAnswer);
                    break;
                case 28:
                    const totalOutcomes = Math.floor(Math.random() * 20) + 5;  // Total number of possible outcomes
                    const favorableOutcomes = Math.floor(Math.random() * (totalOutcomes - 1)) + 1;  // Favorable outcomes (less than total outcomes)
                    const probability = (favorableOutcomes / totalOutcomes).toFixed(2);  // Probability = favorable outcomes / total outcomes
                    question = `What is the probability of an event occurring if there are ${favorableOutcomes} favorable outcomes out of ${totalOutcomes} total outcomes? __`;
                    correctAnswer = probability;
                    options = generateOptions(correctAnswer);
                    break;
                case 29:
                    const angle1 = Math.floor(Math.random() * 60) + 30;  // Angle 1 between 30 and 90 degrees
                    const angle2 = Math.floor(Math.random() * (90 - angle1)) + 1;  // Angle 2 such that total angles <= 180 degrees
                    const missingAngle = 180 - angle1 - angle2;  // Sum of angles in a triangle = 180°
                    question = `In a triangle, if one angle is ${angle1}° and another angle is ${angle2}°, what is the missing angle? __°`;
                    correctAnswer = missingAngle;
                    options = generateOptions(correctAnswer);
                    break;
                case 30:
                    const totalDistance = Math.floor(Math.random() * 200) + 50;  // Random distance between 50 km and 250 km
                    const totalTime = Math.floor(Math.random() * 5) + 1;  // Random time between 1 hour and 5 hours
                    const averageSpeed = (totalDistance / totalTime).toFixed(2);  // Average speed = distance / time
                    question = `A vehicle covers a total distance of ${totalDistance} km in ${totalTime} hours. What is the average speed? __ km/h`;
                    correctAnswer = averageSpeed;
                    options = generateOptions(correctAnswer);
                    break;
                case 31:
                    const numbers = [];
                    for (let i = 0; i < 4; i++) {
                        numbers.push(Math.floor(Math.random() * 50) + 1);  // Random numbers between 1 and 50
                    }
                    const oddOneOut = numbers[Math.floor(Math.random() * 4)];
                    numbers.sort((a, b) => a - b);
                    numbers[3] = oddOneOut;  // Make sure the "odd one out" is in the list
                    question = `Identify the odd one out from the following numbers: ${numbers.join(", ")}. __`;
                    correctAnswer = oddOneOut;
                    options = generateOptions(correctAnswer);
                    break;
                case 32:
                    const num1LP = Math.floor(Math.random() * 10) + 1;
                    const num2LP = Math.floor(Math.random() * 10) + 1;
                    const num3LP = Math.floor(Math.random() * 10) + 1;
                    const puzzleResult = (num1LP + num2LP) * num3LP;  // Puzzle equation result
    
                    question = `What is the result of ( ${num1LP} + ${num2LP} ) * ${num3LP}? __`;
                    correctAnswer = puzzleResult;
                    options = generateOptions(correctAnswer);
                    break;
                case 33:
                    const hour = Math.floor(Math.random() * 12) + 1;  // Random hour between 1 and 12
                    const minute = Math.floor(Math.random() * 60);  // Random minute between 0 and 59
                    const angle = Math.abs((30 * hour) - (5.5 * minute)).toFixed(2);  // Angle formula = |(30 * hour) - (5.5 * minute)|
    
                    question = `At ${hour}:${minute}, what is the angle between the hour and minute hands? __°`;
                    correctAnswer = angle;
                    options = generateOptions(correctAnswer);
                    break;
                case 34:
                    const opposite = Math.floor(Math.random() * 10) + 1;  // Opposite side length
                    const adjacent = Math.floor(Math.random() * 10) + 1;  // Adjacent side length
                    const hypotenuse = Math.sqrt(opposite**2 + adjacent**2).toFixed(2);  // Hypotenuse using Pythagoras theorem
                    const sine = (opposite / hypotenuse).toFixed(2);
    
                    question = `If a right triangle has opposite side = ${opposite} and adjacent side = ${adjacent}, what is sin(θ)? __`;
                    correctAnswer = sine;
                    options = generateOptions(correctAnswer);
                    break;
                case 35:
                    const opposite2 = Math.floor(Math.random() * 10) + 1;
                    const adjacent2 = Math.floor(Math.random() * 10) + 1;
                    const angleInRad = Math.atan(opposite2 / adjacent2).toFixed(2);  // Angle using arctangent
    
                    question = `For a right triangle with opposite side = ${opposite2} and adjacent side = ${adjacent2}, what is tan(θ)? __`;
                    correctAnswer = (opposite2 / adjacent2).toFixed(2);  // Tangent = opposite/adjacent
                    options = generateOptions(correctAnswer);
                    break;
                case 36:
                    const sideA = Math.floor(Math.random() * 10) + 1;
                    const sideB = Math.floor(Math.random() * 10) + 1;
                    const hypotenuseLength = Math.sqrt(sideA**2 + sideB**2).toFixed(2);
    
                    question = `For a right triangle with sides ${sideA} and ${sideB}, what is the length of the hypotenuse? __`;
                    correctAnswer = hypotenuseLength;
                    options = generateOptions(correctAnswer);
                    break;
                case 37:
                    const opposite3 = Math.floor(Math.random() * 10) + 1;
                    const adjacent3 = Math.floor(Math.random() * 10) + 1;
                    const angleInDeg = Math.atan(opposite3 / adjacent3) * (180 / Math.PI);  // Convert from radians to degrees
    
                    question = `If the opposite side is ${opposite3} and the adjacent side is ${adjacent3}, what is the angle θ? __°`;
                    correctAnswer = angleInDeg.toFixed(2);
                    options = generateOptions(correctAnswer);
                    break;
                case 38:
                    const cosTheta = Math.random().toFixed(2);
                    const sinTheta = Math.sqrt(1 - cosTheta**2).toFixed(2);  // Using sin²θ + cos²θ = 1 to find sin(θ)
    
                    question = `If cos(θ) = ${cosTheta}, what is sin(θ)? __`;
                    correctAnswer = sinTheta;
                    options = generateOptions(correctAnswer);
                    break;
                case 39:
                    const distanceToObject = Math.floor(Math.random() * 100) + 1;  // Distance to the object (in meters)
                    const angleOfElevation = Math.floor(Math.random() * 45) + 1;  // Angle of elevation in degrees
                    const height = (distanceToObject * Math.tan(angleOfElevation * Math.PI / 180)).toFixed(2);  // Calculate height
    
                    question = `A person stands ${distanceToObject} meters from a building. Given the angle of elevation is ${angleOfElevation}°, what is the building's height? __ meters.`;
                    correctAnswer = height;
                    options = generateOptions(correctAnswer);
                    break;

            }
    
            const questionStr = `${question} (Options: ${options.join(", ")})`;
            if (usedQuestions.includes(questionStr)) {
                return generateQuestion();
            } else {
                usedQuestions.push(questionStr);
                return {
                    question,
                    correct: correctAnswer,
                    options
                };
            }
        }

        function generateOptions(correctAnswer) {
            const incorrectAnswers = [
                correctAnswer + Math.floor(Math.random() * 5) + 1,
                correctAnswer - Math.floor(Math.random() * 5) - 1
            ];

            while (incorrectAnswers.includes(correctAnswer)) {
                incorrectAnswers[0] = correctAnswer + Math.floor(Math.random() * 5) + 1;
                incorrectAnswers[1] = correctAnswer - Math.floor(Math.random() * 5) - 1;
            }

            const allOptions = [correctAnswer, ...incorrectAnswers];
            return allOptions.sort(() => Math.random() - 0.5);
        }
        function generateOptionsForString(correctAnswer) {
            const incorrectAnswers = [
                correctAnswer === "Even" ? "Odd" : "Even"
            ];
            const allOptions = [correctAnswer, ...incorrectAnswers];
            return allOptions.sort(() => Math.random() - 0.5);
        }

        function createConfetti() {
            const colors = ['#ff3b30', '#ff9500', '#4cd964', '#007aff', '#5856d6', '#ff2d55'];
            for (let i = 0; i < 50; i++) {
                const piece = document.createElement('div');
                piece.classList.add('confetti-piece');
                piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                piece.style.left = Math.random() * 100 + 'vw';
                piece.style.animationDuration = Math.random() * 2 + 2 + 's';
                piece.style.animationDelay = Math.random() * 2 + 's';
                confettiContainer.appendChild(piece);
            }
            setTimeout(() => confettiContainer.innerHTML = '', 5000);
        }
        function handleOptionClick(isCorrect) {
            const correctSound = document.getElementById('correct-sound');
            const wrongSound = document.getElementById('wrong-sound');
            
            if (isCorrect) {
                correctSound.play(); // Play correct sound
            } else {
                wrongSound.play(); // Play wrong sound
            }
            setTimeout(() => handleOptionClick(true), 1000);  // Correct answer simulation
            setTimeout(() => handleOptionClick(false), 3000);
        }

        function loadQuestion() {
            if (questionCount >= 1000) {
                endGame();
                return;
            }

            const { question, correct, options } = generateQuestion();
            questionEl.textContent = question;
            optionsEl.innerHTML = '';
            options.forEach(option => {
                const button = document.createElement('button');
                button.textContent = option;
                button.classList.add('option');
                button.onclick = () => {
                    const filledQuestion = `${question.split('__')[0]}<span class="${option === correct ? 'correct' : 'incorrect'}">${option}</span>${question.split('__')[1]}`;
                    questionEl.innerHTML = filledQuestion;
                    button.disabled = true;

                    if (option === correct) {
                        // Calculate XP gain based on question difficulty
                        const xpGain = calculateExperienceGain(1); // You can adjust difficulty based on question type
                        experiencePoints += xpGain;
                        checkLevelUp();
    
                        score += 10;
                        scoreEl.textContent = score;
                        createConfetti();
                        startTimer();
                        questionCount++;
                        setTimeout(loadQuestion, 1000);
                    } else {
                        lives--;
                        updateLivesDisplay();
                        if (lives <= 0) {
                            endGame();
                        }
                    }
                };

                optionsEl.appendChild(button);
            });
        }

        function skipQuestion() {
            clearInterval(timer);
            startTimer();
            questionCount++;
            loadQuestion();
        }

        function endGame() {
            clearInterval(timer);
            finalScoreEl.textContent = score;
            gameOverEl.style.display = 'flex';
        }
        function gameOver() {
            const gameOverSound = document.getElementById('game-over-sound');
            gameOverSound.play(); // Play game over sound
            setTimeout(gameOver, 5000);
        }

        skipBtn.onclick = skipQuestion;
        tryAgainBtn.onclick = () => {
            score = 0;
            lives = 5;
            questionCount = 0;
            currentLevel = 1;
            experiencePoints = 0;
            experienceToNextLevel = 100;
            updateLivesDisplay();
            updateLevelDisplay();
            scoreEl.textContent = score;
            gameOverEl.style.display = 'none';
            startTimer();
            loadQuestion();
        };

        exitBtn.onclick = () => {
            window.close();
        };

        // Game start logic
        startTimer();
        loadQuestion();
        document.addEventListener('DOMContentLoaded', () => {
            updateLevelDisplay();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True)
