const $guessForm = $("#submit-guess");
const $msg = $("#message");
const $score = $("#score");
const $timer = $("#timer");

let score = 0;

async function checkGuess(e) {
    e.preventDefault();
    const guess = $("#guess-word").val()

    const res = await axios.get("/submit-guess", { params: { guess: guess}});
    const responseVal = res.data.result;

    if(responseVal == "ok") {
        score += guess.length;
    }
    showScore(score);
    showMessage(responseVal, score);
}

let timeLeft = 5;
let gameTimer;

function timer() {
    gameTimer = setInterval(updateTimer, 1000);
}

timer();

function updateTimer() {
    timeLeft -= 1;
    showTimer(timeLeft);
    if(timeLeft == 0) {
        clearInterval(gameTimer);
        $guessForm.hide();
        postScore(score);
    }
}

function showTimer(seconds) {
    $timer.text(`${seconds} seconds remaining!`);
}

function showScore(score) {
    $score.text(`Score: ${score}`);
}

async function postScore(score) {
    const res = await axios.post("/post-score", { score: score});
    return res;
}

function showMessage(message) {
    $msg.text(message);
}

$guessForm.on("submit", checkGuess);