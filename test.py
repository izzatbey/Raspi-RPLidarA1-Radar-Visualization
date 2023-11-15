# Import necessary libraries
import random
import threading
from rplidar import RPLidar
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
socketio = SocketIO(app)
PORT_NAME = 'COM5'
lidar = RPLidar(PORT_NAME)

# Initial data for the polar chart
theta = []
r = []


# Function to update data and emit to clients
def update_chart():
    global theta, r, lidar
    for item in lidar.iter_measures():
        # data = item.pop()
        
        # if not item[0]:
        #     continue
        
        # Update theta and r with random values for demonstration
        theta.append(round(item[2], 2))
        r.append(round(item[3], 2))
        
        # print(data)

        # Keep only the last 100 data points to prevent memory issues
        theta = theta[-360:]
        r = r[-360:]
        
        # theta = random.randint(0, 360)

        # Emit the updated data to all connected clients
        socketio.emit('update_chart', {'theta': theta, 'r': r}, namespace='/test')

        # Sleep for a short interval (simulating real-time updates)
        # socketio.sleep(0.3)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event for initial data when a client connects
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('update_chart', {'theta': theta, 'r': r})


# Start the data update thread when the app is run
if __name__ == '__main__':
    update_thread = threading.Thread(target=update_chart)
    update_thread.start()
    socketio.run(app, allow_unsafe_werkzeug=True)
    lidar.stop()
    lidar.disconnect()
