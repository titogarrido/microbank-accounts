pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('test') {
      steps {
        sh 'python --version'
      }
    }
  }
  environment {
    MONGOSERVER = 'mongo'
    MONGOPORT = '27017'
  }
}