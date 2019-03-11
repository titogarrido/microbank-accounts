pipeline {
  agent any
  stages {
    stage('Docker image') {
      steps {
        sh 'docker build .'
      }
    }
  }
  environment {
    MONGOSERVER = 'mongo'
    MONGOPORT = '27017'
  }
}