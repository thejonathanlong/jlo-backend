from JLLiveData import LiveData
from JLFoundationData import FoundationData

def main():
	# columns = ["column_1", "column_2", "column_3"]
	# results = [("a", "b", "c"), ("d", "e", "f"), ("g", "h", "i")]
	j = LiveData("TestData.json")
	zone = {"zone_name" : "Zone2"}
	post = {"title": "DoReyMe", "body" : "World ", "zone_id" : 2}
	# j.insert_zone(zone)
	j.insert_post(post)
	# print j.get_column_names("Zone")
	# print j.table_properties("Zone")

	# print j.get_column_names("Post")
	# print j.table_properties("Post")
	
	# print j.get_post("Hello Worl")
	# j.update_post_title("New Title", "Hello World")

if __name__ == '__main__':
	main()