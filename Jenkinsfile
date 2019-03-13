pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('Testing') {
      steps {
        sh 'docker run --rm microbank-account pytest'
      }
    }
  }
}