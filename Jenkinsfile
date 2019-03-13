pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('Checking environment') {
      steps {
        sh '''python --version
pip freeze'''
      }
    }
  }
}