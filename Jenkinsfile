pipeline {
  agent any
  stages {
    stage('Building image') {
      steps {
        sh 'docker build -t microbank-account:B${BUILD_NUMBER} -f Dockerfile .'
      }
    }
    stage('testing') {
      steps {
        sh 'pip freeze'
      }
    }
  }
}