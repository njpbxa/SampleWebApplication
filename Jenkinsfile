pipeline {
    agent any
    stages {
		stage('Stage: Compile') {
			steps {
				echo 'Compiling the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn clean compile'
				}
			}
		}
		stage('Stage: Unit Test') {
			steps {
				echo 'Running Unit Tests ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn test'
				}
			}
		}
		stage('Stage: Packaging') {
			steps {
				echo 'Packaging the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn package'
				}
			}
		}
		
		stage('Stage: Deploy in WAS') {
			steps {
				echo 'Deploying in WAS ..............'
				build job: 'DeployToWAS', parameters: [string(name: 'warPath', value: 'PipelineByAlakD/*.war')]
			}
		}
    }
}
