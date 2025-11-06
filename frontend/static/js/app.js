const API_URL = 'http://localhost:5000'; // Будет переопределено при запуске

async function calculate() {
    const a = document.getElementById('a').value;
    const b = document.getElementById('b').value;
    const operation = document.getElementById('operation').value;
    
    // Очищаем предыдущие результаты
    document.getElementById('result').innerHTML = '';
    document.getElementById('error').innerHTML = '';
    
    if (!a || !b) {
        showError('Please enter both numbers');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                operation: operation,
                a: parseFloat(a),
                b: parseFloat(b)
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'An error occurred');
            return;
        }
        
        showResult(data);
    } catch (error) {
        showError('Failed to connect to server');
    }
}

function showResult(data) {
    const operationSymbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    };
    
    const symbol = operationSymbols[data.operation];
    document.getElementById('result').innerHTML = 
        `${data.a} ${symbol} ${data.b} = <span style="color: #4caf50;">${data.result}</span>`;
}

function showError(message) {
    document.getElementById('error').innerHTML = message;
}

function setExample(a, b, operation) {
    document.getElementById('a').value = a;
    document.getElementById('b').value = b;
    document.getElementById('operation').value = operation;
    
    // Очищаем результаты при установке примера
    document.getElementById('result').innerHTML = '';
    document.getElementById('error').innerHTML = '';
}