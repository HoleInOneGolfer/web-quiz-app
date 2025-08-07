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
