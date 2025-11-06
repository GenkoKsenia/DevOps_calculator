from flask import Flask, request, jsonify
from flask_cors import CORS
from src.calculator import add, subtract, multiply, divide
import argparse

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от фронтенда

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        operation = data.get('operation')
        a = data.get('a')
        b = data.get('b')
        
        if operation is None or a is None or b is None:
            return jsonify({'error': 'Missing parameters. Required: operation, a, b'}), 400
        
        try:
            a = float(a)
            b = float(b)
        except ValueError:
            return jsonify({'error': 'Parameters a and b must be numbers'}), 400
        
        if operation == 'add':
            result = add(a, b)
        elif operation == 'subtract':
            result = subtract(a, b)
        elif operation == 'multiply':
            result = multiply(a, b)
        elif operation == 'divide':
            result = divide(a, b)
        else:
            return jsonify({'error': 'Invalid operation. Use: add, subtract, multiply, divide'}), 400
            
        return jsonify({
            'operation': operation,
            'a': a,
            'b': b,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    print(f"Starting Calculator API server on port {args.port}...")
    app.run(host='0.0.0.0', port=args.port, debug=False)