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
                // Clone the specified branch from the Git repository
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
                echo 'Repository cloned.'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                // Install dependencies locally to check for any issues before deploying
                sh 'pip install -r requirements.txt'
                echo 'Dependencies installed.'
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    echo 'Deploying to EC2...'
                    // Use the SSH key stored in Jenkins credentials
                    withCredentials([sshUserPrivateKey(credentialsId: EC2_SSH_CREDENTIALS_ID, keyFileVariable: 'KEYFILE', usernameVariable: 'USER')]) {
                        sh '''
                        echo "Connecting to EC2 instance at $EC2_HOST..."
                        ssh -i $KEYFILE -o StrictHostKeyChecking=no $USER@$EC2_HOST << EOF
                        echo "Navigating to application directory..."
                        # Navigate to application directory
                        cd ${APP_PATH}
                        
                        echo "Pulling the latest code from the specified branch..."
                        # Pull the latest code from the specified branch
                        git pull origin ${GIT_BRANCH}
                        
                        echo "Activating the virtual environment..."
                        # Activate the virtual environment
                        source ${VENV_PATH}/bin/activate
                        
                        echo "Installing dependencies..."
                        # Install dependencies
                        pip install -r requirements.txt
                        
                        echo "Killing any existing Gunicorn processes..."
                        # Kill any existing Gunicorn processes
                        pkill gunicorn || true
                        
                        echo "Starting Gunicorn to run the Flask application..."
                        # Start Gunicorn to run the Flask application
                        gunicorn --bind 0.0.0.0:5000 run:app &
                        echo "Gunicorn started."
                        EOF
                        '''
                    }
                    echo 'Deployment to EC2 completed.'
                }
            }
        }
    }
}
