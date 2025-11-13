from flask import Flask, render_template
import argparse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=3000, help='Port to run the server on')
    parser.add_argument('--api-url', type=str, default='http://91.240.254.209/:5000', help='Backend API URL')
    args = parser.parse_args()
    
    # Сохраняем URL API в конфигурации приложения
    app.config['API_URL'] = args.api_url
    
    print(f"Starting Calculator Frontend on port {args.port}...")
    print(f"Backend API URL: {args.api_url}")
    app.run(host='0.0.0.0', port=args.port, debug=False)