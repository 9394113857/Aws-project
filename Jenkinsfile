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
                echo 'Cloning the repository...'
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
                echo 'Repository cloned.'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Creating virtual environment...'
                sh 'python3 -m venv ${VENV_PATH}'
                sh 'source ${VENV_PATH}/bin/activate && pip install --upgrade pip'
                echo 'Installing dependencies...'
                sh 'source ${VENV_PATH}/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    echo 'Deploying to EC2...'
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
                        gunicorn --bind 0.0.0.0:5000 run:app &
                        EOF
                        '''
                    }
                }
            }
        }
    }
}
