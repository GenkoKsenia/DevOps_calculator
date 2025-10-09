from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.calculator import add, subtract, multiply, divide

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Calculator API</h1>
    <p>Use /calculate?operation=add&a=5&b=3</p>
    <p>Operations: add, subtract, multiply, divide</p>
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
            return jsonify({'error': 'Invalid operation'}), 400
            
        return jsonify({'operation': operation, 'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)