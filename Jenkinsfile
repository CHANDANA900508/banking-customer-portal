pipeline {
    agent any
    environment {
        IMAGE_NAME = "customer-portal"
        CONTAINER_NAME = "customer-portal-test"
        APP_PORT = "8085"
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Checking Python application syntax...'
                bat '''
                    docker run --rm ^
                    -v "%CD%:/workspace" ^
                    -w /workspace ^
                    python:3.12-slim ^
                    python -m compileall app
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Running automated tests...'
                bat '''
                    docker run --rm ^
                    -v "%CD%:/workspace" ^
                    -w /workspace ^
                    python:3.12-slim ^
                    sh -c "pip install -r requirements.txt && pytest -v"
                '''
            }
        }
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                bat 'docker build -t %IMAGE_NAME%:build-%BUILD_NUMBER% .'
            }
        }
        stage('Container Verification') {
            steps {
                echo 'Starting temporary container...'
                bat 'docker run -d --name %CONTAINER_NAME% -p %APP_PORT%:8080 %IMAGE_NAME%:build-%BUILD_NUMBER%'
                echo 'Waiting for application to start...'
               bat 'ping 127.0.0.1 -n 11 > nul'
                echo 'Checking health endpoint...'
                bat 'curl -f http://localhost:%APP_PORT%/health'
            }
        }
    }
    post {
        always {
            echo 'Cleaning up temporary container...'
            bat 'docker rm -f %CONTAINER_NAME% || exit /b 0'
        }
    }
}