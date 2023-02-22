const createButton = document.getElementById("create-btn");
var createTaskPanel = document.createElement("div");
createTaskPanel.classList.add("create-task-panel");
// createTaskPanel.tabIndex = 0;

createTaskPanel.innerHTML = 
`
<h2>Create Task</h2>
<br>

<form id="create-task-form">
	<input type="text" name="task-name" placeholder="Task Name" value="NEW TASK" required>
	
	<br>
	<br>

	<!-- Repeat function force enabled because of issues. All tasks will repeat every week automatically. Option to disable may be added in future versions. -->
	<!-- <input type="checkbox" name="repeat" checked> Repeat Every Week -->
	
	<br>
	<br>
	
	<table>
		<tr>
			<td>Monday</td>
			<td>Tuesday</td>
			<td>Wedesday</td>
			<td>Thursday</td>
			<td>Friday</td>
			<td>Saturday</td>
			<td>Sunday</td>
		</tr>
	
		<tr>
			<td><input type="checkbox" name="monday"></td>
			<td><input type="checkbox" name="tuesday"></td>
			<td><input type="checkbox" name="wednesday"></td>
			<td><input type="checkbox" name="thursday"></td>
			<td><input type="checkbox" name="friday"></td>
			<td><input type="checkbox" name="saturday"></td>
			<td><input type="checkbox" name="sunday"></td>
		</tr>
	</table>

	<br>
	
	<input type="submit" value="Save">
</form>
`;

document.body.appendChild(createTaskPanel);

// Show create task panel when activated
createButton.addEventListener('click', e => {
	e.preventDefault();
	createTaskPanel.classList.add("show");
});


// Send new task to server when save button is clicked
document.getElementById("create-task-form").addEventListener('submit', e => {
	e.preventDefault();
	
	var form = document.getElementById("create-task-form");
	var formData = new FormData(form);
	
	var xhr = new XMLHttpRequest();

	xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      displayMessage(JSON.parse(xhr.responseText).message);
    }
  };

	xhr.open('POST', '/api/v1/save', true);
	xhr.send(formData);

	createTaskPanel.classList.remove("show");
	form.reset();

	// Wait 1 second before requesting new data to give enough time to process the submitted task
	setTimeout(() => {
		refreshContent();
	}, 1000);
});