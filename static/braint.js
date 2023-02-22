// Vars (Maybe used by multiple scripts)
var currentDate = new Date();
var currentDay = currentDate.getDay();
var completionCode = currentDate.getFullYear().toString()+(currentDate.getMonth()+1).toString()+currentDate.getDate().toString();
const daysByIdx = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];

// Functions (Maybe used by multiple scripts)
function displayMessage(msg) {
	var messageDiv = document.createElement("div");
	messageDiv.id = "message-div";
	var message = document.createElement("p");
	message.innerHTML = msg;
	messageDiv.appendChild(message);
	var checkMark = document.createElement("img");
	checkMark.src = "/static/images/checkmark.png";
	messageDiv.appendChild(checkMark);
	document.body.appendChild(messageDiv);

	setTimeout(() => {
		messageDiv.remove();
	}, 5000);
}

function displayError(err = "Something went wrong!") {
	var errorDiv = document.createElement("div");
	errorDiv.id = "error";
	var errorHead = document.createElement("div");
	errorHead.id = "error-head";
	errorDiv.appendChild(errorHead);
	var errorHeading = document.createElement("h2");
	errorHeading.innerHTML = "Error!";
	errorHead.appendChild(errorHeading);

	var errorBody = document.createElement("div");
	errorBody.id = "error-body";
	errorDiv.appendChild(errorBody);
	
	var errorText = document.createElement("p");
	errorText.innerHTML = err;
	errorBody.appendChild(errorText);
	
	var lineBreak = document.createElement("br");
	errorDiv.appendChild(lineBreak);
	
	var dismissButton = document.createElement("button");
	dismissButton.innerHTML = "Dismiss";
	dismissButton.id = "dismiss-button";
	dismissButton.addEventListener('click', e => {
		// window.location.reload();
		document.body.style.pointerEvents = "auto";
		document.body.style.userSelect = "auto";
		errorDiv.remove();
	});
	errorBody.appendChild(dismissButton);

	document.body.style.pointerEvents = "none";
	errorDiv.style.pointerEvents = "auto";
	document.body.style.userSelect = "none";
	
	document.body.appendChild(errorDiv);
}

