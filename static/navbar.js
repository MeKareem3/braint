const navbar = document.getElementById("navbar");
const navContent = 
`<img src="/static/images/logo.png" alt="logo" class="logo" title="Braint">
<ul>
	<li>
		<a href="/">Today</a>
	</li>

	<li>
		<a href="/logout">Logout</a>
	</li>
</ul>

<ul id="pages-bar">
	<a href="/create" id="create-btn">
		<li>Create Task</li>
	</a>

	<a href="/#completed">
		<li>Completed Tasks</li>
	</a>

	<a href="/calendar">
		<li>Calendar</li>
	</a>

	<hr>

	<a href="/settings">
		<li>Settings</li>
	</a>
</ul>`;

navbar.innerHTML = navContent;

// Change properties of selected nav button
var page = window.location.toString().split('/');

var pageNavButton = document.querySelectorAll(`#pages-bar a[href="/${page[page.length-1]}"]`)[0];

// Add class of selected to change properties in CSS
pageNavButton.classList.add("selected");