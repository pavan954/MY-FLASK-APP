from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Number Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
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
            border: 10px solid #ff6600;
            background-color: #fff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 20px;
        }
        .timer-text {
            font-size: 1.5rem;
            font-weight: bold;
            color: #40E0D0;
            position: absolute;
        }
        .circle-background {
            width: 100%;
            height: 100%;
            position: absolute;
            border-radius: 50%;
            background-color: #DCDCDC;
        }
        .progress-ring {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(#B22222 calc(var(--percent) * 1%), #cccccc calc(var(--percent) * 1%));
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
            display: none; /* Initially hidden */
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh; /* Full height of the viewport */
            background-color: rgba(255, 255, 255, 0.9); /* Transparent background */
            z-index: 100; /* Ensure it's on top of everything */
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

        /* Correct / Incorrect Answer Styling */
        .correct {
            color: green;
            font-weight: bold;
        }
        .incorrect {
            color: red;
            font-weight: bold;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .score-time {
                flex-direction: column;
                align-items: center;
            }
            .score {
                font-size: 1.8rem;
            }
            .timer {
                width: 60px;
                height: 60px;
            }
            .timer-text {
                font-size: 1.2rem;
            }
            .question {
                font-size: 8vw;
            }
            .option {
                flex: 1 1 45%;
                font-size: 1.3rem;
            }
            .game-over h2 {
                font-size: 1.5rem;
            }
            .game-over p {
                font-size: 1.2rem;
            }
        }

        @media (max-width: 480px) {
            .score-time {
                flex-direction: column;
                align-items: center;
                padding: 0;
            }
            .score {
                font-size: 1.5rem;
            }
            .timer {
                width: 50px;
                height: 50px;
            }
            .timer-text {
                font-size: 1rem;
            }
            .question {
                font-size: 10vw;
            }
            .option {
                flex: 1 1 100%;
                font-size: 1.2rem;
            }
            button {
                padding: 12px 25px;
                font-size: 1.3rem;
            }
            .game-over h2 {
                font-size: 1.2rem;
            }
            .game-over p {
                font-size: 1.1rem;
            }
        }
    </style>
</head>
<body>
    <div style="font-size: 1.5rem; font-weight: bold; color: #333; margin-bottom: 10px;">Number Game</div>
    <div class="score-time">
        <div>Score: <span id="score" class="score">0</span></div>
        <div id="lives" style="font-size: 1.5rem; font-weight: bold; color: #ffffff; background-color: #ff0000; padding: 10px 20px; border-radius: 12px; margin-top: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); animation: bounce 1s ease-in-out infinite, pulse 1.5s ease-in-out infinite;">Lives: 5</div>
        <div class="timer">
            <div class="circle-background"></div>
            <div class="progress-ring" id="progress-ring" style="--percent: 100;"></div>
            <span class="timer-text" id="timer-text">30</span>
        </div>
    </div>
    <div class="question" id="question">Loading...</div>
    <div class="options" id="options"></div>
    <button id="skip" class="skip-button">Skip</button>
    <div class="confetti" id="confetti"></div>
    <div class="game-over" id="game-over" style="display: none;">
        <h2>Game Over!</h2>
        <p>Final Score: <span id="final-score">0</span></p>
        <div>
            <button id="try-again">Try Again</button>
            <button id="exit" class="exit-button">Exit</button>
        </div>
    </div>

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
    const operationType = Math.floor(Math.random() * 9); // Adjusted to include cases from 0 to 8

    let question, correctAnswer, options;

    switch (operationType) {
        case 0:  // Addition
            const resultAdd = Math.floor(Math.random() * 20) + num1;
            question = `${num1} + __ = ${resultAdd}`;
            correctAnswer = resultAdd - num1;
            options = generateOptions(correctAnswer);
            break;
        case 1:  // Subtraction
            const resultSub = num1 + Math.floor(Math.random() * 10) + 1;
            question = `${num1} - __ = ${resultSub}`;
            correctAnswer = num1 - resultSub;
            options = generateOptions(correctAnswer);
            break;
        case 2:  // Multiplication
            const resultMul = num1 * Math.floor(Math.random() * 12) + 1;
            question = `${num1} * __ = ${resultMul}`;
            correctAnswer = resultMul / num1;
            options = generateOptions(correctAnswer);
            break;
        case 3:  // Division
            const divisor = Math.floor(Math.random() * 10) + 1;
            const resultDiv = num1 * divisor;  // Ensures we have a valid result
            question = `${resultDiv} ÷ __ = ${num1}`;
            correctAnswer = divisor;
            options = generateOptions(correctAnswer);
            break;
        case 4:  // Complex addition
            const num2 = Math.floor(Math.random() * 20) + 1;
            const resultAdd2 = Math.floor(Math.random() * 20) + num1 + num2;
            question = `${num1} + __ + ${num2} = ${resultAdd2}`;
            correctAnswer = resultAdd2 - num1 - num2;
            options = generateOptions(correctAnswer);
            break;
        case 5:  // Complex subtraction
            const num3 = Math.floor(Math.random() * 10) + 1;
            const resultSub2 = num1 + num3;
            question = `${num1} - __ - ${num3} = ${resultSub2}`;
            correctAnswer = num1 - resultSub2 - num3;
            options = generateOptions(correctAnswer);
            break;
        case 6:  // Complex multiplication
            const num4 = Math.floor(Math.random() * 12) + 1;
            const resultMul2 = num1 * num4;
            question = `${num1} * __ * ${num4} = ${resultMul2}`;
            correctAnswer = resultMul2 / (num1 * num4);;
            options = generateOptions(correctAnswer);
            break;
        case 7:  // Complex division
            const num5 = Math.floor(Math.random() * 10) + 1;
            const resultDiv2 = num1 * num5;
            question = `${num1} ÷ __ ÷ ${num5} = ${resultDiv2}`;
            correctAnswer = num1 / (resultDiv2 * num5);
            options = generateOptions(correctAnswer);
            break;
    }

    const questionStr = `${question} (Options: ${options.join(", ")})`;
    if (usedQuestions.includes(questionStr)) {
        return generateQuestion();  // Ensure no duplicate questions
    } else {
        usedQuestions.push(questionStr);
        return {
            question,
            correct: correctAnswer,
            options
        };
    }
}

// Function to generate options (one correct answer, two wrong ones)
function generateOptions(correctAnswer) {
    const incorrectAnswers = [
        correctAnswer + Math.floor(Math.random() * 5) + 1,
        correctAnswer - Math.floor(Math.random() * 5) - 1
    ];

    // Make sure there are no duplicates among the options
    while (incorrectAnswers.includes(correctAnswer)) {
        incorrectAnswers[0] = correctAnswer + Math.floor(Math.random() * 5) + 1;
        incorrectAnswers[1] = correctAnswer - Math.floor(Math.random() * 5) - 1;
    }

    // Shuffle the options so the correct answer isn't always in the same place
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

        function loadQuestion() {
            if (questionCount >= 100) {
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
                        score += 10;
                        scoreEl.textContent = score;
                        createConfetti();
                        startTimer();
                        questionCount++;
                        setTimeout(loadQuestion, 1000);
                    } else {
                        lives--;  // Reduce a life on incorrect answer
                        updateLivesDisplay();  // Update the life display
                        if (lives <= 0) {
                            endGame();  // Trigger game over if no lives remain
                        }
                    }
                };

                optionsEl.appendChild(button);
            });
        }

        function skipQuestion() {
            clearInterval(timer); // Stop the current timer
            startTimer(); // Restart the timer
            questionCount++; // Increment question count
            loadQuestion(); // Load the next question
        }

        skipBtn.addEventListener('click', skipQuestion);

        function endGame() {
            clearInterval(timer);
            finalScoreEl.textContent = score;
            gameOverEl.style.display = 'flex'; // Display Game Over screen
            document.body.style.overflow = 'hidden'; // Disable scrolling during game over
        }

        function startGame() {
            score = 0;
            questionCount = 0;
            lives = 5;
            scoreEl.textContent = score;
            updateLivesDisplay();
            gameOverEl.style.display = 'none';
            startTimer();
            loadQuestion();
        }

        tryAgainBtn.addEventListener('click', startGame);
        exitBtn.addEventListener('click', () => window.close());

        window.onload = startGame;
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True)
