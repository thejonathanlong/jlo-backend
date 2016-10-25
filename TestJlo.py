from JLData import JLData
from JloData import JloData

def main():
	# columns = ["column_1", "column_2", "column_3"]
	# results = [("a", "b", "c"), ("d", "e", "f"), ("g", "h", "i")]
	j = JLData("TestData.json")
	zone = {"zone_name" : "My Other Zone"}
	post = {"title": "Hello World", "body" : "World ", "zone_id" : 1}
	# j.insert_zone(zone)
	# j.insert_post(post)
	
	print j.get_post("Hello Worl")

if __name__ == '__main__':
	main()