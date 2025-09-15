from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import threading
import time
from traffic_logic import TrafficSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'traffic_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global trafik sistemi instance
trafik_sistemi = TrafficSystem()


# ===================== WEB ROUTES =====================

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')



@app.route('/api/status')
def get_status():
    """Sistem durumunu JSON olarak döndür"""
    return jsonify(trafik_sistemi.get_system_status())



@app.route('/api/start', methods=['POST'])
def start_system():
    """Sistemi başlat"""
    data = request.get_json()
    car_interval = data.get('car_interval', 1)
    car_count = data.get('car_count', 10)
    walker_interval = data.get('walker_interval', 1)
    walker_count = data.get('walker_count', 3)
    trafik_sistemi.car_interval = int(car_interval)
    trafik_sistemi.car_count = int(car_count)
    trafik_sistemi.walker_interval = int(walker_interval)
    trafik_sistemi.walker_count = int(walker_count)
    if trafik_sistemi.start():
        return jsonify({"status": "success", "message": "Sistem başlatıldı"})
    else:
        return jsonify({"status": "error", "message": "Sistem zaten çalışıyor"})
    

    
@app.route('/api/stop', methods=['POST'])
def stop_system():
    """Sistemi durdur"""
    if trafik_sistemi.stop():
        return jsonify({"status": "success", "message": "Sistem durduruldu"})
    else:
        return jsonify({"status": "error", "message": "Sistem zaten durmuş"})




@app.route('/api/reset', methods=['POST'])
def reset_system():
    """Sistemi sıfırla"""
    global trafik_sistemi
    trafik_sistemi.stop()
    time.sleep(1)
    trafik_sistemi = TrafficSystem()
    return jsonify({"status": "success", "message": "Sistem sıfırlandı"})

# ===================== WEBSOCKET EVENTS =====================
@socketio.on('connect')
def handle_connect():
    """İstemci bağlandığında"""
    print('İstemci bağlandı')
    emit('status', trafik_sistemi.get_system_status())

@socketio.on('disconnect')
def handle_disconnect():
    """İstemci ayrıldığında"""
    print('İstemci ayrıldı')

@socketio.on('request_status')
def handle_status_request():
    """İstemci durum istediğinde"""
    emit('status', trafik_sistemi.get_system_status())
# ===================== BACKGROUND UPDATES =====================

def background_updates():
    """Arka planda sürekli durum güncelleme gönder"""
    while True:
        if trafik_sistemi.running:
            status = trafik_sistemi.get_system_status()
            socketio.emit('status', status)
        time.sleep(1)  # Her saniye güncelle

# Background thread başlat
update_thread = threading.Thread(target=background_updates)
update_thread.daemon = True
update_thread.start()

# ===================== MAIN EXECUTION =====================

if __name__ == '__main__':
    print("Flask Traffic System Web Interface")
    print("http://localhost:5000 adresinde çalışıyor...")
    #trafik_sistemi.start()  # Otomatik başlat
    socketio.run(app, debug=True, port=5000)