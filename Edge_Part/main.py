from flask import Flask, request, jsonify
import Adafruit_DHT
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas_gbq
import time
import RPi.GPIO as GPIO



# Initialiser la bibliotheque GPIO
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 22
GPIO.setup(BUZZER_PIN, GPIO.OUT)


app = Flask(__name__)

@app.route('/sensor_data', methods=['POST'])
def sensor_data():
    measurements = request.json  # This is now a list of measurements
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(measurements)
    
    # Check each measurement for high temperature
    for index, row in df.iterrows():
        if row['temperature'] > 50 and row['humidity'] < 30:
            print(f"High temperature alert from Sensor {row['id']}!")
            
            # Trigger the sound alarm
            play_sound()

    
    # Load data to BigQuery
    destination_project_id = "edge-computing-423409"
    dataset_id = "dht11"
    table_id = "fullData"
    load_data_to_bigquery(df, dataset_id, table_id, destination_project_id)
    
    print("Received data from sensors. Processed successfully.")


    return jsonify({"status": "success", "message": "Data received and processed"}), 200

# Fonction pour jouer un son sur le buzzer
def play_sound():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Activer le buzzer
    time.sleep(2)  # Jouer le son pendant 1 seconde
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Desactiver le buzzer
    
    
def load_data_to_bigquery(dataframe, dataset_id, table_id, destination_project_id="datalake-380714"):
    credentials = service_account.Credentials.from_service_account_file("edge-computing-ecriture.json")
    client_bigquery = bigquery.Client(project=destination_project_id, credentials=credentials)
    table_ref = bigquery.dataset.DatasetReference.from_string(dataset_id, default_project=destination_project_id).table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = True
    job_config.max_bad_records = 100
   
    #Method in case of bugs :
    destination_table = f"{dataset_id}.{table_id}"
    pandas_gbq.to_gbq(
        dataframe,
        destination_table,
        project_id=destination_project_id,
        credentials=credentials,
        if_exists="append",  
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
