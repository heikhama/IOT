import Adafruit_DHT

def read_temperature(sensor_pin=4):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor_pin)
        if temperature is None:
            raise ValueError("Temperature sensor returned None")
        return round(temperature, 2)
    except Exception as e:
        print("Error reading sensor:", e)
        return None