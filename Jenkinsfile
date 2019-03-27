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
        sh "docker exec -i ${containerID} py.test --cov-report xml:tests/coverage.xml --cov=api --junit-xml=tests/results.xml tests/"
        sh "docker cp ${containerID}:/usr/src/app/tests/results.xml results.xml"
        sh "docker cp ${containerID}:/usr/src/app/tests/coverage.xml coverage.xml"
        sh 'docker-compose down'
        sh 'docker-compose rm'
      }
    }
    stage('Exporting tests report') {
      steps {
        junit(testResults: 'results.xml', healthScaleFactor: 1)
        cobertura(coberturaReportFile: 'coverage.xml', autoUpdateHealth: true, autoUpdateStability: true)
      }
    }
  }
  environment {
    registry = 'titogarrido/microbank-accounts'
    registryCredential = 'docker-hub-credentials'
  }
}