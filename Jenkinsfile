pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'export BUILD_NUMBER=${BUILD_NUMBER}'
        sh 'docker-compose up -d'
      }
    }
    stage('Test') {
      parallel {
        stage('Test') {
          steps {
            script {
              containerID = sh( script: "docker-compose ps -q accounts", returnStdout: true)
            }
            echo "ContainerID: ${containerID}"
            script {
              containerID = sh( script: "docker exec -it ${containerID} pytest --junit-xml=tests/results.xml", returnStdout: true)
            }
            sh "docker cp ${containerID}:tests/results.xml results.xml"
            sh 'docker-compose stop'
          }
        }
        stage('') {
          steps {
            echo 'ieie'
          }
        }
      }
    }
  }
}