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
	medias?
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
	MEDIA_TABLE = "Media"
	POST_TABLE = "Post"
	UNIQUE_ID_PROPERTY = "ID"
	
	def DB_NAME(self):
		return "JLBLogData.db"

	#####################
	# Insert Operations #
	#####################
	def insert_zone(self, values):
		self.commit(self.insert_zone_statement(), self.table_properties(self.ZONE_TABLE), values)

	def insert_post(self, values):
		self.commit(self.insert_post_statement(), self.table_properties(self.POST_TABLE), values)

	def insert_comment(self, values):
		self.commit(self.insert_comment_statement(), self.table_properties(self.COMMENT_TABLE), values)

	def insert_image(self, values):
		self.commit(self.insert_image_statement(), self.table_properties(self.MEDIA_TABLE), values)

	#####################
	# Insert Statements #
	#####################
	def insert_zone_statement(self):
		return JLData.insert_statement(self.ZONE_TABLE, self.table_properties(self.ZONE_TABLE))

	def insert_post_statement(self):
		return JLData.insert_statement(self.POST_TABLE, self.table_properties(self.POST_TABLE))

	def insert_comment_statement(self):
		return JLData.insert_statement(self.COMMENT_TABLE, self.table_properties(self.COMMENT_TABLE))

	def insert_media_statement(self):
		return JLData.insert_statement(self.media_TABLE, self.table_properties(self.media_TABLE))

	############
	# Get Data #
	############
	#Zones
	def get_all_zones(self):
		return self.select_all(self.ZONE_TABLE)

	def get_id_for_zone(self, zone_name):
		condition = 'zone_name=\'' + str(zone_name) + '\''
		return self.select_all(self.ZONE_TABLE, condition)

	#Posts
	def get_all_posts(self):
		return self.select_all(self.POST_TABLE)

	def get_all_posts_in_zone(self, zone_name):
		zone_id = self.get_id_for_zone(zone_name)[0][self.UNIQUE_ID_PROPERTY]
		condition = 'zone_id=\'' + str(zone_id) + '\''
		return self.select_all(self.POST_TABLE, condition)

	def get_id_for_post(self, title):
		return self.get_post(title)[0][self.UNIQUE_ID_PROPERTY]

	def get_post(self, title=None, post_id=0):
		if post_id <= 0:
			assert(title != None)
			condition = 'title=\'' + str(title) + '\''
			return self.select_all(self.POST_TABLE, condition)
		condition = self.UNIQUE_ID_PROPERTY + '=\'' + str(post_id) + '\''
		return self.select_all(self.POST_TABLE)

	#Media
	def get_all_media(self):
		return self.select_all(self.MEDIA_TABLE)

	def get_media_for_post(self, title=None, post_id=0):
		if post_id <= 0:
			assert(title != None)
			post_id = self.get_id_for_post(title)
		condition = 'post_id=\'' + str(post_id) + '\''
		return self.select_all(self.MEDIA_TABLE, condition)

	#Comments
	def get_all_comments(self):
		return self.select_all(self.COMMENT_TABLE)

	def get_comments_for_post(self, title=None, post_id=0):
		if post_id <= 0:
			assert(title != None)
			post_id = self.get_id_for_post(title)
		condition = 'post_id=\'' + str(post_id) + '\''
		return self.select_all(self.COMMENT_TABLE, condition)


	##################
	# Column Helpers #
	##################
	def zone_columns(self):
		return self.get_column_names(self.ZONE_TABLE)

	def post_columns(self):
		return self.get_column_names(self.POST_TABLE)

	def media_columns(self):
		return self.get_column_names(self.media_TABLE)

	def comment_columns(self):
		return self.get_column_names(self.COMMENT_TABLE)

	##################
	# Dictionary Helpers #
	##################
	def comments_with_columns(self, comments):
		resulting_comments = []
		columns = self.comment_columns()
		for comment in comments:
			resulting_comments.append(dict(zip(columns, comment)))
		return resulting_comments

	def medias_with_columns(self, medias):
		resulting_medias = []
		columns = self.comment_columns()
		for media in medias:
			resulting_medias.append(dict(zip(columns, media)))
		return resulting_medias

	def posts_with_columns(self, posts):
		resulting_posts = []
		columns = self.comment_columns()
		for post in posts:
			resulting_posts.append(dict(zip(columns, post)))
		return resulting_posts

	def zones_with_columns(self, zones):
		resulting_zones = []
		columns = self.comment_columns()
		for zone in zones:
			resulting_zones.append(dict(zip(columns, zone)))
		return resulting_zones
	

		