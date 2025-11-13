pipeline {
    agent any 

    environment {
        SSH_CREDS_ID = 'server-key' 
        HOST = 'root@91.240.254.209'
        PROD_DIR = '/root/prod/DevOps_calculator'
        DOCKER_REGISTRY = 'your-docker-registry' // Например, Docker Hub
        DOCKER_IMAGE_PREFIX = 'your-username'
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
        
        stage('Build Docker Images') {
            steps {
                echo "Building Docker images..."
                
                script {
                    // Сборка backend образа
                    docker.build("${env.DOCKER_IMAGE_PREFIX}/calculator-backend:${env.BUILD_ID}", "./backend")
                    
                    // Сборка frontend образа
                    docker.build("${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:${env.BUILD_ID}", "./frontend")
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                script {
                    dir('backend') {
                        // Запускаем тесты напрямую из рабочей директории
                        sh 'python -m pytest tests/test_calculator.py -v'
                    }
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch 'master'
            }
            steps {
                echo "Pushing images to registry..."
                
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        // Логин в registry
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                        
                        // Пуш образов
                        sh "docker push ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:${env.BUILD_ID}"
                        sh "docker push ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:${env.BUILD_ID}"
                        
                        // Также тегируем как latest
                        sh """
                            docker tag ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:${env.BUILD_ID} ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:latest
                            docker tag ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:${env.BUILD_ID} ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:latest
                            docker push ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:latest
                            docker push ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'master'
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                }
            }
            steps {
                script {
                    echo "Deploying to production server..."
                    
                    withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY')]) {
                        sh '''
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ''' + SSH_KEY + ''' ''' + env.HOST + ''' << 'EOF'
# Останавливаем и удаляем старые контейнеры
docker stop calculator-backend calculator-frontend || true
docker rm calculator-backend calculator-frontend || true

# Удаляем старые образы (опционально)
docker image prune -f

# Логин в registry (если нужно)
echo ''' + DOCKER_PASS + ''' | docker login -u ''' + DOCKER_USER + ''' --password-stdin

# Запускаем новые контейнеры
docker run -d \\
  --name calculator-backend \\
  --network host \\
  --restart unless-stopped \\
  ''' + env.DOCKER_IMAGE_PREFIX + '''/calculator-backend:latest

docker run -d \\
  --name calculator-frontend \\
  --network host \\
  --restart unless-stopped \\
  ''' + env.DOCKER_IMAGE_PREFIX + '''/calculator-frontend:latest

# Проверяем что контейнеры запущены
docker ps

echo "Deployment complete!"
echo "Backend: http://localhost:5000/api/health"
echo "Frontend: http://localhost:3000"
EOF
'''
                    }
                }
            }
        }
    }

    post {
        always {
            // Очистка Docker образов с агента Jenkins
            sh 'docker system prune -f || true'
            cleanWs()
        }
        success {
            echo 'Pipeline Finished Successfully!'
        }
        failure {
            echo 'Pipeline Failed!'
        }
    }
}

// pipeline {
//     agent any 

//     environment {
//         SSH_CREDS_ID = 'server-key' 
//         HOST = 'root@91.240.254.209'
//         PROD_DIR = '/root/prod/DevOps_calculator'
//         BACKEND_PORT = '5000'
//         FRONTEND_PORT = '3000'
//     }

//     options {
//         timeout(time: 10, unit: 'MINUTES')
//         skipDefaultCheckout()
//     }

//     stages {
        
//         stage('SCM Checkout') {
//             steps {
//                 checkout scm
//             }
//         }
        
//         stage('Build Backend') {
//             steps {
//                 echo "Building backend..."
//                 dir('backend') {
//                     sh 'sudo apt install -y python3.10-venv' 
//                     sh 'python3 -m venv venv' 
//                     sh '. venv/bin/activate && pip install -r requirements.txt' 
//                 }
//             }
//         }

//         stage('Build Frontend') {
//             steps {
//                 echo "Building frontend..."
//                 dir('frontend') {
//                     sh 'python3 -m venv venv' 
//                     sh '. venv/bin/activate && pip install -r requirements.txt' 
//                 }
//             }
//         }

//         stage('Run Backend Tests') {
//             steps {
//                 script {
//                     dir('backend') {
//                         sh '. venv/bin/activate && python -m pytest tests -v'
//                     }
//                 }
//             }
//         }

//         stage('Deploy to Staging') {
//             when {
//                 branch 'master'
//                 expression {
//                     currentBuild.result == null || currentBuild.result == 'SUCCESS' 
//                 }
//             }
//             steps {
//                 script {
//                     echo "Starting CD: Deploying to Staging Server (${env.HOST})..."
                    
//                     def artifactName = "DevOps_calculator-${env.BUILD_ID}.tar.gz"
                    
//                     echo "Archiving project to /tmp/${artifactName}..."
                    
//                     sh "tar -czf /tmp/${artifactName} --exclude='.git' --exclude='.pytest_cache' --exclude='*/venv' --exclude='Jenkinsfile' --exclude='*.log' ."

                    
//                     withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY')]) {
                        
//                         echo "Copying archive from /tmp/${artifactName} to ${env.HOST}:/tmp/..."
//                         sh 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY /tmp/' + artifactName + ' ' + env.HOST + ':/root/'
                        
//                         echo "Executing remote deployment script in ${env.PROD_DIR}..."
//                         sh '''
// ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ''' + SSH_KEY + ''' ''' + env.HOST + ''' << 'EOF'
// mkdir -p ''' + env.PROD_DIR + '''
// cd ''' + env.PROD_DIR + '''
// tar -xzf /root/''' + artifactName + ''' --strip-components=1
// rm /root/''' + artifactName + '''

// # Install system dependencies
// apt update
// apt install -y python3.10-venv

// # Setup Backend
// echo "Setting up backend..."
// cd backend
// python3 -m venv venv
// source venv/bin/activate
// pip install -r requirements.txt

// # Setup Frontend
// echo "Setting up frontend..."
// cd ../frontend
// python3 -m venv venv
// source venv/bin/activate
// pip install -r requirements.txt

// # Kill any existing processes
// pkill -f "python.*app.py" || true
// sleep 2

// # Start Backend
// echo "Starting backend on port ''' + env.BACKEND_PORT + '''..."
// cd ../backend
// source venv/bin/activate && nohup python app.py --port ''' + env.BACKEND_PORT + ''' > backend.log 2>&1 &

// # Start Frontend
// echo "Starting frontend on port ''' + env.FRONTEND_PORT + '''..."
// cd ../frontend
// source venv/bin/activate && nohup python app.py --port ''' + env.FRONTEND_PORT'''

// # Wait for services to start
// sleep 5

// # Check if services are running
// echo "Checking services..."
// ps aux | grep -E "(app.py)" | grep -v grep

// echo "Deployment complete!"
// echo "Backend: http://localhost:''' + env.BACKEND_PORT + '''/api/health"
// echo "Frontend: http://localhost:''' + env.FRONTEND_PORT + '''"
// EOF
// '''
//                     }
//                     echo "Deployment to Staging complete. Services restarted."
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             cleanWs() 
//         }
//         success {
//             echo 'Pipeline Finished Successfully! Tests Passed.'
//         }
//         failure {
//             echo 'Pipeline Failed! Check test results and logs.'
//         }
//     }
// }