from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import keyboard  # Biblioteca para simular entradas no teclado

app = Flask(__name__)
socketio = SocketIO(app)

# Rota simples para testar o serviço
@app.route('/')
def home():
    return "Virtual Button Box WebService is running!"

# Endpoint para receber comandos do cliente
@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    print('os dados sao', data)
    key = data.get('key')  # A tecla enviada pelo cliente

    if key:
        try:
            keyboard.press_and_release(key)  # Simula a entrada de teclado
            return jsonify({"status": "success", "message": f"Key {key} pressed."})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "No key provided."})

# Para comunicação em tempo real
@socketio.on('send_command')
def handle_realtime_command(data):
    key = data.get('key')
    if key:
        keyboard.press_and_release(key)
        socketio.emit('response', {'status': 'success', 'message': f'Key {key} pressed.'})
    else:
        socketio.emit('response', {'status': 'error', 'message': 'No key provided.'})


# if __name__ == '__main__':
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
if __name__ == '__main__':
    app.run(host='10.0.0.8', port=5000, debug=True)

