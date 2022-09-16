pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'echo "building the repo"'
                sh "python3 app.py"
            }
        }
    }
}
