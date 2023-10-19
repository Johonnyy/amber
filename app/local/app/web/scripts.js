var dataDisplayActive = false;

$(document).ready(async function () {
	// use ipc to load config and then use it to change config
	await setImage();

	setInterval(async () => {
		await setImage();
	}, 1000 * 60 * 60);
});

eel.expose(setImage);

async function setImage() {
	config = await eel.get_config()();

	console.log(config);

	if (config.local.source == "nasa") {
		fetch(
			`https://api.nasa.gov/planetary/apod?api_key=${config.local.nasaApiKey}`
		).then(async (result) => {
			var json = await result.json();
			$("#body").css("background-image", `url(${json.hdurl})`);
			// $("#body").css("background-image", `url(${json.hdurl})`);
		});
	} else if (config.local.source == "bing") {
		fetch("https://bing.biturl.top/").then(async (result) => {
			var json = await result.json();
			$("#body").css("background-image", `url(${json.url})`);
			// $("#body").css("background-image", `url(${json.hdurl})`);
		});
	}
}

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

eel.expose(closeApp);

function closeApp() {
	window.close();
}
