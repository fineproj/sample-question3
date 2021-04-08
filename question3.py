import flask
from flask import request,jsonify
import requests
import json
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True
time_format = "%Y-%m-%dT%H:%M:%SZ"

url = 'https://gitlab.com/-/snippets/2094509/raw/master/sample_json_3.json'
r = requests.get(url)
data = r.content
system_data = json.loads(data)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Home</h1>"

@app.route('/api/produnit/all', methods=['GET'])
def api_all():
    return jsonify(system_data)

@app.route('/api/produnit', methods=['GET'])
def api_time():
    if 'start_time'in request.args:
        start_time = datetime.strptime(str(request.args['start_time']),time_format)
    
    if 'end_time'in request.args:
        end_time = datetime.strptime(str(request.args['end_time']),time_format)

    result = []
    list_of_ids = []
    for data in system_data:
        current_time = datetime.strptime(str(data['time']),"%Y-%m-%d %H:%M:%S")
        ID = int(str(data['id']).replace("ch00",''))        
        if(start_time <= current_time <= end_time):
            if ID not in list_of_ids:
                list_of_ids.append(ID)
                temp = {}
                temp['id'] = ID

                if data['state'] == True:
                    temp['belt1'] = 0
                    temp['belt2'] = data['belt2']

                elif data['state'] == False:
                    temp['belt1'] = data['belt1']
                    temp['belt2'] = 0                    

                result.append(temp)
                
            else:
                count = 0
                for row in result:
                    if row["id"] == ID:
                        if data['state'] == True:
                            result[count]['belt2'] = int((result[count]['belt2'] + data['belt2'])/2)
                        
                        elif data['state'] == False:
                            result[count]['belt1'] = int((result[count]['belt1'] + data['belt1'])/2)

                    count = count + 1

            
    result = sorted(result, key = lambda i: i['id'])
    return jsonify(result)
app.run()

