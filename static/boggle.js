const $guessForm = $("#submit-guess");
const $guessInput = $("#guess-word");
const $msg = $("#message");
const $score = $("#score");
const $timer = $("#timer");

class Boggle {
    constructor(board, time) {
        this.timeLeft = time;
        this.gameTimer = setInterval(this.updateTimer.bind(this), 1000);
        this.showTimer();

        this.score = 0;
        this.board = board;
        this.words = new Set();

        $guessForm.on("submit", this.checkGuess.bind(this));
    }

    updateTimer() {
        this.timeLeft -= 1;
        this.showTimer();
        if(this.timeLeft == 0) {
            clearInterval(this.gameTimer);
            $guessForm.hide();
            this.postScore();
        }
    }

    showTimer() {
        $timer.text(`${this.timeLeft} seconds remaining!`);
    }

    async checkGuess(e) {
        e.preventDefault();
        const guess = $guessInput.val();
    
        const res = await axios.get("/submit-guess", { params: { guess: guess}});
        const responseVal = res.data.result;
    
        if(responseVal == "ok" && !this.words.has(guess)) {
            this.score += guess.length;
            this.words.add(guess);
            this.showMessage(`'${guess}' was found!`);
        } else if(responseVal == "not-on-board") {
            this.showMessage(`'${guess}' is not on the board.`);
        } else if(responseVal == "not-word") {
            this.showMessage(`'${guess}' is not a word.`);
        }
        $guessInput.val('');
        this.showScore();
    }

    showScore() {
        $score.text(`Score: ${this.score}`);
    }
    
    async postScore() {
        const res = await axios.post("/post-score", { score: this.score});
        if(res.data.newHighScore) {
            this.showMessage("New High Score! : " + this.score);
        } else {
            this.showMessage("Final Score : " + this.score)
        }
    }
    
    showMessage(message) {
        $msg.text(message);
    }
    
}
