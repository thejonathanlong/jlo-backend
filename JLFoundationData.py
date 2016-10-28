import json
import sqlite3, os
from JELPrettyPrint import JELPrettyPrint as printer

TABLES_KEY = "tables"
PROPERTIES_KEY = "properties"
TABLE_NAME_KEY = "table_name"
FOREIGN_KEY_INFO_KEY = "keys"

DEBUG_MODE = True
def print_debug(s):
	if (DEBUG_MODE): print s

class FoundationData(object):
	#############
	# Properties #
	#############

	def DB_NAME():
		''' 
			@returns (str): The name of the database.
		'''
		return "DEFAULT_NAME"

	##############
	# Constructor #
	##############
	def __init__(self, json_file=''):
		'''
			Creates a new instance of FoundationData from a json file. 
			@param json_file (str) : path to the JSON file
		'''
		assert(json_file != '')
		data = None
		with open(os.path.expanduser(json_file)) as data_file:
			json_data = json.load(data_file)
		self.create_data_from_json(json_data)


	##############
	# JSON Parsing #
	##############
	def create_data_from_json(self, json_data):
		'''
			Parses the JSON data and creates the database with the schema described in the JSON 
			@param json_data : The result of json.loads(path_to_json_file)
		'''
		tables = json_data[TABLES_KEY]

		#Connect to the DB and get the cursor
		db = sqlite3.connect(self.DB_NAME())
		cursor = db.cursor()

		for table in tables:
			property_names = table[PROPERTIES_KEY].keys()
			properties = zip(property_names, table[PROPERTIES_KEY].values())
			table_name = table[TABLE_NAME_KEY] 

			create_table_command = FoundationData.create_table_command(table_name, properties, table[FOREIGN_KEY_INFO_KEY])
			print_debug(str(create_table_command))
			cursor.execute(create_table_command)
		db.commit()

	#################
	# SQL Statements #
	#################
	@staticmethod
	def create_table_command(table_name, property_qualifier_pairs, foreign_key_info, should_have_primary_key_id=True):
		'''
			Static method that retuns a statement to create a new table in the database
			@param table_name (str) : The name of the new table
			@param property_qualifier_pairs ([Tuples]) : A list of the properties and database qualifiers (i.e. title TEXT NOT NULL)
			@param foreign_key_info ([str]) : A list of strings that identify the foreign key information for this table (i.e. ["FOREIGN KEY(post_id) REFERENCES Post(ID)"])
			@param should_have_primary_key_id (bool) : If the table should have an autoincrement primary ID named ID. Defaulst to true
			@returns (str): The SQL command to create the table specified.
		'''
		command = 'CREATE TABLE IF NOT EXISTS ' + table_name + '('
		if should_have_primary_key_id:
			command = command + 'ID INTEGER PRIMARY KEY ASC'
		PROPERTY_NAME_INDEX = 0
		QUALIFIER_INDEX = 1

		for pair in property_qualifier_pairs:
			command = command + ', ' + pair[PROPERTY_NAME_INDEX] + ' ' + pair[QUALIFIER_INDEX]
		
		for fk in foreign_key_info:
			command = command + ', ' + fk

		return command + ')'
	
	##########
	# Insert #
	##########
	def insert_statement(self, table_name):
		'''
			Static method that returns a statement to insert values into a table.
			@param table_name (str): the name of the table in which to INSERT
			@returns (str): The SQL command to insert into the specified table.
		'''
		properties = self.get_table_properties_excluding_ID(table_name)
		insert = 'INSERT into ' + table_name + '('
		property_index = 0
		values_string = 'values('
		for the_property in properties:
			insert = insert + the_property
			values_string = values_string + '?'
			if property_index != len(properties) - 1:
				insert = insert + ','
				values_string = values_string + ','
			else:
				insert = insert + ')'
				values_string = values_string + ')'
			property_index = property_index + 1
		
		insert = insert + ' ' + values_string
		print "Insert - " + str(insert)
		return insert


	##########
	# Select #
	##########
	def get_table_properties(self, table_name):
		'''
			@param table_name (str): the name of the table
			@Returns ([str]): A list containing the property names for the specified table excluding the ID.
		'''
		select = 'SELECT * from ' + str(table_name)
		cursor = self.__execute(select)
		return [description[0] for description in cursor.description][0:]

	def get_table_properties_excluding_ID(self, table_name):
		return self.get_table_properties(table_name)[1:]

	def get_rows(self, table_name, condition=None):
		'''
			@param table_name (str): the name of the table
			@param condition (str): the condition to be met for the select statement (i.e. where id=1)
			@returns ([str]): A list containing all of the results that met the condition
		'''
		if condition != None and condition != "" and condition != " ":
			select = 'SELECT * from ' + table_name +' where ' + condition
		else:
			select = 'SELECT * from ' + table_name
		results = self.__execute(select).fetchall()
		return results

	def select_all(self, table_name, condition=None):
		'''
			A convenience for returning the results of a SELECT as a dictionary.
			@param table_name (str): the name of the table
			@param condition (str): the condition to be met for the select statement (i.e. where id=1)
			@returns ([{str : Object}]): A dictionary containing the result that matched the condition with property values as the keys and what is stored as the value
		'''
		rows = self.get_rows(table_name, condition)
		columns = self.get_table_properties(table_name)
		print_debug(str(columns))
		return map(lambda row : dict(zip(columns, row)), rows)

	##########
	# Update #
	##########
	def update_table(self, table_name, property_set_statment, condition):
		'''
			Updates the specified table property.
			@param table_name (str): the name of the table
			@param property_set_statement (str): the property value to set (i.e. times_answered = 1, av_answeringTimes = 10)
			@param condition (str): the condition to be met for the select statement (i.e. where id=1)
		'''
		update = 'UPDATE ' + table_name + ' set ' + property_set_statment + ' where ' + condition
		self.__update(update)
		printer.pretty_print_positive(update)

	#################
	# DB Operations #
	#################
	def commit(self, statement, properties, values):
		'''
			Actually persists the data to the database TODO#1
			@param table_name (str): the name of the table
			@param properties ([str]): the list of properties in the table
			@param values ({str:any}): a dictonary with properties as the keys and the new value of that property as values
		'''
		new_vales = None
		if values != None and properties != None:
			new_values = order_values_for_properties(values, properties)
		db = sqlite3.connect(self.DB_NAME())
		cursor = db.cursor()
		if new_values != None:
			committed = cursor.execute(statement, new_values)
		else:
			committed = cursor.execute(statement)	
		printer.pretty_print("Prepared for Commit: " + str(statement))
		db.commit()
		printer.pretty_print("Saving to the database.")
		db.close()

	def __execute(self, statement):
		'''
			Execute the SQL statement
			@param statement (str): SQL statement
		'''
		db = sqlite3.connect(self.DB_NAME())
		cursor = db.cursor()
		executed = cursor.execute(statement)
		printer.pretty_print("Executed: " + str(statement))
		return executed

	def __update(self, statement):
		self.commit(statement, None, None)

'''END FoundationData '''

def order_values_for_properties(values, properties):
		''' 
			@param values - {string:id} - A dictionary of string id pairs where the string corresponds to a property
			@param properties - [string] - An array of strings. One for each column in the table
		'''
		new_values = []
		for the_property in properties:
			new_values.append(values[the_property])
		return new_values