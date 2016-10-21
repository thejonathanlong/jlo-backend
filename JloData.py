import json
import os

TABLES_KEY = "tables"
PROPERTIES_KEY = "properties"
TABLE_NAME_KEY = "table_name"
FOREIGN_KEY_INFO_KEY = "keys"

class JloData(object):
	def __init__(self, json_file=''):
		assert(json_file != '')
		data = None
		# try:
		with open(os.path.expanduser(json_file)) as data_file:
			json_data = json.load(data_file)
		# except IOError:
		# 	print "Can not open file named: - " + str(json_file)
		# 	exit(1)
		# except:
		# 	print "There was an unexpected error creating the DB"
		# 	exit(1)
		self.create_data_from_json(json_data)


	def create_data_from_json(self, json_data):
		tables = json_data[TABLES_KEY]
		table_names = []
		properties = [] # An array of tuples such that tuple[0] = property_name and tuple[1] = qualifier
		# ex [('photoDestination' , 'TEXT NOT NULL'), ('photoID' , 'INTEGER NOT NULL')
		foreign_key_info = [] # An array of arrays describing the foreign key values for each table

		for table in tables:
			# table_names.append(tables[TABLE_NAME_KEY])
			properties = zip(table[PROPERTIES_KEY].keys(), table[PROPERTIES_KEY].values())
			# foreign_key_info = tables[FOREIGN_KEY_INFO_KEY]
			create_table_command = JloData.create_table_command(table[TABLE_NAME_KEY], properties, table[FOREIGN_KEY_INFO_KEY])
			print create_table_command


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