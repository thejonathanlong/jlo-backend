from JloData import JloData

'''
JLData is a database representation for a Blog. 
A Blog is defined as:
Zone
	id
	Posts
	Name

Post
	id
	name
	title
	images?
	comments?

Image
	imageDestination
	post

Comment
	user_name
	post_id
	body
'''

class JLData(JloData):
	# Table Names
	ZONE_TABLE = "Zone"
	COMMENT_TABLE = "Comment"
	IMAGE_TABLE = "Image"
	POST_TABLE = "Post"
	
	def DB_NAME(self):
		return "JLBLogData.db"

	def insert_zone_statement(self, values):
		return JLData.insert_statement(self.ZONE_TABLE, self.table_properties(self.ZONE_TABLE), values)

	def insert_post_statement(self, values):
		for value in values:
			print value
		return JLData.insert_statement(self.POST_TABLE, self.table_properties(self.POST_TABLE), values)

	def insert_comment_statement(self, values):
		return JLData.insert_statement(self.COMMENT_TABLE, self.table_properties(self.COMMENT_TABLE), values)

	def insert_image_statement(self, values):
		return JLData.insert_statement(self.IMAGE_TABLE, self.table_properties(self.IMAGE_TABLE), values)

	

		