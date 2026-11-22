
from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = "hangman_secret_key"

words = {
    "apple": "A fruit that keeps the doctor away",
    "tiger": "A wild animal with black stripes",
    "python": "A popular programming language",
    "school": "A place where students learn",
    "flower": "A beautiful part of a plant",
    "elephant": "The largest land animal",
    "computer": "An electronic device",
    "rainbow": "Appears after rain",
    "guitar": "A musical instrument with strings",
    "butterfly": "An insect with colorful wings",
    "cricket": "A popular sport with bat and ball",
    "diamond": "A precious sparkling stone",
    "chocolate": "A sweet treat made from cocoa",
    "hospital": "A place where doctors work",
    "mountain": "A very tall natural elevation",
    "telephone": "Used to communicate with people",
    "dolphin": "An intelligent sea animal",
    "umbrella": "Protects you from rain",
    "astronaut": "A person who travels into space",
    "keyboard": "Used to type on a computer",
    "football": "A sport played with a round ball",
    "library": "A place full of books",
    "sunflower": "A yellow flower that follows the sun",
    "volcano": "A mountain that can erupt",
    "pencil": "Used for writing and drawing",
    "octopus": "A sea animal with eight arms",
    "camera": "Used to capture photographs",
    "planet": "A celestial body orbiting a star",
    "raincoat": "Worn to stay dry in rain",
    "strawberry": "A red fruit with tiny seeds"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/new_game", methods=["POST"])
def new_game():
    secret_word = random.choice(list(words.keys()))

    session["secret_word"] = secret_word
    session["guessed_letters"] = []
    session["attempts"] = 6
    session["game_finished"] = False
    session["round_score"] = 60

    return jsonify({
        "hint": words[secret_word],
        "word": "_ " * len(secret_word),
        "attempts": 6,
        "score": 60,
        "status": "playing"
    })


@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json(silent=True) or {}
    letter = data.get("letter", "").lower()

    if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha():
        return jsonify({"error": "Enter one alphabet only"}), 400

    if "secret_word" not in session:
        return jsonify({"error": "Start a new game first"}), 400

    if session.get("game_finished"):
        return jsonify({"error": "Game is already over"}), 400

    secret_word = session["secret_word"]
    guessed_letters = session["guessed_letters"]
    attempts = session["attempts"]

    if letter in guessed_letters:
        return jsonify({"error": "Letter already guessed"}), 400

    guessed_letters.append(letter)

    if letter not in secret_word:
        attempts -= 1

    display_word = " ".join(
        char if char in guessed_letters else "_"
        for char in secret_word
    )

    if all(char in guessed_letters for char in secret_word):
        status = "won"
        round_score = attempts * 10
        session["game_finished"] = True

    elif attempts == 0:
        status = "lost"
        round_score = 0
        session["game_finished"] = True

    else:
        status = "playing"
        round_score = attempts * 10

    session["guessed_letters"] = guessed_letters
    session["attempts"] = attempts
    session["round_score"] = round_score

    return jsonify({
        "word": display_word,
        "attempts": attempts,
        "status": status,
        "secret_word": secret_word if status != "playing" else None,
        "round_score": round_score,
        "score": round_score,
        "wrong_guesses": 6 - attempts
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)