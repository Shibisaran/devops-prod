pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        USE_SQLITE = 'true'
        DJANGO_SETTINGS_MODULE = 'config.settings'
        DJANGO_SECRET_KEY = 'jenkins-ci-secret'
        DJANGO_DEBUG = 'True'
        VENV = "${WORKSPACE}/.venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv "${VENV}"
                    . "${VENV}/bin/activate"
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . "${VENV}/bin/activate"
                    mkdir -p reports
                    pytest --junitxml=reports/junit.xml
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            cleanWs(deleteDirs: true, notFailBuild: true)
        }
        success {
            echo 'Login app tests passed. Build is ready.'
        }
        failure {
            echo 'Tests failed. Check the pytest report in Jenkins.'
        }
    }
}
