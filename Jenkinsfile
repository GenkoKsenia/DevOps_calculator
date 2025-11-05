pipeline {
    agent any 

	environment {
	        SSH_CREDS_ID = 'server-key' 
	        HOST = 'root@91.240.254.209'
	        PROD_DIR = '/root/prod/filedropper'
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
        
        stage('Build Backend Image') {
            steps {
                echo "Building backend..."
                sh 'python -m venv venv' 
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt' 
                sh 'python app.py --port 8080' 
            }
        }

//         stage('Run Backend Tests') {
//             steps {
//                 script {
//                     echo "Starting up services (db, namenode, backend) for testing..."
//                     sh 'docker rm -f filedropper_db filedropper_hdfs_namenode filedropper_hdfs_datanode1 filedropper_hdfs_datanode2 filedropper_backend filedropper_frontend || true'

// 					sh 'docker-compose up -d --remove-orphans'                    

// 					echo "Waiting for services to be ready..."
// 					    sh '''
// 					        timeout 180s bash -c '
// 					            until docker-compose ps backend | grep -q "healthy\\|Up"; do
// 					                echo "Waiting for backend to be ready..."
// 					                sleep 5
// 					            done
// 					        '
// 					        echo "Backend is ready!"
// 					'''

// 					echo "Waiting for HDFS to be ready (5 min timeout)..."
//                     sh '''
//                         timeout 300s bash -c ' 
//                             until docker-compose exec -T namenode hadoop fs -ls / > /dev/null 2>&1; do
//                                 echo "Waiting for HDFS namenode..."
//                                 sleep 5
//                             done
//                         '
//                         echo "HDFS is ready!"
//                     '''

//                     echo "Running database migrations..."
//                     sh 'docker-compose exec -T backend alembic upgrade head' 
                    
//                     echo "Executing backend tests with pytest..."
//                     sh 'docker-compose exec -T backend python -m pytest tests'
//                 }
//             }
//             post {
//                 always {
//                     echo "Shutting down docker-compose services..."
//                     sh 'docker-compose down -v --remove-orphans'
//                 }
//             }
//         }

//         stage('Deploy to Staging') {
//             when {
//                 branch 'main'
//                 expression {
//                     currentBuild.result == null || currentBuild.result == 'SUCCESS' 
//                 }
//             }
//             steps {
//                 script {
//                     echo "Starting CD: Deploying to Staging Server (${env.HOST})..."
                    
//                     def artifactName = "filedropper-${env.BUILD_ID}.tar.gz"
                    
//                     echo "Archiving project to /tmp/${artifactName}..."
                    
//                     sh "tar -czf /tmp/${artifactName} --exclude='.git' --exclude='node_modules' --exclude='Jenkinsfile' --exclude='*.log' ."

                    
//                     withCredentials([sshUserPrivateKey(credentialsId: env.SSH_CREDS_ID, keyFileVariable: 'SSH_KEY')]) {
                        
//                         echo "Copying archive from /tmp/${artifactName} to ${env.HOST}:/tmp/..."
//                         sh 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY /tmp/' + artifactName + ' ' + env.HOST + ':/root/'
//                         // sh 'scp -o StrictHostKdocker-compose up -d --build --remove-orphanseyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY /tmp/' + artifactName + ' ' + env.HOST + ':/root/'
//                         echo "Executing remote deployment script in ${env.PROD_DIR}..."
//                         sh '''
// ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ''' + SSH_KEY + ''' ''' + env.HOST + ''' << EOF
// mkdir -p ''' + env.PROD_DIR + '''
// cd ''' + env.PROD_DIR + '''
// tar -xzf /root/''' + artifactName + '''
// rm /root/''' + artifactName + '''
// docker-compose up -d --build --remove-orphans
// EOF
// '''
//                     }
//                     echo "✅ Deployment to Staging complete. Service restarted."
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             script {
//                 if (currentBuild.result != 'SUCCESS') {
//                     echo "Collecting logs after failure..."
//                     sh 'docker-compose logs > docker-compose-failure.log'
//                     archiveArtifacts artifacts: 'docker-compose-failure.log', onlyIfSuccessful: false
//                 }
//             }
//         }
//         success {
//             echo 'Pipeline Finished Successfully! Tests Passed.'
//         }
//         failure {
//             echo 'Pipeline Failed! Check test results and logs.'
//         }
     }


    
}