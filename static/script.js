
const keyboard = document.getElementById("keyboard");
const wordDisplay = document.getElementById("word-display");
const hintDisplay = document.getElementById("hint");
const attemptsDisplay = document.getElementById("attempts");
const message = document.getElementById("message");
const restartButton = document.getElementById("restart-btn");
const scoreDisplay = document.getElementById("score");

let gameOver = false;

const bodyParts = [
    "head",
    "body",
    "left-arm",
    "right-arm",
    "left-leg",
    "right-leg"
];

// Create alphabet buttons
function createKeyboard() {
    keyboard.innerHTML = "";

    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);

        const button = document.createElement("button");
        button.textContent = letter;

        button.addEventListener("click", () => {
            makeGuess(letter.toLowerCase(), button);
        });

        keyboard.appendChild(button);
    }
}

// Draw the person according to wrong guesses
function updateHangman(wrongGuesses) {
    bodyParts.forEach((part, index) => {
        const element = document.getElementById(part);

        if (index < wrongGuesses) {
            element.classList.add("show");
        } else {
            element.classList.remove("show");
        }
    });
}

// Start a new game
async function newGame() {
    try {
        const response = await fetch("/new_game", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to start game");
        }

        gameOver = false;

        hintDisplay.textContent = data.hint;
        wordDisplay.textContent = data.word;

        attemptsDisplay.textContent =
            "Remaining Attempts: " + data.attempts;

        scoreDisplay.textContent = data.score + " / 60";

        updateHangman(0);

        message.textContent = "Choose a letter to begin!";
        message.classList.remove("win-animation");

        createKeyboard();

    } catch (error) {
        message.textContent = "Unable to start game. Please refresh!";
        console.error(error);
    }
}

// Guess a letter
async function makeGuess(letter, button) {
    if (gameOver || button.disabled) {
        return;
    }

    button.disabled = true;

    try {
        const response = await fetch("/guess", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                letter: letter
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.error;
            button.disabled = false;
            return;
        }

        wordDisplay.textContent = data.word;

        attemptsDisplay.textContent =
            "Remaining Attempts: " + data.attempts;

        scoreDisplay.textContent = data.score + " / 60";

        updateHangman(data.wrong_guesses);

        if (data.status === "won") {
            message.textContent =
                "🎉 Congratulations! You won! " +
                data.round_score + " / 60 marks!";

            message.classList.add("win-animation");
            gameOver = true;

        } else if (data.status === "lost") {
            message.textContent =
                "😢 Game Over! The word was " + data.secret_word +
                ". You scored 0 / 60.";

            gameOver = true;

        } else if (data.word.split(" ").includes(letter)) {
            message.textContent = "✅ Excellent! Correct guess!";

        } else {
            message.textContent = "❌ Wrong guess! Try again.";
        }

        if (gameOver) {
            document.querySelectorAll(".keyboard button")
                .forEach(btn => btn.disabled = true);
        }

    } catch (error) {
        message.textContent = "Something went wrong. Try again!";
        button.disabled = false;
        console.error(error);
    }
}

restartButton.addEventListener("click", newGame);

newGame();
