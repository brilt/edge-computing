import time
import board
import adafruit_dht
import json
import requests

# Initialiser le capteur de température et d'humidité
sensor = adafruit_dht.DHT11(board.D17)

# Route API à laquelle envoyer les données
api_url = 'http://192.168.213.35:5000/sensor_data'

# Liste pour stocker les mesures
measurements = []

# Fonction pour envoyer les données au serveur via une requête POST
def send_data(measurements):
    data = json.dumps(measurements)  # Convertir la liste des mesures en JSON
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=data, headers=headers)
    print("Status Code:", response.status_code)
    print(response.text)  # Afficher la réponse du serveur
    print(data)
    measurements.clear()  # Vider la liste après l'envoi des données

while True:
    try:
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        print("Temp={0:0.1f}°C, Humidity={1:0.1f}%".format(temperature_c, humidity))
        
        # Ajouter la mesure courante à la liste
        measurements.append({
            'id': 1,  # Vous pouvez modifier cette valeur si vous avez plusieurs capteurs
            'temperature': temperature_c,
            'humidity': humidity
        })
        
        # Vérifier si on a atteint 10 mesures
        if len(measurements) == 10:
            send_data(measurements)
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(1.0)
        continue

    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(1.0)
