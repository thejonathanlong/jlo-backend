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
	
	def DB_NAME(self):
		return "JLBLogData.db"

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
	def get_all_zones(self):
		select = 'SELECT * from ' + str(self.ZONE_TABLE)
		zones = self.__execute(select).fetchall()
		zones_dict = self.albums_with_columns(zones)
		return zones_dict

	def get_id_for_zone(self, zone_name):
		select = 'SELECT * from ' + str(self.ZONE_TABLE) + ' where zone_name=\'' + str(zone_name) + '\''
		album = self.__execute(select)
		return album.fetchone()[0]

	def get_all_posts_in_zone(self, zone_name):
		condition = 'zone_id=\'' + str(zone_id) + '\''
		return self.get_rows(self.POST_TABLE, condition)

	def get_all_media(self):
		select = 'SELECT * from ' + str(self.media_TABLE)
		media = self.__execute(select).fetchall()
		media_dict = self.albums_with_columns(media)
		return media_dict

	def get_all_comments(self):
		select = 'SELECT * from ' + str(self.COMMENT_TABLE)
		comments = self.__execute(select).fetchall()
		comments_dict = self.albums_with_columns(comments)
		return comments_dict

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
	

		