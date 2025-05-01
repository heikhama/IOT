from flask import Flask, render_template, request, redirect, session, jsonify
import psutil, time
import matplotlib.pyplot as plt
import os
from read_sensors import get_cpu_stats

app = Flask(__name__)
app.secret_key = "supersecret"

# --- Login Validation ---
def validate_user(username, password):
    path = os.path.join(os.path.dirname(__file__), 'users.txt')
    with open(path, "r") as file:
        for line in file:
            u, p = line.strip().split(":")
            if u == username and p == password:
                return True
    return False

# --- Routes ---
@app.route('/')
def home():
    return render_template("main.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/do_login', methods=["POST"])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        session['user'] = username
        return render_template("dashboard.html")
    else:
        return "<script>alert('Wrong username or password!'); window.location.href='/login';</script>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# --- CPU & Fan Data Endpoint ---
# @app.route('/data')
# def get_data():
#     temp = psutil.sensors_temperatures().get("coretemp", [{}])[0].get("current", 45)
#     fan_speed = psutil.sensors_fans().get("fan1", [{}])[0].get("current", 0)
#     return jsonify(
#         {"temperature": 50, 
#          "fan_speed": 2500, 
#          "time": time.time()
#          })

@app.route('/data')
def data():
    stats = get_cpu_stats()
    return jsonify({
        'temperature': stats['temperature'],
        'power': stats['power']
    })

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    temperature = data['temperature']
    power = data['power']
    timestamp = data['timestamp']

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.txt')
    
    with open(file_path, 'a') as f:
        f.write(f"{timestamp} - Temperature: {temperature}°C, Power: {power}W\n")

    return jsonify({"status": "success"}), 200

@app.route('/datadisplay')
def data_page():
    rows = []
    try:
        with open('data.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    time, data = parts
                    temp_part, power_part = data.split(', ')
                    temp = temp_part.split(':')[1].strip()
                    power = power_part.split(':')[1].strip()
                    rows.append((time, temp, power))
    except FileNotFoundError:
        rows = []

    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
