pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t titogarrido/microbank-accounts:${BUILD_NUMBER} -f Dockerfile .'
      }
    }
    stage('Test') {
      steps {
        sh 'docker run -d --rm titogarrido/microbank-accounts:${BUILD_NUMBER}'
      }
    }
  }
}