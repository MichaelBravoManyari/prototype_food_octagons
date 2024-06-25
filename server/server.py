from flask import Flask, request, jsonify
import subprocess
import signal
import os
import time
import threading

app = Flask(__name__)
process = None

@app.route('/start_prototype', methods=['POST'])
def start_prototype():
    global process
    if process is None:
        if os.path.exists('/tmp/prototype_started'):
            os.remove('/tmp/prototype_started')
        try:
            process = subprocess.Popen(['/home/maic753/my_env/bin/python', '../main.py'], preexec_fn=os.setsid)
            start_time = time.time()
            while not os.path.exists('/tmp/prototype_started'):
                time.sleep(0.1) 
                if time.time() - start_time > 35:
                    process.terminate()
                    print("Se agoto el tiempo de espera")
                    return jsonify({'status': 'error_when_turning_on_prototype'}), 500
 
            print("Se inicio el prototipo")
            return jsonify({'status': 'prototype_started'}), 200
        except Exception as e:
            process = None
            print("Hubo un error al encender el prototipo")
            return jsonify({'status': 'error_when_turning_on_prototype', 'message': str(e)}), 500
    else:
        print("El prototipo ya esta encendido")
        return jsonify({'status': 'prototype_is_already_running'}), 400

@app.route('/stop_prototype', methods=['POST'])
def stop_prototype():
    global process
    if process is not None:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print("Se apago el prototipo")
            process = None
            def shutdown_raspberry_pi():
                time.sleep(1)
                subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
            threading.Thread(target=shutdown_raspberry_pi).start()
            return jsonify({'status': 'prototype_off'}), 200
        except Exception as e:
            process = None
            print("Hubo un error al encender el prototipo")
            return jsonify({'status': 'error_turning_off_prototype', 'message': str(e)}), 500
    else:
        print("El prototipo esta apagado")
        return jsonify({'status': 'prototype_is_not_running'}), 400
    
@app.route('/prototype_status', methods=['GET'])
def prototype_status():
    global process
    if process is not None:
        return jsonify({'status': 'prototype_is_already_running'}), 200
    else:
        return jsonify({'status': 'prototype_off'}), 200

@app.route('/restart_prototype', methods=['POST'])
def restart_prototype():
    global process
    if process is not None:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print("Se apago el prototipo")
            process = None
        except Exception as e:
            return jsonify({'status': 'error_turning_off_prototype', 'message': str(e)}), 500

    if os.path.exists('/tmp/prototype_started'):
        os.remove('/tmp/prototype_started')

    try:
        process = subprocess.Popen(['/home/maic753/my_env/bin/python', '../main.py'], preexec_fn=os.setsid)
        start_time = time.time()
        while not os.path.exists('/tmp/prototype_started'):
            time.sleep(0.1)
            if time.time() - start_time > 35:
                process.terminate()
                return jsonify({'status': 'timeout_waiting_for_prototype'}), 500

        print("Se reinicio el prototipo")
        return jsonify({'status': 'prototype_restarted'}), 200
    except Exception as e:
        process = None
        prototype_running = False
        return jsonify({'status': 'error_when_restarting_prototype', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
