from JLData import JLData

def main():
	j = JLData("TestData.json")
	v = ["Hello World", "Hello World", 1]
	i = j.insert_post_statement(v)
	j.commit(i, v)

if __name__ == '__main__':
	main()