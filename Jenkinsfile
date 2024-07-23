pipeline {
    agent any

    environment {
        // Define environment variables
        EC2_SSH_CREDENTIALS_ID = 'ec2-ssh-key' // ID of the SSH credentials
        GIT_REPO = 'https://github.com/9394113857/Aws-project.git' // Git repository URL
        GIT_BRANCH = 'raghu' // Branch to checkout
        EC2_HOST = '54.174.86.167' // Your EC2 instance IPv4 address
        APP_PATH = '/home/ubuntu/Aws-project' // Path to your application on EC2
        VENV_PATH = '/home/ubuntu/Aws-project/venv' // Path to your virtual environment
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the specified branch from the Git repository
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install dependencies locally to check for any issues before deploying
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    // Use the SSH key stored in Jenkins credentials
                    withCredentials([sshUserPrivateKey(credentialsId: EC2_SSH_CREDENTIALS_ID, keyFileVariable: 'KEYFILE', usernameVariable: 'USER')]) {
                        sh '''
                        ssh -i $KEYFILE -o StrictHostKeyChecking=no $USER@$EC2_HOST << EOF
                        # Navigate to application directory
                        cd ${APP_PATH}
                        
                        # Pull the latest code from the specified branch
                        git pull origin ${GIT_BRANCH}
                        
                        # Activate the virtual environment
                        source ${VENV_PATH}/bin/activate
                        
                        # Install dependencies
                        pip install -r requirements.txt
                        
                        # Kill any existing Gunicorn processes
                        pkill gunicorn || true
                        
                        # Start Gunicorn to run the Flask application
                        nohup gunicorn --bind 0.0.0.0:5000 run:app &
                        EOF
                        '''
                    }
                }
            }
        }
    }
}
