//const { Howl, Howler } = require("howler");

var tadLeft;
var tadBottom;

var dataDisplayActive = false;

var socketio;

fetch(
	"https://api.nasa.gov/planetary/apod?api_key=***REMOVED***"
).then(async (result) => {
	var json = await result.json();
	console.log(json);
	$("#body").css("background-image", `url(${json.url})`);
	// $("#body").css("background-image", `url(${json.hdurl})`);
});

$(document).ready(async function () {
	// updateConfig();
	// use ipc to load config and then use it to change config

	setInterval(() => {
		if (new Date().getHours() === 6) {
			fetch(
				"https://api.nasa.gov/planetary/apod?api_key=***REMOVED***"
			).then(async (result) => {
				var json = await result.json();
				console.log(json);
				$("#body").css("background-image", `url(${json.url})`);
				// $("#body").css("background-image", `url(${json.hdurl})`);
			});
		}
	}, 1000 * 60 * 60);
});

function refreshTime() {
	//time
	const timeDisplay = document.getElementById("time");
	const timeString = new Date().toLocaleTimeString("en-US");
	timeDisplay.textContent = timeString;

	//date
	const dateDisplay = document.getElementById("date");
	const date = new Date();
	const formattedDate = new Intl.DateTimeFormat("en-GB", {
		day: "numeric",
		month: "long",
		year: "numeric",
	}).format(date);

	dateDisplay.textContent = formattedDate;
}
setInterval(refreshTime, 1000);
refreshTime();

eel.expose(showListening);

function showListening() {
	console.log("show");

	$("#listening").removeClass("fadeout");
	$("#listening").addClass("fadein");
	setTimeout(function () {
		$("#listening").css({ opacity: 1 });
		$(".bar").each(function () {
			$(this).addClass("bar-animation");
		});
	}, 249);
}

eel.expose(hideListening);

function hideListening() {
	$("#listening").removeClass("fadein");
	$("#listening").addClass("fadeout");
	setTimeout(function () {
		$("#listening").css({ opacity: 0 });
		$(".bar").each(function () {
			$(this).removeClass("bar-animation");
		});
	}, 249);
}
