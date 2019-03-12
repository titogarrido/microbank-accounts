pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/titogarrido/microbank-accounts', branch: 'master')
      }
    }
  }
}