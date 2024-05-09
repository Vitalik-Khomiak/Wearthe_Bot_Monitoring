pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'vitalik136/wearthe_bot_monitoring-art_bot'
    }
    stages {
        stage('Start') {
            steps {
                echo 'Cursova_Bot: nginx/custom'
            }
        }

        stage('Build nginx/custom') {
            steps {
                sh 'docker-compose build'
                sh 'docker tag wearthe_bot_monitoring-art_bot vitalik136/wearthe_bot_monitoring-art_bot:latest'
                sh 'docker tag wearthe_bot_monitoring-art_bot vitalik136/wearthe_bot_monitoring-art_bot:$BUILD_NUMBER'
            }
        }

        stage('Test nginx/custom') {
            steps {
                echo 'Pass'
            }
        }

        stage('Deploy nginx/custom'){
            steps{
                sh "docker stop \$(docker ps | grep '$DOCKER_IMAGE' | awk           ''{print \$1}') || true"
                sh "docker container prune --force"
                sh "docker image prune --force"
                sh "docker-compose up -d"
            }
        }
    }   
}
