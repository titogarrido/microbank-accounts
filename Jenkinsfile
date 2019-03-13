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
        script {
                  containerID = sh( script: "docker run -d --rm titogarrido/microbank-accounts:${BUILD_NUMBER}", returnStdout: true)
                }
	      echo "ContainerID: ${containerID}"
      }
    }
  }
}
