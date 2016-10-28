#!flask/bin/python
from flask import Flask, request, jsonify
from LiveData import LiveData

app = Flask(__name__)
data = LiveData("TestData.json")

@app.route("/")
def index():
    return "Hello!"

@app.route("/posts", methods=["GET", "POST", "PUT"])
def posts():
    return "POSTS!"

@app.route("/zones", methods=["GET", "POST", "PUT"])
def zones():
	if "POST" == request.method:
		return "POST"
	elif "GET" == request.method:
		return handle_zone_get(request)
	elif "PUT" == request.method:
		return "POST"

def handle_zone_get(request):
	zones = []
	if "zone_name" in request.args:
		zones = data.get_zone(request.args.get("zone_name"))
	else:
		zones = data.get_all_zones()

	return jsonify(zones)

# def handle_zone_post(request):

# def handle_zone_put(request):

if __name__ == '__main__':
    app.run(debug=True)
