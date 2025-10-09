from flask import Flask, request, jsonify
from src.calculator import add, subtract, multiply, divide
import argparse

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Calculator API</h1>
    <p>Test endpoints:</p>
    <ul>
        <li><a href="/calculate?operation=add&a=5&b=3">Add 5+3</a></li>
        <li><a href="/calculate?operation=subtract&a=10&b=4">Subtract 10-4</a></li>
        <li><a href="/calculate?operation=multiply&a=6&b=7">Multiply 6×7</a></li>
        <li><a href="/calculate?operation=divide&a=15&b=3">Divide 15÷3</a></li>
    </ul>
    '''

@app.route('/calculate')
def calculate():
    try:
        operation = request.args.get('operation')
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        
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
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    args = parser.parse_args()
    
    print(f"Starting Calculator server on port {args.port}...")
    app.run(host='0.0.0.0', port=args.port, debug=False)