import json
import web3

from web3 import Web3
from flask import Flask, Response, request, jsonify, redirect
from flask_cors import CORS

from math import radians, sin, cos, acos

import requests

from eth_account.messages import defunct_hash_message

#------------------------------------------------------------------------------

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]
print(w3.eth.accounts[0])

# Get stored abi and contract_address
with open("build\contracts\PathFinder.json", 'r') as f:
    datastore = json.load(f)

# Create the contract instance with the newly-deployed address
pathFinder = w3.eth.contract(
    address=datastore['networks']['5777']['address'],
    abi=datastore['abi'],
)

#------------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)


@app.route("/markers", methods=['GET'])
def show_markers():
    markerCount = pathFinder.functions.getMarkerCount().call()
    list = []
    for i in range(1, markerCount + 1):
        list.append(pathFinder.functions.getMarker(i).call())
    return jsonify({"data": list}), 200



@app.route("/user_markers/<address>", methods=['GET'])
def show_markers_by_address(address):
    markerCount = pathFinder.functions.getMarkerCount().call()
    list = []
    for i in range(1, markerCount + 1):
        marker = pathFinder.functions.getMarker(i).call()
        if marker[6] == address:
            list.append(marker)
    return jsonify({"data": list}), 200



@app.route("/users", methods=['GET'])
def show_users():
    userCount = len(w3.eth.accounts)
    list = []
    for i in range(1, userCount):
        list.append(w3.eth.accounts[i])
    return jsonify({"data": list}), 200



@app.route("/targets", methods=['GET'])
def show_targets():
    targetCount = pathFinder.functions.getTargetCount().call()
    list = []
    for i in range(1, targetCount + 1):
        list.append(pathFinder.functions.getTarget(i).call())
    return jsonify({"data": list}), 200



@app.route("/new_marker", methods=['POST'])
def add_marker():
    data = request.json
    msg_hash = defunct_hash_message(text = data['description'])
    signed_message = w3.eth.account.signHash(msg_hash, private_key = data['private_key'])
    #print("\nSIGNED MESSAGE: ", signed_message, "\n")
    tx_hash = pathFinder.functions.submitMarker(data['description'], str(data['latitude']), str(data['longitude']), str(data['progress']), str(data['status']), signed_message.messageHash, signed_message.signature).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    return redirect("http://localhost:5000/markers", code=200)



@app.route("/check_arrived", methods=['POST'])
def check():
    status = "FALSE"
    targetCount = pathFinder.functions.getTargetCount().call()
    data = request.json
    for i in range(1, targetCount + 1):
        target = pathFinder.functions.getTarget(i).call()
        dist = distance(data['latitude'], data['longitude'], target[2], target[3])
        if  dist < 250:
            status = "TRUE"
    return jsonify({"status": status}), 200



def distance(longitude_A, latitude_A, longitude_B, latitude_B):
    slat = radians(float(latitude_A))
    slon = radians(float(longitude_A))
    elat = radians(float(latitude_B))
    elon = radians(float(longitude_B))
    #Distanza in metri
    dist = 6371.01 * 1000 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist

if __name__=='__main__':
    app.run()
