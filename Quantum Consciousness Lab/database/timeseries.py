from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import WritePrecision
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "my-token")
INFLUX_ORG = os.getenv("INFLUX_ORG", "my-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "consciousness")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api()

def write_eeg_timeseries(data: np.ndarray, sfreq: float):
    """
    Writes EEG time-series to InfluxDB.
    """
    points = [
        Point("eeg")
        .tag("channel", f"ch{i}")
        .field("amplitude", float(data[i, t]))
        .time(t / sfreq, WritePrecision.S)
        for i in range(data.shape[0])
        for t in range(data.shape[1])
    ]
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=points)
