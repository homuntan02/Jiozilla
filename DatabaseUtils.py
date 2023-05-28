import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

def setup():
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	# Setup all the tables

	user_sql = "CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY);"

	org_sql = "CREATE TABLE IF NOT EXISTS organisation(id PRIMARY KEY, name);"

	org_rltn_sql = "CREATE TABLE IF NOT EXISTS orgToUser(user_id, org_id, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(org_id) REFERENCES organisation(id));"

	jio_sql = "CREATE TABLE IF NOT EXISTS jio(id PRIMARY KEY, date, start_t, end_t, location, org_id, FOREIGN KEY(org_id) REFERENCES organisation(id));"
	cur.execute(user_sql)
	cur.execute(org_sql)
	cur.execute(org_rltn_sql)
	cur.execute(jio_sql)


	# Creating the triggers

	# Adding placeholder user/organisation whenever
	# new user is added to orgToUser
	cur.execute("""
	
		CREATE TRIGGER IF NOT EXISTS update_tables_trigger
		AFTER INSERT ON orgToUser
		FOR EACH ROW

		BEGIN 
			INSERT OR IGNORE INTO organisation(id, name)
				VALUES (new.org_id, "Organisation Name TBA");

			INSERT OR IGNORE INTO users(id) VALUES (new.user_id);

		END;

	""")

	# Add placeholder organisation whenever a new organisation
	# That has not been added to organisation is added
	# as part of a jio
	# Of course, programmer should ensure that organisation is valid before a jio can be added, this is just in case the whole thing breaks

	cur.execute("""
	
	CREATE TRIGGER IF NOT EXISTS update_org_trigger
	AFTER INSERT ON jio
	FOR EACH ROW

	BEGIN
		INSERT OR IGNORE INTO organisation(id, name)
		VALUES (new.org_id, "Organisation Name TBA");
	END;
	""")

	con.commit()
	con.close()

### Boolean Checks ###

def user_in_users(user_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
	result = cur.fetchall()
	con.close()
	return len(result) != 0

def org_id_in_organisations(org_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT * FROM organisation WHERE id={org_id}")
	result = cur.fetchall()
	con.close()
	return len(result) != 0

def org_name_in_organisations(org_name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT * FROM organisation WHERE name='{org_name}'")
	result = cur.fetchall()
	con.close()
	return len(result) != 0

def jio_id_in_jios(jio_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT * FROM jio WHERE id={jio_id};")
	result = cur.fetchall()
	con.close()
	return len(result) != 0

### Adding Functions ###

def add_user(user_id, org_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	add_to_user_table = f"INSERT OR IGNORE INTO users(id) VALUES ('{user_id}');"
	check_org_table = f"""SELECT EXISTS(SELECT 1 FROM organisation WHERE id={org_id});""" 
	add_to_orgRltn_table = f"""INSERT OR IGNORE INTO orgToUser(user_id, org_id) VALUES ('{user_id}', {org_id});"""
	cur.execute(check_org_table)
	result = cur.fetchone()

	if result:
		cur.execute(add_to_user_table)
		cur.execute(add_to_orgRltn_table)
		con.commit()
	else:
		# do something if organisation does not exist
		print(f"{org_id} does not exist")

	con.close()

def all_users_from(org_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	all_user_sql = f"SELECT user_id FROM orgToUser where org_id={org_id};"		
	
	cur.execute(all_user_sql)
	result = cur.fetchall()

	if result:
		table = [res[0] for res in result]
		print(table)
	else:
		print(f"{org_id} does not exist")

	con.close()

def add_org(org_id, org_name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	org_sql = f"INSERT OR IGNORE INTO organisation(id, name) VALUES ({org_id}, {org_name});"
	cur.execute(org_sql)
	con.commit()
	con.close()

def update_org_name(org_id, org_name):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"""

	UPDATE organisation
	SET name = '{org_name}'

	WHERE id = {org_id};
	""")
	con.commit()
	con.close()

def add_jio(jio_id, date, start_t, end_t, location, org_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()

	cur.execute(f"""

	INSERT OR IGNORE INTO jio(id, date, start_t, end_t, location, org_id)

	VALUES ({jio_id}, '{date}', '{start_t}', '{end_t}', '{location}', {org_id});

	""")

	con.commit()
	con.close()
	

def get_jio_with_id(jio_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT * FROM jio WHERE id={jio_id};")
	result = cur.fetchall()
	if result:
		print(result)
	else:
		print("Provided Jio_id is not valid")
	con.close()

def get_jio_starting_at(jio_starting_t):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT id FROM jio WHERE start_t='{jio_starting_t}';")
	result = cur.fetchall()
	if result:
		print(result)
	else:
		print("Provided Jio starting time is not valid")
	con.close()

def get_jio_ending_at(jio_ending_t):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"select id from jio where end_t='{jio_ending_t}';")
	result = cur.fetchall()
	if result:
		print(result)
	else:
		print("provided jio ending time is not valid")
	con.close()

def get_all_jios_with_org(org_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT id FROM jio WHERE org_id={org_id}")
	result = cur.fetchall()
	if result:
		print(result)
	else:
		print("Provided org_id is not part of our database")
	con.close()

def complete_jio(jio_id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute(f"DELETE FROM jio WHERE id={jio_id};")
	con.commit()
	con.close()

# TODO: Remove all incomplete jios after a certain amount of time


##### DEBUGGING FUNCTIONS ####
def list_all_users():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM users;")
	for res in cur.fetchall():
		print(res)
	con.close()


def list_all_org():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM organisation;")
	for res in cur.fetchall():
		print(res)
	con.close()

def list_all_org_to_user():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM orgToUser;")
	for res in cur.fetchall():
		print(res)
	con.close()

def list_all_jio():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM jio;")
	for res in cur.fetchall():
		print(res)
	con.close()

