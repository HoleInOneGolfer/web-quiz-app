// Process the raw data from sheets to a quiz
const RAW_SHEET_DATA = JSON.parse($("#sheet-data").text());
const SHEET_DATA = [];

// Create questions in the quiz
for (var i = 0; i < RAW_SHEET_DATA.length; i++) {
	var q = {};
	// Set the question
	q.question = RAW_SHEET_DATA[i].question_text;

	q.answers = [];
	// Set the answers
	if (RAW_SHEET_DATA[i].answer_1 != "") {
		q.answers.push(RAW_SHEET_DATA[i].answer_1);
	}
	if (RAW_SHEET_DATA[i].answer_2 != "") {
		q.answers.push(RAW_SHEET_DATA[i].answer_2);
	}
	if (RAW_SHEET_DATA[i].answer_3 != "") {
		q.answers.push(RAW_SHEET_DATA[i].answer_3);
	}
	if (RAW_SHEET_DATA[i].answer_4 != "") {
		q.answers.push(RAW_SHEET_DATA[i].answer_4);
	}

	// Set the correct Answers
	q.correctAnswers = [];
	if (RAW_SHEET_DATA[i].answer_1_correct == true) {
		q.correctAnswers.push(1);
	}
	if (RAW_SHEET_DATA[i].answer_2_correct == true) {
		q.correctAnswers.push(2);
	}
	if (RAW_SHEET_DATA[i].answer_3_correct == true) {
		q.correctAnswers.push(3);
	}
	if (RAW_SHEET_DATA[i].answer_4_correct == true) {
		q.correctAnswers.push(4);
	}

	// Set the hint
	q.hint = RAW_SHEET_DATA[i].hint;

	// Set the image
	q.bgImage = RAW_SHEET_DATA[i].bg_image;
	q.hImage = RAW_SHEET_DATA[i].hint_image;

	// push to the array
	SHEET_DATA.push(q);
}

// tries
let MAX_TRIES = 0;
let TRIES = 0;

// Set the current question
let CURRENT_QUESTION = 0;

// Session array
const SESSION = {
	QUIZ_NAME: document.title,
	START_TIME: 0,
	END_TIME: 0,
	TOTAL_TIME_MS: 0,
	SCORE: 0,
	NUMBER_OF_QUESTIONS: SHEET_DATA.length,
};
// Session
for (var i = 0; i < SHEET_DATA.length; i++) {
	SESSION["QUESTION_" + i + "_HINT_USED"] = false;
	SESSION["QUESTION_" + i + "_TRIES_TAKEN"] = 0;
	SESSION["QUESTION_" + i + "_CORRECT"] = false;
	SESSION["QUESTION_" + i + "_SELECTIONS"] = "";
}

// States
const QUIZ_STATE = {
	START: 0,
	INFO: 1,
	MAIN: 2,
	FINISH: 3,
};

// audio boolean
let AUDIO = true;

console.log("DATA.js Loaded Successfully ✅...");
