from flask import Flask, request, jsonify
import exportar_musicas
import threading
import os
from pathlib import Path

app = Flask(__name__)

# Estado global para controle da exportação
export_status = {"running": False, "progress": 0, "total": 0, "message": "Aguardando início"}
export_thread = None

def callback(idx, total):
    global export_status
    export_status["progress"] = idx
    export_status["total"] = total
    export_status["message"] = f"Exportando música {idx} de {total}..."

def cancel_check():
    global export_status
    return not export_status["running"]

@app.route('/start', methods=['POST'])
def start_export():
    global export_status, export_thread
    if export_status["running"]:
        return jsonify({"error": "Exportação já em andamento"}), 400

    db_path = request.json.get('db_path', 'C:\\Program Files (x86)\\Louvor JA\\config\\database.db')
    if not os.path.exists(db_path):
        return jsonify({"error": "Caminho do banco de dados inválido"}), 400

    export_status["running"] = True
    export_status["progress"] = 0
    export_status["total"] = 0
    export_status["message"] = "Iniciando exportação..."

    export_thread = threading.Thread(target=run_export, args=(db_path,), daemon=True)
    export_thread.start()
    return jsonify({"message": "Exportação iniciada", "status": export_status}), 200

def run_export(db_path):
    global export_status
    result = exportar_musicas.exportar_musicas(db_path, callback, cancel_check)
    export_status["running"] = False
    export_status["message"] = result

@app.route('/status', methods=['GET'])
def get_status():
    global export_status
    return jsonify(export_status), 200

@app.route('/cancel', methods=['POST'])
def cancel_export():
    global export_status
    if not export_status["running"]:
        return jsonify({"error": "Nenhuma exportação em andamento"}), 400
    export_status["running"] = False
    export_status["message"] = "Exportação cancelada"
    return jsonify({"message": "Exportação cancelada", "status": export_status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)