pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t titogarrido/microbank-account:latest .'
      }
    }
    stage('Tests') {
      steps {
        sh 'python --help'
      }
    }
  }
  environment {
    MONGOSERVER = 'mongo'
    MONGOPORT = '27017'
  }
}