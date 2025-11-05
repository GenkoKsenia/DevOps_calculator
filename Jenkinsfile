pipeline {
    agent any 

	environment {
	        SSH_CREDS_ID = 'server-key' 
	        HOST = 'root@91.240.254.209'
	        PROD_DIR = '/root/prod/DevOps_calculator'
	}

    options {
        timeout(time: 5, unit: 'MINUTES')
        skipDefaultCheckout()
    }

    stages {
        
        stage('SCM Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Backend ') {
            steps {

                echo "Building backend..."
                sh 'sudo apt install -y python3.10-venv' 
                sh 'python -m venv venv' 
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt' 
            }
        }


        stage('Run Tests') {
            steps {
                script {
                    sh 'python -m pytest tests'
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
                    
                    sh "tar -czf /tmp/${artifactName} --exclude='.git' --exclude='.pytest_cache' --exclude='venv' --exclude='Jenkinsfile' --exclude='*.log' ."

                    
                    withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY')]) {
                        
                        echo "Copying archive from /tmp/${artifactName} to ${env.HOST}:/tmp/..."
                        sh 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY /tmp/' + artifactName + ' ' + env.HOST + ':/root/'
                        echo "Executing remote deployment script in ${env.PROD_DIR}..."
                        sh '''
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ''' + SSH_KEY + ''' ''' + env.HOST + ''' << EOF
mkdir -p ''' + env.PROD_DIR + '''
cd ''' + env.PROD_DIR + '''
tar -xzf /root/''' + artifactName + '''
rm /root/''' + artifactName + '''
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
sh 'python app.py --port 8081' 
EOF
'''
                    }
                    echo "✅ Deployment to Staging complete. Service restarted."
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