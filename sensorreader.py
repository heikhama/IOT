import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4  # GPIO4

def read_temp():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return round(temperature, 2) if temperature else None