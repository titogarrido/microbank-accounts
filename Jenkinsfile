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
        sh 'docker run -it --rm titogarrido/microbank-accounts:${BUILD_NUMBER}'
      }
    }
  }
}
