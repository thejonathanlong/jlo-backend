import json
import sqlite3, os
from JELPrettyPrint import JELPrettyPrint as printer

TABLES_KEY = "tables"
PROPERTIES_KEY = "properties"
TABLE_NAME_KEY = "table_name"
FOREIGN_KEY_INFO_KEY = "keys"

DEBUG_MODE = False
def print_debug(s):
	if (DEBUG_MODE): print create_table_command

class JloData(object):
	#############
	# Properties #
	#############
	schema = [] # array of tupes such that tuple[0] is table_name and tuple[1] is an array of properties

	def DB_NAME():
		return "DEFAULT_NAME"

	##############
	# Constructor #
	##############
	def __init__(self, json_file=''):
		assert(json_file != '')
		data = None
		with open(os.path.expanduser(json_file)) as data_file:
			json_data = json.load(data_file)
		self.create_data_from_json(json_data)


	##############
	# JSON Parsing #
	##############
	def create_data_from_json(self, json_data):
		tables = json_data[TABLES_KEY]

		#Connect to the DB and get the cursor
		db = sqlite3.connect(self.DB_NAME())
		cursor = db.cursor()

		for table in tables:
			property_names = table[PROPERTIES_KEY].keys()
			properties = zip(property_names, table[PROPERTIES_KEY].values())
			table_name = table[TABLE_NAME_KEY] 

			create_table_command = JloData.create_table_command(table_name, properties, table[FOREIGN_KEY_INFO_KEY])
			print_debug(str(create_table_command))
			cursor.execute(create_table_command)
			self.schema.append((table_name, property_names))
		db.commit()

	#################
	# SQL Statements #
	#################
	@staticmethod
	def create_table_command(table_name, property_qualifier_pairs, foreign_key_info, shouldHavePrimaryKeyID=True):
		command = 'CREATE TABLE IF NOT EXISTS ' + table_name + '('
		if shouldHavePrimaryKeyID:
			command = command + 'ID INTEGER PRIMARY KEY ASC'
		PROPERTY_NAME_INDEX = 0
		QUALIFIER_INDEX = 1

		for pair in property_qualifier_pairs:
			command = command + ', ' + pair[PROPERTY_NAME_INDEX] + ' ' + pair[QUALIFIER_INDEX]
		
		for fk in foreign_key_info:
			command = command + ', ' + fk

		return command + ')'
	
	@staticmethod
	def insert_statement(table_name, properties, values):
		insert = 'INSERT into ' + table_name + '('
		property_index = 0
		for the_property in properties:
			insert = insert + the_property
			if property_index != len(properties) - 1:
				insert = insert + ','
			property_index = property_index + 1
		
		property_index = 0
		insert = insert + ') values('
		for value in values:
			insert = insert + '?'
			if property_index != len(values) - 1:
				insert = insert + ','
			property_index = property_index + 1
		insert = insert + ')'
		print "Insert - " + str(insert)
		return insert


	def table_properties(self, table_name):
		for table in self.schema:
			if table[0] == table_name:
				return table[1]
		return []

	def commit(self, statement, values):
		db = sqlite3.connect(self.DB_NAME())
		cursor = db.cursor()
		committed = cursor.execute(statement, values)
		printer.pretty_print("Prepared for Commit: " + str(statement))
		db.commit()
		printer.pretty_print("Saving to the database.")
		db.close()