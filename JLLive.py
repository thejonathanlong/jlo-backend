#!flask/bin/python
from flask import Flask, request, jsonify, make_response
from JLLiveData import LiveData

app = Flask(__name__)
data = LiveData("TestData.json")

@app.route("/")
def index():
    return "Hello!"

#########
# Zones #
#########
@app.route("/posts", methods=["GET", "POST", "PUT"])
def posts():
	if "POST" == request.method:
		return handle_post_post(request)
	elif "GET" == request.method:
		return handle_post_get(request)
	elif "PUT" == request.method:
		return handle_post_put(request)

def handle_post_get(request):
	posts = []
	if "zone_name" in request.args:
		posts = data.get_all_posts_in_zone(request.args.get("zone_name"))
	elif "title" in request.args:
		posts = data.get_post(request.args.get("title"))
	else:
		posts = data.get_all_posts()

	return make_response(jsonify(posts), 200)

def handle_post_post(request):
	input_json = request.get_json()
	post = input_json["post"]
	post_values = []


def handle_post_put(request):
	return "Not done yet."

#########
# Zones #
#########
@app.route("/zones", methods=["GET", "POST", "PUT"])
def zones():
	if "POST" == request.method:
		return handle_zone_post(request)
	elif "GET" == request.method:
		return handle_zone_get(request)
	elif "PUT" == request.method:
		return handle_zone_put(request)

def handle_zone_get(request):
	zones = []
	if "zone_name" in request.args:
		zones = data.get_zone(request.args.get("zone_name"))
	else:
		zones = data.get_all_zones()

	return make_response(jsonify(zones), 200)

'''
	To Test:
			curl -H "Content-Type: application/json" -X POST -d '{"zone" : {"zone_name" : "Jonathan"}}' http://localhost:5000/zones
'''
def handle_zone_post(request):
	input_json = request.get_json()
	zone = input_json['zone']
	data.insert_zone(zone)
	return make_response(jsonify({}), 200)

def handle_zone_put(request):
	return "Not done yet."

if __name__ == '__main__':
    app.run(debug=True)
