from flask import Flask, jsonify
import requests

app = Flask('__name__')

URL = "https://b7jdbsdx6c.execute-api.eu-central-1.amazonaws.com/dev/passengers"
headers = {"Content-Type": "application/json"}
params = {"qs": "somevalue"}
data_payload = {"payload": "payload"}


@app.route("/passengers", methods=['GET'])
def passengers_read():
    r = requests.request("GET", URL)
    return jsonify(r.text)


@app.route("/passengers", methods=['PUT'])
def passengers_create():
    r = requests.request("PUT", URL)
    return jsonify(r.text)


@app.route("/passengers", methods=['DELETE'])
def passengers_delete():
    r = requests.request("DELETE", URL)
    return jsonify(r.text)


@app.route("/")
def home():
    r = requests.request("DELETE", URL)
    return "Welcome to the local Flask-API /n Operate from here with the serverless RDS - API-Gateway on the \'\/passengers"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
