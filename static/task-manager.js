var uncompletedTasksContainer = document.getElementById("uncompleted-tasks");
var completedTasksContainer = document.getElementById("completed-tasks");


// Get tasks
// Refresh task list
function refreshContent() {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/api/v1/tasks", true);
	
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Retrieve information
			tasks = JSON.parse(xhr.responseText).tasks;

			// Clear tasks & replace with new response
			uncompletedTasksContainer.innerHTML = "";
			completedTasksContainer.innerHTML = "";

			// Look through each task
			for (let i = 0; i < tasks.length; i++) {
				// Get JSON taskDATA
				var taskData = tasks[i].at(-1);

				// If task occurs today
				if (taskData[daysByIdx[currentDay]]) {

					// If task is completed, put in completed section
					if (taskData['completed'].includes(completionCode)) {
						completedTasksContainer.innerHTML += `<div class="task complete" id="${tasks[i][0]}" title="Mark as incomplete"><p>${tasks[i][1]}</p></div>`;
						continue;
					}

					// If the tasks aren't completed
					if (taskData['repeat']) {
						// If task is on repeat, add class
						uncompletedTasksContainer.innerHTML += `<div class="task incomplete" id="${tasks[i][0]}" title="Repeats every week"><p>${tasks[i][1]}</p></div>`;
					} else {
						// If task is not repeating
					uncompletedTasksContainer.innerHTML += `<div class="task incomplete no-repeat" id="${tasks[i][0]}"><p>${tasks[i][1]}</p></div>`;
					}
				}
			}

			// Mark task as done when clicked
			var uncompletedTaskElements = document.querySelectorAll(".incomplete");

			uncompletedTaskElements.forEach(task => {
			  task.addEventListener('click', e => {
					completeTask(e.target.id);
			  });
			});

			// Unmark task when clicked
			var completedTaskElements = document.querySelectorAll(".complete");
		
			completedTaskElements.forEach(task => {
				task.addEventListener('click', e => {
					restoreTask(e.target.id);
				});
			});
		}
	};

	xhr.send();
}

function completeTask(taskID) {
	var xhr = new XMLHttpRequest();

	for (let i = 0; i < tasks.length+1; i++) {
		// If task doesn't exist, return error.
		if (i == tasks.length) {
			displayError("That task doesn't exist.");
		}

		// If task exists, mark as complete
		if (tasks[i][0] == taskID) {
			var taskData = tasks[i].at(-1);
			xhr.open("GET", `/api/v1/complete-task?task_id=${taskID}&date=${completionCode}`, true);
			break;
		} else {
			continue;
		}
	}
	
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			refreshContent();
			var response = JSON.parse(xhr.responseText);
			if (response['status'] == "success") {
				displayMessage(response['message']);
			} else {
				displayError(response['message']);
			}
		}
	};
	
	xhr.send();
}

function restoreTask(taskID) {
	var xhr = new XMLHttpRequest();

	for (let i = 0; i < tasks.length+1; i++) {
		if (i == tasks.length) {
			displayError("That task doesn't exist.");
		}
		
		if (tasks[i][0] == taskID) {
			var taskData = tasks[i].at(-1);
			xhr.open("GET", `/api/v1/restore?task_id=${taskID}&date=${completionCode}`, true);
			break;
		} else {
			continue;
		}
	}
	
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			refreshContent();
			var response = JSON.parse(xhr.responseText);
			if (response['status'] == "success") {
				displayMessage(response['message']);
			} else {
				displayError(response['message']);
			}
		}
	};
	
	xhr.send();
}

function deleteTask(taskID) {
	var xhr = new XMLHttpRequest();

	for (let i = 0; i < tasks.length+1; i++) {
		if (i == tasks.length) {
			displayError("That task doesn't exist.");
		}
		
		if (tasks[i][0] == taskID) {
			var taskData = tasks[i].at(-1);
			xhr.open("GET", `/api/v1/delete-task?task_id=${taskID}`, true);
			break;
		} else {
			continue;
		}
	}
	
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			refreshContent();
			var response = JSON.parse(xhr.responseText);
			if (response['status'] == "success") {
				displayMessage(response['message']);
			} else {
				displayError(response['message']);
			}
		}
	};
	
	xhr.send();
}

// Load tasks first when page loads
refreshContent();