from JLData import JLData
from JloData import JloData

def main():
	j = JLData("TestData.json")
	# v = {"title": "Hello World", "body" : "World ", "zone_id" : 1}
	# i = j.insert_post_statement()
	# j.commit(i, j.table_properties(j.POST_TABLE), v)
	x = j.get_all_posts()
	print x

if __name__ == '__main__':
	main()