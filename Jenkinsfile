pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials') // Replace with your Jenkins credentials ID
    }
    triggers {
        githubPush() // Automatically triggers on GitHub push
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/RachitTanwar/IDS_Capstone.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t emuljax/intrusion-detection-system:latest .'
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    sh 'docker login -u $DOCKER_HUB_CREDENTIALS_USR -p $DOCKER_HUB_CREDENTIALS_PSW'
                    sh 'docker push emuljax/intrusion-detection-system:latest'
                }
            }
        }
    }
    post {
        success {
            echo "Build and push successful."
        }
        failure {
            echo "Build or push failed."
        }
    }
}
