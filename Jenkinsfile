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
      steps {
        script {
          containerID = sh( script: "docker-compose ps -q accounts", returnStdout: true).trim()
        }

        echo "ContainerID: ${containerID}"
        sh "docker exec -i ${containerID} pytest --junit-xml=tests/results.xml"
        sh "docker cp ${containerID}:/usr/src/app/tests/results.xml results.xml"
        sh 'docker-compose down'
        sh 'docker-compose rm'
      }
    }
    stage('Archive Tests') {
      steps {
        junit(testResults: 'results.txt', healthScaleFactor: 1)
      }
    }
  }
  post {
    always {
      junit 'results.xml'

    }

  }
}