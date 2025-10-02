pipeline {
    agent any
    
    tools {
        python "Python3"
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
        
        stage('Publish Test Results') {
            steps {
                junit 'test-results.xml'
            }
        }
        
        stage('Deploy to Dev') {
            when {
                branch 'dev'
            }
            steps {
                sh 'echo "Deploying to development server..."'
                // Пока просто эхо, потом можно добавить реальный деплой
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                sh 'echo "Deploying to production server..."'
                // Пока просто эхо
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed for branch: ' + env.BRANCH_NAME
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}