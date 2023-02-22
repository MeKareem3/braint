// Refresh calendar
function refreshContent() {
	// Highlight current day as shown on the calendar
	document.querySelector(`table tr:nth-child(1) td:nth-child(${currentDay != 0 ? currentDay : 7})`).style.cssText = "background-color: lightgrey; font-weight: bold;";
	
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/api/v1/tasks", true);
	
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Retrieve information
			tasks = JSON.parse(xhr.responseText).tasks;

			// Clear Calendar
			var calendarLists = document.querySelectorAll("#all-tasks td ul");
			
			for (let i = 0; i < calendarLists.length; i++) {
				calendarLists[i].innerHTML = "";
			}
			
			for (let i = 0; i < tasks.length; i++) {
				// Get JSON taskDATA
				var taskData = tasks[i].at(-1);

				// Iterate through days
				for (let j = 0; j < 7; j++) {
					if (taskData[daysByIdx[j]]) {
						var target = document.querySelector(`#all-tasks td:nth-child(${j != 0 ? j : 7}) ul`);
						
						target.innerHTML += `<li class="display-task" id="${tasks[i][0]}">${tasks[i][1]}</li>`;
					} else {
						continue;
					}
				}
			}
		}
	};
	
	xhr.send();
}

refreshContent();