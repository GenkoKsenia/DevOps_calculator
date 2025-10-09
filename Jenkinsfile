pipeline {
    agent any
    
    environment {
        DEPLOY_SERVER = 'http://91.240.254.209/'  
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
                sh 'pip3 install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/ -v --junitxml=test-results.xml'
            }
        }
        
        stage('Deploy to Dev') {
            when {
                branch 'dev'
            }
            steps {
                sh '''
                    echo "Starting development server..."
                    # Останавливаем предыдущую версию
                    pkill -f "python3 app.py" || true
                    # Запускаем новую версию в фоне
                    nohup python3 app.py --port ${DEV_PORT} > dev.log 2>&1 &
                    echo "Development server started on port ${DEV_PORT}"
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "Starting PRODUCTION server..."
                    # Останавливаем предыдущую версию
                    pkill -f "python3 app.py" || true
                    # Запускаем production версию
                    nohup python3 app.py --port ${PROD_PORT} > prod.log 2>&1 &
                    echo "PRODUCTION server started on port ${PROD_PORT}"
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed for branch: ' + env.BRANCH_NAME
        }
        success {
            echo "Deployment completed! Server running on port ${env.BRANCH_NAME == 'main' ? PROD_PORT : DEV_PORT}"
        }
        failure {
            echo 'Tests failed!'
        }
    }
}