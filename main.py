import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
# Import helper scripts
from braint import tasks, settings

# Create the application instance
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


### Functions ###

# Generate random ID for the tasks
def braint_task_id():
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()

	task_id = ""
	for i in range(20):
		task_id += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890")

	if len(c.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchall()) == 0:
		conn.close()
		return task_id
	else:
		conn.close()
		return braint_task_id()

def bool_to_int(bool):
	if bool:
		return 1
	else:
		return 0

### Main Pages ###

# Index Page
@app.route('/')
def index():
	if 'logged_in' not in session:
		return redirect('/login')

	return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	# If the user is already logged in, redirect to the main page
	if 'logged_in' in session:
		return redirect('/')
	
	# If the user is submitting the login form
	if request.method == 'POST':
		# Get the username and password from the form
		username = request.form['username']
		password = request.form['password']
		# Check if the username and password are correct
		conn = sqlite3.connect('db.sqlite3')
		c = conn.cursor()
	
		# Refresh if account doesn't exist
		if len(c.execute("SELECT username FROM users WHERE lower(username) = ?", (username.lower(),)).fetchall()) == 0:
			return redirect('/login')
		else:
			pass
			
		pwhash = c.execute("SELECT pwhash FROM users WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
		saved_username = c.execute("SELECT username FROM users WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
		if check_password_hash(pwhash, password):
			# Close database connection
			conn.close()
			# If the username and password are correct, set the session
			session['logged_in'] = True
			session['username'] = saved_username
			# Redirect to the main page
			return redirect('/')
		else:
			# Close database connection
			conn.close()
			# If the username and password are incorrect, redirect to the login page
			return redirect('/login')
	
	# If the user is not logged in, render the login page
	return render_template('login.html')
	
	
# Register Page
@app.route('/register', methods=['POST', 'GET'])
def register():
	# If the user is already logged in, redirect to the main page
	if 'logged_in' in session:
		return redirect('/')
	
	# If the user is submitting the register form
	if request.method == 'POST':
		# Get the username and password from the form
		username = request.form['username']
		password = request.form['password']
		# Check if the username is already taken
		conn = sqlite3.connect('db.sqlite3')
		c = conn.cursor()
	
		if c.execute("SELECT * FROM users WHERE lower(username) = ?", (username.lower(),)).fetchall():
			# Close database connection
			conn.close()
			# If the username is already taken, redirect to the register page
			return redirect('/register')
		else:
			# Close database connection
			conn.close()
			# If the username is not taken, create a new account
			conn = sqlite3.connect('db.sqlite3')
			c = conn.cursor()
			pwhash = generate_password_hash(password)
			c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, pwhash, ""))
			conn.commit()
			conn.close()
			# If the username and password are correct, set the session
			session['logged_in'] = True
			session['username'] = username
			# Redirect to the main page
			return redirect('/')
	
	# If the user is not logged in, render the register page
	return render_template('register.html')
	
# Logout Page
@app.route('/logout')
def logout():
	# If the user is logged in, log them out
	if 'logged_in' in session:
		session.pop('logged_in', None)
		session.pop('username', None)
	# Redirect to the main page
	return redirect('/')


### Other Pages ###

# All tasks page
@app.route('/calendar')
def show_calendar():
	if 'logged_in' not in session:
		return redirect('/login')

	return render_template('calendar.html', tasks=tasks.get_tasks(session['username']))

# Settings Page
@app.route('/settings')
def get_settings():
	if 'logged_in' not in session:
		return redirect('/login')

	return render_template('settings.html', settings=settings.get_settings(session['username']))

# Change Password
@app.route('/change-password', methods=['POST', 'GET'])
def change_password():
	if 'logged_in' not in session:
		return redirect('/login')

	if request.method == "POST":
		current_password = request.form.get("current-password")
		new_password = request.form.get("new-password")
		new_password2 = request.form.get("new-password2")
		if not settings.change_password(session['username'], current_password, new_password, new_password2):
			return redirect('/change-password')

		return redirect('/settings')

	return render_template('change-password.html')


### API ###

# Create task
@app.route('/api/v1/save', methods=["POST"])
def save_task():
	if 'logged_in' not in session:
		return redirect('/login')

	task_id = braint_task_id()
	task_name = request.form.get('task-name')
	# Repeat function disabled. May be added in future versions.
	# repeat = request.form.get('repeat')
	repeat = "on"
	task_data = {"repeat": repeat, "monday": request.form.get('monday'), "tuesday": request.form.get('tuesday'), "wednesday": request.form.get('wednesday'), "thursday": request.form.get('thursday'), "friday": request.form.get('friday'), "saturday": request.form.get('saturday'), "sunday": request.form.get('sunday')}

	# Replace form values with 1 or 0
	for idx, key in enumerate(task_data):
		if task_data[key] == None:
			task_data[key] = 0
		else:
			task_data[key] = 1

	task_data['completed'] = ""

	return tasks.store_task(task_id, task_name, session['username'], task_data)

# Get Tasks
@app.route('/api/v1/tasks')
def get_tasks():
	if 'logged_in' not in session:
		return redirect('/login')

	return tasks.get_tasks(session['username'])

# Complete Task
@app.route('/api/v1/complete-task', methods=['GET'])
def complete_task():
	if 'logged_in' not in session:
		return redirect('/login')

	task_id = request.args.get('task_id')
	date = request.args.get('date')
		
	return tasks.complete_task(session['username'], task_id, date)

# Restore Task from completion
@app.route('/api/v1/restore')
def restore_task():
	if 'logged_in' not in session:
		return redirect('/login')

	task_id = request.args.get("task_id")
	date = request.args.get("date")

	return tasks.restore_task(session['username'], task_id, date)

# Delete Task
@app.route('/api/v1/delete-task')
def delete_task():
	if 'logged_in' not in session:
		return redirect('/login')

	task_id = request.args.get('task_id')

	return tasks.delete_task(session['username'], task_id)

# Reset account
@app.route('/reset-account')
def reset_account():
	if 'logged_in' not in session:
		return redirect('/login')
		
	settings.reset_account(session['username'])
	return redirect("/")

@app.route('/delete-account')
def delete_account():
	if 'logged_in' not in session:
		return redirect('/login')
		
	settings.delete_account(session['username'])
	session.clear()
	return redirect("/register")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)