pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker-compose up'
      }
    }
    stage('Test') {
      steps {
        script {
          containerID = sh( script: "docker run -d --rm titogarrido/microbank-accounts:${BUILD_NUMBER}", returnStdout: true)
        }

        echo "ContainerID: ${containerID}"
        sh "docker exec -it ${containerID} pytest --junit-xml=​tests/results.xml"
        sh "docker cp ${containerID}:tests/results.xml results.xml"
        sh "docker stop ${containerID}"
        sh "docker rm ${containerID}"
      }
    }
  }
  environment {
    BUILD_NUMBER = '${BUILD_NUMBER}'
  }
}