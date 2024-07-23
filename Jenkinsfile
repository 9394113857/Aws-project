pipeline {
    agent any
    
    environment {
        // Define the virtual environment path
        VENV_PATH = '/home/ubuntu/venv'
    }
    
    stages {
        stage('Checkout SCM') {
            steps {
                // Checkout code from Git repository
                checkout([$class: 'GitSCM',
                    userRemoteConfigs: [[url: 'https://github.com/9394113857/Aws-project.git']],
                    credentialsId: 'ec2-ssh-key'
                ])
            }
        }
        
        stage('Create Virtual Environment') {
            steps {
                script {
                    // Create virtual environment
                    sh "python3 -m venv ${VENV_PATH}"
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    // Activate virtual environment and install dependencies
                    sh """
                    source ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                // Add your deployment steps here
                echo 'Deploying to EC2...'
            }
        }
    }
    
    post {
        failure {
            echo 'Pipeline failed.'
        }
    }
}
