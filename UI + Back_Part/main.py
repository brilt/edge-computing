from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import pandas_gbq

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "edge-computing-lecture.json"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/data', methods=['GET'])
def sensor_data():
    # Get the range parameter from the query string
    range_param = request.args.get('range', default=10, type=int)
    
    # Read data from BigQuery and sort by timestamp
    df = read_bigquery_table(range_param)
    
    # Convert the DataFrame to JSON format
    json_data = df.to_json(orient='records')
    
    # Use jsonify to send the JSON data
    return jsonify(json_data), 200

def read_bigquery_table(range_param):
    # Full table id in standard SQL form
    full_table_id = 'edge-computing-423409.dht11.fullData'
    query = f'''
        SELECT *
        FROM `{full_table_id}`
        ORDER BY timestamp DESC
        LIMIT {range_param}
    '''

    df = pandas_gbq.read_gbq(query, project_id='edge-computing-423409', dialect='standard')

    return df

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
