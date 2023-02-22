import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_settings(username):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	settings = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()[0]
	conn.commit()
	conn.close()
	return settings

# Delete account
def delete_account(username):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	user_task_ids = list(c.execute("SELECT tasks FROM users WHERE username = ?", (username,)).fetchall()[0])

	for task_id in user_task_ids:
		c.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))

	c.execute("DELETE FROM users WHERE username = ?", (username,))

	conn.commit()
	conn.close()

# Reset account
def reset_account(username):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	user_task_ids = list(c.execute("SELECT tasks FROM users WHERE username = ?", (username,)).fetchall()[0])

	for task_id in user_task_ids:
		c.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))

	c.execute("UPDATE users SET tasks = '' WHERE username = ?", (username,))

	conn.commit()
	conn.close()

# Change Password
def change_password(username, current_password, new_password, new_password2):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()

	if not check_password_hash(c.execute("SELECT pwhash FROM users WHERE username = ?", (username,)).fetchall()[0][0], current_password):
		conn.commit()
		conn.close()
		return False

	if new_password != new_password2:
		conn.commit()
		conn.close()
		return False

	c.execute("UPDATE users SET pwhash = ? WHERE username = ?", (generate_password_hash(new_password), username))
	conn.commit()
	conn.close()

	return True