from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import Adafruit_DHT
from flask import session, redirect

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'iotdemo'

mysql = MySQL(app)
sensor = Adafruit_DHT.DHT22
pin = 4

# Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, passwd))
        user = cur.fetchone()
        cur.close()
        if user:
            session['user'] = uname
            return redirect('/dashboard')
    return render_template('login.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

# API for live data
@app.route('/temp')
def get_temp():
    temp = read_temp()
    return jsonify({'temperature': temp, 'timestamp': datetime.now().strftime("%H:%M:%S")})

# Save temperature
@app.route('/save', methods=['POST'])
def save_temp():
    temp = read_temp()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO temperature_data (sensor_id, temperature) VALUES (%s, %s)", ("Sensor1", temp))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

def read_temp():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return round(temperature, 2) if temperature else 0.0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
