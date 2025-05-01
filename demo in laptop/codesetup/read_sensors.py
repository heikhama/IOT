import wmi
import pythoncom

def get_cpu_stats():
    pythoncom.CoInitialize()
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    
    temperature = None
    power = None

    for sensor in w.Sensor():
        if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
            temperature = sensor.Value
        if sensor.SensorType == 'Power' and 'CPU' in sensor.Name:
            power = sensor.Value

    return {
        'temperature': temperature if temperature is not None else 0.0,
        'power': power if power is not None else 0.0
    }
