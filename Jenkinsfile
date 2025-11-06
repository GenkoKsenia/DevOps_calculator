pipeline {
    agent any 

    environment {
        SSH_CREDS_ID = 'server-key' 
        HOST = 'root@91.240.254.209'
        PROD_DIR = '/root/prod/DevOps_calculator'
        BACKEND_PORT = '5000'
        FRONTEND_PORT = '3000'
    }

    options {
        timeout(time: 10, unit: 'MINUTES')
        skipDefaultCheckout()
    }

    stages {
        
        stage('SCM Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Backend') {
            steps {
                echo "Building backend..."
                dir('backend') {
                    sh 'sudo apt install -y python3.10-venv' 
                    sh 'python3 -m venv venv' 
                    sh '. venv/bin/activate && pip install -r requirements.txt' 
                }
            }
        }

        stage('Build Frontend') {
            steps {
                echo "Building frontend..."
                dir('frontend') {
                    sh 'python3 -m venv venv' 
                    sh '. venv/bin/activate && pip install -r requirements.txt' 
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                script {
                    dir('backend') {
                        sh '. venv/bin/activate && python -m pytest tests -v'
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'master'
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                }
            }
            steps {
                script {
                    echo "Starting CD: Deploying to Staging Server (${env.HOST})..."
                    
                    def artifactName = "DevOps_calculator-${env.BUILD_ID}.tar.gz"
                    
                    echo "Archiving project to /tmp/${artifactName}..."
                    
                    sh "tar -czf /tmp/${artifactName} --exclude='.git' --exclude='.pytest_cache' --exclude='*/venv' --exclude='Jenkinsfile' --exclude='*.log' ."

                    
                    withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY')]) {
                        
                        echo "Copying archive from /tmp/${artifactName} to ${env.HOST}:/tmp/..."
                        sh 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY /tmp/' + artifactName + ' ' + env.HOST + ':/root/'
                        
                        echo "Executing remote deployment script in ${env.PROD_DIR}..."
                        sh '''
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ''' + SSH_KEY + ''' ''' + env.HOST + ''' << 'EOF'
mkdir -p ''' + env.PROD_DIR + '''
cd ''' + env.PROD_DIR + '''
tar -xzf /root/''' + artifactName + ''' --strip-components=1
rm /root/''' + artifactName + '''

# Install system dependencies
apt update
apt install -y python3.10-venv

# Setup Backend
echo "Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Frontend
echo "Setting up frontend..."
cd ../frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Kill any existing processes
pkill -f "python.*app.py" || true
sleep 2

# Start Backend
echo "Starting backend on port ''' + env.BACKEND_PORT + '''..."
cd ../backend
nohup source venv/bin/activate && python app.py --port ''' + env.BACKEND_PORT + ''' > backend.log 2>&1 &

# Start Frontend
echo "Starting frontend on port ''' + env.FRONTEND_PORT + '''..."
cd ../frontend
nohup source venv/bin/activate && python app.py --port ''' + env.FRONTEND_PORT + ''' --api-url http://localhost:''' + env.BACKEND_PORT + ''' > frontend.log 2>&1 &

# Wait for services to start
sleep 5

# Check if services are running
echo "Checking services..."
ps aux | grep -E "(app.py)" | grep -v grep

echo "✅ Deployment complete!"
echo "Backend: http://localhost:''' + env.BACKEND_PORT + '''/api/health"
echo "Frontend: http://localhost:''' + env.FRONTEND_PORT + '''"
EOF
'''
                    }
                    echo "✅ Deployment to Staging complete. Services restarted."
                }
            }
        }
        
        stage('Health Check') {
            when {
                branch 'master'
            }
            steps {
                script {
                    sleep 10  // Даем время сервисам запуститься
                    withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY')]) {
                        sh '''
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ''' + SSH_KEY + ''' ''' + env.HOST + ''' << 'EOF'
echo "Checking backend health..."
curl -f http://localhost:''' + env.BACKEND_PORT + '''/api/health || echo "Backend health check failed"

echo "Checking frontend..."
curl -f http://localhost:''' + env.FRONTEND_PORT + ''' > /dev/null && echo "Frontend is running" || echo "Frontend check failed"

echo "Checking processes..."
ps aux | grep -E "(app.py)" | grep -v grep
EOF
'''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs() 
        }
        success {
            echo 'Pipeline Finished Successfully! Tests Passed.'
        }
        failure {
            echo 'Pipeline Failed! Check test results and logs.'
        }
    }
}