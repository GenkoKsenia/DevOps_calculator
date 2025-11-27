pipeline {
    agent any 

    environment {
        SSH_CREDS_ID = 'server-key' 
        HOST = 'root@91.240.254.209'
        DOCKER_IMAGE_PREFIX = 'kseniagenko' 
    } 

    options {
        timeout(time: 10, unit: 'MINUTES')
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
                    docker.build("${env.DOCKER_IMAGE_PREFIX}/calculator-backend:${env.BUILD_ID}", "./backend")
                    docker.build("${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:${env.BUILD_ID}", "./frontend")
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                script {
                    dir('backend') {
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
                        sh """
                            echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                            docker push ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:${env.BUILD_ID}
                            docker push ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:${env.BUILD_ID}
                            
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
                    withCredentials([
                        sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY'),
                        usernamePassword(
                            credentialsId: 'docker-hub-credentials',
                            usernameVariable: 'DOCKER_USER', 
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh """
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ${SSH_KEY} ${env.HOST} << 'EOF'
# Логин в registry
echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin

# Останавливаем и удаляем старые контейнеры
docker stop calculator-backend calculator-frontend || true
docker rm calculator-backend calculator-frontend || true

# Pull последних образов
docker pull ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:latest
docker pull ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:latest

# Запускаем новые контейнеры
docker run -d \\
  --name calculator-backend \\
  -p 5000:5000 \\
  --restart unless-stopped \\
  ${env.DOCKER_IMAGE_PREFIX}/calculator-backend:latest

docker run -d \\
  --name calculator-frontend \\
  -p 3000:3000 \\
  --restart unless-stopped \\
  ${env.DOCKER_IMAGE_PREFIX}/calculator-frontend:latest

# Проверяем что контейнеры запущены
echo "=== Running containers ==="
docker ps

echo "=== Service health checks ==="
sleep 5
curl -f http://localhost:5000/api/health && echo "Backend OK" || echo "Backend NOT OK"
curl -f http://localhost:3000 && echo "Frontend OK" || echo "Frontend NOT OK"

echo "Deployment complete!"
echo "Backend: http://91.240.254.209:5000/api/health"
echo "Frontend: http://91.240.254.209:3000"
EOF
"""
                    }
                }
            }
        }
    }

    post {
        always {
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