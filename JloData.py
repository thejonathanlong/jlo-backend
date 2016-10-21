import json
import sqlite3, os

TABLES_KEY = "tables"
PROPERTIES_KEY = "properties"
TABLE_NAME_KEY = "table_name"
FOREIGN_KEY_INFO_KEY = "keys"

DEBUG_MODE = False
def print_debug(s):
	if (DEBUG_MODE): print create_table_command

class JloData(object):
	tables = [] # array of tupes such that tuple[0] is table_name and tuple[1] is an array of properties
	def __init__(self, json_file=''):
		assert(json_file != '')
		data = None
		with open(os.path.expanduser(json_file)) as data_file:
			json_data = json.load(data_file)
		self.create_data_from_json(json_data)


	def create_data_from_json(self, json_data):
		tables = json_data[TABLES_KEY]

		#Connect to the DB and get the cursor
		db = sqlite3.connect(self.DB_NAME)
		cursor = db.cursor()

		for table in tables:
			property_names = table[PROPERTIES_KEY].keys()
			properties = zip(property_names, table[PROPERTIES_KEY].values())
			table_name = table[TABLE_NAME_KEY] 

			create_table_command = JloData.create_table_command(table_name, properties, table[FOREIGN_KEY_INFO_KEY])
			print_debug(str(create_table_command))
			cursor.execute(create_table_command)
			



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
		# 	insert = insert + '\'' + str(value) + '\''
			if property_index != len(values) - 1:
				insert = insert + ','
			property_index = property_index + 1
		insert = insert + ')'
		print "Insert - " + str(insert)
		return insert