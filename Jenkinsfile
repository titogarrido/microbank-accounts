pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t titogarrido/microbank-account:latest .'
      }
    }
  }
  environment {
    MONGOSERVER = 'mongo'
    MONGOPORT = '27017'
  }
}