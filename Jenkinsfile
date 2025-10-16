pipeline {
    agent any
    
    environment {
        DEPLOY_SERVER = '91.240.254.209'
        DEV_PORT = '8001'
        PROD_PORT = '8000'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing dependencies..."
                    pip3 install flask
                    pip3 install -r requirements.txt
                    echo "Dependencies installed"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/ -v --junitxml=test-results.xml'
            }
        }
        
        stage('Publish Test Results') {
            steps {
                junit 'test-results.xml'
            }
        }
        
        stage('Deploy to Dev') {
            when {
        anyOf {
            branch 'dev'
            expression { env.BRANCH_NAME == null }
        }
    }
    steps {
        sh """
            echo "Deploying to DEVELOPMENT server..."
            
            # Останавливаем ВСЕ предыдущие процессы
            pkill -f "python.*app.py" || echo "No previous processes"
            sleep 3
            
            # Переходим в папку проекта
            cd /var/lib/jenkins/workspace/Ksenia_DevOps
            
            # Запускаем приложение с правильным nohup
            echo "=== Starting application ==="
            nohup python3 app.py --port 8001 > /tmp/calculator_dev.log 2>&1 </dev/null &
            
            # Даем время на запуск
            sleep 10
            
            echo "=== Deployment Check ==="
            echo "Processes:"
            ps aux | grep python | grep app.py
            echo "Ports:"
            netstat -tlnp | grep 800
            echo "Recent logs:"
            tail -10 /tmp/calculator_dev.log
            
            echo "=== Testing application ==="
            if curl -s --connect-timeout 10 http://localhost:8001/ > /dev/null; then
                echo "Application is RUNNING and RESPONDING!"
                echo "Access at: http://91.240.254.209:8001/"
            else
                echo "Application failed to start"
                echo "=== Full logs ==="
                cat /tmp/calculator_dev.log
            fi
        """
    }
        }
        
        stage('Deploy to Production') {
            when {
                anyOf {
                    branch 'main'
                    expression { env.BRANCH_NAME == 'main' }
                }
            }
            steps {
                sh """
                    echo "Deploying to PRODUCTION server..."
                    
                    # Останавливаем предыдущие процессы на порту 8000
                    pkill -f "python.*app.py.*8000" || echo "No previous prod processes"
                    sleep 2
                    
                    # Запускаем production версию на порту 8000
                    cd /var/lib/jenkins/workspace/Ksenia_DevOps
                    nohup python3 app.py --port ${PROD_PORT} > /tmp/calculator_prod.log 2>&1 &
                    
                    sleep 5
                    echo "=== Production Deployment Check ==="
                    ps aux | grep python | grep app.py
                    
                    # Тестируем приложение
                    echo "Testing production server..."
                    curl -s http://localhost:${PROD_PORT}/ || echo "Prod server starting..."
                    
                    echo "PRODUCTION server deployed successfully!"
                    echo "Access at: http://${DEPLOY_SERVER}:${PROD_PORT}/"
                """
            }
        }
    }
    
    post {
        always {
            echo "Pipeline completed for branch: ${env.BRANCH_NAME}"
        }
        success {
            echo 'All stages completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
