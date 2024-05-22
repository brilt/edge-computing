Below is a `README.md` file for your project based on the provided details and the project report.

---

# Edge Computing and IoT Data Processing Framework

## Overview

This project aims to create a framework for collecting, processing, and analyzing environmental data using IoT devices, Edge Computing, and AI. The system is designed to measure temperature and humidity, detect potential fire hazards, and present the data through a user-friendly web interface.

## Project Structure

```
UI + Back Part
├── home.html
├── main.py
└── credentials-reader.json

Edge Part
├── main.py
└── credentials-writer.json

Hardware Part
└── fire.py
```

### UI + Back Part
- **home.html**: The main HTML file for the user interface.
- **main.py**: Flask server for serving sensor data from BigQuery to the frontend.
- **credentials-reader.json**: JSON file with credentials for reading from BigQuery.

### Edge Part
- **main.py**: Flask server for processing sensor data and storing it in BigQuery.
- **credentials-writer.json**: JSON file with credentials for writing to BigQuery.

### Hardware Part
- **fire.py**: Script running on a Raspberry Pi to collect data from a DHT11 sensor and send it to the Edge server.

## Setup and Installation

### Prerequisites

- flask
- Adafruit_DHT
- RPi.GPIO
- pandas-gbq
- google-cloud-bigquery
- requests
- Flask
- Flask-Cors

### Hardware Setup

1. **Sensor Connection**:
    - Connect the DHT11 sensor to the Raspberry Pi:
      - Data pin to GPIO17
      - VCC to 3.3V
      - GND to Ground
    - Connect the buzzer:
      - Negative pin to GND
      - Positive pin to a GPIO pin (e.g., GPIO22)
![Picture1](https://github.com/brilt/edge-computing/assets/30219055/9ab55074-8c53-48c1-aa40-c229470d8a7f)

### Software Setup

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/brilt/edge-computing.git
    cd edge-computing
    ```

2. **Set Up Python Environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Set Up Google Cloud Credentials**:
    - Place the `credentials-reader.json` and `credentials-writer.json` files in the respective directories.
    - Ensure the environment variables point to these credential files:
      ```sh
      export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials-reader.json"
      ```

Here are permissions example for each credential:

Here BQ reader is the credential in UI + Back Part.
![image](https://github.com/brilt/edge-computing/assets/30219055/d4e155bb-bb59-4453-a326-7b5cf91f114c)

Here BQ uploader is the credential in Edge Part.
![image](https://github.com/brilt/edge-computing/assets/30219055/ca6f7acf-18dc-4558-9ddd-3c1032861c42)


### Running the Application

1. **Start the Edge Server**:
    ```sh
    cd Edge_Part
    python main.py
    ```

2. **Start the Backend Server**:
    ```sh
    cd UI + Back_Part
    python main.py
    ```

3. **Run the Hardware Script**:
    ```sh
    cd Hardware_Part
    sudo python3 fire.py
    ```

## Usage

- Access the web interface at `http://<your-server-ip>:5001` to view the dashboard.
- The dashboard allows you to fetch and display temperature and humidity data.
- The data is updated every 5 seconds automatically. You can change this value in ```setInterval(fetchData, 5000)```.
 
## Architecture

1. **Sensor Layer**:
    - Collects temperature and humidity data using DHT11 sensors connected to Raspberry Pi.

2. **IoT Gateway Layer**:
    - Processes and filters data before sending it to the Edge Computing layer.

3. **Edge Computing Layer**:
    - Processes data, triggers alarms if necessary, and sends summarized data to the cloud.

4. **Cloud Layer**:
    - Stores data in BigQuery and serves it to the user interface.

5. **User Interface Layer**:
    - Displays data through a web dashboard using charts and tables.

## Contributions

- Kaoutar RHFOUDA (AI)
- Killian BOISSEAU (AI)
- Gauthier PERRAULT (IoT)
- Sana DEIRI (IoT)
- Piotr KRUPINSKI (AI)

## Supervisor

- NDIAYE Fatou Diop


## Acknowledgments

- This project was completed as part of an academic course on Edge Computing and IoT.
- Special thanks to the team members and supervisor for their contributions and guidance.
