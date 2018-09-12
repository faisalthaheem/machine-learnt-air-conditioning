from flask import Flask,jsonify,request
import shared
import subprocess
from classify_state import StateClassifier
from classify_temperature import TemperatureClassifier
import json
import numpy as np
from pprint import pprint
import os

app = Flask(__name__)
scripts_path = "./"

@app.route('/')
def index():
	return "Hello world"
	
@app.route('/learn-state')
def learn_state():
	
	s_path = scripts_path + "learn_state.py"
	p = subprocess.Popen(['python',s_path,'-d 90'])
	
	response = dict()
	response["response"] = "Started new learn-state.py with process id [%d]" % p.pid
	print(response["response"])
	
	return jsonify(response)
	
@app.route('/learn-thermostat')
def learn_thermostat():
	
	s_path = scripts_path + "learn_thermostat.py"
	p = subprocess.Popen(['python',s_path,'-d 90'])
	
	response = dict()
	response["response"] = "Started new learn-thermostat.py with process id [%d]" % p.pid
	print(response["response"])
	
	return jsonify(response)
	
@app.route('/classify-state', methods=['POST'])
def classify_state():
	
	state_classifier = StateClassifier()
	state_classifier.initialize()
	
	pprint(request.json)
	input = request.json['input']
	input = np.array(input).reshape((1,11))
	
	pprint(input)
    
	response = dict()
	response["predictions"] = state_classifier.loaded_model.predict(input).tolist()
	response["classes"] = state_classifier.loaded_model.predict_classes(input).tolist()
	pprint(response)
    
	return jsonify(response)
	
@app.route('/classify-thermostat', methods=['POST'])
def classify_thermostat():
	
	temperature_classifier = TemperatureClassifier()
	temperature_classifier.initialize()
	
	pprint(request.json)
	input = request.json['input']
	input = np.array(input).reshape((1,11))
	
	pprint(input)
    
	response = dict()
	response["predictions"] = temperature_classifier.loaded_model.predict(input).tolist()
	response["classes"] = temperature_classifier.loaded_model.predict_classes(input).tolist()
	response["labels"] = [temperature_classifier.labels_map[str(i)] for i in response["classes"]]
	pprint(response)
    
	return jsonify(response)
	
if __name__ == '__main__':
	if os.environ.get("APP_ENV") == 'Docker':
		print("Running inside docker, will search /scripts/ for files..")
		scripts_path = "/scripts/"
	else:
		print("Not running in a container")
	app.run(debug=True, host='0.0.0.0', use_reloader=False)