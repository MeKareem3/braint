# Script for managing the tasks
import sqlite3
from flask import jsonify
import ast


# Insert task_data into database & save to user
def store_task(task_id, task_name, user, data):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute("INSERT INTO tasks VALUES (?, ?, ?, ?)", (task_id, task_name, user, str(data)))

	# Assign task to user
	user_task_data = c.execute("SELECT tasks FROM users WHERE username = ?", (user,)).fetchall()[0][0].split(",")
	user_task_data.append(task_id)

	for task in user_task_data:
		if task == "":
			user_task_data.remove(task)

	user_task_data = ",".join(user_task_data)
	c.execute("UPDATE users SET tasks = ? WHERE username = ?", (user_task_data, user))
	
	conn.commit()
	conn.close()
	return jsonify({"task_id": task_id, "status": "success", "message": "Task Saved"})


# Get user tasks
def get_tasks(username):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	tasks = c.execute("SELECT tasks FROM users WHERE username = ?", (username,)).fetchall()[0][0].split(",")

	tasks_arr = []

	if len(tasks) > 0 and tasks[0] != '':
		for task in tasks:
			task_query = list(c.execute("SELECT * FROM tasks WHERE task_id = ?", (task,)).fetchall()[0])
			task_data = ast.literal_eval(task_query[3])
			task_query[3] = task_data
			tasks_arr.append(task_query)
	else:
		pass

	conn.commit()
	conn.close()

	return jsonify({"status": "success", "message": "Fetched Tasks", "tasks": tasks_arr})


# Mark task as complete
def complete_task(username, task_id, date):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()

	# Get owner of stored task
	task_owner = c.execute("SELECT username FROM tasks WHERE task_id = ?", (task_id,)).fetchall()[0][0]

	# If user does not own task, deny completion
	if username != task_owner:
		# Close db and return failed status
		conn.commit()
		conn.close()
		return jsonify({"status": "failed", "message": "Failed to mark task as complete."})

	# Convert the data column of table tasks
	task_data = ast.literal_eval(c.execute("SELECT data FROM tasks WHERE task_id = ?", (task_id,)).fetchall()[0][0])

	# Hand task over to delete task function if task is not going to repeat
	if not task_data['repeat']:
		delete_task(username, task_id)
		return jsonify({"status": "success", "message": "Task Completed"})

	# Convert completed to array
	completedDates = task_data['completed'].split(',')

	if date in completedDates:
		return jsonify({"status": "failed", "message": "Task already completed."})

	# Remove empty values, and append  new date
	if "" in completedDates:
		completedDates.remove("")
		
	completedDates.append(date)

	# Convert back to string & insert into dict
	task_data['completed'] = ','.join(completedDates)

	# Insert into table
	c.execute("UPDATE tasks SET data = ? WHERE task_id = ?", (str(task_data), task_id))

	# Save & Close db
	conn.commit()
	conn.close()

	# Return success!
	return jsonify({"status": "success", "message": "Task Completed"})


# Delete Task
def delete_task(username, task_id):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()

	# Get owner of stored task
	task_owner = c.execute("SELECT username FROM tasks WHERE task_id = ?", (task_id,)).fetchall()[0][0]

	# If user does not own task, deny deletion
	if username != task_owner:
		# Close db and return failed status
		conn.commit()
		conn.close()
		return jsonify({"status": "failed", "message": "Failed to delete task."})


	c.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
	user_task_data = c.execute("SELECT tasks FROM users WHERE username = ?", (username,)).fetchall()[0][0].split(',')

	user_task_data.remove(task_id)
	user_task_data = ','.join(user_task_data)
	c.execute("UPDATE users SET tasks = ? WHERE username = ?", (user_task_data, username))

	conn.commit()
	conn.close()

	return jsonify({"status": "success", "message": "Task Deleted"})

# Restore Task
def restore_task(username, task_id, date):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	task_owner = c.execute("SELECT username FROM tasks WHERE task_id = ?", (task_id,)).fetchall()[0][0]

	if username != task_owner:
		# Close db and return failed status
		conn.commit()
		conn.close()
		return jsonify({"status": "failed", "message": "Failed to restore task."})

	task_data = ast.literal_eval(c.execute("SELECT data FROM tasks WHERE task_id = ?", (task_id,)).fetchall()[0][0])

	completedDates = task_data['completed'].split(',')

	if date in completedDates:
		completedDates.remove(date)

	task_data['completed'] = ','.join(completedDates)

	c.execute("UPDATE tasks SET data = ? WHERE task_id = ?", (str(task_data), task_id))

	conn.commit()
	conn.close()

	# Return success!
	return jsonify({"status": "success", "message": "Task Restored"})