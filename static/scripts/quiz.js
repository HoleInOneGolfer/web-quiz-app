// Set background images
function getImageUrl(path) {
	return `${window.location.origin}${path.startsWith("/") ? "" : "/"}${path}`;
}

const bgImage = SHEET_DATA[0].bgImage
	? getImageUrl(`/static/images/${SHEET_DATA[0].bgImage}`)
	: getImageUrl("/static/images/placeholders/bg-placeholder.jpg");

START.style.backgroundImage = `url('${bgImage}')`;
INFO.style.backgroundImage = `url('${bgImage}')`;
MAIN.style.backgroundImage = `url('${bgImage}')`;
FINISH.style.backgroundImage = `url('${bgImage}')`;

// Set logo
LOGO.innerHTML = `<img src="/static/images/logo.png" alt="Logo">`;

// Set the current state to START */
let CURRENT_STATE = QUIZ_STATE.START;
updateDOMState();

/** Set Hint Image  */
function setHint() {
	//HINT_TOGGLE.style.backgroundImage = SHEET_DATA[CURRENT_QUESTION].hImage ? SHEET_DATA[CURRENT_QUESTION].hImage : "static/images/Hint-Person-Placeholder.png";
	HINT_TOGGLE.innerHTML = SHEET_DATA[CURRENT_QUESTION].hImage
		? `<img src="/static/images/${SHEET_DATA[0].hImage}" alt="Hint Image">`
		: `<img src="/static/images/placeholders/Hint-Person-Placeholder.png" alt="Hint Image">`;
	HINT_TEXT.innerHTML = SHEET_DATA[CURRENT_QUESTION].hint;
}
/** Toggle Hint and set `hint_used` to `true` for the session */
function toggleHint() {
	SESSION["QUESTION_" + CURRENT_QUESTION + "_HINT_USED"] = true;
	HINT_TEXT.classList.toggle("hidden");
}
/** Hide the Hint */
function disableHint() {
	HINT_TEXT.classList.toggle("hidden", true);
}

/** update DOM based on state */
function updateDOMState() {
	switch (CURRENT_STATE) {
		case QUIZ_STATE.START:
			START.style.display = "flex";
			INFO.style.display = "none";
			MAIN.style.display = "none";
			FINISH.style.display = "none";
			break;
		case QUIZ_STATE.INFO:
			START.style.display = "none";
			INFO.style.display = "flex";
			MAIN.style.display = "none";
			FINISH.style.display = "none";
			break;
		case QUIZ_STATE.MAIN:
			START.style.display = "none";
			INFO.style.display = "none";
			MAIN.style.display = "flex";
			FINISH.style.display = "none";
			break;
		case QUIZ_STATE.FINISH:
			START.style.display = "none";
			INFO.style.display = "none";
			MAIN.style.display = "none";
			FINISH.style.display = "flex";
			break;
	}
}

/** Set state function - Start */
function setStateStart() {
	CURRENT_STATE = QUIZ_STATE.START;
	CURRENT_QUESTION = 0;

	resetSession();
	updateDOMState();
}

function setStateInfo() {
	CURRENT_QUESTION = 0;

	resetSession();

	CURRENT_STATE = QUIZ_STATE.INFO;
	updateDOMState();
}

/** Set state function - Main */
function setStateMain() {
	CURRENT_STATE = QUIZ_STATE.MAIN;
	resetSession();

	disableHint();
	setHint();

	MUSIC.play();

	loadQuestion();
	updateStatus();

	SESSION.START_TIME = Date.now();
	updateDOMState();
}

/** Set state function - Finish  */
function setStateFinish() {
	CURRENT_STATE = QUIZ_STATE.FINISH;
	SESSION.END_TIME = Date.now();
	SESSION.TOTAL_TIME_MS = SESSION.END_TIME - SESSION.START_TIME;

	finishDOM();
	updateDOMState();
	sendData();
}

/** Reset SESSION */
function resetSession() {
	SESSION.SCORE = 0;
	SESSION.START_TIME = 0;
	SESSION.END_TIME = 0;
	SESSION.TOTAL_TIME_MS = 0;
	for (var i = 0; i < SESSION.NUMBER_OF_QUESTIONS; i++) {
		SESSION["QUESTION_" + i + "_HINT_USED"] = false;
		SESSION["QUESTION_" + i + "_TRIES_TAKEN"] = 0;
		SESSION["QUESTION_" + i + "_CORRECT"] = false;
		SESSION["QUESTION_" + i + "_SELECTIONS"] = "";
	}
}

/** Next Question */
function nextQuestion() {
	if (CURRENT_QUESTION < SHEET_DATA.length - 1) {
		CURRENT_QUESTION++;
	} else {
		setStateFinish();
	}

	loadQuestion();
	disableHint();
	setHint();
	updateStatus();
}

/** finish DOM */
function finishDOM() {
	QUIZ_RESULTS.innerHTML = `<h2>${
		(SESSION.SCORE / SHEET_DATA.length) * 100 > 70
			? "Congratulations!"
			: "Better Luck Next Time!"
	}</h2>
         <p>You have completed the quiz!</p>
         <p>Your score is: ${parseInt(
						(SESSION.SCORE / SHEET_DATA.length) * 100
					)}%</p>`;
}

/** Status */
function updateStatus() {
	QUIZ_STATUS.innerHTML = `Question ${CURRENT_QUESTION + 1}/${
		SHEET_DATA.length
	}`;
	QUIZ_SCORE.innerHTML = `Score ${parseInt(
		(SESSION.SCORE / SHEET_DATA.length) * 100
	)}%`;
	QUIZ_TRIES.innerHTML = `${TRIES}/${MAX_TRIES} Tries Remaining`;
}

/** load question */
function loadQuestion() {
	// Set the question
	QUESTION.innerHTML = SHEET_DATA[CURRENT_QUESTION].question;

	// Set the answers
	for (var i = 0; i < ANSWERS.length; i++) {
		if (SHEET_DATA[CURRENT_QUESTION].answers[i]) {
			ANSWERS[i].classList.toggle("correct", false);
			ANSWERS[i].classList.toggle("incorrect", false);
			ANSWERS[i].innerHTML = SHEET_DATA[CURRENT_QUESTION].answers[i];
			ANSWERS[i].classList.toggle("hidden", false);
		} else {
			ANSWERS[i].classList.toggle("hidden", true);
		}
	}

	// remove animation from nextQuestion
	NEXT_QUESTION.classList.remove("animate-button");

	// set Tries
	MAX_TRIES = 0;
	for (var i = 0; i < SHEET_DATA[CURRENT_QUESTION].answers.length; i++) {
		if (SHEET_DATA[CURRENT_QUESTION].answers[i]) {
			MAX_TRIES++;
		}
	}
	MAX_TRIES--;
	TRIES = MAX_TRIES;
}

/** answer */
function answerEvent(answerIndex) {
	if (
		TRIES > 0 &&
		!SESSION["QUESTION_" + CURRENT_QUESTION + "_SELECTIONS"].includes(
			answerIndex
		) &&
		!SESSION["QUESTION_" + CURRENT_QUESTION + "_CORRECT"]
	) {
		if (SHEET_DATA[CURRENT_QUESTION].correctAnswers[answerIndex]) {
			CORRECT.currentTime = 0;
			CORRECT.play();
			SESSION["QUESTION_" + CURRENT_QUESTION + "_CORRECT"] = true;
			SESSION.SCORE++;
			ANSWERS[answerIndex].classList.toggle("correct", true);
			NEXT_QUESTION.classList.toggle("animate-button", true);
		} else {
			INCORRECT.currentTime = 0;
			INCORRECT.play();
			ANSWERS[answerIndex].classList.toggle("incorrect", true);
		}
		SESSION["QUESTION_" + CURRENT_QUESTION + "_SELECTIONS"] +=
			answerIndex + ",";
		TRIES--;
		SESSION["QUESTION_" + CURRENT_QUESTION + "_TRIES_TAKEN"]++;

		if (TRIES <= 0) {
			// reveal correct answer
			for (
				var i = 0;
				i < SHEET_DATA[CURRENT_QUESTION].correctAnswers.length;
				i++
			) {
				if (SHEET_DATA[CURRENT_QUESTION].correctAnswers[i]) {
					ANSWERS[i].classList.toggle("correct", true);
				}
			}
			NEXT_QUESTION.classList.toggle("animate-button", true);
		}

		updateStatus();
	}
}

/** audio controls */
function toggleAudio() {
	AUDIO = !AUDIO;
	for (let index = 0; index < AUDIOS.length; index++) {
		const element = AUDIOS[index];
		element.muted = !AUDIO;
	}
	AUDIO_TOGGLE.innerText = AUDIO ? "volume_up" : "volume_off";
}

/** User timeout after 60 seconds of inactivity */
function debounce(callback, timeout, _this) {
	var timer;
	return function (e) {
		var _that = this;
		if (timer) clearTimeout(timer);
		timer = setTimeout(function () {
			callback.call(_this || _that, e);
		}, timeout);
	};
}

/** User timeout after 60 seconds of inactivity */
var userAction = debounce(function (e) {
	setStateStart();
	MUSIC.pause();
	MUSIC.currentTime = 0;
}, 60 * 1000);

var refresh = debounce(function (e) {
	location.reload();
}, 15 * 60 * 1000);

/** User timeout after 60 seconds of inactivity */
document.body.onload = () => {
	document.addEventListener("mousemove", userAction, false);
	document.addEventListener("click", userAction, false);
	document.addEventListener("scroll", userAction, false);
	document.addEventListener("keypress", userAction, false);

	document.addEventListener("mousemove", refresh, false);
	document.addEventListener("click", refresh, false);
	document.addEventListener("scroll", refresh, false);
	document.addEventListener("keypress", refresh, false);
};

/** send analytics to server */
function sendData() {
	fetch("/send_score", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ SESSION }),
	}).catch((err) => console.error(err));
}
